from .mock_service import BeginWorkerMock
from freezegun import freeze_time
import pytest

APP_ID = 1
LICENSE_KEY = 10
USER_ID = 123

FREEZE_TIME = "2021-05-16"

# Method signature tests


def test_update_interaction_numerical_value_without_attribute():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_numerical_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="", attribute_value=0.4)


def test_update_interaction_numerical_value_without_value():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_numerical_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="discount", attribute_value='')


def test_update_interaction_boolean_value_without_attribute():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_boolean_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="", attribute_value=False)


def test_update_interaction_boolean_value_without_value():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_boolean_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="discount", attribute_value="")


def test_update_interaction_date_value_without_attribute():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_date_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="", attribute_value=False)


def test_update_interaction_date_value_without_value():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_boolean_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="last_purchase", attribute_value=None)


def test_update_interaction_id_value_without_attribute():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_id_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="", attribute_value="bg1987")


def test_update_interaction_id_value_without_value():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_id_field(
            user_id=USER_ID, object_name='product', object_id=1, action='purchase', interaction_attribute="last_purchase", attribute_value=None)

# Numbers (float and int)


@freeze_time(FREEZE_TIME)
def test_interaction_numerical_attribute_stored_in_interaction_properties():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"

    bw.update_interaction_numerical_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute="discount", attribute_value=0)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results == {
        OBJECT_ID_ONE: [
            {
                'action': ACTION_ONE,
                'properties': {
                    "discount": 0
                },
                'created_at': 1621123200.0
            },
        ]
    }


@freeze_time(FREEZE_TIME)
def test_interaction_numerical_attribute_stored_in_interaction_properties_with_number_type_for_int():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "discount"

    bw.update_interaction_numerical_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value=12)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == 12


def test_interaction_numerical_attribute_stored_in_interaction_properties_with_number_type_for_float():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "discount"

    bw.update_interaction_numerical_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value=12.0)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == 12.0

# Booleans


@freeze_time(FREEZE_TIME)
def test_interaction_boolean_attribute_stored_in_interaction_properties():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"

    bw.update_interaction_boolean_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute="discount", attribute_value=True)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results == {
        OBJECT_ID_ONE: [
            {
                'action': ACTION_ONE,
                'properties': {
                    "discount": True
                },
                'created_at': 1621123200.0
            },
        ]
    }


def test_interaction_boolean_attribute_stored_in_interaction_properties_with_boolean_type_for_bool_false():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "discount"

    bw.update_interaction_boolean_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value=False)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == False


def test_interaction_boolean_attribute_stored_in_interaction_properties_with_boolean_type_for_bool_true():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "discount"

    bw.update_interaction_boolean_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value=True)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == True


def test_interaction_boolean_attribute_throws_error_for_string_type_attribute_value():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "discount"

    with pytest.raises(ValueError):
        bw.update_interaction_boolean_field(
            user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value="cabbage")

# Datetimes


@freeze_time(FREEZE_TIME)
def test_interaction_datetime_attribute_stored_in_interaction_properties():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"

    bw.update_interaction_date_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute="discount", attribute_value="22-05-2022")

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results == {
        OBJECT_ID_ONE: [
            {
                'action': ACTION_ONE,
                'properties': {
                    "discount":  "22-05-2022"                    
                },
                'created_at': 1621123200.0
            },
        ]
    }


def test_interaction_date_attribute_throws_error_for_non_parsable_attribute_value():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = "product"
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "last_purchased"

    with pytest.raises(ValueError):
        bw.update_interaction_date_field(
            user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value="cabbage")


def test_interaction_date_attribute_throws_error_for_incorrect_format_attribute_value_1():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = "product"
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "last_purchased"

    with pytest.raises(ValueError):
        bw.update_interaction_date_field(
            user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value="02/05/2022")


def test_interaction_date_attribute_throws_error_for_incorrect_format_attribute_value_2():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = "product"
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "last_purchased"

    with pytest.raises(ValueError):
        bw.update_interaction_date_field(
            user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value="2022-05-22")


def test_interaction_datetime_attribute_stored_in_interaction_properties_with_datetime_for_datetime_string():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "discount"

    bw.update_interaction_date_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value="22-05-2022")

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == "22-05-2022"


# IDS


@freeze_time(FREEZE_TIME)
def test_interaction_id_attribute_stored_in_interaction_properties():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"

    bw.update_interaction_id_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute="discount", attribute_value="bg1987")

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results == {
        OBJECT_ID_ONE: [
            {
                'action': ACTION_ONE,
                'properties': {
                    "discount":  "bg1987"                    
                },
                'created_at': 1621123200.0
            },
        ]
    }


def test_interaction_id_attribute_stored_in_interaction_properties_for_string():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "user_id"

    bw.update_interaction_id_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value="bg1987")

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == "bg1987"


def test_interaction_id_attribute_stored_in_interaction_properties_for_int():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)
    OBJECT_NAME = 'product'
    OBJECT_ID_ONE = 1
    ACTION_ONE = "purchase"
    ACTION_ATTRIBUTE = "user_id"

    bw.update_interaction_id_field(
        user_id=USER_ID, object_name=OBJECT_NAME, object_id=OBJECT_ID_ONE, action=ACTION_ONE, interaction_attribute=ACTION_ATTRIBUTE, attribute_value=10872694672)

    data = bw.get_data()
    results = data.get("interactions").get(USER_ID).get(OBJECT_NAME)
    assert results[OBJECT_ID_ONE][0]["properties"][ACTION_ATTRIBUTE] == 10872694672

def test_update_interaction_numerical_value_for_session():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    with pytest.raises(ValueError):
        bw.update_interaction_numerical_field(
            user_id=USER_ID, object_name='session', object_id=1, action='purchase', interaction_attribute="value", attribute_value=0.4)
