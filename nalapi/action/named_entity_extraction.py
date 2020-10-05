"""Extracts named entities from the given content."""
import logging

import nltk

from action.abstract_action import AbstractAction
from action.word_pos_tagging import WordPosTagging


class NamedEntityExtraction(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('ne', 'Extracts named entities')

    def validate_content(self, content):
        """Validates the provided content to ensure it was produced by WordPosTagging.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            WordPosTagging.produced(content)
        )

    def apply(self, content):
        """Applies the named entity extraction action to the given content.

        :param content: The content to extract named entities from.
        :type content: dict
        :return: A dict containing this action's name and the named entities,
                    or the provided content if this action was invalid.
        :rtype: dict
        """

        logging.info('Extracting Named Entities')

        named_entities = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            try:

                chunks = nltk.ne_chunk(prepared_content)

                for chunk in chunks:

                    if hasattr(chunk, 'label'):

                        named_entities.append(
                            (chunk.label(),
                                ' '.join(c[0] for c in chunk)))

                named_entities = {
                    AbstractAction.ACTION: self.__class__.__name__,
                    AbstractAction.RESULT: named_entities,
                    AbstractAction.HISTORY: []}

            except Exception as e:

                logging.error(
                    'Error while trying to extract named_entities!')

                logging.error(e)

                self.outcome = self.FAILURE

                named_entities = content

        else:

            logging.warning(
                'Content wasn\'t valid for extracting named entities.')

            self.outcome = self.FAILURE

            named_entities = content

        self.record_outcome(named_entities, content)

        return named_entities
