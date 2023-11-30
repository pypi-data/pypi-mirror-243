import click

from lightctl.client.healthz_client import HealthzClient
from lightctl.command.common import ContextObject
from lightctl.version import __version__

healthz_client = HealthzClient()


@click.command()
@click.pass_obj
def version(context_obj: ContextObject):
    """
    show lightctl version and cluster information
    """
    server_info = healthz_client.get_healthz_info()
    backend_image = server_info["image_and_tags"]["backend"]
    backend_version = backend_image.split("@")[0].split(":")[1]
    res = {
        "lightctl version": __version__,
        "cluster": healthz_client.url_base,
        "cluster version": backend_version,
    }
    context_obj.printer.print(res)
