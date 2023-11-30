from beginai.utils.date import parse_date_to_format
from . import Parser
from ...orchapi.api import OrchAPI
from tqdm import tqdm
import pandas as pd
import datetime
from beginai.exec.embeddings.instructions.utils import sort_instructions


class AlgorithmsApplier(object):

    host = "https://sdk-a1ummign.uc.gateway.dev"

    INTERACTIONS = 'interactions'
    CREATED_AT = 'beginai_created_at'
    INTERVENTION_TIMESTAMP = 'intervention_timestamp'
    INTERVENTION_NAME = 'intervention_name'
    ALGORITHM_UUID = 'algorithm'
    LABELS = 'labels'
    SESSION = 'session'
    BATCH_SIZE = 20000

    def __init__(self, app_id, license_key, host=None, debug=False):
        self.orchapi = OrchAPI()
        self.orchapi.configure_orch_connection(host or self.host)
        self.orchapi.set_debug(debug)
        self.orchapi.set_app_id_and_license_key(
            app_id=app_id, license_key=license_key)
        self._submission_in_progress = False

        self.embeddings = {}
        self.files = {}

    def load_user_data(self, filename, unique_identifier_column, label_column=None, created_at_column=None, file_separator=","):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        self._add_data_to_files_dictionary(
            filename, 'user', unique_identifier_column, label_column=label_column, created_at_column=created_at_column, file_separator=file_separator)

    def load_object_data(self, filename, object_name, unique_identifier_column, label_column=None, created_at_column=None, file_separator=","):
        if object_name == '' or object_name is None:
            raise ValueError(
                'The object name must be provied before the file is loaded')

        if object_name == self.SESSION:
            raise ValueError(
                'Session can only be used through a load_session_data() method')

        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        self._add_data_to_files_dictionary(
            filename, object_name, unique_identifier_column, label_column=label_column, created_at_column=created_at_column, file_separator=file_separator)

    def load_interactions(self, filename, unique_identifier_column, target_object_name,
                          target_unique_identifier_column, interaction_column_name, created_at_column=None, file_separator=","):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')
        if target_object_name == '' or target_object_name is None:
            raise ValueError(
                'The target object when registering an interaction must be provided')
        if target_unique_identifier_column == '' or target_unique_identifier_column is None:
            raise ValueError(
                'The target unique indentifer column when registering an interaction must be provided')
        if interaction_column_name == '' or interaction_column_name is None:
            raise ValueError(
                'The interaction column when registering an interaction must be provided')

        target_object_name = target_object_name.lower()

        if target_object_name == self.SESSION:
            raise ValueError(
                "Session interactions can only be added through the load_session_data() method")

        target_object = {
            'name': target_object_name,
            'uuid_column': target_unique_identifier_column.lower(),
            'interaction_column': interaction_column_name.lower()
        }

        self._add_data_to_files_dictionary(
            filename, self.INTERACTIONS, unique_identifier_column, target_object, created_at_column=created_at_column, file_separator=file_separator)

    def load_session_data(self, filename, unique_identifier_column, session_date_column, duration_column, file_separator=","):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        if session_date_column == '' or session_date_column is None:
            raise ValueError(
                'The Session date column must be provided')

        if duration_column == '' or duration_column is None:
            raise ValueError(
                'The Session duration column must be provided')

        target_object = {
            'name': self.SESSION,
            'uuid_column': session_date_column.lower(),
            'interaction_column': 'plays',
            'session_date_column': session_date_column.lower()
        }

        self._add_data_to_files_dictionary(
            filename, self.SESSION, unique_identifier_column, target_object, created_at_column=None, file_separator=file_separator)

    def _add_data_to_files_dictionary(self, filename, object_name, uuid_column, target_object={}, label_column=None, created_at_column=None, file_separator=","):
        self.files[object_name] = {
            'data': self._read_file(filename, file_separator),
            'uuid_column': uuid_column.lower(),
            'target_object': target_object,
            'label_column': label_column.lower() if label_column is not None else None,
            'created_at_column': created_at_column.lower() if created_at_column is not None else None,
        }

    def _read_file(self, filename, file_separator):
        if filename == '' or filename is None:
            raise ValueError('File must be provided')

        df = pd.read_csv(filename, dtype=str, sep=file_separator)
        df = df.rename(columns=str.lower)
        df = df.drop(df.columns[df.columns.str.contains(
            'unnamed', case=False)], axis=1)
        return df

    def _get_instructions(self):
        return self.orchapi.fetch_instructions()

    def learn_from_data(self, update=False):
        if len(self.files) == 0:
            return

        print("Start time: ", datetime.datetime.now())

        instructions_id, current_embeddings_version, instructions = \
            self._get_instructions()

        self._generate_embeddings(instructions)

        self._submit_embeddings(
            instructions_id, current_embeddings_version, update)

        print("End time: ", datetime.datetime.now())
        self.flush_memory()

    def flush_memory(self):
        self.embeddings = {}
        self.files = {}

    def _generate_embeddings(self, instructions):
        parser = Parser(instructions)

        for object_key in self.files.keys():
            object_config = self.files[object_key]

            df: pd.DataFrame = object_config['data']
            uuid_column = object_config['uuid_column']

            df = self._preparing_dataframe(
                df, object_config, object_key, instructions)

            dictionary = df.to_dict(orient='records')

            if object_key == self.INTERACTIONS:
                target_object = object_config['target_object']
                target_object_name = target_object['name']

                self._generate_embeddings_for_interactions(
                    df, uuid_column, target_object, target_object_name, parser)

            elif object_key == self.SESSION:
                target_object = object_config['target_object']
                session_date_column: str = target_object['session_date_column']

                df = df.fillna('')

                df[session_date_column] = pd.to_datetime(df[session_date_column], format="%d-%m-%Y").dt.strftime("%d-%m-%Y")

                session_object = df[session_date_column].unique()

                if len(session_object) > 0:
                    object_data = []
                    parser.feed({})
                    empty_embedding_structure = parser.parse(object_key)

                    for session_date in session_object:
                        object_data.append(
                            [session_date, empty_embedding_structure])

                    self.embeddings[self.SESSION] = object_data

                    df['plays'] = 'plays'

                    self._generate_embeddings_for_interactions(
                        df, uuid_column, target_object, self.SESSION, parser)
            else:
                object_data = []

                for index, row in tqdm(enumerate(dictionary)):
                    parser.feed(row)
                    results = parser.parse(object_key)
                    if len(results) > 0:
                        key = row[uuid_column]
                        object_data.append([key, results])

                if len(object_data) > 0:
                    if object_key not in self.embeddings:
                        self.embeddings[object_key] = []

                    self.embeddings[object_key] = object_data

    def _generate_embeddings_for_interactions(self, df: pd.DataFrame, uuid_column: str, target_object: str, target_object_name: str, parser: Parser):
        user_interactions = self._parse_interactions(
            df, uuid_column, target_object, target_object_name)

        grouped_interactions = {
            'interactions': []
        }

        for user_id in user_interactions.keys():
            value = user_interactions[user_id]
            parser.feed(value)
            results = parser.parse(self.INTERACTIONS)
            if len(results) > 0:
                grouped_interactions['interactions'].append(
                    [str(user_id), target_object_name, results[self.INTERACTIONS]])

        if len(grouped_interactions[self.INTERACTIONS]) > 0:
            if self.INTERACTIONS not in self.embeddings:
                self.embeddings[self.INTERACTIONS] = {
                    self.INTERACTIONS: []
                }
            self.embeddings[self.INTERACTIONS][self.INTERACTIONS] += grouped_interactions[self.INTERACTIONS]

    def _preparing_dataframe(self, df: pd.DataFrame, object_config: dict, object_key: str, instructions: dict) -> pd.DataFrame:
        label_column = object_config['label_column']
        created_at_column = object_config['created_at_column']
        # Rename columns representing begin constructs as identified by the user
        if object_key != self.INTERACTIONS and label_column is not None:
            try:
                df = df.rename(
                    columns={label_column: self.LABELS}, errors="raise")
            except:
                raise ValueError(
                    f"The [labels] column provided [{label_column}] was not found in the csv.")

        if created_at_column is not None:
            try:
                df = df.rename(
                    columns={created_at_column: self.CREATED_AT}, errors="raise")
            except:
                raise ValueError(
                    f"The [created_at] column provided [{created_at_column}] was not found in the csv.")

            df[self.CREATED_AT] = pd.to_datetime(
                df[self.CREATED_AT], infer_datetime_format=True)
            df[self.CREATED_AT] = df[self.CREATED_AT].apply(
                lambda x:  x.timestamp())
        else:
            df[self.CREATED_AT] = datetime.datetime.now(
                datetime.timezone.utc).timestamp()

        tokenize_instructions = instructions.get("tokenize", {})
        identifiers_instructions = instructions.get("identifiers", {})

        is_object_key_text_tokenize = tokenize_instructions.get(
            object_key, None) is not None
        is_object_key_id = identifiers_instructions.get(
            object_key, None) is not None
        if object_key != self.INTERACTIONS and (is_object_key_text_tokenize == True or is_object_key_id == True):
            tokenize_properties = tokenize_instructions.get(object_key, [])

            for tokenize_property_name in tokenize_properties:
                df[tokenize_property_name].fillna(value="", inplace=True)

            identifier_properties = identifiers_instructions.get(
                object_key, [])
            for identifier_property_name in identifier_properties:
                df[identifier_property_name].fillna(value="", inplace=True)
        return df

    def _parse_interactions(self, df: pd.DataFrame, uuid_column: str, target_object: dict, target_object_name: str) -> dict:
        interaction_column: str = target_object['interaction_column']
        target_uuid_column = target_object['uuid_column']
        df = df.rename(
            columns={interaction_column: 'action', self.CREATED_AT: 'created_at'})
        # Fill NA with '' to tell the parsers that the value doesn't exist
        df = df.fillna('')
        df = df.groupby(
            [uuid_column, target_uuid_column], as_index=False)

        interactions = {}
        for key, group in tqdm(df):
            uuid = key[0]
            target_uuid = key[1]

            if uuid not in interactions:
                interactions[uuid] = {}

            if target_object_name not in interactions[uuid]:
                interactions[uuid][target_object_name] = {}

            if target_uuid not in interactions[uuid][target_object_name]:
                interactions[uuid][target_object_name][target_uuid] = []

            grouped_columns = group[group.columns[~group.columns.isin(
                [target_uuid_column, uuid_column])]]

            for data in grouped_columns.to_dict(orient='records'):
                action = data['action']
                if len(action) == 0:
                    continue

                del data['action']

                interactions[uuid][target_object_name][target_uuid].append({
                    "action": action,
                    "properties": data,
                    "created_at": data['created_at']
                })

        return interactions

    def _submit_intervention_dates(self, data):
        if self._submission_in_progress:
            return

        self._submission_in_progress = True

        end_counter = self.BATCH_SIZE
        start_counter = 0
        all_ = len(data)

        while(start_counter < all_):
            slice = data[start_counter:end_counter]
            self.orchapi.submit_intervention_dates_batch(slice)
            print(
                f"Submitted {len(slice)} at index {start_counter} out of {all_} interventions")
            start_counter += self.BATCH_SIZE
            end_counter += self.BATCH_SIZE

        self._submission_in_progress = False

    def _submit_embeddings(self, instructions_id, current_version, update):
        if self._submission_in_progress or len(self.embeddings) == 0:
            return

        print("Working on submitting existing set. please wait.")

        self._submission_in_progress = True

        self._update_interactions_structure_before_batch()

        interactions_data = []

        for key in self.embeddings.keys():
            print(f"Submitting embeddings associated with {key}")
            if key == self.INTERACTIONS:
                interactions_data = self.embeddings[key]
            else:
                self._submit_objects(
                    self.embeddings[key], key, instructions_id, current_version, None, update)

        # Forces interactions to be send only after users and objects are done
        if len(interactions_data) > 0:
            self._submit_interactions(
                interactions_data, instructions_id, current_version)

        self._submission_in_progress = False

    def _update_interactions_structure_before_batch(self):
        if len(self.embeddings) == 0 or self.INTERACTIONS not in self.embeddings:
            return

        def _remap_object_based_on_type(person_id: str, interactions_dictionary: dict) -> list:
            remapped_list = []
            for object_id in interactions_dictionary.keys():
                remapped_list.append({
                    'person_id': person_id,
                    'object_id': str(object_id),
                    'interaction': interactions_dictionary[object_id],
                })
            return remapped_list

        grouped_interactions = self.embeddings[self.INTERACTIONS]
        interactions = {}

        for key in grouped_interactions:
            grouped_by_target_object = {}
            for data in grouped_interactions[key]:
                person_id = data[0]
                target_object = data[1]
                interactions_dictionary = data[2]

                if target_object not in grouped_by_target_object:
                    grouped_by_target_object[target_object] = []

                if len(interactions_dictionary) > 0:
                    grouped_by_target_object[target_object].extend(
                        _remap_object_based_on_type(person_id, interactions_dictionary[target_object]))
            interactions[key] = grouped_by_target_object

        self.embeddings[self.INTERACTIONS] = interactions

    def _submit_interactions(self, interactions_dictionary, instructions_id, current_version):
        for key in interactions_dictionary:
            for target_object in interactions_dictionary[key]:
                self._submit_objects(
                    interactions_dictionary[key][target_object], key, instructions_id, current_version, target_object, update=False)

    def _submit_objects(self, data, key, instructions_id, current_version, target_object=None, update=False):
        end_counter = self.BATCH_SIZE
        start_counter = 0
        all_ = len(data)
        while(start_counter < all_):
            slice = data[start_counter:end_counter]
            self.orchapi.submit_embeddings_batch(
                slice, instructions_id, current_version, key, target_object, update)
            print(
                f"Submitted {len(slice)} at index {start_counter} out of {all_} {key}")
            start_counter += self.BATCH_SIZE
            end_counter += self.BATCH_SIZE

    def recommend(self, project_id, user_id, limit=None, page=None):
        return self.orchapi.recommend(project_id, user_id, limit, page)

    def predict_engagement(self, project_id, user_id, object_id):
        return self.orchapi.predict_engagement(project_id, user_id, object_id)

    def fake_detect(self, project_id, target_id):
        return self.orchapi.fake_detect(project_id, target_id)

    def classify(self, project_id, target_id):
        return self.orchapi.classify(project_id, target_id)

    def get_training_performance(self, project_id):
        return self.orchapi.training_results(project_id)

    def record_intervention_dates(self, filename, unique_identifier_column, intervention_date, intervention_name, algorithm_uuid, file_separator=','):
        if unique_identifier_column == '' or unique_identifier_column is None:
            raise ValueError('The unique indentifier column must be provided')

        if intervention_date == '' or intervention_date is None:
            raise ValueError('The intervention date must be provided')

        if intervention_name == '' or intervention_name is None:
            raise ValueError('The intervention name must be provided')

        if filename == '' or filename is None:
            raise ValueError('The filename must be provided')
        
        if algorithm_uuid == '' or algorithm_uuid is None:
            raise ValueError('The algorithm UUID must be provided')

        df = self._read_file(filename=filename, file_separator=file_separator)
        df = df.rename(columns={unique_identifier_column: 'internal_id',
                       intervention_date: self.INTERVENTION_TIMESTAMP, intervention_name: self.INTERVENTION_NAME, algorithm_uuid: self.ALGORITHM_UUID})
        
        df = df.dropna()

        df[self.INTERVENTION_TIMESTAMP] = pd.to_datetime(
            df[self.INTERVENTION_TIMESTAMP], format="%d-%m-%Y").dt.tz_localize(None)

        df[self.INTERVENTION_TIMESTAMP] = df[self.INTERVENTION_TIMESTAMP].apply(lambda x:  x.timestamp())

        df = df[['internal_id', self.INTERVENTION_TIMESTAMP, self.INTERVENTION_NAME, self.ALGORITHM_UUID]]
        
        dictionary = df.to_dict(orient='records')

        self._submit_intervention_dates(dictionary)

    def engagement_score(self, project_id, target_id, start_date, end_date):
        start_date = parse_date_to_format(start_date)
        end_date = parse_date_to_format(end_date)

        return self.orchapi.engagement_score(project_id, target_id, start_date, end_date)

    # maintenance end points

    def learn_from_data_dry_run(self):
        """
        does not submit embeddings, only generates them.
        """
        if len(self.files) == 0:
            return

        print("Start time: ", datetime.datetime.now())

        instructions_id, current_embeddings_version, instructions = self._get_instructions()
        self._generate_embeddings(instructions)
        return self.embeddings

    def get_embedding_position_label(self, object_type):
        instructions_id, current_embeddings_version, data = self._get_instructions()

        position_label = []

        if len(data) == 0:
            return position_label

        sorted_dictionary = sort_instructions(data)

        if object_type not in sorted_dictionary:
            return position_label

        instructions_for_object = sorted_dictionary[object_type]
        for instruction in instructions_for_object:
            position_label.append(instruction['f_id'])

        return position_label
