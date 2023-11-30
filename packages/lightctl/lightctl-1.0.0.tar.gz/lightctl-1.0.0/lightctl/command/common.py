from lightctl.util import CliPrinter, FileLoader


class ContextObject:
    """Object to pass to all child commands"""

    def __init__(self, printer: CliPrinter, file_loader: FileLoader, workspace_id: str):
        self.printer: CliPrinter = printer
        self.file_loader: FileLoader = file_loader
        self.workspace_id: str = workspace_id
