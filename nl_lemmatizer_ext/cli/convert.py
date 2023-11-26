from collections import defaultdict
from pathlib import Path
from typing import Dict
from radicli import Arg
import srsly

from . import cli


POS_MAPPING = {
    "ADP": "ADP",
    "ADV": "ADV",
    "AA": "ADJ",
    "CONJ": "CONJ",
    "INT": "INTJ",
    "NOU-C": "NOUN",
    "NOU-P": "PROPN",
    "NUM": "NUM",
    "PD": "PRON",
    "COLL": "COLL",
    "RES": "RES",
    "VRB": "VERB",
}

FILTER_TAGS = {"COLL", "RES"}


def ud_pos_tag(pos_tag):
    # GiGaNT has POS tags like NOU-C(gender=m,number=sg), for the UD
    # mapping we do not need the additional features.
    paren_idx = pos_tag.find("(")
    if paren_idx != -1:
        pos_tag = pos_tag[:paren_idx]
    pos_tag = POS_MAPPING[pos_tag]
    return pos_tag


def skip_form_lemma(form: str, lemma: str) -> bool:
    # Filter collocations.
    if " " in form:
        return True

    # Filter separable verbs.
    if " " in lemma:
        return True

    return False


@cli.command(
    "convert",
    gigant_tsv_path=Arg(help="GiGaNT TSV file"),
    lexicon_path=Arg(help="Lexicon output file"),
)
def convert(gigant_tsv_path: Path, lexicon_path: Path):
    """Convert GiGaNT-Molex TSV data to JSON lexicon"""
    lexicon: Dict[str, Dict[str, str]] = defaultdict(dict)

    with open(gigant_tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            lemma = parts[1]
            pos = ud_pos_tag(parts[2])
            form = parts[4]

            if pos in FILTER_TAGS:
                continue

            if skip_form_lemma(form, lemma):
                continue

            lexicon[pos][form] = lemma

    srsly.write_json(lexicon_path, lexicon)
