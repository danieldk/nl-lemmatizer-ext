from collections import defaultdict
from pathlib import Path
import re

import srsly
from radicli import Arg

from . import cli
from .convert import read_and_convert_gigant

_VALUES = re.compile(r"VALUES \((.*)\);$")
_DELIMITER = re.compile(r", ?")

_VERB_INSERT = r"INSERT INTO `Werkwoorden`"


@cli.command(
    "convert-rbn",
    rbn_sql_path=Arg(help="RBN SQL dump file"),
    gigant_tsv_path=Arg(help="GiGaNT TSV file"),
    lexicon_path=Arg(help="Lexicon output file"),
)
def convert_rbn(rbn_sql_path: Path, gigant_tsv_path: Path, lexicon_path: Path):
    """Extract lemmas with irregular inflection paradigm from RBN."""
    with open(gigant_tsv_path, "r", encoding="utf-8") as f:
        gigant_lexicon = read_and_convert_gigant(f)
    gigant_verbs = gigant_lexicon["VERB"]

    # This is a bit ugly, the data set is provided as an Access database
    # or an access SQL dump. To avoid a dependency on a SQL parser, SQL
    # database, or worse, Access, we'll do some good regex parsing of the
    # SQL insertions for irregular verbs.
    irregular_lexicon = defaultdict(set)
    with open(rbn_sql_path, "r", encoding="utf8") as f:
        for line in f:
            if not line.startswith(_VERB_INSERT):
                continue

            match = _VALUES.search(line)
            if not match:
                continue

            values = _DELIMITER.split(match.group(1))

            lemma = values[0].strip("'")
            conjugation = values[10].strip("'")
            if conjugation == "regular":
                continue

            if lemma in gigant_verbs:
                irregular_lexicon["VERB"].add(lemma)

    # JSON does not support sets, so convert lemma sets to lists.
    srsly.write_json(
        lexicon_path, {pos: list(lemmas) for pos, lemmas in irregular_lexicon.items()}
    )
