"""Calculates a sentiment for the given text."""
import logging

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from action.abstract_action import AbstractAction
from action.sentence_extraction import SentenceExtraction


class SentimentCalculation(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('sntmnt', 'Calculates Sentiment.')

    def validate_content(self, content):
        """Validates the provided content to ensure it's either a string or
        was produced by SentenceExtraction.

        :param content: The content to validate.
        :type content: dict
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
        """Prepares the content for sentiment calculation.

        :param content: The content to prepare.
        :type content: dict
        :return: The prepared content, in this case a string.
        :rtype: str
        """

        prepared_content = super().prepare_content(content)

        if SentenceExtraction.produced(content):

            prepared_content = ' '.join(prepared_content)

        return prepared_content

    def apply(self, content):
        """Applies the sentiment calculation action to the given content.

        :param content: The content to calculate a sentiment for.
        :type content: dict
        :return: A dict containing this action's name and a dict with the
                    scores, or the provided content if this action was
                    invalid.
        :rtype: dict
        """

        logging.info('Calculating Sentiment')

        sentiment = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            sia = SentimentIntensityAnalyzer()

            sentiment = sia.polarity_scores(prepared_content)

            sentiment = {
                AbstractAction.ACTION: self.__class__.__name__,
                AbstractAction.RESULT: sentiment,
                AbstractAction.HISTORY: []}

        else:

            logging.warning('Content wasn\'t valid for sentiment calculation.')

            sentiment = content

        self.record_outcome(sentiment, content)

        return sentiment
