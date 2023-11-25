import git
from jinja2 import Environment
from jinja2.ext import Extension


class GitConfigExtension(Extension):

    def get_value(self, *keys: str) -> str:
        return self.gitconfig.get_value(*keys)

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        self.gitconfig = git.config.GitConfigParser()
        environment.globals['gitconfig_get_value'] = self.get_value
