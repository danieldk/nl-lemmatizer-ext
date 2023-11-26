from radicli import Radicli

cli = Radicli()

from . import convert
from . import extend_model


def main():
    cli.run()
