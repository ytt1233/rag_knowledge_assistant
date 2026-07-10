import sys

sys.path.append(r"F:\mycode\rag_knowledge_assistant")

from generator.ollama_generator import OllamaGenerator


def test_generate():
    """
    Test Ollama text generation.
    """

    # =====================================================
    # Arrange
    # =====================================================

    generator = OllamaGenerator()

    prompt = """
You are a helpful AI assistant.

Question
--------
What is artificial intelligence?

Answer
------
"""

    # =====================================================
    # Act
    # =====================================================

    answer = generator.generate(prompt)

    # =====================================================
    # Assert
    # =====================================================

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0

    print("\nGenerated Answer")
    print("=" * 60)
    print(answer)


def main():

    print("=" * 60)
    print("Ollama Generator Test")
    print("=" * 60)

    test_generate()

    print("✓ test_generate")

    print("\nAll tests completed.")


if __name__ == "__main__":
    main()