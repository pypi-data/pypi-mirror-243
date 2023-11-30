import logging
import urllib.parse
from typing import Optional

from lightctl.client.base_client import BaseClient
from lightctl.config import API_VERSION

logger = logging.getLogger(__name__)


class DatapointClient(BaseClient):
    """
    Helper functions for accessing datapoints
    """

    def metric_datapoints_url(self, workspace_id: str, metric_uuid: str) -> str:
        """
        Returns:
           str: The metric datapoints endpoint, used for getting list of datapoints
           for a metric
        """
        return urllib.parse.urljoin(
            self.url_base,
            f"/api/{API_VERSION}/ws/{workspace_id}/metrics/{metric_uuid}/datapoints",
        )

    def get_metric_datapoints(
        self,
        workspace_id: str,
        metric_uuid: str,
        start_ts: Optional[int] = None,
        end_ts: Optional[int] = None,
    ) -> list[dict]:
        """
        get datapoints for an input metric
        """
        endpoint = self.metric_datapoints_url(workspace_id, metric_uuid)
        args = []
        if start_ts:
            args.append(f"start_ts={start_ts}")
        if end_ts:
            args.append(f"end_ts={end_ts}")
        if args:
            endpoint += f"?{'&'.join(args)}"
        return self.get(endpoint)

    def monitor_datapoints_url(self, workspace_id: str, monitor_uuid: str) -> str:
        """
        Returns:
           str: The monitor datapoints endpoint, used for getting list of datapoints
           for a monitor
        """
        return urllib.parse.urljoin(
            self.url_base,
            f"/api/{API_VERSION}/ws/{workspace_id}/monitors/{monitor_uuid}/metrics",
        )

    def get_monitor_datapoints(
        self, workspace_id: str, monitor_uuid: str, start_ts: int, end_ts: int
    ) -> list[dict]:
        """
        get datapoints for an input monitor
        """
        endpoint = self.monitor_datapoints_url(workspace_id, monitor_uuid)
        args = []
        args.append(f"start_ts={start_ts}")
        args.append(f"end_ts={end_ts}")
        endpoint += f"?{'&'.join(args)}"

        return self.get(endpoint)
