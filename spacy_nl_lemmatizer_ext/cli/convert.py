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


def skip_form_lemma(*, form: str, lemma: str, lemma_pos: str, ud_pos: str) -> bool:
    # Filter collocations.
    if ud_pos != "VERB" and " " in form:
        return True

    # Filter separable verbs.
    if " " in lemma:
        return True

    # Skip plural noun lemmas.
    if ud_pos == "NOUN" and "number=pl" in lemma_pos:
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
            ud_pos = ud_pos_tag(parts[2])
            lemma_pos = parts[2]
            form = parts[4]

            if ud_pos in FILTER_TAGS:
                continue

            if skip_form_lemma(
                form=form, lemma=lemma, lemma_pos=lemma_pos, ud_pos=ud_pos
            ):
                continue

            if ud_pos in lexicon:
                if form in lexicon[ud_pos]:
                    if lexicon[ud_pos][form] != lemma:
                        print(
                            f"Existing entry for {form}/{ud_pos}: {lexicon[ud_pos][form]} -> {lemma}"
                        )

            lexicon[ud_pos][form] = lemma

    srsly.write_json(lexicon_path, lexicon)
