from action.abstract_action import AbstractAction
from nalapi.action.content_reversal import ContentReversal
from nalapi.action.word_extraction import WordExtraction
from nalapi.action.word_pos_tagging import WordPosTagging
from nalapi.action.consolidation import Consolidation


class TestContentReversal:

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
        """Tests the ContentReversal apply method."""

        test_content = Consolidation().apply(
            WordPosTagging().apply(
                WordExtraction().apply(
                    self.TEXT)))

        reversed_content = ContentReversal().apply(test_content)

        assert reversed_content is not None

        assert len(reversed_content[AbstractAction.RESULT]) > 0

        assert len(reversed_content[AbstractAction.RESULT]) == 25

    def test_was_produced_by_action(self):
        """Tests the ContentReversal produced method."""

        test_content = {
            AbstractAction.ACTION: ContentReversal.__name__,
            AbstractAction.RESULT: None
        }

        assert ContentReversal.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not ContentReversal.produced(test_content)
