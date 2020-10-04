"""Extracts phrases from content."""
import logging

import nltk

from action.abstract_action import AbstractAction
from action.word_pos_tagging import WordPosTagging


class PhraseExtraction(AbstractAction):

    def __init__(self):
        """Constructor"""

        super().__init__('phrs', 'Extracts phrases.')

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
        """Applies the phrase extraction action to the given content.

        :param content: The content to extract phrases from.
        :type content: dict
        :return: A dict containing this action's name and the phrases, or the
                    provided content if this action was invalid.
        :rtype: dict
        """

        logging.info('Extracting Phrases')

        phrases = []

        if self.validate_content(content):

            prepared_content = self.prepare_content(content)

            try:

                grammar = r"""
                  NP: {<DT|JJ|NN.*>+}       # Chunk sequences of DT, JJ, NN
                  PP: {<IN><NP>}            # Chunk prepositions followed by NP
                  VP: {<VB.*><NP|PP|S>+$}   # Chunk rightmost verbs and
                                            # arguments/adjuncts
                  S:  {<NP><VP>}            # Chunk NP, VP
                  """

                # https://stackoverflow.com/a/33816257
                regexp_parser = nltk.RegexpParser(grammar)

                parsed_data = regexp_parser.parse(prepared_content)

                for subtree in parsed_data.subtrees():

                    if subtree.label() in ['NP', 'PP', 'VP']:

                        phrases.append(
                            ' '.join(
                                word
                                for word, tag
                                in subtree.leaves()
                            ))

                phrases = {
                    AbstractAction.ACTION: self.__class__.__name__,
                    AbstractAction.RESULT: phrases,
                    AbstractAction.HISTORY: []}

            except Exception as e:

                logging.error(
                    'Error while trying to extract phrases from text!')

                logging.error(e)

                self.outcome = self.FAILURE

                phrases = content

        else:

            logging.warning('Content wasn\'t valid for extracting phrases.')

            self.outcome = self.FAILURE

            phrases = content

        self.record_outcome(phrases, content)

        return phrases
