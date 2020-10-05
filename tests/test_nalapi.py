"""Unit tests for nalapi."""

import pytest
import socket
import time
import threading
import requests

from nalapi.nalapi import nalapi
from nalapi.action.abstract_action import AbstractAction


def wait_for_server_startup():
    """Continues to attempt connections to localhost:8888
    until it's successful. When successful, returns.

    This is so the future tests don't begin until the
    service endpoints are accesible.
    """

    target_socket = socket.socket()

    while True:

        try:

            target_socket.connect(('localhost', 8888))

            # Port ready to accept requests.
            break

        except BaseException:

            # Port not ready to accept requests.
            pass

    target_socket.close()


def start_server_thread():
    """Starts the thread which boots the testing server."""

    nalapi = nalapi()

    nalapi.run(host='localhost', port=8888, debug=True)


@pytest.fixture(scope='session', autouse=True)
def setUpClass():
    """Starts the bottle server for testing."""

    server_thread = threading.Thread(
        target=start_server_thread,
        daemon=True
    )

    server_thread.start()

    wait_for_server_startup()


class Testnalapi:

    BASE_URL = 'http://localhost:8888/'

    TEXT = (
        'Check back tomorrow; I will see if the book has arrived.' +
        ' A purple pig and a green donkey flew a kite in the middle of the ' +
        'night and ended up sunburnt. She always speaks to him in a loud ' +
        'voice. She works two jobs to make ends meet; at least, that was ' +
        'her reason for not having time to join us. My Mum tries to be cool ' +
        'by saying that she likes all the same things that I do. I am never ' +
        'at home on Sundays. If the Easter Bunny and the Tooth Fairy had ' +
        'babies would they take your teeth and leave chocolate for you? I ' +
        'am counting my calories, yet I really want dessert. I love eating ' +
        'toasted cheese and tuna sandwiches. Sometimes, all you need to do ' +
        ' is completely make an ass of yourself and laugh it off to realise ' +
        'that life isn’t so bad after all.')

    def test_pos(self):
        """Tests the /pos endpoint."""

        from action.word_pos_tagging import WordPosTagging

        json = self.__make_request(['pos'])

        assert WordPosTagging.produced(json)

    def test_pos_unq(self):
        """Tests the /pos/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['pos', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_pos_phrs(self):
        """Tests the /pos/phrs endpoint."""

        from action.phrase_extraction import PhraseExtraction

        json = self.__make_request(['pos', 'phrs'])

        assert PhraseExtraction.produced(json)

    def test_pos_ne(self):
        """Tests the /pos/ne endpoint."""

        from action.named_entity_extraction import NamedEntityExtraction

        json = self.__make_request(['pos', 'ne'])

        assert NamedEntityExtraction.produced(json)

    def test_pos_cnsl(self):
        """Tests the /pos/cnsl endpoint."""

        from action.consolidation import Consolidation

        json = self.__make_request(['pos', 'cnsl'])

        assert Consolidation.produced(json)

    def test_pos_phrs_unq(self):
        """Tests the /pos/phrs/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['pos', 'phrs', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_pos_phrs_freq(self):
        """Tests the /pos/phrs/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['pos', 'phrs', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_pos_ne_unq(self):
        """Tests the /pos/ne/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['pos', 'ne', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_pos_ne_freq(self):
        """Tests the /pos/ne/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['pos', 'ne', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_pos_cnsl_rev(self):
        """Tests the /pos/cnsl/rev endpoint."""

        from action.content_reversal import ContentReversal

        json = self.__make_request(['pos', 'cnsl', 'rev'])

        assert ContentReversal.produced(json)

    def test_pos_ne_cnsl_rev(self):
        """Tests the /pos/ne/cnsl/rev endpoint."""

        from action.content_reversal import ContentReversal

        json = self.__make_request(['pos', 'ne', 'cnsl', 'rev'])

        assert ContentReversal.produced(json)

    def test_ne(self):
        """Tests the /ne endpoint."""

        from action.named_entity_extraction import NamedEntityExtraction

        json = self.__make_request(['ne'])

        assert NamedEntityExtraction.produced(json)

    def test_ne_unq(self):
        """Tests the /ne/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['ne', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_ne_freq(self):
        """Tests the /ne/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['ne', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_ne_cnsl(self):
        """Tests the /ne/cnsl endpoint."""

        from action.consolidation import Consolidation

        json = self.__make_request(['ne', 'cnsl'])

        assert Consolidation.produced(json)

    def test_ne_cnsl_rev(self):
        """Tests the /ne/cnsl/rev endpoint."""

        from action.content_reversal import ContentReversal

        json = self.__make_request(['ne', 'cnsl', 'rev'])

        assert ContentReversal.produced(json)

    def test_phrs(self):
        """Tests the /phrs endpoint."""

        from action.phrase_extraction import PhraseExtraction

        json = self.__make_request(['phrs'])

        assert PhraseExtraction.produced(json)

    def test_phrs_unq(self):
        """Tests the /phrs/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['phrs', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_phrs_freq(self):
        """Tests the /phrs/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['phrs', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_snt(self):
        """Tests the /snt endpoint."""

        from action.sentence_extraction import SentenceExtraction

        json = self.__make_request(['snt'])

        assert SentenceExtraction.produced(json)

    def test_snt_sntmnt(self):
        """Tests the /snt/sntmnt endpoint."""

        from action.sentiment_calculation import SentimentCalculation

        json = self.__make_request(['snt', 'sntmnt'])

        assert SentimentCalculation.produced(json)

    def test_snt_word(self):
        """Tests the /snt/word endpoint."""

        from action.word_extraction import WordExtraction

        json = self.__make_request(['snt', 'word'])

        assert WordExtraction.produced(json)

    def test_sntmnt(self):
        """Tests the /sntmnt endpoint."""

        from action.sentiment_calculation import SentimentCalculation

        json = self.__make_request(['sntmnt'])

        assert SentimentCalculation.produced(json)

    def test_word(self):
        """Tests the /word endpoint."""

        from action.word_extraction import WordExtraction

        json = self.__make_request(['word'])

        assert WordExtraction.produced(json)

    def test_word_freq(self):
        """Tests the /word/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['word', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_word_unq(self):
        """Tests the /word/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['word', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_word_pos(self):
        """Tests the /word/pos endpoint."""

        from action.word_pos_tagging import WordPosTagging

        json = self.__make_request(['word', 'pos'])

        assert WordPosTagging.produced(json)

    def test_word_pos_unq(self):
        """Tests the /word/pos/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['word', 'pos', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_word_pos_phrs(self):
        """Tests the /word/pos/phrs endpoint."""

        from action.phrase_extraction import PhraseExtraction

        json = self.__make_request(['word', 'pos', 'phrs'])

        assert PhraseExtraction.produced(json)

    def test_word_pos_ne(self):
        """Tests the /word/pos/ne endpoint."""

        from action.named_entity_extraction import NamedEntityExtraction

        json = self.__make_request(['word', 'pos', 'ne'])

        assert NamedEntityExtraction.produced(json)

    def test_word_pos_cnsl(self):
        """Tests the /word/pos/cnsl endpoint."""

        from action.consolidation import Consolidation

        json = self.__make_request(['word', 'pos', 'cnsl'])

        assert Consolidation.produced(json)

    def test_word_pos_phrs_unq(self):
        """Tests the /word/pos/phrs/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['word', 'pos', 'phrs', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_word_pos_phrs_freq(self):
        """Tests the /word/pos/phrs/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['word', 'pos', 'phrs', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_word_pos_ne_unq(self):
        """Tests the /word/pos/ne/unq endpoint."""

        from action.unique_filtering import UniqueFiltering

        json = self.__make_request(['word', 'pos', 'ne', 'unq'])

        assert UniqueFiltering.produced(json)

    def test_word_pos_ne_freq(self):
        """Tests the /word/pos/ne/freq endpoint."""

        from action.frequency_calculation import FrequencyCalculation

        json = self.__make_request(['word', 'pos', 'ne', 'freq'])

        assert FrequencyCalculation.produced(json)

    def test_word_pos_ne_cnsl(self):
        """Tests the /word/pos/ne/cnsl endpoint."""

        from action.consolidation import Consolidation

        json = self.__make_request(['word', 'pos', 'ne', 'cnsl'])

        assert Consolidation.produced(json)

    def test_word_pos_cnsl_rev(self):
        """Tests the /word/pos/cnsl/rev endpoint."""

        from action.content_reversal import ContentReversal

        json = self.__make_request(['word', 'pos', 'cnsl', 'rev'])

        assert ContentReversal.produced(json)

    def test_word_pos_ne_cnsl_rev(self):
        """Tests the /word/pos/ne/cnsl/rev endpoint."""

        from action.content_reversal import ContentReversal

        json = self.__make_request(['word', 'pos', 'ne', 'cnsl', 'rev'])

        assert ContentReversal.produced(json)

    def test_history_success(self):
        """Tests a successful result history."""

        endpoints = ['snt', 'word', 'pos', 'cnsl', 'rev']

        history = self.__history_test(endpoints, 200)

        for action, outcome in history:

            assert outcome == AbstractAction.SUCCESS

    def test_history_failure(self):
        """Tests a failed result history."""

        endpoints = ['snt', 'word', 'cnsl', 'rev']

        history = self.__history_test(endpoints, 409)

        for action, outcome in history:

            # /snt & /word
            if action in endpoints[0:2]:

                # Test should have succeeded.
                assert outcome == AbstractAction.SUCCESS

            # /cnsl & /rev
            else:

                # Action should have failed.
                assert outcome == AbstractAction.FAILURE

    def __history_test(self, endpoints, expected_status_code):
        """Performs the overlapping tests in 
        self.test_history_failure and self.test_history_success.
        
        :param endpoints: The endpoints to use when testing the history.
        :type endpoints: list
        :param expected_status_code: The expected response status code.
        :type expected_status_code: int
        :return: The history pulled out of the response content.
        :rtype: list
        """

        url = f'http://localhost:8888/{"/".join(endpoints)}'

        response = requests.get(url,
                                json={
                                    nalapi.TEXT: self.TEXT})

        assert response.status_code == expected_status_code

        assert nalapi.CONTENT_TYPE in response.headers

        assert response.headers[nalapi.CONTENT_TYPE] == 'application/json'

        json = response.json()

        assert json is not None

        assert len(json) > 0

        assert AbstractAction.HISTORY in json.keys()

        history = json[AbstractAction.HISTORY]

        assert len(history) > 0

        assert isinstance(history, list)

        assert len(history[0]) == 2

        assert isinstance(history[0], list)

        action_names = [action for action, outcome in history]

        for endpoint in endpoints:

            assert endpoint in action_names

        return history

    def test_help(self):
        """Tests the /help endpoint."""

        # Can't use self.__make_request since this endpoint doesn't return json.
        url = self.BASE_URL + 'help'

        response = requests.get(url)

        assert response.status_code == 200

    def __make_request(self, endpoints):
        """Makes a request to the test url, using the given endpoints.
        
        :param endpoints: The endpoints to use when making the request.
        :type endpoints: list
        :return: The json produced by making the request.
        :rtype: dict
        """

        url = self.BASE_URL + '/'.join(endpoints)

        response = requests.get(url,
                                json={
                                    nalapi.TEXT: self.TEXT})

        assert response.status_code == 200

        return response.json()
