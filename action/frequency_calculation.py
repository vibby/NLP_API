"""Calculates a frequency for the given content."""
from collections import Counter
import logging

from action.abstract_action import AbstractAction
from action.word_extraction import WordExtraction
from action.named_entity_extraction import NamedEntityExtraction
from action.phrase_extraction import PhraseExtraction


class FrequencyCalculation(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('freq', 'Calculates frequencies')

    def validate_content(self, content):
        """Validates the provided content to ensure it was produced by
        NamedEntityExtraction, WordExtraction, or PhraseExtraction.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid.
        :rtype: bool
        """

        return (
            super().validate_content(content) and
            (
                NamedEntityExtraction.produced(content) or
                PhraseExtraction.produced(content) or
                WordExtraction.produced(content)
            )
        )

    def prepare_content(self, content):
        """Prepares the content for frequency calculation.

        :param content: The content to prepare.
        :type content: dict
        :return: The prepared content, in this case a list of strings.
        :rtype: list
        """

        prepared_content = super().prepare_content(content)

        if NamedEntityExtraction.produced(content):

            prepared_content = [
                second
                for first, second
                in prepared_content
            ]

        return prepared_content

    def apply(self, content):
        """Applies the frequency calculation action to the given content.

        :param content: The content to calculate a frequency for.
        :type content: dict
        :return: A dict containing this action's name and the frequency
                    calculation, or the provided content if this action
                    was invalid.
        :rtype: dict
        """

        logging.info('Extracting Frequencies')

        frequencies = {}

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            frequencies = dict(Counter(prepared_content).most_common())

            frequencies = {
                AbstractAction.ACTION: self.__class__.__name__,
                AbstractAction.RESULT: frequencies,
                AbstractAction.HISTORY: []}

        else:

            logging.warning(
                'Content wasn\'t valid for extracting frequencies.')

            self.content = self.FAILURE

            frequencies = content

        self.record_outcome(frequencies, content)

        return frequencies
