from nlp_api.action.abstract_action import AbstractAction
from nlp_api.action.frequency_calculation import FrequencyCalculation
from nlp_api.action.word_extraction import WordExtraction


class TestFrequencyCalculation:

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

    def test_apply(self):
        """Tests the FrequencyCalculation apply method."""

        freqs = FrequencyCalculation().apply(WordExtraction().apply(self.TEXT))

        assert freqs is not None

        assert None not in freqs[AbstractAction.RESULT]

        assert len(freqs[AbstractAction.RESULT]) > 0

        assert len(freqs[AbstractAction.RESULT]) == 120

        assert isinstance(freqs[AbstractAction.RESULT], dict)

    def test_was_produced_by_action(self):
        """Tests the FrequencyCalculation produced method."""

        test_content = {
            AbstractAction.ACTION: FrequencyCalculation.__name__,
            AbstractAction.RESULT: None
        }

        assert FrequencyCalculation.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not FrequencyCalculation.produced(test_content)
