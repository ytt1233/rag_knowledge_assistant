

# import sys
# sys.path.append(r'F:\mycode\rag_knowledge_assistant')
from ingestion.corpus_loader import CorpusLoader

loader = CorpusLoader()

snapshot = loader.load(
    "data/corpus_packages/package_20260702_143520"
)

print(snapshot)