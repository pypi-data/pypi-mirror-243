# TODO rename the file from entity_constants.py to i.e. country_constants.py

from logger_local.LoggerComponentEnum import LoggerComponentEnum

# <Entity> i.e. Country
class CountryLocalConstants:

    DEVELOPER_EMAIL = 'jenya.b@circ.zone'
    MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID = 243
    MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME = 'location local python package'
    MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_CODE_LOGGER_OBJECT = {
        'component_id': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': DEVELOPER_EMAIL
    }
    MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_TEST_LOGGER_OBJECT = {
        'component_id': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': MESSAGE_SEND_PLATFORM_INVITATION_LOCAL_PYTHON_COMPONENT_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': DEVELOPER_EMAIL
    }

    # TODO Please replace <ENTITY> i.e. COUNTRY
    UNKNOWN_COUNTRY_ID = 0

    # TODO Please update if you need default values i.e. for testing
    #DEFAULT_XXX_NAME = None
    #DEFAULT_XXX_NAME = None

    # TODO In the case of non-ML Table, please replace <entity> i.e. country
    COUNTRY_TABLE_NAME = '<entity>_table'
    COUNTRY_VIEW_NAME = '<entity>_ml_table'

    # TODO In the case of ML Table, please replace <entity> i.e. country
    COUNTRY_TABLE_NAME = '<entity>_table'
    COUNTRY_ML_TABLE_NAME = '<entity>_ml_table'
    COUNTRY_ML_VIEW_NAME = '<entity>_ml_view'
