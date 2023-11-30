import click

from lightctl.client.source_client import SourceClient

source_client = SourceClient()


@click.group()
def source():
    """
    configure and query lightup datasources
    """


@source.command()
@click.pass_obj
def list(context_obj):
    """
    list all datasources configurations in a workspace
    """
    res = source_client.list_sources(context_obj.workspace_id)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def get(context_obj, id):
    """
    list datasource configuration for specified source uuid in a workspace
    """
    res = source_client.get_source(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def delete(context_obj, id):
    """
    delete datasource based on specified source uuid
    """
    res = source_client.delete_source(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.option(
    "--metric_uuids",
    is_flag=False,
    metavar="<metric_uuids>",
    type=click.STRING,
    help="Set metric uuids",
)
@click.option(
    "--table_uuids",
    is_flag=False,
    metavar="<table_uuids>",
    type=click.STRING,
    help="Set table uuids",
)
@click.pass_obj
def trigger(context_obj, id, metric_uuids, table_uuids):
    """
    trigger metric or metrics under a table that are configured as triggered
    """
    res = source_client.get_source(context_obj.workspace_id, id)
    if not res:
        context_obj.printer.print({"error": "not found"})
        return
    data = {}
    if metric_uuids:
        metric_uuids = [c.strip() for c in metric_uuids.split(",")]
        data["metricUuids"] = metric_uuids
    if table_uuids:
        table_uuids = [c.strip() for c in table_uuids.split(",")]
        data["tableUuids"] = table_uuids

    res = source_client.trigger_source(context_obj.workspace_id, id, data)
    context_obj.printer.print(res)


@source.command()
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def create(context_obj, file):
    """
    create a datasource in the workspace from json or yaml file
    """
    data = context_obj.file_loader.load(file)
    res = source_client.create_source(context_obj.workspace_id, data)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def update(context_obj, id, file):
    """
    update datasource in the workspace from json or yaml file
    """
    data = context_obj.file_loader.load(file)
    res = source_client.update_source(context_obj.workspace_id, id, data)
    context_obj.printer.print(res)


@source.command()
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def inspect(context_obj, file):
    """
    test datasource configuration validity without saving it
    """
    data = context_obj.file_loader.load(file)
    res = source_client.inspect(context_obj.workspace_id, data)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def list_tables(context_obj, id):
    """
    list all table profiles in a datasource
    """
    res = source_client.list_tables(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.pass_obj
def list_schemas(context_obj, id):
    """
    list all schema profiles in a datasource
    """
    res = source_client.list_schemas(context_obj.workspace_id, id)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.argument("table_id", type=click.UUID)
@click.pass_obj
def list_columns(context_obj, id, table_id):
    """
    list all column profiles in the table in datasource
    """
    res = source_client.list_columns(context_obj.workspace_id, id, table_id)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.argument("table_name")
@click.pass_obj
def table_schema(context_obj, id, table_name):
    """
    get schema for a table in a datasource
    """
    res = source_client.get_table_schema(context_obj.workspace_id, id, table_name)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.argument("table_uuid", type=click.UUID)
@click.pass_obj
def list_table(context_obj, id, table_uuid):
    """
    list a table profile in a datasource
    """
    res = source_client.get_table(context_obj.workspace_id, id, table_uuid)
    context_obj.printer.print(res)


@source.command()
@click.argument("id", type=click.UUID)
@click.argument("table_uuid", type=click.UUID)
@click.argument("file", type=click.Path(exists=True))
@click.pass_obj
def update_table_profiler_config(context_obj, id, table_uuid, file):
    """
    update the profiler config of the table
    """
    data = context_obj.file_loader.load(file)
    res = source_client.update_profiler_config(
        context_obj.workspace_id, id, table_uuid, data
    )
    context_obj.printer.print(res)
