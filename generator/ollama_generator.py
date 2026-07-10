from ollama import Client

from generator.base_generator import BaseGenerator


class OllamaGenerator(BaseGenerator):
    """
    Generator implementation based on Ollama.
    """

    def __init__(
        self,
        model_name: str = "qwen2.5:7b",
        host: str = "http://localhost:11434",
        temperature: float = 0.2
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.client = Client(host=host)

    def generate(
        self,
        prompt: str
    ) -> str:
        """
        Generate an answer from the given prompt.
        """

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": self.temperature
            }
        )

        # Compatible with different versions of the Ollama Python SDK.
        try:
            return response.message.content
        except AttributeError:
            return response["message"]["content"]