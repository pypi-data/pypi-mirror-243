import logging
import urllib.parse

from lightctl.client.base_client import BaseClient

logger = logging.getLogger(__name__)


class WorkspaceClient(BaseClient):
    """
    Helper functions for acessing the workspaces in a cluster

    Example:
      wc = WorkspaceClient()
      workspaces = wc.list_workspaces()
      new_workspace = wc.create_workspace("test_workspace")
    """

    def workspaces_url(self) -> str:
        """
        Returns:
           str: The workspaces endpoint, used for getting existing workspaces, creating new workspaces, and deleting workspaces
        """
        return urllib.parse.urljoin(self.url_base, "/api/v1/workspaces/")

    def create_workspace(self, name: str):
        """
        Create a new workspace

        Args:
            name (str): Name of workspace

        Returns:
            dict: The workspace created

        Example:
            wc = workspace_client()
            new_workspace = wc.create_workspace("new_workspace")
            print(f'Name of workspace is {new_workspace["name"]}, uuid of workspace is {new_workspace["uuid"]}')
        """
        url = self.workspaces_url()
        payload = {"name": name}
        res = self.post(url, payload)
        return res["data"]

    def delete_workspace(self, workspace_id: str) -> dict:
        """
        Delete a workspace

        Args:
            workspace_id (str): UUID of workspace

        Returns:
            str: The uuid of the workspace deleted
        """
        # note that delete workspace is associated with different url.
        url = urllib.parse.urljoin(self.url_base, "/api/v1/ws/")
        return self.delete(url, workspace_id, force=True)

    def list_workspaces(self) -> list[dict]:
        """
        Get all workspaces

        Returns:
            list: a list of workspaces
        """
        res = self.get(self.workspaces_url())
        return res["data"]
