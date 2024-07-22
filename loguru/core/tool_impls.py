from langchain_core.pydantic_v1 import BaseModel, Field
from prettytable import PrettyTable

from loguru.core.models.config import Config


def print_dict(dict_to_print: dict, column_names=None):
    if column_names is None:
        column_names = ["Key", "Value"]
    t = PrettyTable(column_names)
    for k in dict_to_print:
        t.add_row([k, dict_to_print[k]])
    print(t)


class LogSearchTool(BaseModel):
    """Find or search logs of a specified pattern"""
    severity: str = Field(None,
                          description="A type or level or severity of log. Example: ERROR, WARN, WARNING, INFO, DEBUG, SEVERE or ALL")
    pattern: str = Field(None, description="Pattern to search with. Example: *, *.thread")

    def run(self, config: dict, user_query: str):
        config = Config(**config)
        print(f"Finding logs with severity: {self.severity}, pattern: {self.pattern}. User query: {user_query}")
