"""POS-Tags a list of words."""
import logging

import nltk

from action.abstract_action import AbstractAction
from action.word_extraction import WordExtraction


class WordPosTagging(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('pos', 'POS-Tags the words in the given text.')

    def validate_content(self, content):
        """Validates the provided content to ensure it was produced by WordExtraction.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            WordExtraction.produced(content)
        )

    def apply(self, content):
        """Applies the word pos tagging action to the given content.

        :param content: The content to pos tag.
        :type content: dict
        :return: A dict containing this action's name and the pos-tagged words,
                    or the provided content if this action was invalid.
        :rtype: dict
        """

        logging.info('POS Tagging Words')

        tagged_words = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            try:

                tagged_words = nltk.pos_tag(prepared_content)

                tagged_words = {
                    AbstractAction.ACTION: self.__class__.__name__,
                    AbstractAction.RESULT: tagged_words,
                    AbstractAction.HISTORY: []}

            except Exception as e:

                logging.error('Error while trying to pos tag words!')

                logging.error(e)

                self.outcome = self.FAILURE

                tagged_words = content

        else:

            logging.warning('Content wasn\'t valid for pos tagging words.')

            tagged_words = content

            self.outcome = self.FAILURE

        self.record_outcome(tagged_words, content)

        return tagged_words
