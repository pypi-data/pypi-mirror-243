import click

from lightctl.client.monitor_client import MonitorClient

monitor_client = MonitorClient()


@click.group()
def monitor():
    """
    configure and query lightup monitors
    """


@monitor.command()
@click.pass_obj
def list(context_obj):
    """
    list all monitors in a workspace
    """
    res = monitor_client.list_monitors(context_obj.workspace_id)
    context_obj.printer.print(res)


@monitor.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def get(context_obj, id):
    """
    list specified monitor in a workspace
    """
    res = monitor_client.get_monitor(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@monitor.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def delete(context_obj, id):
    """
    delete the specified monitor
    """
    res = monitor_client.delete_monitor(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@monitor.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def clone(context_obj, id):
    """
    clone a monitor by id; new monitor name will have _Clone added to it
    """
    res = monitor_client.get_monitor(context_obj.workspace_id, id)
    if not res:
        context_obj.printer.print({"error": "not found"})

    res["metadata"].pop("uuid")
    res["metadata"]["name"] += "_Clone"
    res = monitor_client.create_monitor(res)
    context_obj.printer.print(res)


@monitor.command()
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def create(context_obj, file):
    """
    create a monitor in the specified workspace from json or yaml file
    """
    data = context_obj.file_loader.load(file)
    res = monitor_client.create_monitor(context_obj.workspace_id, data)
    context_obj.printer.print(res)


@monitor.command()
@click.argument("id", type=click.UUID)
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def update(context_obj, id, file):
    """
    update a monitor in the specified workspace from json or yaml file
    """
    data = context_obj.file_loader.load(file)
    res = monitor_client.update_monitor(context_obj.workspace_id, id, data)
    context_obj.printer.print(res)
