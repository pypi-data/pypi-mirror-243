from lightctl.client.datapoint_client import DatapointClient
from lightctl.client.healthz_client import HealthzClient
from lightctl.client.incident_client import IncidentClient
from lightctl.client.metric_client import MetricClient
from lightctl.client.monitor_client import MonitorClient
from lightctl.client.profiler_client import ProfilerClient
from lightctl.client.source_client import SourceClient
from lightctl.client.user_client import UserClient
from lightctl.client.workspace_client import WorkspaceClient


class LightupClient:
    def __init__(self):
        self.datapoint = DatapointClient()
        self.healthz = HealthzClient()
        self.incident = IncidentClient()
        self.metric = MetricClient()
        self.monitor = MonitorClient()
        self.profiler = ProfilerClient()
        self.source = SourceClient()
        self.user = UserClient()
        self.workspace = WorkspaceClient()
