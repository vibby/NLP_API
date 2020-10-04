"""Removes duplicates in content."""
import logging

from action.abstract_action import AbstractAction
from action.word_extraction import WordExtraction
from action.word_pos_tagging import WordPosTagging
from action.named_entity_extraction import NamedEntityExtraction
from action.phrase_extraction import PhraseExtraction


class UniqueFiltering(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('unq', 'Filters all but the unique items.')

    def validate_content(self, content):
        """Validates the provided content to ensure it was produced by
        WordExtraction, WordPosTagging, NamedEntityExtraction,
        or PhraseExtraction.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            (
                WordPosTagging.produced(content) or
                NamedEntityExtraction.produced(content) or
                WordExtraction.produced(content) or
                PhraseExtraction.produced(content)
            )
        )

    def apply(self, content):
        """Applies the Unique Filtering action to the given content.

        :param content: The content to remove duplicates from.
        :type content: dict
        :return: A dict containing this action's name and the unique items, or
                    the provided content if this action was invalid.
        :rtype: dict
        """

        logging.info('Filtering out non-unique items.')

        unique_items = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            unique_items = list(set(prepared_content))

            unique_items = {
                AbstractAction.ACTION: self.__class__.__name__,
                AbstractAction.RESULT: unique_items,
                AbstractAction.HISTORY: []}

        else:

            logging.warning(
                'Content wasn\'t valid for filtering out non-unique items.')

            unique_items = content

            self.outcome = self.FAILURE

        self.record_outcome(unique_items, content)

        return unique_items
