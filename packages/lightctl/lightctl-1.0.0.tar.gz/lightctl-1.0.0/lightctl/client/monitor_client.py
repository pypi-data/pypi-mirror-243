import logging
import urllib.parse
from typing import Optional
from uuid import UUID

from lightctl.client.base_client import BaseClient
from lightctl.config import API_VERSION

logger = logging.getLogger(__name__)


class MonitorClient(BaseClient):
    """
    Helper functions for acessing monitors

    Example:
        mc = MetricClient()
        wc = WorkspaceClient()
        rc = MonitorClient()
        workspace_list = wc.list_workspaces()
        for workspace in workspace_list:
            workspace_id = workspace["uuid"]
            metric_list = mc.list_metrics(workspace_id)
            for metric in metric_list:
                metric_id = metric["metadata"]["uuid"]
                monitor_list = rc.get_monitors_by_metric(workspace_id, metric_id)
                for monitor in monitor_list:
                    print("Workspace {workspace["name"]} Metric {metric["metatdata"]["name"]} Monitor {monitor["metadata"]["name"]}
    """

    def monitors_url(self, workspace_id: str) -> str:
        """
        Returns:
           str: The monitors endpoint, used for getting and modifying monitors
        """
        return urllib.parse.urljoin(
            self.url_base, f"/api/{API_VERSION}/ws/{workspace_id}/monitors/"
        )

    def list_monitors(self, workspace_id: str) -> list[dict]:
        """
        Get all monitors in the workspace

        Args:
            workspace_id (str): Workspace id

        Returns:
            list: a list of monitors
        """
        res = self.get(self.monitors_url(workspace_id))
        return res.get("data", [])

    def get_monitor(self, workspace_id: str, id: UUID) -> dict:
        """
        Get a monitor by its uuid

        Args:
            workspace_id (str): Workspace id
            id (UUID): monitor id to return

        Returns:
            dict: a monnitor
        """
        url = urllib.parse.urljoin(self.monitors_url(workspace_id), f"{id}")
        monitor = self.get(url)
        return monitor

    def get_monitor_by_name(self, workspace_id: str, name: str) -> list[dict]:
        """
        Get a monitor by its name

        Args:
            workspace_id (str): Workspace id
            name (str): monitor name to return

        Returns:
            dict: a monitor
        """
        url = urllib.parse.urljoin(self.monitors_url(workspace_id), f"?names={name}")
        # name is not unique
        return self.get(url)

    def create_monitor(self, workspace_id: str, data: dict) -> dict:
        """
        Create a monitor

        Args:
            workspace_id (str): Workspace id
            data (dict) attributes of monitor

        Returns:
            dict: the monitor created
        """
        return self.post(self.monitors_url(workspace_id), data)

    def update_monitor(self, workspace_id: str, id: UUID, data: dict) -> dict:
        """
        Update a monnitor

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of metric to update
            data (dict) new attributes of the monitor

        Returns:
            dict: the monitor updated
        """
        url = urllib.parse.urljoin(self.monitors_url(workspace_id), f"{id}")
        return self.put(url, data)

    def delete_monitor(self, workspace_id: str, id: UUID):
        """
        Delete a monitor

        Args:
            workspace_id (str): Workspace id
            id (UUID): id of monitor to update

        """
        self.delete(self.monitors_url(workspace_id), f"{id}")

    def get_monitors_by_metric(
        self, workspace_id: str, metric_uuid: UUID
    ) -> list[dict]:
        """
        Get all monitors on a metric

        Args:
            workspace_id (str): Workspace id
            metric_uuid (UUID): Metric id

        Returns:
            list: a list of monitors
        """
        url = urllib.parse.urljoin(
            self.monitors_url(workspace_id), f"?metric_uuids={metric_uuid}"
        )
        return self.get(url)

    def last_processed_timestamp(self, workspace_id: str, id: UUID) -> Optional[float]:
        """
        Get the timestamp of the last processed datapoint for a monitor

        Args:
            workspace_id (str): Workspace id
            id (UUID): Monitor id

        Returns:
            float: timestamp of last processed datapointlist: a list of monitors
        """
        monitor = self.get_monitor(id, workspace_id)
        if monitor is None:
            return None
        return monitor["status"]["lastSampleTs"]
