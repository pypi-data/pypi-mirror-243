from rich.table import Table
from rich.console import Console
import psutil

def create_table(params, values):
    table = Table()
    for param, value in zip(params, values):
        table.add_column(param)
    table.add_row(*values)
    console = Console()
    console.print(table)

def get_ram_usage():
    return f'{round(psutil.virtual_memory().used / 10000000)} MB'
