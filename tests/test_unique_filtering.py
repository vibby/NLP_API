from nalapi.action.abstract_action import AbstractAction
from nalapi.action.unique_filtering import UniqueFiltering
from nalapi.action.word_extraction import WordExtraction


class TestUniqueFiltering:

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
        """Tests the UniqueFiltering apply method."""

        unique_items = UniqueFiltering().apply(WordExtraction().apply(
            self.TEXT))

        assert unique_items is not None

        assert None not in unique_items

        assert len(unique_items[AbstractAction.RESULT]) > 0

        assert len(unique_items[AbstractAction.RESULT]) == 120

        assert isinstance(unique_items[AbstractAction.RESULT], list)

    def test_was_produced_by_action(self):
        """Tests the UniqueFiltering produced action."""

        test_content = {
            AbstractAction.ACTION: UniqueFiltering.__name__,
            AbstractAction.RESULT: ['One', 'Two']
        }

        assert UniqueFiltering.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not UniqueFiltering.produced(test_content)
