from datetime import date

from jinja2 import Environment
from jinja2.ext import Extension


class CurrentYearExtension(Extension):
    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.globals["current_year"] = date.today().year
