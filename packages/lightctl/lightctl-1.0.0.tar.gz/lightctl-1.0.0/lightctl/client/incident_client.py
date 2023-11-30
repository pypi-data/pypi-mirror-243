import logging
import urllib.parse
from typing import Optional
from uuid import UUID

from lightctl.client.base_client import BaseClient

logger = logging.getLogger(__name__)


class IncidentClient(BaseClient):
    """
    Helper functions for acessing incidents

    Example:
        mc = MetricClient()
        wc = WorkspaceClient()
        rc = MonitorClient()
        ic = IncidentClient()
        workspace_list = wc.list_workspaces()
        for workspace in workspace_list:
            workspace_id = workspace["uuid"]
            metric_list = mc.list_metrics(workspace_id)
            for metric in metric_list:
                metric_id = metric["metadata"]["uuid"]
                monitor_list = rc.get_monitors_by_metric(workspace_id, metric_id)
                for monitor in monitor_list:
                    incidents = ic.get_incidents(workspace_id, monitor["metadata"]["uuid"], start_ts, end_ts)
                    num_incidents = 0
                    if len(incidents) > 0:
                        num_incidents = len(incidents)
                        print("Workspace {workspace['name']} Metric {metric['metatdata']['name']} Monitor {monitor['metadata']['name']} {num_incidents} Incidents)
    """

    INCIDENT_STATUS_MAP = {
        "unviewed": 1,
        "viewed": 2,
        "rejected": 3,
        "submitted": 4,
        "closed": 5,
    }

    def incidents_url(self, workspace_id) -> str:
        """
        Returns:
           str: The incidents endpoint, used for getting incidents
        """
        return urllib.parse.urljoin(
            self.url_base, f"/api/v0/ws/{workspace_id}/incidents/"
        )

    def list_incidents(
        self,
        workspace_id: str,
        start_ts: int,
        end_ts: int,
        *,
        monitor_id: Optional[str] = None,
        metric_id: Optional[str] = None,
        source_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        """
        Args:
            workspace_id (str): Id of workspace
            start_ts (int): start of time range in which to search for incidents
            end_ts (int): end of time range in which to search for incidets
            monitor_id (str): [Optional] Id of monitor associated with the incident
            metric_id (str): [Optional] Id of metric associated with the incident
            source_id (str): [Optional] Id of datasource associated with the incident
            status (str): [Optional] Incident status

        Returns:
            list: List of matching incidents in the specified time range
        """
        assert UUID(workspace_id)
        monitor_id_str = f"&monitor_uuids={monitor_id}" if monitor_id else ""
        metric_id_str = f"&metric_uuids={metric_id}" if metric_id else ""
        source_id_str = f"&source_uuids={source_id}" if source_id else ""

        status = self.INCIDENT_STATUS_MAP.get(status)
        status_list_str = f"&status_list={status}" if status else ""

        assert start_ts is not None
        assert end_ts is not None
        assert start_ts < end_ts

        url = (
            self.incidents_url(workspace_id)
            + f"?start_ts={start_ts}&end_ts={end_ts}"
            + f"{monitor_id_str}{metric_id_str}{source_id_str}"
            + f"{status_list_str}"
        )
        return self.get(url).get("data")

    def update_incident_status(self, workspace_id: str, id: str, status: str) -> dict:
        incident_status = self.INCIDENT_STATUS_MAP.get(status)
        assert incident_status is not None, f"invalid incident status '{status}'"
        url = urllib.parse.urljoin(self.incidents_url(workspace_id), f"{id}")
        return self.patch(url, data={"status": incident_status})

    def update_incident_validation(
        self, workspace_id: str, id: str, status: str
    ) -> dict:
        validation_status = status.lower()
        assert validation_status in [
            "running",
            "canceling",
        ], f"invalid validation status '{status}"
        url = urllib.parse.urljoin(self.incidents_url(workspace_id), f"{id}")
        return self.patch(url, data={"validation": {"status": validation_status}})
