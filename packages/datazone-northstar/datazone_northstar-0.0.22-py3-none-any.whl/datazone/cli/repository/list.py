from rich.console import Console
from rich.table import Table

from datazone.service_callers.crud import CrudServiceCaller

schedule_columns = ["ID", "Name", "Draft"]


def list_func(page_size: int = 20):
    response_data = CrudServiceCaller(service_name="job", entity_name="project").get_entity_list(
        params={"page_size": page_size},
    )
    console = Console()

    table = Table(*schedule_columns)
    for datum in response_data.get("items"):
        values = [
            datum.get("_id"),
            datum.get("name"),
            "Y" if datum.get("is_draft") else "N",
        ]
        table.add_row(*values)
    console.print(table)
