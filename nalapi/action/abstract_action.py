"""Abstract action base class."""
from abc import ABC
from abc import abstractmethod


class AbstractAction(ABC):

    SUCCESS = 'success'
    FAILURE = 'failure'
    ACTION = 'action'
    HISTORY = 'history'
    RESULT = 'result'

    def __init__(self, name, description):
        """Constructor"""

        self.name = name

        self.description = description

        self.outcome = self.SUCCESS

    @abstractmethod
    def validate_content(self, content):
        """Validates the given content, ensuring this action can process it.
        Additional validation defined by sub-class.

        :param content: The content to validate.
        :type content: dict
        :return: True if the content is valid for processing.
        :rtype: bool
        """

        return (
            content is not None and
            (
                isinstance(content, str) or
                (
                    isinstance(content, dict) and
                    self.ACTION in content.keys() and
                    self.RESULT in content.keys()
                )
            )
        )

    def prepare_content(self, content):
        """Prepares the content so it can be processed by this action.
        Additional preparation defined by sub-class.

        :param content: The content to prepare.
        :type content: dict
        :return: The prepared content.
        :rtype: *
        """

        return content[self.RESULT] if isinstance(content, dict) else content

    @abstractmethod
    def apply(self, content):
        """Applies this action to the given content.
        Action defined by sub-class.

        :param content: The content to apply this action to.
        :type content: dict
        """

        pass

    @classmethod
    def produced(cls, content):
        """Determines whether the given content was produced by this action.

        :param content: The content to review.
        :type content: dict
        :return: True if the content was produced by this action.
        :rtype: bool
        """

        return (
            isinstance(content, dict) and
            cls.ACTION in content.keys() and
            content[cls.ACTION] == cls.__name__
        )

    def record_outcome(self, new_content, old_content):
        """Records the outcome of applying this action to the old_content.

        :param new_content: The content produced by applying this action; the history to append to.
        :type new_content: dict
        :param old_content: The old content this action was applied to.
        :type old_content: dict
        """

        if isinstance(new_content, dict):

            if isinstance(old_content, dict):

                new_content[self.HISTORY] = old_content[self.HISTORY]

            new_content[self.HISTORY].append([self.name, self.outcome])

        # Reset outcome since this instance is being used
        # for future processing in nalapi.
        # FIXME I really don't like this.
        self.outcome = self.SUCCESS
