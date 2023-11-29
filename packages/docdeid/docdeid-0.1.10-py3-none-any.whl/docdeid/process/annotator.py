import re
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Union

from docdeid.annotation import Annotation
from docdeid.document import Document
from docdeid.ds.lookup import LookupSet, LookupTrie
from docdeid.pattern import TokenPattern
from docdeid.process.doc import DocProcessor
from docdeid.str.processor import StringModifier
from docdeid.tokenize import Token, Tokenizer


class Annotator(DocProcessor, ABC):
    """
    Abstract class for annotators, which are responsible for generating annotations from a given document. Instatiations
    should implement the annotate method.

    Args:
        tag: The tag to use in the annotations.
    """

    def __init__(self, tag: str, priority: int = 0) -> None:
        self.tag = tag
        self.priority = priority

    def process(self, doc: Document, **kwargs) -> None:
        """
        Process a document, by adding annotations to its :class:`.AnnotationSet`.

        Args:
            doc: The document to be processed.
            **kwargs: Any other settings.
        """
        doc.annotations.update(self.annotate(doc))

    @abstractmethod
    def annotate(self, doc: Document) -> list[Annotation]:
        """
        Generate annotations for a document.

        Args:
            doc: The document that should be annotated.

        Returns:
            A list of annotations.
        """


class SingleTokenLookupAnnotator(Annotator):
    """
    Matches single tokens based on lookup values.

    Args:
        tag: The tag to use in the annotations.
        lookup_values: An iterable of strings that should be used for lookup.
        matching_pipeline: An optional pipeline that can be used for matching (e.g. lowercasing). Note that this
            degrades performance.
        tokenizer_name: If not taking tokens from the ``default`` tokenizer, specify which tokenizer to use. The
            tokenizer should be present in :attr:`.DocDeid.tokenizers`.
    """

    def __init__(
        self,
        lookup_values: Iterable[str],
        *args,
        matching_pipeline: Optional[list[StringModifier]] = None,
        tokenizer_name: str = "default",
        **kwargs,
    ) -> None:

        self.lookup_set = LookupSet(matching_pipeline=matching_pipeline)
        self.lookup_set.add_items_from_iterable(items=lookup_values)
        self._tokenizer_name = tokenizer_name
        super().__init__(*args, **kwargs)

    def _tokens_to_annotations(self, tokens: list[Token]) -> list[Annotation]:
        """
        Process the matched tokens to annotations.

        Args:
            tokens: The list of matched tokens.

        Returns: The list of annotations.
        """

        return [
            Annotation(
                text=token.text,
                start_char=token.start_char,
                end_char=token.end_char,
                tag=self.tag,
                priority=self.priority,
                start_token=token,
                end_token=token,
            )
            for token in tokens
        ]

    def annotate(self, doc: Document) -> list[Annotation]:
        annotate_tokens: list[Token]
        tokens = doc.get_tokens(tokenizer_name=self._tokenizer_name)

        if self.lookup_set.has_matching_pipeline():
            annotate_tokens = [token for token in tokens if token.text in self.lookup_set]
        else:
            annotate_tokens = list(tokens.token_lookup(self.lookup_set.items()))

        return self._tokens_to_annotations(annotate_tokens)


class MultiTokenLookupAnnotator(Annotator):
    """
    Matches lookup values against tokens, where the ``lookup_values`` may themselves be sequences.

    Args:
        tag: The tag to use in the annotations.
        lookup_values: An iterable of strings, that should be matched. These are tokenized internally.
        tokenizer: A tokenizer that is used to create the sequence patterns from ``lookup_values``.
        matching_pipeline: An optional pipeline that can be used for matching (e.g. lowercasing). This has no specific
            impact on matching performance, other than overhead for applying the pipeline to each string.
        overlapping: Whether the annotator should match overlapping sequences, or should process from left to right.
    """

    def __init__(
        self,
        lookup_values: Iterable[str],
        tokenizer: Tokenizer,
        *args,
        matching_pipeline: Optional[list[StringModifier]] = None,
        overlapping: bool = False,
        **kwargs,
    ) -> None:

        self.overlapping = overlapping
        self.trie = LookupTrie(matching_pipeline=matching_pipeline)

        for val in lookup_values:
            self.trie.add_item([token.text for token in tokenizer.tokenize(val)])

        super().__init__(*args, **kwargs)

    def annotate(self, doc: Document) -> list[Annotation]:
        tokens = doc.get_tokens()
        tokens_text = [token.text for token in tokens]
        annotations = []

        for i in range(len(tokens_text)):

            longest_matching_prefix = self.trie.longest_matching_prefix(tokens_text[i:])

            if longest_matching_prefix is None:
                continue

            start_token = tokens[i]
            end_token = tokens[i + len(longest_matching_prefix) - 1]

            annotations.append(
                Annotation(
                    text=doc.text[start_token.start_char : end_token.end_char],
                    start_char=start_token.start_char,
                    end_char=end_token.end_char,
                    start_token=start_token,
                    end_token=end_token,
                    tag=self.tag,
                    priority=self.priority,
                )
            )

            if not self.overlapping:
                i += len(longest_matching_prefix)  # skip ahead

        return annotations


class RegexpAnnotator(Annotator):
    """
    Create annotations based on regular expression patterns. Note that these patterns do not necessarily start/stop on
    token boundaries.

    Args:
        tag: The tag to use in the annotations.
        regexp_pattern: A compiled ``re.Pattern``, that will be used for matching.
        capturing_group: The capturing group of the pattern that should be used to produce the annotation. By default,
            the entire match is used.
    """

    def __init__(self, regexp_pattern: Union[re.Pattern, str], *args, capturing_group: int = 0, **kwargs) -> None:

        if isinstance(regexp_pattern, str):
            regexp_pattern = re.compile(regexp_pattern)

        self.regexp_pattern = regexp_pattern
        self.capturing_group = capturing_group
        super().__init__(*args, **kwargs)

    def _validate_match(self, match: re.Match, doc: Document) -> bool:
        return True

    def annotate(self, doc: Document) -> list[Annotation]:
        annotations = []

        for match in self.regexp_pattern.finditer(doc.text):

            if not self._validate_match(match, doc):
                continue

            text = match.group(self.capturing_group)
            start_char, end_char = match.span(self.capturing_group)

            annotations.append(
                Annotation(text=text, start_char=start_char, end_char=end_char, tag=self.tag, priority=self.priority)
            )

        return annotations


class TokenPatternAnnotator(Annotator):
    """
    Annotate based on :class:`.TokenPattern`.

    Args:
        pattern: The token pattern that should be used.
    """

    def __init__(self, pattern: TokenPattern, *args, **kwargs) -> None:
        self.pattern = pattern
        kwargs["tag"] = pattern.tag
        super().__init__(*args, **kwargs)

    def annotate(self, doc: Document) -> list[Annotation]:
        annotations: list[Annotation] = []

        if not self.pattern.doc_precondition(doc):
            return annotations

        for token in doc.get_tokens():

            if not self.pattern.token_precondition(token):
                continue

            match = self.pattern.match(token, doc.metadata)

            if match is None:
                continue

            start_token, end_token = match

            annotations.append(
                Annotation(
                    text=doc.text[start_token.start_char : end_token.end_char],
                    start_char=start_token.start_char,
                    end_char=end_token.end_char,
                    tag=self.tag,
                    priority=self.priority,
                    start_token=start_token,
                    end_token=end_token,
                )
            )

        return annotations
