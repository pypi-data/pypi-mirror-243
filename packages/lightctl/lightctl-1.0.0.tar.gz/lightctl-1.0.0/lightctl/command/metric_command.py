import click

from lightctl.client.metric_client import MetricClient

metric_client = MetricClient()


@click.group()
def metric():
    """
    configure and query lightup metrics
    """


@metric.command()
@click.pass_obj
def list(context_obj):
    """
    list all metrics in a workspace
    """
    res = metric_client.list_metrics(context_obj.workspace_id)
    context_obj.printer.print(res)


@metric.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def get(context_obj, id):
    """
    list metric based on uuid
    """
    res = metric_client.get_metric(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@metric.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def delete(context_obj, id):
    """
    delete metric based on uuid
    """
    res = metric_client.delete_metric(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@metric.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def clone(context_obj, id):
    """
    clone a metric by uuid. clone will add _Clone to the metric name
    """
    res = metric_client.get_metric(context_obj.workspace_id, id)
    if not res:
        context_obj.printer.print({"error": "not found"})

    res["metadata"].pop("uuid")
    res["metadata"]["name"] += "_Clone"
    res = metric_client.create_metric(context_obj.workspace_id, res)
    context_obj.printer.print(res)


@metric.command()
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def create(context_obj, file):
    """
    create metric from yaml or json file
    """
    data = context_obj.file_loader.load(file)
    res = metric_client.create_metric(context_obj.workspace_id, data)
    context_obj.printer.print(res)


@metric.command()
@click.argument("id", type=click.UUID)
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def update(context_obj, id, file):
    """
    update metric from yaml or json file
    """
    data = context_obj.file_loader.load(file)
    res = metric_client.update_metric(context_obj.workspace_id, id, data)
    context_obj.printer.print(res)
