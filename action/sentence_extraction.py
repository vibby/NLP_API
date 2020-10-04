"""Extracts sentences from text."""
import logging

import nltk

from action.abstract_action import AbstractAction


class SentenceExtraction(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('snt', 'Extracts sentences.')

    def validate_content(self, content):
        """Validates the provided content to ensure it's a string.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return super().validate_content(content) and isinstance(content, str)

    def apply(self, content):
        """Applies the sentence extraction action to the given content.

        :param content: The content to extract sentences from.
        :type content: dict
        :return: A dict containing this action's name and the sentences, or
                    the provided content if this action was invalid.
        :rtype: dict
        """

        logging.info('Extracting Sentences')

        sentences = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            try:

                sentences = nltk.sent_tokenize(prepared_content)

                sentences = {
                    AbstractAction.ACTION: self.__class__.__name__,
                    AbstractAction.RESULT: sentences,
                    AbstractAction.HISTORY: []}

            except Exception as e:

                logging.error(
                    'Error while trying to extract sentences from text!')

                logging.error(e)

                self.outcome = self.FAILURE

                sentences = content

        else:

            logging.warning('Content wasn\'t valid for extracting sentences.')

            self.outcome = self.FAILURE

            sentences = content

        self.record_outcome(sentences, content)

        return sentences
