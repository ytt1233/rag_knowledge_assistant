from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """
    Abstract base class for text generators.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate an answer from a prompt.
        """
        pass