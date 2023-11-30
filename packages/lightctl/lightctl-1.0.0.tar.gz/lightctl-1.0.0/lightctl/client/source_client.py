import logging
import urllib.parse
from uuid import UUID

from lightctl.client.base_client import BaseClient
from lightctl.config import API_VERSION

logger = logging.getLogger(__name__)


class SourceClient(BaseClient):
    """
    Helper functions for acessing datasources

    Example:
        sc = SourceClient()
        datasource_list = list_sources()
        for datasource in datasource_list:
            print("Datasource {datasource["name"]})
    """

    def sources_url(self, workspace_id: str) -> str:
        """
        Returns:
           str: The datasources endpoint, used for getting and modifying datasources
        """
        return urllib.parse.urljoin(
            self.url_base, f"/api/{API_VERSION}/ws/{workspace_id}/sources/"
        )

    def list_sources(self, workspace_id: str) -> list[dict]:
        """
        Get all datasources in the workspace

        Args:
            workspace_id (str): Workspace id

        Returns:
            list: a list of datasources
        """
        return self.get(self.sources_url(workspace_id))

    def get_source(self, workspace_id: str, id: UUID) -> dict:
        """
        Get a datasources by its uuid

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of datasource to return

        Returns:
            dict: a datasource
        """
        url = urllib.parse.urljoin(self.sources_url(workspace_id), f"{id}")
        return self.get(url)

    def get_source_by_name(self, workspace_id: str, name: str) -> list[dict]:
        """
        Get a datasource by its name

        Args:
            workspace_id (str): Workspace id
            name (str): name of datasource to return

        Returns:
            dict: a datasource
        """
        ret_sources = []
        sources = self.list_sources(workspace_id)
        for source in sources:
            if source["metadata"]["name"] == name:
                ret_sources.append(source)
        return ret_sources

    def create_source(self, workspace_id: str, data: dict) -> dict:
        """
        Create a datasource

        Args:
            workspace_id (str): Workspace id
            data (dict) attributes of datasource

        Returns:
            dict: the datasource created
        """
        return self.post(self.sources_url(workspace_id), data)

    def update_source(self, workspace_id: str, id: UUID, data: dict) -> dict:
        """
        Update a datasource

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of datasource to update
            data (dict) new attributes of the datasource

        Returns:
            dict: the datasource updated
        """
        url = urllib.parse.urljoin(self.sources_url(workspace_id), f"{id}")
        return self.put(url, data)

    def delete_source(self, workspace_id: str, id: UUID) -> dict:
        """
        Delete a datasource

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of datasource to delete

        """
        self.delete(self.sources_url(workspace_id), f"{id}")

    def inspect(self, workspace_id: str, data: dict) -> dict:
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), "/sources/inspection"
        )
        return self.post(url, data, expected_status=200)

    def list_columns(self, workspace_id: str, id: UUID, table_id: UUID) -> list[dict]:
        """
        Get all columns in a table

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id
            table_id (UUID): Table id

        Returns:
            list: a list of tables
        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), f"{id}/profile/tables/{table_id}/columns"
        )
        columns = self.get(url)
        return columns

    def get_column(
        self, workspace_id: str, id: UUID, table_id: UUID, column_id: UUID
    ) -> dict:
        """
        Get a column from its column_id

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id
            table_id (UUID): Table id
            column_id (UUID): Column id

        Returns:
            dict: a column
        """

        url = urllib.parse.urljoin(
            self.sources_url(workspace_id),
            f"{id}/profile/tables/{table_id}/columns/{column_id}",
        )
        column = self.get(url)
        return column

    def list_tables(self, workspace_id: str, id: UUID) -> list[dict]:
        """
        Get all tables in a datasource

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id

        Returns:
            list: a list of tables
        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), f"{id}/profile/tables"
        )
        tables = self.get(url)
        return tables["data"]

    def get_table(self, workspace_id: str, id: UUID, table_id: UUID) -> dict:
        """
        Get a table from its table id

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id
            table_id (UUID): Table id

        Returns:
            dict: a table
        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), f"{id}/profile/tables/{table_id}"
        )
        table = self.get(url)
        return table

    def get_table_schema(self, workspace_id: str, id: UUID, table_name: str) -> dict:
        """
        Get a table's schema by table name

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id
            table_name (UUID): Table name

        Returns:
            dict: a schema
        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id),
            f"{id}/schema?table_name={table_name}",
        )
        return self.get(url)

    def list_schemas(self, workspace_id: str, id: UUID) -> list[dict]:
        """
        Get all schemas in the datasource

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id

        Returns:
            list: a list of schemas
        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), f"{id}/profile/schemas"
        )
        schemas = self.get(url)
        return schemas["data"]

    def get_schema(self, workspace_id: str, id: UUID, schema_id: UUID) -> dict:
        """
        Get a schema from its schema id

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id
            schema_id (UUID): Schema id

        Returns:
            dict: a schema
        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), f"{id}/profile/schemas/{schema_id}"
        )
        schema = self.get(url)
        return schema

    def update_profiler_config(
        self, workspace_id: str, id: UUID, table_uuid: str, data: dict
    ) -> dict:
        """
        Update configuration for a table in a datasource

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of datasource
            table_id (UUID): id of table
            data (dict) new table configuration

        """
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id),
            f"{id}/profile/tables/{table_uuid}/profiler-config",
        )
        return self.put(url, data)

    def trigger_source(self, workspace_id: str, id: UUID, data: dict) -> dict:
        """
        Trigger data collection on all triggered metrics in a datasource

        Args:
            workspace_id (str): Workspace id
            id (UUID): Datasource id

        """
        url = urllib.parse.urljoin(self.sources_url(workspace_id), f"{id}/trigger")
        return self.post(url, data=data)

    def activate_source(self, workspace_id: str, id: UUID, enable: bool = True):
        source = self.get_source(workspace_id, id)
        profiler_config = source["config"]["profiler"]
        if profiler_config["enabled"] == enable:
            return profiler_config

        profiler_config["enabled"] = enable
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id), f"{id}/profile/profiler-config"
        )
        return self.put(url, data=profiler_config)

    def activate_schema(
        self, workspace_id: str, id: UUID, schema_id: UUID, enable: bool = True
    ):
        schema = self.get_schema(workspace_id, id, schema_id)
        profiler_config = schema["profilerConfig"]
        if profiler_config["enabled"] == enable:
            return profiler_config

        profiler_config["enabled"] = enable
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id),
            f"{id}/profile/schemas/{schema_id}/profiler-config",
        )
        return self.put(url, data=profiler_config)

    def activate_table(
        self, workspace_id: str, id: UUID, table_id: UUID, enable: bool = True
    ):
        table = self.get_table(workspace_id, id, table_id)
        profiler_config = table["profilerConfig"]
        if profiler_config["enabled"] == enable:
            return profiler_config

        profiler_config["enabled"] = enable
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id),
            f"{id}/profile/tables/{table_id}/profiler-config",
        )
        return self.put(url, data=profiler_config)

    def activate_column(
        self,
        workspace_id: str,
        id: UUID,
        table_id: UUID,
        column_id: UUID,
        enable: bool = True,
    ):
        column = self.get_column(workspace_id, id, table_id, column_id)
        profiler_config = column["profilerConfig"]
        if profiler_config["enabled"] == enable:
            return profiler_config

        profiler_config["enabled"] = enable
        url = urllib.parse.urljoin(
            self.sources_url(workspace_id),
            f"{id}/profile/tables/{table_id}/columns/{column_id}/profiler-config",
        )
        return self.put(url, data=profiler_config)
