import logging
import urllib.parse
from uuid import UUID

from lightctl.client.base_client import BaseClient
from lightctl.config import API_VERSION

logger = logging.getLogger(__name__)


class MetricClient(BaseClient):
    """
    Helper functions for acessing metrics

    Example:
        mc = MetricClient()
        wc = WorkspaceClient()
        workspace_list = wc.list_workspaces()
        for workspace in workspace_list:
            workspace_id = workspace["uuid"]
            metric_list = mc.list_metrics(workspace_id)
            for metric in metric_list:
                print("Workspace {workspace["name"]} Metric {metric["metatdata"]["name"]}
    """

    def metrics_url(self, workspace_id: str) -> str:
        """
        Returns:
           str: The metrics endpoint, used for getting and modifying metrics
        """
        return urllib.parse.urljoin(
            self.url_base, f"/api/{API_VERSION}/ws/{workspace_id}/metrics/"
        )

    def list_metrics(self, workspace_id: str) -> list[dict]:
        """
        Get all metrics in the workspace

        Args:
            workspace_id (str): Workspace id

        Returns:
            list: a list of metrics
        """
        return self.get(self.metrics_url(workspace_id))

    def get_metric(self, workspace_id: str, id: UUID) -> dict:
        """
        Get a metric by its uuid

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of metric to return

        Returns:
            dict: a metric
        """
        url = urllib.parse.urljoin(self.metrics_url(workspace_id), f"{id}")
        return self.get(url)

    def get_metric_by_name(self, workspace_id: str, name: str) -> list[dict]:
        """
        Get a metric by its name

        Args:
            workspace_id (str): Workspace id
            name (str): name of metric to return

        Returns:
            dict: a metric
        """
        url = urllib.parse.urljoin(self.metrics_url(workspace_id), f"?name={name}")
        return self.get(url)

    def create_metric(self, workspace_id: str, data: dict) -> dict:
        """
        Create a metric

        Args:
            workspace_id (str): Workspace id
            data (dict) attributes of metric

        Returns:
            dict: the metric created
        """
        return self.post(self.metrics_url(workspace_id), data)

    def update_metric(
        self, workspace_id: str, id: UUID, data: dict, force: bool = False
    ) -> dict:
        """
        Update a metric

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of metric to update
            data (dict): new attributes of the metric
            force (bool): if true, update metric and delete all dependent monitors. If false, only update metric if there are no dependent monitors

        Returns:
            dict: the metric updated
        """
        url = urllib.parse.urljoin(self.metrics_url(workspace_id), f"{id}")
        return self.put(url, data, force=force)

    def delete_metric(self, workspace_id: str, id: UUID, force: bool = False):
        """
        Delete a metric

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of metric to delete
            force (bool): if true, delete metric and all dependent monitors. If false, only delete metric if there are no dependent monitors
        """
        self.delete(self.metrics_url(workspace_id), f"{id}", force=force)
