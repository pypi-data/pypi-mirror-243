import click

from lightctl.client.workspace_client import WorkspaceClient

workspace_client = WorkspaceClient()


@click.group()
def workspace():
    """
    configure and query lightup workspaces
    """


@workspace.command()
@click.pass_obj
def list(context_obj):
    """
    list all workspaces accessible to the user
    """
    res = workspace_client.list_workspaces()
    context_obj.printer.print(res)


@workspace.command()
@click.argument("name")
@click.pass_obj
def create(context_obj, name):
    """
    create a workspace
    """
    res = workspace_client.create_workspace(name)
    context_obj.printer.print(res)


@workspace.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def delete(context_obj, id):
    """
    delete workspace based on specified uuid
    """
    res = workspace_client.delete_workspace(id)
    context_obj.printer.print(res)
