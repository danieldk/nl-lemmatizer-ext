from pathlib import Path
from typing import Callable

import spacy
from spacy.language import Language
from spacy.training import Example
import srsly


def create_remove_irregular_lemmas(
    lexicon: Path,
) -> Callable[[Language, Example], Example]:
    """Augmenter that removes lemmas with irregular forms.

    This augmenter can be used to train a lemmatizer on lemmas with
    a regular inflection paradigm."""
    irregular = srsly.read_json(lexicon)
    irregular = {pos: set(lemmas) for pos, lemmas in irregular.items()}

    def augment(nlp: Language, example: Example):
        for token in example.reference:
            # Auxiliary verbs are in the VERB lookup table.
            pos = "VERB" if token.pos_ == "AUX" else token.pos_

            irregular_lemmas = irregular.get(pos)
            if irregular_lemmas is not None and token.lemma_ in irregular_lemmas:
                token.lemma = 0
        yield example

    return augment
