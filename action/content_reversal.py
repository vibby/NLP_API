"""Reverses previously processed content."""
import logging

from action.abstract_action import AbstractAction
from action.consolidation import Consolidation


class ContentReversal(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('rev', 'Reverses the given content.')

    def validate_content(self, content):
        """Validates the provided content to ensure it was produced by Consolidation.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            Consolidation.produced(content)
        )

    def apply(self, content):
        """Applies the reversal action to the given content.

        :param content: The content to reverse.
        :type content: dict
        :return: A dict containing this action's name and the reversed content,
                    or the provided content if this action was invalid.
        :rtype: dict
        """

        logging.info('Reversing Content.')

        reversed_content = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            unique_items = set()

            for values in prepared_content.values():

                unique_items.update(set(values))

            reversed_content = {
                unique_item: list(set([
                    key
                    for key, values
                    in prepared_content.items()
                    if unique_item in values
                ]))
                for unique_item
                in unique_items
            }

            # Sorting dict based on length of values list
            tmp = {}

            for key, value in sorted(
                reversed_content.items(), key=lambda kv: len(
                    kv[1]), reverse=True):

                tmp[key] = value

            reversed_content = tmp

            reversed_content = {
                AbstractAction.ACTION: self.__class__.__name__,
                AbstractAction.RESULT: reversed_content,
                AbstractAction.HISTORY: []}

        else:

            logging.warning('Content wasn\'t valid for reversal.')

            self.outcome = self.FAILURE

            reversed_content = content

        self.record_outcome(reversed_content, content)

        return reversed_content
