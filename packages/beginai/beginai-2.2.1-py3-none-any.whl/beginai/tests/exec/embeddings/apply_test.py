from freezegun import freeze_time
from .mock_service import BeginAlgorithmsApplierMock
import json
import os

APP_ID = 1
LICENSE_KEY = 10


@freeze_time("2021-05-16")
def test_learn_from_data_for_user():
    bw = BeginAlgorithmsApplierMock(APP_ID, LICENSE_KEY)

    current_path = os.getcwd()

    bw.load_user_data(
        current_path + '/beginai/tests/csvs_for_unit_test/users.csv', 'user_id')

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = [['22', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1621123200.0}], [
        '90', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1621123200.0}]]
    assert result == expected


@freeze_time("2021-05-16")
def test_learn_from_data_for_object():
    bw = BeginAlgorithmsApplierMock(APP_ID, LICENSE_KEY)

    current_path = os.getcwd()

    bw.load_object_data(
        current_path + '/beginai/tests/csvs_for_unit_test/books.csv',
        'book',
        'book_id'
    )

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = [['5333265', {'embedding': [1.0, 0.00011, 27.0, 26.0, 9.0, 28.0, 135.0, 34.0, 1.0, 7.0, 5.0, 0.00011, 0.00011, 0.00011], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1621123200.0}], ['1333909', {'embedding': [1.0, 0.00011, 22.0, 154.0, 10.0, 2.0, 1.0, 34.0, 70.0, 7.0, 4.0, 5.0, 0.00011, 0.00011], 'labels': [
    ], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1621123200.0}], ['7327624', {'embedding': [1.0, 0.00011, 27.0, 61.0, 0.00011, 24.0, 30.0, 34.0, 13.0, 7.0, 3.0, 4.0, 6.0, 8.0], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1621123200.0}]]
    assert result == expected


@freeze_time("2021-05-16")
def test_learn_from_data_for_interactions():
    bw = BeginAlgorithmsApplierMock(APP_ID, LICENSE_KEY)

    current_path = os.getcwd()

    bw.load_interactions(
        current_path + '/beginai/tests/csvs_for_unit_test/interactions.csv',
        'user_id',
        'book',
        'target_book_id', 'interaction_label'
    )

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = [{'person_id': '100', 'object_id': '6066819', 'interaction': {}}, {'person_id': '120', 'object_id': '6066819', 'interaction': {'rated_2': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '22', 'object_id': '6066819', 'interaction': {'rated_3': [{'embedding': None, 'created_at': 1621123200.0}], 'rated_4': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '301', 'object_id': '6066819', 'interaction': {'rated_4': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '308', 'object_id': '6066819', 'interaction': {
        'rated_4': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '321', 'object_id': '6066819', 'interaction': {'rated_4': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '370', 'object_id': '6066819', 'interaction': {'rated_2': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '451', 'object_id': '6066819', 'interaction': {'rated_3': [{'embedding': None, 'created_at': 1621123200.0}]}}, {'person_id': '495', 'object_id': '6066819', 'interaction': {'rated_5': [{'embedding': None, 'created_at': 1621123200.0}]}}]
    assert result == expected


@freeze_time("2021-05-16")
def test_learn_from_data_for_interactions_with_properties():
    bw = BeginAlgorithmsApplierMock(APP_ID, LICENSE_KEY, use_hero_schema=True)

    current_path = os.getcwd()

    bw.load_interactions(current_path + '/beginai/tests/csvs_for_unit_test/interaction_with_properties.csv',
                         'user_id', 'hero', 'hero_id', 'interaction')

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = [{'person_id': 'user1', 'object_id': 'hero1', 'interaction': {'has': [{'embedding': [-2.0, 1.0, 1.0, 1.0, 0.00011, 0.00011, 0.00011, 0.00011], 'created_at': 1621123200.0}], 'played': [{'embedding': [], 'created_at': 1621123200.0}]}}, {'person_id': 'user1', 'object_id': 'hero2',
                                                                                                                                                                                                                                                          'interaction': {'has': [{'embedding': [-2.0, 1.0, 1.0, 2.0, 0.00011, 0.00011, 0.00011, 0.00011], 'created_at': 1621123200.0}]}}, {'person_id': 'user2', 'object_id': 'hero1', 'interaction': {'has': [{'embedding': [0.0, 0.00011, 0.00011, 4.0, 0.00011, 0.00011, 0.00011, 0.00011], 'created_at': 1621123200.0}]}}]
    assert result == expected


@freeze_time("2024-05-16")
def test_learn_from_data_for_session():
    bw = BeginAlgorithmsApplierMock(
        APP_ID, LICENSE_KEY, use_hero_schema=False, use_session_data=True)

    current_path = os.getcwd()

    bw.load_session_data(current_path + '/beginai/tests/csvs_for_unit_test/session.csv',
                         'user_id', 'session_date', 'duration')

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = [['01-01-2023', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': None}], ['02-02-2023', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': None}], {'person_id': 'user1', 'object_id': '01-01-2023', 'interaction': {'plays': [
        {'embedding': [100.0, 0.00011], 'created_at': 1715817600.0}, {'embedding': [5000.0, 0.00011], 'created_at': 1715817600.0}]}}, {'person_id': 'user1', 'object_id': '02-02-2023', 'interaction': {'plays': [{'embedding': [130.0, 0.00011], 'created_at': 1715817600.0}]}}, {'person_id': 'user2', 'object_id': '01-01-2023', 'interaction': {'plays': [{'embedding': [900.0, 0.00011], 'created_at': 1715817600.0}]}}]

    assert result == expected


@freeze_time("2024-05-16")
def test_learn_from_data_for_session_and_interactions_and_object():
    bw = BeginAlgorithmsApplierMock(
        APP_ID, LICENSE_KEY, use_hero_schema=False, use_session_data=True)

    current_path = os.getcwd()

    bw.load_user_data(
        current_path + '/beginai/tests/csvs_for_unit_test/users.csv', 'user_id')

    bw.load_session_data(current_path + '/beginai/tests/csvs_for_unit_test/session.csv',
                         'user_id', 'session_date', 'duration')

    bw.load_object_data(
        current_path + '/beginai/tests/csvs_for_unit_test/books.csv',
        'book',
        'book_id'
    )

    bw.load_interactions(current_path + '/beginai/tests/csvs_for_unit_test/interaction_with_properties.csv',
                         'user_id', 'hero', 'hero_id', 'interaction')

    bw.learn_from_data()

    result = bw.get_embeddings()

    expected = [['22', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1715817600.0}], ['90', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': 1715817600.0}], ['01-01-2023', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': None}], ['02-02-2023', {'embedding': [], 'labels': [], 'tokens': {'input_ids': [], 'attention_mask': [], 'len_': 0}, 'identifiers': {}, 'created_at': None}], {'person_id': 'user1', 'object_id': '01-01-2023', 'interaction': {'plays': [{'embedding': [100.0, 0.00011], 'created_at': 1715817600.0}, {'embedding': [5000.0, 0.00011], 'created_at': 1715817600.0}]}}, {'person_id': 'user1', 'object_id': '02-02-2023', 'interaction': {'plays': [{'embedding': [130.0, 0.00011], 'created_at': 1715817600.0}]}}, {'person_id': 'user2', 'object_id': '01-01-2023', 'interaction': {'plays': [{'embedding': [900.0, 0.00011], 'created_at': 1715817600.0}]}}, {'person_id': 'user1', 'object_id': 'hero1', 'interaction': {'has': [{'embedding': [1.0, 1.0, 1.0, 1.0, 0.00011, 0.00011, 0.00011, 0.00011], 'created_at': 1715817600.0}], 'played': [{'embedding': [], 'created_at': 1715817600.0}]}}, {'person_id': 'user1', 'object_id': 'hero2', 'interaction': {'has': [{'embedding': [1.0, 1.0, 1.0, 2.0, 0.00011, 0.00011, 0.00011, 0.00011], 'created_at': 1715817600.0}]}}, {'person_id': 'user2', 'object_id': 'hero1', 'interaction': {'has': [{'embedding': [3.0, 0.00011, 0.00011, 4.0, 0.00011, 0.00011, 0.00011, 0.00011], 'created_at': 1715817600.0}]}}]

    assert result == expected

@freeze_time("2024-05-16")
def test_record_intervention_dates():
    bw = BeginAlgorithmsApplierMock(
        APP_ID, LICENSE_KEY, use_hero_schema=False, use_session_data=True)

    current_path = os.getcwd()

    bw.record_intervention_dates(current_path + '/beginai/tests/csvs_for_unit_test/interventions.csv',
                         'user_id', 'intervention_date', 'name', 'algo')

    result = bw.get_intervention_data()

    expected = [{'internal_id': 'user1', 'intervention_timestamp': 1672531200.0, 'intervention_name': 'test', 'algorithm': '1234'}, {'internal_id': 'user1', 'intervention_timestamp': 1672531200.0, 'intervention_name': 'test2', 'algorithm': '12'}, {'internal_id': 'user1', 'intervention_timestamp': 1675296000.0, 'intervention_name': 'test4', 'algorithm': '312'}]
    assert result == expected
