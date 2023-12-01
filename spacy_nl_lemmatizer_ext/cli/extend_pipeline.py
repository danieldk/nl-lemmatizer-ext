from pathlib import Path
from typing import Dict

import srsly
from radicli import Arg
import spacy

from . import cli


@cli.command(
    "extend-pipeline",
    model=Arg(help="spaCy model to extend"),
    lexicon=Arg(help="Lexicon file"),
    model_output=Arg(help="Extended spaCy model"),
)
def extend_pipeline(model: str, lexicon: Path, model_output: Path):
    """Add the GiGaNT lemmatizer to a pipeline"""
    nlp = spacy.load(model)
    lexicon: Dict[str, Dict[str, str]] = srsly.read_json(lexicon)
    lemmatizer = nlp.add_pipe("gigant_lemmatizer")
    lemmatizer.initialize(lexicon=lexicon)
    nlp.to_disk(model_output)
