# 🚀 项目简介 | Project Overview

RAG Knowledge Assistant 是系统基于 **Milvus + BGE-M3 + BGE-Reranker-v2-M3 + Qwen2.5** 构建的本地化 Retrieval-Augmented Generation（RAG）知识助手。

该项目实现了完整的RAG流程，包含：

* 治理后知识资产加载（Governed JSONL）
* 多文档知识库构建
* 批量数据导入流水线
* 向量嵌入生成
* 基于Milvus的向量存储
* 语义检索与重排序
* 基于元数据的检索过滤
* 大模型答案生成与引用溯源 

它可作为企业级知识库问答系统的基础框架。

A local Retrieval-Augmented Generation (RAG) Knowledge Assistant built with:

* Milvus
* BGE-M3
* BGE-Reranker-v2-M3
* Qwen2.5

The project implements a complete RAG pipeline including:

* Document ingestion and governance-ready asset loading
* Multi-document knowledge base construction
* Batch ingestion pipeline
* Embedding generation
* Vector storage with Milvus
* Semantic retrieval and reranking
* Metadata-aware retrieval
* Answer generation and citation tracing

It can serve as a foundation for enterprise knowledge base Q&A systems. 

---

# 🎯 应用场景 | Scenarios

本项目模拟企业知识库问答系统，可应用于：

- 企业文档问答
- 年报分析
- 制度检索
- 知识查询
- AI知识助手

This project simulates an enterprise knowledge base assistant.

Typical use cases include:

- Corporate document Q&A
- Annual report analysis
- Internal policy search
- Knowledge retrieval and summarization
- RAG-based AI assistants

---

# 🎪 项目定位 | Project Positioning

本项目是知识工程路线图中的下游项目。

上游项目：
Unstructured Data Governance

输出：
Governed Knowledge Assets
(JSONL + Metadata + Hash)

当前项目：
RAG Knowledge Assistant

本项目消费治理后的知识资产，
实现企业知识检索、重排序、
答案生成和引用溯源。

This project is the downstream component of the
Knowledge Engineering roadmap.

Upstream Project:
Unstructured Data Governance

Output:
Governed Knowledge Assets
(JSONL + Metadata + Hash)

Current Project:
RAG Knowledge Assistant

The system consumes governance-ready knowledge assets
and provides enterprise knowledge retrieval,
reranking, answer generation, and citation tracing. 

---

# 🏗️ 系统架构  | System Architecture

<img src="img/系统架构图.svg" width="800" height="600"> 

---

# ✨ 项目亮点

* 🔒 完全本地化部署（Ollama + Milvus）| Fully Local RAG Deployment (Ollama + Milvus)
* 📚 多文档知识库构建 | Multi-Document Knowledge Base
* ⚡ 批量数据导入流水线 | Batch Ingestion Pipeline
* 🗂 集合管理 | Collection Management
* 🏷 元数据过滤 | Metadata Filtering
* 🔍 BGE-M3 语义检索 | Semantic Retrieval with BGE-M3
* 🎯 BGE-Reranker-v2-M3 重排序 | Reranking with BGE-Reranker-v2-M3
* 🤖 Qwen2.5 大模型回答生成 | LLM-based Answer Generation with Qwen2.5
* 📖 Citation 引用溯源 | Citation Tracking and Source Attribution
* 🌐 FastAPI REST API 服务化 | FastAPI-based RESTful API Service  

---

# 🛠️ 技术栈 | Technology Stack

| Category           | Technology         |
| ------------------ | ------------------ |
| Language           | Python 3.11        |
| API Framework      | FastAPI            |
| LLM                | Qwen2.5            |
| Embedding Model    | BGE-M3             |
| Reranker           | BGE-Reranker-v2-M3 |
| Vector Database    | Milvus             |
| Model Runtime      | Ollama             |
| Container Runtime  | Docker             |

---

# 🔄 工作流 | RAG Workflow

```text
Governed JSONL Files
↓
Batch Ingestion Pipeline
↓
JSONL Loader
↓
Chunk Objects
↓
Embedding (BGE-M3)
↓
Milvus Collection
↓
Metadata Filtering
↓
Semantic Retrieval
↓
Reranking (BGE-Reranker-v2-M3)
↓
Qwen2.5
↓
Answer + Citation
``` 
Multiple governed documents can be ingested into a single Milvus collection,
forming a unified knowledge base while preserving document-level metadata.

---



# 💡 例子 | Example

### Question

```text
2025年归属于上市公司股东的净利润是多少？
```

### Answer

```text
2025年归属于上市公司股东的净利润为
-1,763,294,889.03元。
```

### Citation

```text
[1] 北方华锦化学工业股份有限公司2025年年度报告摘要（第2页）
```

---

# 🌐 API Service

Start service:

```bash
python main.py
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Chat API

### Request

```json
{
  "query": "2025年归属于上市公司股东的净利润是多少？"
}
```

### Response

```json
{
  "answer": "2025年归属于上市公司股东的净利润为-1,763,294,889.03元。",
  "citations": [
    {
      "title": "北方华锦化学工业股份有限公司2025年年度报告摘要",
      "page": 2
    }
  ]
}
```

---

# 🚀 快速开始 | Quick Start

## 1. Clone Repository

```bash
git clone https://github.com/ytt1233/rag_knowledge_assistant.git
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Start Milvus

```bash
docker compose up -d
```

## 4. Model Preparation

### Ollama Models

```bash
ollama serve
```
```bash
ollama pull bge-m3
ollama pull qwen2.5:7b
```

### Reranker Model

Download:

```bash
hf download BAAI/bge-reranker-v2-m3 --local-dir D:\models\bge-reranker-v2-m3
```

Or download manually from HuggingFace:

https://huggingface.co/BAAI/bge-reranker-v2-m3

Configure the local model path in:

```python
retriever/reranker.py
```
## 5. Prepare Knowledge Assets

#### Place governed JSONL files into:

data/governed_docs/

#### Example:

data/governed_docs/

├── strategy_meeting.jsonl 

├── annual_report.jsonl 

├── product_plan.jsonl  


## 6. Build Knowledge Base

#### Run batch ingestion:

python -m tests.test_batch_ingestion

#### This step will:

Load multiple governed JSONL documents 

Generate embeddings with BGE-M3 

Store vectors in Milvus 

Build a unified multi-document knowledge base 

## 7. Run Application

```bash
python main.py
```

---


# 🗺️ 路线图 | Roadmap

## v1.0.0

* [√] JSONL Document Loading
* [√] Chunk Management
* [√] Embedding Generation
* [√] Milvus Integration
* [√] Semantic Retrieval
* [√] Reranker
* [√] Qwen2.5 Integration
* [√] Citation
* [√] FastAPI Service

## v1.1.0

* [√] Multi-document Knowledge Base
* [√] Batch Ingestion Pipeline
* [√] Collection Management
* [√] Metadata Filtering

## v1.2.0

* [ ] Deduplicated Knowledge Base
* [ ] Incremental Ingestion Preparation
* [ ] Corpus Quality Monitoring

## v1.3.0

* [ ] Hybrid Search (BM25 + Vector)
* [ ] Metadata-Aware Retrieval
* [ ] Table-Aware Retrieval
* [ ] Retrieval Evaluation

## v1.4.0
* [ ] Incremental Indexing
* [ ] Knowledge Versioning
* [ ] Source Traceability
* [ ] Query Analytics


---

# 📄 License

MIT License
