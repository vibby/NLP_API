"""Extracts words from text."""
import logging

import nltk

from action.abstract_action import AbstractAction
from action.sentence_extraction import SentenceExtraction


class WordExtraction(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('word', 'Extracts words.')

    def validate_content(self, content):
        """Validates the provided content to ensure it is a string or was
        produced by SentenceExtraction.

        :param content: The content to validate.
        :type content: dict or str
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            (
                isinstance(content, str) or
                SentenceExtraction.produced(content)
            )
        )

    def prepare_content(self, content):
        """Prepares the content for word extraction.

        :param content: The content to prepare.
        :type content: dict or str
        :return: The prepared content, in this case a string.
        :rtype: str
        """

        prepared_content = super().prepare_content(content)

        if SentenceExtraction.produced(content):

            prepared_content = ' '.join(prepared_content)

        return prepared_content

    def apply(self, content):
        """Applies the word extraction action to the given content.

        :param content: The content to extract words from.
        :type content: dict or str
        :return: A dict containing this action's name and the words, or the
                    provided content if this action was invalid.
        :rtype: list
        """

        logging.info('Extracting Words')

        words = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            try:

                words = nltk.tokenize.word_tokenize(prepared_content)

                words = {
                    AbstractAction.ACTION: self.__class__.__name__,
                    AbstractAction.RESULT: words,
                    AbstractAction.HISTORY: []}

            except Exception as e:

                logging.error(
                    'Error while trying to extract words from text!')

                logging.error(e)

                self.outcome = self.FAILURE

                words = content

        else:

            logging.warning('Content wasn\'t valid for extracting words.')

            self.outcome = self.FAILURE

            words = content

        self.record_outcome(words, content)

        return words
