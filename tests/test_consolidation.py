from action.abstract_action import AbstractAction
from nlp_api.action.consolidation import Consolidation


class TestConsolidation:

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
        """Tests the Consolidation apply method."""

        nes = {AbstractAction.ACTION: 'NamedEntityExtraction', AbstractAction.RESULT: [
            ('ORG', 'WHO'), ('ORG', 'DOA'), ('PERSON', 'Steve')],
            AbstractAction.HISTORY: [['word', 'success'], ['pos', 'success']]}

        consolidated_nes = Consolidation().apply(nes)

        assert consolidated_nes is not None

        assert None not in consolidated_nes[AbstractAction.RESULT]

        assert len(consolidated_nes[AbstractAction.RESULT]) > 0

        assert len(consolidated_nes[AbstractAction.RESULT]) == 2

        assert isinstance(consolidated_nes[AbstractAction.RESULT], dict)

    def test_was_produced_by_action(self):
        """Tests the Consolidation produced method."""

        test_content = {
            AbstractAction.ACTION: Consolidation.__name__,
            AbstractAction.RESULT: {'test': ['one', 'two'],
                                    AbstractAction.HISTORY: [['word', 'success'], ['pos', 'success']]}
        }

        assert Consolidation.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not Consolidation.produced(test_content)
