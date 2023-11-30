from logger_local.LoggerComponentEnum import LoggerComponentEnum


class UrlProfileLocalConstants:

    URL_PROFILE_LOCAL_PYTHON_COMPONENT_ID = 234
    URL_PROFILE_COMPONENT_NAME = 'profile_url_local/profile_url_local.py'
    URL_PROFILE_TESTS_COMPONENT_NAME = 'tests/test_profile_url_local.py'
    SCHEMA_NAME = 'profile_url'
    DEFAULT_COLUMN_NAME = 'url'
    DEFAULT_TABLE_NAME = 'url_table'

    OBJECT_FOR_LOGGER_CODE = {
        'component_id': URL_PROFILE_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': URL_PROFILE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'developer_email': 'michael.l@circ.zone'
    }

    OBJECT_FOR_LOGGER_TEST = {
        'component_id': URL_PROFILE_LOCAL_PYTHON_COMPONENT_ID,
        'component_name': URL_PROFILE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'michael.l@circ.zone'
    }
