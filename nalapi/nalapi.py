"""Accepts REST requests via Bottle for processing text, returns the results
as json responses.
"""
import json
import logging

from bottle import Bottle
from bottle import request
from bottle import response

from action.abstract_action import AbstractAction
from action.sentence_extraction import SentenceExtraction
from action.word_extraction import WordExtraction
from action.word_pos_tagging import WordPosTagging
from action.phrase_extraction import PhraseExtraction
from action.named_entity_extraction import NamedEntityExtraction
from action.frequency_calculation import FrequencyCalculation
from action.unique_filtering import UniqueFiltering
from action.content_reversal import ContentReversal
from action.consolidation import Consolidation
from action.sentiment_calculation import SentimentCalculation


class nalapi(Bottle):

    TEXT = 'text'
    CONTENT_TYPE = 'Content-Type'

    def __init__(self):
        """Constructor
        """

        super(nalapi, self).__init__()

        logging.debug('Starting nalapi')

        """The actions to take when a given url path section is encountered."""
        self.__actions = [
            SentenceExtraction(),
            WordExtraction(),
            WordPosTagging(),
            PhraseExtraction(),
            NamedEntityExtraction(),
            FrequencyCalculation(),
            UniqueFiltering(),
            ContentReversal(),
            Consolidation(),
            SentimentCalculation()
        ]

        self.__url_shortcuts = {
            'ne': 'word/pos/ne',
            'phrs': 'word/pos/phrs',
            'pos': 'word/pos'
        }

        self.route('/help', callback=self.help)

        """Ensures all other url paths are redirected to self.process"""
        self.route('/:url#.+#', callback=self.process)

    def help(self):
        """Provides helpful info for using nalapi.

        :return: Some info about using the api and some links to add'l info.
        :rtype: str
        """

        return f'''
====
HELP
====

******** LEGACY ********
NLP-API on readthedocs.io: https://nlp-api.readthedocs.io/en/latest/
NLP-API on github: https://github.com/William-Lake/NLP-API

The available url endpoints are:

{json.dumps({action.name:action.description for action in self.__actions},
indent=4)}

Not all endpoints are usable on their own, more info on which are/aren't along with usage examples can be found here:

https://nlp-api.readthedocs.io/en/latest/usage.html
        '''

    def process(self, url):
        """Processes an incoming REST request.

        :param url: The url used when making the request.
        :type url: str
        :return: The response.
        :rtype: str
        """

        logging.info(f'Processing url: {url}')

        url = url.lower()

        return_msg = ''

        text = self.__gather_text()

        actions = self.__gather_actions(url)

        if text and actions:

            # This might not be a great idea. The text may be VERY long.
            logging.debug(f'Processing {text} via {actions}')

            if isinstance(text, list):

                content = [
                    self.__apply_actions(item, actions)
                    for item
                    in text
                ]

            else:

                content = self.__apply_actions(text, actions)

            if response.status_code == 200:

                test_content = content[0] if isinstance(
                    content, list) else content

                if len(
                        test_content[AbstractAction.HISTORY]) != [
                        outcome for action,
                        outcome in test_content[AbstractAction.HISTORY]].count(
                        AbstractAction.SUCCESS):

                    response.status = 409

                response.headers[self.CONTENT_TYPE] = 'application/json'

                return_msg = json.dumps(content, indent=4)

            else:

                return_msg = 'Error while processing text with path.'

        else:

            response.status = 400

            return_msg = f'''
Bad Request

Possible options are:

{json.dumps({action.name:action.description for action in self.__actions},
indent=4)}

Use /help for add'l info.
            '''

        return return_msg

    def __gather_text(self):
        """Gathers the text from the request.

        :return: The request text.
        :rtype: str
        """

        logging.debug('Gathering text from the request.')

        text = ''

        try:

            if request.headers[self.CONTENT_TYPE] == 'application/json':

                text = request.json[self.TEXT]

            else:

                raise ValueError('Content-Type isn\'t application/json.')

        except KeyError as e:

            logging.error('Error while trying to gather text from request!')

            logging.error(e)

        return text

    def __gather_actions(self, url):
        """Gathers the actions corresponding to each url section.

        :param url: The url used when making the request.
        :type url: str
        :return: The actions corresponding to each url section.
        :rtype: list
        """

        logging.debug('Gathering actions')

        url_parts = url.split('/')

        # If the url starts with one of the shortcuts,
        # We need to replace it with the expanded version.
        if url_parts[0] in self.__url_shortcuts.keys():

            tmp = self.__url_shortcuts[url_parts[0]].split('/')

            tmp.extend(url_parts[1:])

            url_parts = tmp

        actions = [
            self.__gather_action_for_path(url_part)
            for url_part
            in url_parts
        ]

        actions = [action for action in actions if action is not None]

        """All url path sections must be valid."""
        if len(actions) != len(url_parts):

            actions = []

            logging.warning('Not all url path sections were valid!')

        return actions

    def __gather_action_for_path(self, path_item):
        """Gathers an action object for the given path string.

        :param path_item: The path string to find an action for. E.g. 'word'
        :type path_item: str
        :return: The action associated with the given path, or None if one isn't found.
        :rtype: AbstractAction sub-class
        """

        action = None

        for a in self.__actions:

            if path_item == a.name:

                action = a

                break

        return action

    def __apply_actions(self, text, actions):
        """Applies the given actions to the given text.

        :param text: The text to apply the actions to.
        :type text: str
        :param actions: The actions to apply to the text.
        :type actions: list
        :return: The final content produced.
        :rtype: dict
        """
        content = text

        for action in actions:

            try:

                logging.debug(f'Processing via {action.name}')

                content = action.apply(content)

                response.status = 200

            except Exception as e:

                logging.error(
                    'Error while trying to process result of type' +
                    f'{type(content)} via {action}!')

                logging.error(e)

                response.status = 500

                break

        if isinstance(content, dict):

            content['original'] = text

        return content
