import logging
import urllib.parse
from typing import Optional

from lightctl.client.base_client import BaseClient
from lightctl.config import API_VERSION

logger = logging.getLogger(__name__)


class ProfilerClient(BaseClient):
    """
    Helper functions for acessing table configuration

    """

    def profiler_base_url(self, workspace_id: str, source_uuid) -> str:
        """
        Returns:
           str: The profiler endpoint, used for getting and modifying profiler configuration
        """
        return urllib.parse.urljoin(
            self.url_base,
            f"/api/{API_VERSION}/ws/{workspace_id}/sources/{source_uuid}/profile/",
        )

    # schema level functions
    def schema_uuid_from_schema_name(
        self, workspace_id: str, source_uuid: str, schema_name: str
    ) -> str:
        """
        Get schema uuid from schema name

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): id of datasource
            schema_name (str): name of schema

        Returns:
            str: schema uuid
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)
        url = urllib.parse.urljoin(base_url, "schemas")

        schemas = self.get(url)
        for schema in schemas["data"]:
            if schema["name"] == schema_name:
                return schema["uuid"]

    def get_schema_profiler_config(
        self, workspace_id: str, source_uuid: str, schema_uuid: str
    ) -> dict:
        """
        Get schema configuration

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): id of datasource
            schema_uuid (str): id of schema

        Returns:
            dict: schema config
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(
            base_url,
            f"schemas/{schema_uuid}/profiler-config",
        )
        return self.get(url)

    def update_schema_profiler_config(
        self, workspace_id: str, source_uuid: str, schema_uuid: str, data: dict
    ) -> dict:
        """
        Update configuration for a schema in a datasource

        Args:
            workspace_id (str): Workspace id
            source_id (str): id of datasource
            schema_uuid (str): id of schema
            data (dict) new schema configuration

        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(base_url, f"schemas/{schema_uuid}/profiler-config")
        return self.put(url, data)

    # table level functions
    def table_uuid_from_table_name(
        self,
        workspace_id: str,
        source_uuid: str,
        table_name: str,
        schema_name: Optional[str] = None,
    ) -> Optional[str]:
        """
        Get table uuid from table name

        Args:
            workspace_id (str): Workspace id
            source_id (id): id of datasource
            table_name (str): name of table
            schema_name (str): name of schema that table is in

        Returns:
            str: table uuid
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(base_url, f"tables?table_names={table_name}")

        if schema_name:
            url += f"&schema_names={schema_name}"

        res = self.get(url)
        if len(res["data"]) != 1:
            return None

        table_profile = res["data"][0]
        return table_profile.get("uuid")

    def get_table_profiler_config(
        self, workspace_id: str, source_uuid: str, table_uuid: str
    ) -> dict:
        """
        Get table configuration

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): id of datasource
            schema_uuid (str): id of schema

        Returns:
            dict: table config
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(
            base_url,
            f"tables/{table_uuid}/profiler-config",
        )
        return self.get(url)

    def update_table_profiler_config(
        self, workspace_id: str, source_uuid: str, table_uuid: str, data: dict
    ) -> dict:
        """
        Update configuration for a table in a datasource

        Args:
            workspace_id (str): Workspace id
            source_id (str): id of datasource
            table_uuid (str): id of table
            data (dict) new schema configuration

        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(base_url, f"tables/{table_uuid}/profiler-config")
        return self.put(url, data)

    # column level functions
    def column_uuid_from_column_name(
        self, workspace_id: str, source_uuid: str, table_uuid: str, column_name: str
    ) -> Optional[str]:
        """
        Get column uuid from column name

        Args:
            workspace_id (str): Workspace id
            source_id (str): id of datasource
            table_uuid (str): id of datasource
            column_name (str): name of schema

        Returns:
            str: column uuid
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(
            base_url, f"tables/{table_uuid}/?column_names={column_name}"
        )

        res = self.get(url)
        if len(res["data"]) != 1:
            return None

        column_profile = res["data"][0]
        return column_profile.get("uuid")

    def get_column_profiler_config(
        self, workspace_id: str, source_uuid: str, table_uuid: str, column_uuid: str
    ) -> dict:
        """
        Get column configuration

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): id of datasource
            table_uuid (str): id of schema
            column_uuid (str): id of column

        Returns:
            dict: column config
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(
            base_url, f"tables/{table_uuid}/columns/{column_uuid}/profiler-config"
        )
        return self.get(url)

    def update_column_profiler_config(
        self,
        workspace_id: str,
        source_uuid: str,
        table_uuid: str,
        column_uuid: str,
        data: dict,
    ) -> dict:
        """
        Update configuration for a column

        Args:
            workspace_id (str): Workspace id
            source_id (str): id of datasource
            table_uuid (str): id of schema
            column_uuid (str): id of schema
            data (dict) new schema configuration

        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(
            base_url, f"tables/{table_uuid}/columns/{column_uuid}/profiler-config"
        )
        return self.put(url, data)

    def list_schemas(self, workspace_id: str, source_uuid: str) -> list[dict]:
        """
        Get all schemas in a workspace and specified datasource

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): Datasource id

        Returns:
            list: a list of schemas
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        url = urllib.parse.urljoin(base_url, "schemas")
        return self.get(url)

    def list_tables(
        self, workspace_id: str, source_uuid: str, schema_uuid: Optional[str] = None
    ) -> list[dict]:
        """
        Get all tables in a datasource

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): Datasource id
            schema_uuid (str): [Optional] Schema id

        Returns:
            list: a list of tables
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        tables_url = "tables"
        if schema_uuid is not None:
            tables_url += f"?schema_uuids={schema_uuid}"

        url = urllib.parse.urljoin(base_url, tables_url)
        return self.get(url)

    def list_columns(
        self, workspace_id: str, source_uuid: str, table_uuid: str
    ) -> list[dict]:
        """
        Get all columns in a table

        Args:
            workspace_id (str): Workspace id
            source_uuid (str): Datasource id
            table_uuid (str): Table id

        Returns:
            list: a list of tables
        """
        base_url = self.profiler_base_url(workspace_id, source_uuid)

        columns_url = f"tables/{table_uuid}/columns"

        url = urllib.parse.urljoin(base_url, columns_url)
        return self.get(url)
