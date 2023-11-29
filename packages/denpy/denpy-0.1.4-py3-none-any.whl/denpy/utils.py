from rich.table import Table
from rich.console import Console

def create_table(params, values):
    table = Table()
    for param, value in zip(params, values):
        table.add_column(param)
    table.add_row(*values)
    console = Console()
    console.print(table)
