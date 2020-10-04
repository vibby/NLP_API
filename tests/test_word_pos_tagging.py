"""Tests action.WordPosTagging"""
from nlp_api.action.abstract_action import AbstractAction
from nlp_api.action.word_pos_tagging import WordPosTagging
from nlp_api.action.word_extraction import WordExtraction


class TestWordPosTagging:

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
        """Tests the WordPosTagging apply method."""

        tagged_words = WordPosTagging().apply(WordExtraction().apply(self.TEXT))

        assert tagged_words is not None

        assert None not in tagged_words[AbstractAction.RESULT]

        assert len(tagged_words[AbstractAction.RESULT]) > 0

        assert len(tagged_words[AbstractAction.RESULT]) == 167

        assert isinstance(tagged_words[AbstractAction.RESULT], list)

        assert isinstance(tagged_words[AbstractAction.RESULT][0], tuple)

        assert isinstance(tagged_words[AbstractAction.RESULT][0][0], str)

    def test_was_produced_by_action(self):
        """Tests the WordPosTagging produced action."""

        test_content = {
            AbstractAction.ACTION: WordPosTagging.__name__,
            AbstractAction.RESULT: ['One', 'Two']
        }

        assert WordPosTagging.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not WordPosTagging.produced(test_content)
