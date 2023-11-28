from pathlib import Path

import spacy  # type: ignore
from spacy.language import Language
from spacy.tokenizer import Tokenizer  # type: ignore
from spacy.tokens import Doc, Span
from spacy.util import filter_spans

from .rules import (
    ENTITY_RULER_LABELS,
    INFIXES_OVERRIDE,
    SPAN_RULER_LABELS,
    Label,
    Prov,
    Rule,
    WordAttributes,
    create_special_rules,
    custom_prefix_list,
    custom_suffix_list,
)

RULES_DIR = Path(__file__).parent.joinpath("rules")

ENTITY_RULES = list(Rule.extract_from_files(folder=RULES_DIR, ents=True))

SPAN_RULES = list(Rule.extract_from_files(folder=RULES_DIR, ents=False))


def set_tokenizer(nlp: Language) -> Tokenizer:
    infix_re = spacy.util.compile_infix_regex(INFIXES_OVERRIDE)  # type: ignore
    suffix_re = spacy.util.compile_suffix_regex(custom_suffix_list(nlp))
    prefix_re = spacy.util.compile_prefix_regex(custom_prefix_list(nlp))
    return Tokenizer(
        nlp.vocab,
        rules=create_special_rules(),
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
    )


def set_attribute_ruler(nlp: Language):
    ruler = nlp.get_pipe("attribute_ruler")
    for rule in WordAttributes.make_attr_rules():
        ruler.add(**rule)  # type: ignore
    for rule in Prov.make_attr_rules():
        ruler.add(**rule)  # type: ignore
    return nlp


def set_tokens(nlp: Language):
    nlp.tokenizer = set_tokenizer(nlp)
    nlp = set_attribute_ruler(nlp)
    return nlp


def create_custom_entities(
    nlp: Language,
    rules: list[Rule],
    pipename: str = "entity_ruler",
):
    ents = nlp.add_pipe(
        factory_name="entity_ruler",
        name=pipename,
        config={"overwrite_ents": True, "validate": True},
        validate=True,
    )
    for rule in rules:
        ents.add_patterns(rule.model_dump())  # type: ignore
    return nlp


def create_custom_spans(nlp: Language, rules: list[Rule]):
    for rule in rules:
        container = f"span_ruler_{rule.label.name}"
        try:
            spans = nlp.get_pipe(container)
        except KeyError:
            spans = nlp.add_pipe(
                "span_ruler",
                name=container,
                config={
                    "spans_key": rule.label.name,
                    "validate": True,
                },  # spans_key for accessing doc.spans[spans_key]
                validate=True,
            )
        spans.add_patterns(rule.model_dump())  # type: ignore
    return nlp


@Language.component("provision_num_merger")
def merge_provisions(doc: Doc) -> Doc:
    """Consecutive `ProvisionNum` entities merged as a _single_ `ProvisionNum` token and entity."""
    pairs = [(e.start, e.end) for e in doc.ents if e.label_ == Label.ProvisionNum.name]
    pair = None
    new_ents = []
    for ent in doc.ents:
        if ent.label_ == Label.ProvisionNum.name:
            s = ent.start
            if pair and s == pair[1]:
                s = pair[0]
            pair = (s, ent.end)
        if pair and pair not in pairs:
            new_ents.append(
                Span(doc=doc, start=pair[0], end=pair[1], label=Label.ProvisionNum.name)
            )
    if new_ents:
        doc.ents = filter_spans(new_ents + list(doc.ents))
    return doc


@Language.factory("detector")
class EntitySpanDetectorComponent:
    """Dynamic creation of custom attributes (`doc._.<attribute>`)  based on `Label` objects."""

    def __init__(self, nlp, name):
        labels = ENTITY_RULER_LABELS + SPAN_RULER_LABELS
        for label in labels:
            if not Doc.has_extension(label.snakecase):
                Doc.set_extension(label.snakecase, default=[])

    def __call__(self, doc):
        for label in ENTITY_RULER_LABELS:
            doc._.set(label.snakecase, label.extract_entities(doc))

        for label in SPAN_RULER_LABELS:
            try:
                doc._.set(label.snakecase, label.extract_spans(doc))
            except KeyError:
                continue

        return doc


def lextok(
    model: str = "en_core_web_sm",
    entity_rules: list[Rule] = ENTITY_RULES,
    span_rules: list[Rule] = SPAN_RULES,
) -> Language:
    """Incorporation of:

    1. overrides for `set_tokenizer()` and `set_attribute_ruler()`
    2. extendible entity ruler / span ruler patterns, see the `Rule` object
    3. last pipe `detector` which creates custom attributes on each `Doc`
    based on `Label`s detected.

    Args:
        model (str, optional): Spacy language model. Defaults to "en_core_web_sm".
        entity_rules (list[Rule], optional): List of generic Pydantic models with serialization. Defaults to `ENTITY_RULES`.
        span_rules (list[Rule], optional): List of generic Pydantic models with serialization. Defaults to `SPAN_RULES`.

    Returns:
        Language: A customized rule-based spacy model.
    """
    nlp = set_tokens(spacy.load(model))
    create_custom_entities(nlp, rules=entity_rules, pipename="entity_ruler")
    nlp.add_pipe("merge_entities", after="entity_ruler")
    nlp.add_pipe("provision_num_merger", after="merge_entities")
    create_custom_spans(nlp, rules=span_rules)
    nlp.add_pipe("detector", last=True)
    return nlp
