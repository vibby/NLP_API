"""Consolidates previously processed content."""
import logging

from action.abstract_action import AbstractAction
from action.word_pos_tagging import WordPosTagging
from action.named_entity_extraction import NamedEntityExtraction


class Consolidation(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('cnsl',
                         'Consolidates previously processed content into a dict.')

    def validate_content(self, content):
        """Validates the provided content to ensure it was produced by
        NamedEntityExtraction or WordPosTagging.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            (
                NamedEntityExtraction.produced(content) or
                WordPosTagging.produced(content)
            )
        )

    def apply(self, content):
        """Applies the consolidation action to the given content.

        :param content: The content to consolidate.
        :type content: dict
        :return: A dict containing this action's name and the consolidated
                    content as a dict, or the provided content if this action
                    was invalid.
        :rtype: dict
        """

        logging.info('Consolidating Content.')

        consolidated_content = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            unique_items = list(set([
                first
                for first, second
                in prepared_content
            ]))

            consolidated_content = {
                unique_item: list(set([
                    second
                    for first, second
                    in prepared_content
                    if unique_item == first
                ]))
                for unique_item
                in unique_items
            }

            # Sorting dict based on length of values list
            tmp = {}

            for key, value in sorted(
                consolidated_content.items(), key=lambda kv: len(
                    kv[1]), reverse=True):

                tmp[key] = value

            consolidated_content = tmp

            consolidated_content = {
                AbstractAction.ACTION: self.__class__.__name__,
                AbstractAction.RESULT: consolidated_content,
                AbstractAction.HISTORY: []}

        else:

            logging.warning('Content wasn\'t valid for consolidation.')

            consolidated_content = content

            self.outcome = self.FAILURE

        self.record_outcome(consolidated_content, content)

        return consolidated_content
