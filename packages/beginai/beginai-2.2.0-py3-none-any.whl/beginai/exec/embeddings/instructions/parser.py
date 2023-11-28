"""
TODO: look into how to use empty number when value is nan.
because nan is not empty and so it's difficult to manage.
write some tests for the instructions appliers.
introduce a number of instructions appliers and a tool for mobile testing
of instructions and generated embeddings (API).
develop more instructions.
"""

from . import instructions_map
from .interaction import InteractionEncoding
from .utils import sort_instructions

ERR_NUMBER = 0.00011
EMPTY_NUMBER = 0.00012


class Parser(object):

    INTERACTIONS_KEY = "interactions"
    LABELS_KEY = "labels"
    TOKENIZE_KEY = "tokenize"
    IDENTIFIERS_KEY = "identifiers"

    def __init__(self, data):
        self.instructions = self._group_and_sort_instructions(data)
        self.labels = self._retrieve_labels(data)
        self.tokenization_fields = self._retrieve_tokenization_fields(data)
        self.tokenize_instruction = instructions_map["Tokenize"]()
        self.identifiers = self._retrieve_identifiers(data)

    def _group_and_sort_instructions(self, data):
        return sort_instructions(data)

    def _retrieve(self, data, key):
        if len(data) == 0:
            return {}
        return data.get(key, {})

    def _retrieve_labels(self, data):
        return self._retrieve(data, self.LABELS_KEY)

    def _retrieve_tokenization_fields(self, data):
        return self._retrieve(data, self.TOKENIZE_KEY)

    def _retrieve_identifiers(self, data):
        return self._retrieve(data, self.IDENTIFIERS_KEY)

    def feed(self, values_dict):
        self.values = values_dict

    def _process_instruction(self, value, instruct, provided_values_for_object):
        klass = instructions_map.get(instruct["instruct"])
        if not klass:
            return ERR_NUMBER
        # if instruction involves multiple fields.
        other_value = None

        instruct_params = instruct.get("params", {}).copy()
        # if params point to another field, get that field value too.
        if "field" in instruct_params:
            other_value = provided_values_for_object.get(
                instruct_params["field"])
            del instruct_params["field"]

        obj = klass(**instruct_params)

        try:
            if other_value:
                # in case it involves two fields.
                res = obj.apply(value, other_value)
            else:
                res = obj.apply(value)
        except Exception as e:
            return ERR_NUMBER

        if res is None:
            return ERR_NUMBER
        elif isinstance(res, list):
            return res
        elif isinstance(obj, InteractionEncoding):
            return res
        else:
            return float(res)

    def _process_labels(self, object_name, object_values):
        labels = []
        labels_provided = self.labels.get(object_name)

        if labels_provided == None or len(labels_provided) == 0:
            return labels

        labels_provided = list(set(labels_provided))
        labels_from_api = object_values.get(self.LABELS_KEY, [])
        if isinstance(labels_from_api, list) == False:
            labels_from_api = [labels_from_api]

        if len(labels_from_api) == 0:
            return labels

        for label in labels_provided:
            if label in labels_from_api:
                labels.append(label)

        return labels

    def _process_text_tokens(self, object_name, object_values):
        """
        generates one giant list of tokens for every object.
        does not keep text field seperated.
        """
        tokens = []

        field_names = self.tokenization_fields.get(object_name, [])

        if len(field_names) == 0:
            return tokens

        full_text = ""
        for field_name in field_names:
            if field_name in object_values:
                full_text += object_values[field_name]

        return self.tokenize_instruction.apply(full_text)

    def _process_identifiers(self, object_name, object_values):
        object_identifiers = {}
        identifiers_name = self.identifiers.get(object_name, [])

        if len(identifiers_name) == 0:
            return object_identifiers

        for identifier in identifiers_name:
            object_identifiers[identifier] = object_values.get(identifier, "")

        return object_identifiers

    def _parse_interactions(self) -> dict:
        return {
            "interactions": self._get_interaction_embeddings_and_actions()
        }

    def _parse_object(self, object_name: str) -> dict:
        labels = []
        identifiers = {}
        tokens = {"input_ids": [], "attention_mask": [], "len_": 0}

        # At this point, created_at is used on batch processing only
        created_at = self.values.get("beginai_created_at", None)

        if self.labels.get(object_name) is not None:
            labels = self._process_labels(object_name, self.values)

        if self.tokenization_fields.get(object_name) is not None:
            tokens = self._process_text_tokens(object_name, self.values)

        if self.identifiers.get(object_name) is not None:
            identifiers = self._process_identifiers(
                object_name, self.values)

        embedding = self._process_object_embedding(
            self.instructions.get(object_name.lower()), self.values)

        return {
            "embedding": embedding,
            "labels": labels,
            "tokens": tokens,
            "identifiers": identifiers,
            "created_at": created_at,
        }

    def parse(self, object_name):
        if self.instructions.get(object_name) == None:
            return {}

        if object_name == self.INTERACTIONS_KEY:
            return self._parse_interactions()
        else:
            return self._parse_object(object_name)

    def _process_object_embedding(self, instructions, provided_values_for_object):
        embedding = []
        # Get the instructions set for the object
        for instruct in instructions:
            # Get values set for this object
            value = provided_values_for_object.get(instruct["f_id"].lower())
            if not value and (value != 0 and "instruct" in instruct and instruct["instruct"] == "Boolean"):
                embedding.append(ERR_NUMBER)
                continue

            embedding.append(self._process_object_instructions(
                instruct=instruct, value=value, provided_values_for_object=provided_values_for_object))
        return embedding

    def _process_object_instructions(self, instruct, value, provided_values_for_object):
        result = value
        chains = instruct.get("_chains", None)

        if chains:
            for chain in chains:
                chain_list = sorted(chain, key=lambda k: k["order"])
                for item in chain_list:
                    value = self._process_instruction(
                        value, item, provided_values_for_object)
                # last response in the chain is the return value.
                result = value
        else:
            result = self._process_instruction(
                value, instruct, provided_values_for_object)

        return result

    def _get_interaction_embeddings_and_actions(self):
        embeddings = {}
        object_keys = self.values.keys()

        interactions_from_instruction = self.instructions[self.INTERACTIONS_KEY]

        interaction_keys = interactions_from_instruction.keys()
        matched_keys = list(set(object_keys).intersection(interaction_keys))

        for matched_key in matched_keys:
            actions_associated_with_provided_object = self.values.get(matched_key)
            embeddings[matched_key] = {}

            for target_object_id, actions in actions_associated_with_provided_object.items():
                embeddings[matched_key][target_object_id] = {}

                for action in actions:
                    action_name = action['action']

                    if action_name in interactions_from_instruction[matched_key]['with_embedding'] or action_name in interactions_from_instruction[matched_key]['just_actions']:
                        if action_name not in embeddings[matched_key][target_object_id]:
                            embeddings[matched_key][target_object_id][action_name] = []

                        if action_name in interactions_from_instruction[matched_key]['with_embedding']:
                            instructions = interactions_from_instruction[matched_key]['with_embedding'][action_name]
                            provided_values_for_object = action['properties']
                            processed_embedding = self._process_object_embedding(
                                instructions, provided_values_for_object)
                            
                            embeddings[matched_key][target_object_id][action_name].append({ 
                                "embedding": processed_embedding,
                                "created_at": action['created_at'] if 'created_at' in action else None
                            })

                        elif action_name in interactions_from_instruction[matched_key]['just_actions']:                        
                            embeddings[matched_key][target_object_id][action_name].append({ 
                                "embedding": None,
                                "created_at": action['created_at'] if 'created_at' in action else None
                            })
        return embeddings
