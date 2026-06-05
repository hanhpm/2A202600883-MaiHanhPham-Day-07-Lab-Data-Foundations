# Phase 2 Benchmark Results

## Dataset

| File | Topic | Type | Characters |
|---|---|---|---:|
| `chroma_introduction.md` | chroma | overview | 5112 |
| `chroma_usage_guide.md` | chroma | guide | 30529 |
| `docker_compose_readme.md` | docker | readme | 3693 |
| `fastapi_first_steps.md` | fastapi | tutorial | 13860 |
| `fastapi_tutorial_index.md` | fastapi | tutorial | 5408 |
| `langchain_text_splitters.md` | langchain | guide | 8587 |
| `qdrant_collections.md` | qdrant | manual | 86365 |
| `qdrant_points.md` | qdrant | manual | 107349 |
| `sentence_transformers_sts.md` | sentence_transformers | guide | 66755 |

## Baseline Chunking Comparison

| File | Fixed count / avg | Sentence count / avg | Recursive count / avg |
|---|---:|---:|---:|
| `chroma_usage_guide.md` | 49 / 691.61 | 32 / 951.34 | 52 / 585.17 |
| `fastapi_first_steps.md` | 22 / 696.82 | 22 / 626.23 | 22 / 622.55 |
| `langchain_text_splitters.md` | 14 / 678.36 | 6 / 1427.33 | 15 / 566.2 |
| `qdrant_collections.md` | 137 / 699.89 | 33 / 2612.48 | 129 / 548.88 |

## Query Set

| ID | Query | Gold answer | Expected topic |
|---|---|---|---|
| Q1 | What does Chroma provide for retrieval and metadata filtering? | Chroma provides retrieval infrastructure to store embeddings with metadata, search with dense/sparse vectors, filter by metadata, and retrieve across text, images, and other modalities. | chroma |
| Q2 | How do you run a FastAPI app locally and where can you open interactive API docs? | Copy the app code to main.py, run the development server with fastapi dev, open the app at http://127.0.0.1:8000, and open interactive docs at /docs. | fastapi |
| Q3 | Why is RecursiveCharacterTextSplitter a good default text splitting strategy? | It keeps larger units like paragraphs intact when possible, then falls back to smaller units such as sentences and words to manage chunk size while preserving context. | langchain |
| Q4 | In Qdrant, what is a collection and which distance metrics are supported? | A collection is a named set of points, each containing vectors and optional payload. Qdrant supports Dot, Cosine, Euclidean, and Manhattan distance metrics. | qdrant |
| Q5 | What is the quick start process for Docker Compose? | Define the app environment with a Dockerfile, define services in compose.yaml, then run docker compose up to start the application. | docker |
| Q6 | Which similarity functions are available in Sentence Transformers for semantic textual similarity? | Sentence Transformers supports cosine similarity, dot product, negative Euclidean distance, and negative Manhattan distance. | sentence_transformers |

## Nguyễn Thị Vang - 2A202600723

- Strategy: `SentenceChunker(max_sentences_per_chunk=4)`
- Rationale: Sentence-based chunks giữ câu hoàn chỉnh, giúp tutorial và API documentation dễ đọc khi kiểm tra kết quả.
- Stored chunks: 151
- Average chunk length: 2165.61
- Unfiltered score: 3 / 12
- Filtered score: 12 / 12

| ID | Expected | Top-1 source | Top-1 topic | Score | Top-3 relevant? | Filtered Top-1 source |
|---|---|---|---|---:|---|---|
| Q1 | chroma | `data/downloaded_data/qdrant_points.md` | qdrant | 1 | Yes | `data/downloaded_data/chroma_usage_guide.md` |
| Q2 | fastapi | `data/downloaded_data/docker_compose_readme.md` | docker | 0 | No | `data/downloaded_data/fastapi_first_steps.md` |
| Q3 | langchain | `data/downloaded_data/chroma_usage_guide.md` | chroma | 0 | No | `data/downloaded_data/langchain_text_splitters.md` |
| Q4 | qdrant | `data/downloaded_data/qdrant_collections.md` | qdrant | 2 | Yes | `data/downloaded_data/qdrant_collections.md` |
| Q5 | docker | `data/downloaded_data/chroma_usage_guide.md` | chroma | 0 | No | `data/downloaded_data/docker_compose_readme.md` |
| Q6 | sentence_transformers | `data/downloaded_data/fastapi_first_steps.md` | fastapi | 0 | No | `data/downloaded_data/sentence_transformers_sts.md` |

| ID | Agent answer verification | Agent answer preview |
|---|---|---|
| Q1 | Verified against filtered top-3 context | Grounded answer for: What does Chroma provide for retrieval and metadata filtering?. Evidence preview: [Context 1 / source=data/downloaded_data/chroma_usage_guide.md / score=0.2740] `embeddings` are excluded by default for performance and the `ids` are always  |
| Q2 | Verified against filtered top-3 context | Grounded answer for: How do you run a FastAPI app locally and where can you open interactive API docs?. Evidence preview: [Context 1 / source=data/downloaded_data/fastapi_first_steps.md / score=0.2143] And there are dozens of alternatives, all based on OpenAPI |
| Q3 | Verified against filtered top-3 context | Grounded answer for: Why is RecursiveCharacterTextSplitter a good default text splitting strategy?. Evidence preview: [Context 1 / source=data/downloaded_data/langchain_text_splitters.md / score=0.1012] Copy page pip uv pip install -U langchain-text-splitters  |
| Q4 | Verified against filtered top-3 context | Grounded answer for: In Qdrant, what is a collection and which distance metrics are supported?. Evidence preview: [Context 1 / source=data/downloaded_data/qdrant_collections.md / score=0.2503] And additionally, sparse vectors and dense vectors must have differ |
| Q5 | Verified against filtered top-3 context | Grounded answer for: What is the quick start process for Docker Compose?. Evidence preview: [Context 1 / source=data/downloaded_data/docker_compose_readme.md / score=0.0915] # Table of Contents - [Docker Compose](#docker-compose) - [Where to get Docker Compose |
| Q6 | Verified against filtered top-3 context | Grounded answer for: Which similarity functions are available in Sentence Transformers for semantic textual similarity?. Evidence preview: [Context 1 / source=data/downloaded_data/sentence_transformers_sts.md / score=0.0345] Built with [Sphinx](https://www.sph |

## Phạm Mai Hạnh - 2A202600883

- Strategy: `RecursiveChunker(chunk_size=700)`
- Rationale: Recursive chunks giữ paragraph và section markdown trước, sau đó mới tách nhỏ hơn khi cần.
- Stored chunks: 490
- Average chunk length: 569.07
- Unfiltered score: 3 / 12
- Filtered score: 12 / 12

| ID | Expected | Top-1 source | Top-1 topic | Score | Top-3 relevant? | Filtered Top-1 source |
|---|---|---|---|---:|---|---|
| Q1 | chroma | `data/downloaded_data/qdrant_collections.md` | qdrant | 0 | No | `data/downloaded_data/chroma_introduction.md` |
| Q2 | fastapi | `data/downloaded_data/qdrant_points.md` | qdrant | 0 | No | `data/downloaded_data/fastapi_first_steps.md` |
| Q3 | langchain | `data/downloaded_data/qdrant_points.md` | qdrant | 0 | No | `data/downloaded_data/langchain_text_splitters.md` |
| Q4 | qdrant | `data/downloaded_data/sentence_transformers_sts.md` | sentence_transformers | 1 | Yes | `data/downloaded_data/qdrant_points.md` |
| Q5 | docker | `data/downloaded_data/qdrant_collections.md` | qdrant | 0 | No | `data/downloaded_data/docker_compose_readme.md` |
| Q6 | sentence_transformers | `data/downloaded_data/sentence_transformers_sts.md` | sentence_transformers | 2 | Yes | `data/downloaded_data/sentence_transformers_sts.md` |

| ID | Agent answer verification | Agent answer preview |
|---|---|---|
| Q1 | Verified against filtered top-3 context | Grounded answer for: What does Chroma provide for retrieval and metadata filtering?. Evidence preview: [Context 1 / source=data/downloaded_data/chroma_introduction.md / score=0.2060] ### Collections * [Manage Collections](/docs/collections/manage-collections)  |
| Q2 | Verified against filtered top-3 context | Grounded answer for: How do you run a FastAPI app locally and where can you open interactive API docs?. Evidence preview: [Context 1 / source=data/downloaded_data/fastapi_first_steps.md / score=0.2628] Deploy your app to **[FastAPI Cloud](https://fastapicloud. |
| Q3 | Verified against filtered top-3 context | Grounded answer for: Why is RecursiveCharacterTextSplitter a good default text splitting strategy?. Evidence preview: [Context 1 / source=data/downloaded_data/langchain_text_splitters.md / score=0.2887] * [OpenAI](/oss/python/integrations/providers/openai) * [ |
| Q4 | Verified against filtered top-3 context | Grounded answer for: In Qdrant, what is a collection and which distance metrics are supported?. Evidence preview: [Context 1 / source=data/downloaded_data/qdrant_points.md / score=0.3127] This example removes all points with `{ "color": "red" }` from the colle |
| Q5 | Verified against filtered top-3 context | Grounded answer for: What is the quick start process for Docker Compose?. Evidence preview: [Context 1 / source=data/downloaded_data/docker_compose_readme.md / score=0.1751] > **Note**: About Docker Swarm > Docker Swarm used to rely on the legacy compose file  |
| Q6 | Verified against filtered top-3 context | Grounded answer for: Which similarity functions are available in Sentence Transformers for semantic textual similarity?. Evidence preview: [Context 1 / source=data/downloaded_data/sentence_transformers_sts.md / score=0.3005] * [Pretrained Models](../../sparse_ |

## Comparison Summary

| Student | Strategy | Chunks | Avg length | Unfiltered score | Filtered score |
|---|---|---:|---:|---:|---:|
| Nguyễn Thị Vang | `SentenceChunker(max_sentences_per_chunk=4)` | 151 | 2165.61 | 3 / 12 | 12 / 12 |
| Phạm Mai Hạnh | `RecursiveChunker(chunk_size=700)` | 490 | 569.07 | 3 / 12 | 12 / 12 |
