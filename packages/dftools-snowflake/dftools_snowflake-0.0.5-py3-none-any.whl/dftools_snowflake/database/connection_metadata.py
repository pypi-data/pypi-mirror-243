from typing import List

from dftools.core.database.base import BaseJsonConnectionMetadataService, QueryWrapper
from dftools_snowflake.database.connection import SnowflakeConnectionWrapper
from dftools_snowflake.database.structure_decoder import SnowStructureDecoder
from dftools_snowflake.database.system_queries import SnowflakeSystemQueries


class SnowflakeConnectionMetadataService(BaseJsonConnectionMetadataService):

    STRUCTURE_PRIMARY_KEY_TEMP_TABLE_QUERIES = [
        QueryWrapper(query="SHOW PRIMARY KEYS;")
        , QueryWrapper(query="CREATE OR REPLACE TEMPORARY TABLE DATA_STRUCTURE_PRIMARY_KEYS_{session_id} AS "
                             "SELECT * FROM TABLE(RESULT_SCAN('{last_query_exec_result.query_id}'));")
    ]

    @classmethod
    def structure_decoder(cls) -> SnowStructureDecoder:
        return SnowStructureDecoder()

    @classmethod
    def get_structure_from_database(cls, conn_wrap: SnowflakeConnectionWrapper, namespace: str, table_name: str,
                                    catalog: str = None) -> list:
        data_structure_extract_query = \
            SnowflakeSystemQueries.get_snow_structure_query_for_namespace_and_table(
                namespace=namespace, table_name=table_name) \
                if catalog is None else \
                SnowflakeSystemQueries.get_snow_structure_query_for_catalog_namespace_and_table(
                    catalog=catalog, namespace=namespace, table_name=table_name)

        query_list = []
        query_list.extend(cls.STRUCTURE_PRIMARY_KEY_TEMP_TABLE_QUERIES)
        query_list.append(QueryWrapper(
            query=data_structure_extract_query.replace('DATA_STRUCTURE_PRIMARY_KEYS'
                                                       , 'DATA_STRUCTURE_PRIMARY_KEYS_{session_id}')))

        query_exec_results = conn_wrap.execute_queries(query_list=query_list)
        if query_exec_results.has_failed():
            raise RuntimeError('Failure on structures metadata retrieval.')
        return query_exec_results[2].result_set

    @classmethod
    def get_structures_from_database_queries(cls
                                     , namespace: str, catalog: str = None) -> List[QueryWrapper]:
        structure_names_to_exclude = ['DATA_STRUCTURE_PRIMARY_KEYS']
        data_structure_extract_query = (
            SnowflakeSystemQueries.get_snow_structure_query_for_namespace(
                namespace=namespace, structure_names_to_exclude=structure_names_to_exclude)
            if catalog is None \
                else SnowflakeSystemQueries.get_snow_structure_query_for_catalog_and_namespace(
                catalog=catalog, namespace=namespace, structure_names_to_exclude=structure_names_to_exclude)
        )
        query_list = []
        query_list.extend(cls.STRUCTURE_PRIMARY_KEY_TEMP_TABLE_QUERIES)
        query_list.append(QueryWrapper(
            query=data_structure_extract_query.replace('DATA_STRUCTURE_PRIMARY_KEYS'
                                                       , 'DATA_STRUCTURE_PRIMARY_KEYS_{session_id}')))

        return query_list

        query_exec_results = conn_wrap.execute_queries(query_list=query_list)
        if query_exec_results.has_failed():
            raise RuntimeError('Failure on structures metadata retrieval.')
        return query_exec_results[2].result_set
