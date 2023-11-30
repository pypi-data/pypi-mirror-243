import logging
import urllib.parse

from lightctl.client.base_client import BaseClient

logger = logging.getLogger(__name__)


class HealthzClient(BaseClient):
    """
    Helper functions for acessing metrics

    Example:
        hc = HealthzClient()
        hc.get_healthz_info()

    """

    @property
    def healthz_url(self) -> str:
        """
        Returns:
           str: The healthz endpoint
        """
        return urllib.parse.urljoin(self.url_base, "/api/v0/healthz/")

    def get_healthz_info(self) -> dict:
        """
        Get healthz info

        Returns:
            dict: healthz info
        """
        return self.get(self.healthz_url)
