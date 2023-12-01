from radicli import Radicli

cli = Radicli()

from . import convert
from . import extend_pipeline


def main():
    cli.run()
