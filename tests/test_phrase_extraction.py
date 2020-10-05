from nalapi.action.abstract_action import AbstractAction
from nalapi.action.phrase_extraction import PhraseExtraction
from nalapi.action.word_extraction import WordExtraction
from nalapi.action.word_pos_tagging import WordPosTagging


class TestPhraseExtraction:

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
        """Tests the PhraseExtraction apply method."""

        phrases = PhraseExtraction().apply(
            WordPosTagging().apply(
                WordExtraction().apply(
                    self.TEXT)))

        assert phrases is not None

        assert None not in phrases

        assert len(phrases) > 0

        assert len(phrases[AbstractAction.RESULT]) == 42

        assert isinstance(phrases[AbstractAction.RESULT], list)

        assert isinstance(phrases[AbstractAction.RESULT][0], str)

    def test_was_produced_by_action(self):
        """Tests the PhraseExtraction produced method."""

        test_content = {
            AbstractAction.ACTION: PhraseExtraction.__name__,
            AbstractAction.RESULT: ['One', 'Two']
        }

        assert PhraseExtraction.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not PhraseExtraction.produced(test_content)
