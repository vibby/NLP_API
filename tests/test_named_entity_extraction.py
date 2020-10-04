from nlp_api.action.abstract_action import AbstractAction
from nlp_api.action.named_entity_extraction import NamedEntityExtraction
from nlp_api.action.word_extraction import WordExtraction
from nlp_api.action.word_pos_tagging import WordPosTagging


class TestNamedEntityExtraction:

    TEXT = ('We\'ve had a number of Presidents, and not one of them '
            + 'was PeeWee Herman.')

    def test_apply(self):
        """Tests the NamedEntityExtraction apply method."""

        named_entities = NamedEntityExtraction().apply(
            WordPosTagging().apply(WordExtraction().apply(self.TEXT)))

        assert named_entities is not None

        assert None not in named_entities[AbstractAction.RESULT]

        assert len(named_entities[AbstractAction.RESULT]) > 0

        assert len(named_entities[AbstractAction.RESULT]) == 1

        assert isinstance(named_entities[AbstractAction.RESULT], list)

        assert isinstance(named_entities[AbstractAction.RESULT][0], tuple)

        assert isinstance(named_entities[AbstractAction.RESULT][0][0], str)

    def test_was_produced_by_action(self):
        """Tests the NamedEntityExtraction produced method."""

        test_content = {
            AbstractAction.ACTION: NamedEntityExtraction.__name__,
            AbstractAction.RESULT: None
        }

        assert NamedEntityExtraction.produced(test_content)

        test_content[AbstractAction.ACTION] = ''

        assert not NamedEntityExtraction.produced(test_content)
