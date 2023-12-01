from multipledispatch import dispatch
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from dotenv import load_dotenv

load_dotenv()
from circles_local_database_python.generic_crud import GenericCRUD   # noqa: E402
from logger_local.Logger import Logger  # noqa: E402

PROFILE_METRICS_LOCAL_COMPONENT_ID = 233
PROFILE_METRICS_LOCAL_COMPONENT_NAME = "profile metrics local"
DEVELOPER_EMAIL = "tal.g@circ.zone"
object_for_logger_code = {
    'component_id': PROFILE_METRICS_LOCAL_COMPONENT_ID,
    'component_name': PROFILE_METRICS_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
logger = Logger.create_logger(object=object_for_logger_code)

# TODO Add PROFILE_METRICS_ prefix to all const
SCHEMA_NAME = "profile_metrics"
TABLE_NAME = "profile_metrics_table"
VIEW_NAME = "profile_metrics_view"
DEFAULT_ID_COLUMN_NAME = "profile_metrics_id"


class ProfileMetricsLocal(GenericCRUD):

    def __init__(self):
        super().__init__(default_schema_name=SCHEMA_NAME, default_table_name=TABLE_NAME,
                         default_view_table_name=VIEW_NAME,
                         default_id_column_name=DEFAULT_ID_COLUMN_NAME)

    @dispatch(int, int, int)
    def insert(self, profile_id: int, profile_metrics_type: int, value: int) -> int:
        logger.start(object={'profile_id': profile_id, 'profile_metrics_type': profile_metrics_type, 'value': value})
        profile_metrics_id = super().insert(
            data_json={'profile_id': profile_id, 'profile_metrics_type': profile_metrics_type, 'value': value})
        logger.end(object={'profile_metrics_id': profile_metrics_id})
        return profile_metrics_id

    # 'dict' is used instead of 'Dict' because dispatch can't work with 'Dict'
    # 'dict' is not available in python 3.8 but it is available in python 3.11
    @dispatch(dict)
    def insert(self, data_json: dict[str, int]) -> int:     # noqa: F811
        logger.start(object={'data_json': data_json})
        profile_metrics_id = super().insert(data_json=data_json)
        logger.end(object={'profile_metrics_id': profile_metrics_id})
        return profile_metrics_id

    @dispatch(int, int, int, int)
    def update(self, profile_metrics_id: int, profile_id: int, profile_metrics_type: int, value: int) -> None:
        logger.start(object={'profile_metrics_id': profile_metrics_id, 'profile_id': profile_id,
                     'profile_metrics_type': profile_metrics_type, 'value': value})
        data_json = {'profile_id': profile_id, 'profile_metrics_type': profile_metrics_type, 'value': value}
        profile_metrics_id = self.update_by_id(id_column_value=profile_metrics_id, data_json=data_json)
        logger.end()

    def delete_by_id(self, profile_metrics_id: int) -> None:
        logger.start(object={'profile_metrics_id': profile_metrics_id})
        super().delete_by_id(id_column_value=profile_metrics_id)
        logger.end()

    def select_one_dict_by_id(self, profile_metrics_id: int) -> dict[str, int]:
        logger.start(object={'profile_metrics_id': profile_metrics_id})
        select_clause_value = 'profile_id, profile_metrics_type, value'
        profile_metrics_dict = super().select_one_dict_by_id(
            select_clause_value=select_clause_value,
            id_column_value=profile_metrics_id)
        logger.end(object={'profile_metrics_dict': profile_metrics_dict})
        return profile_metrics_dict
