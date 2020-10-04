from nlp_api.action.abstract_action import AbstractAction
from nlp_api.action.word_extraction import WordExtraction


class TestWordExtraction:

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
        """Tests the WordExtraction apply method."""

        words = WordExtraction().apply(self.TEXT)

        assert words is not None

        assert None not in words[AbstractAction.RESULT]

        assert len(words[AbstractAction.RESULT]) > 0

        assert 167 == len(words[AbstractAction.RESULT])

        assert isinstance(words[AbstractAction.RESULT], list)

        assert isinstance(words[AbstractAction.RESULT][0], str)

        assert len(
            [word for word in words[AbstractAction.RESULT] if ' ' in word]) == 0

    def test_was_produced_by_action(self):
        """Tests the WordExtraction produced method."""

        test_content = {
            AbstractAction.ACTION: WordExtraction.__name__,
            AbstractAction.RESULT: ['One', 'Two']
        }

        assert WordExtraction.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not WordExtraction.produced(test_content)
