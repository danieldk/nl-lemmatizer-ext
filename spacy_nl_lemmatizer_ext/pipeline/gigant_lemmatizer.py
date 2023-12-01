from pathlib import Path
from typing import Optional, Callable, Iterable, Dict, Any, Union, List

import srsly
from spacy import Vocab, util, Language
from spacy.pipeline import Pipe
from spacy.scorer import Scorer
from spacy.tokens import Doc, Token
from spacy.training import Example
from spacy.util import SimpleFrozenList
from thinc.model import Model


Lexicon = Dict[str, Dict[str, str]]


@Language.factory(
    "gigant_lemmatizer",
    assigns=["token.lemma"],
    default_config={
        "model": None,
        "overwrite": True,
        "scorer": {"@scorers": "spacy.lemmatizer_scorer.v1"},
    },
    default_score_weights={"lemma_acc": 1.0},
)
def make_lemmatizer(
    nlp: Language,
    model: Optional[Model],
    name: str,
    overwrite: bool,
    scorer: Optional[Callable],
):
    return GigantLemmatizer(nlp.vocab, model, name, overwrite=overwrite, scorer=scorer)


def lemmatizer_score(examples: Iterable[Example], **kwargs) -> Dict[str, Any]:
    return Scorer.score_token_attr(examples, "lemma", **kwargs)


class GigantLemmatizer(Pipe):
    """
    Lemmatizer using the GiGaNT-Molex lexicon.
    """

    lexicon: Lexicon

    def __init__(
        self,
        vocab: Vocab,
        model: Optional[Model],
        name: str = "gigant_lemmatizer",
        *,
        overwrite: bool = True,
        scorer: Optional[Callable] = lemmatizer_score,
    ):
        self.vocab = vocab
        self.model = model
        self.name = name
        self.overwrite = overwrite
        self.scorer = scorer

    def __call__(self, doc: Doc) -> Doc:
        """Apply the lemmatizer to one document.

        doc (Doc): The Doc to process.
        RETURNS (Doc): The processed Doc.
        """
        error_handler = self.get_error_handler()
        try:
            for token in doc:
                if self.overwrite or token.lemma == 0:
                    lemma = self.lemmatize(token)
                    if lemma is not None:
                        token.lemma_ = lemma
            return doc
        except Exception as e:
            error_handler(self.name, self, [doc], e)

    def initialize(
        self,
        get_examples: Optional[Callable[[], Iterable[Example]]] = None,
        *,
        nlp: Optional[Language] = None,
        lexicon: Optional[Dict[str, Dict[str, str]]] = None,
    ):
        self.lexicon = lexicon

    def lemmatize(self, token: Token) -> Optional[str]:
        """Return the lemma for a token.

        token (Token): the token to lemmatize.
        """
        pos_lexicon = self.lexicon.get(token.pos_)
        if pos_lexicon is None:
            return None

        # Try to look up verb forms with separated particles.
        for particle in self._find_particle(token):
            lemma = pos_lexicon.get(f"{token.text} {particle.text}")
            if lemma is not None:
                return lemma

        return pos_lexicon.get(token.text)

    def _find_particle(self, token: Token) -> List[Token]:
        """Find particles of separable verbs."""

        separated_particles = []
        # This could be refined to check against the relevant verb types.
        if token.pos_ != "VERB":
            return separated_particles

        for child in token.children:
            if child.dep_ == "compound:prt" and child.tag_ == "VZ|fin":
                separated_particles.append(child)

        return separated_particles

    def to_disk(
        self, path: Union[str, Path], *, exclude: Iterable[str] = SimpleFrozenList()
    ):
        """Serialize the pipe to disk.

        path (str / Path): Path to a directory.
        exclude (Iterable[str]): String names of serialization fields to exclude.
        """
        serialize = {}
        serialize["lexicon"] = lambda p: srsly.write_gzip_json(p, self.lexicon)
        util.to_disk(path, serialize, exclude)

    def from_disk(
        self, path: Union[str, Path], *, exclude: Iterable[str] = SimpleFrozenList()
    ) -> "GigantLemmatizer":
        """Load the pipe from disk. Modifies the object in place and returns it.

        path (str / Path): Path to a directory.
        exclude (Iterable[str]): String names of serialization fields to exclude.
        RETURNS (GigantLemmatizer): The modified GigantLemmatizer object.
        """
        deserialize: Dict[str, Callable[[Any], Any]] = {}

        def lexicon_from_disk(p: Path):
            self.lexicon = srsly.read_gzip_json(p)

        deserialize["lexicon"] = lexicon_from_disk
        util.from_disk(path, deserialize, exclude)
        return self

    def to_bytes(self, *, exclude: Iterable[str] = SimpleFrozenList()) -> bytes:
        """Serialize the pipe to a bytestring.

        exclude (Iterable[str]): String names of serialization fields to exclude.
        RETURNS (bytes): The serialized object.
        """
        serialize = {}
        serialize["lexicon"] = lambda: srsly.msgpack_dumps(self.lexicon)
        return util.to_bytes(serialize, exclude)

    def from_bytes(
        self, bytes_data: bytes, *, exclude: Iterable[str] = SimpleFrozenList()
    ) -> "GigantLemmatizer":
        """Load the pipe from a bytestring.

        bytes_data (bytes): The serialized pipe.
        exclude (Iterable[str]): String names of serialization fields to exclude.
        RETURNS (GigantLemmatizer): The loaded GigantLemmatizer.
        """
        deserialize: Dict[str, Callable[[Any], Any]] = {}

        def lexicon_from_bytes(b: bytes):
            self.lexicon = srsly.msgpack_loads(b)

        deserialize["lexicon"] = lexicon_from_bytes
        util.from_bytes(bytes_data, deserialize, exclude)
        return self
