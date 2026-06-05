# Phase 2 Report - Downloaded Data Benchmark

## Thành Viên

| Họ tên | MSSV | Strategy |
|---|---|---|
| Nguyễn Thị Vang | 2A202600723 | `SentenceChunker(max_sentences_per_chunk=4)` |
| Phạm Mai Hạnh | 2A202600883 | `RecursiveChunker(chunk_size=700)` |

## Domain Và Data

Domain nhóm mô phỏng:

```text
Technical Documentation Retrieval for AI Developer Tools
```

Bộ data dùng trong Phase 2 nằm tại:

```text
data/downloaded_data/
```

UI/UX dashboard hiển thị metrics so sánh:

```text
report_ui_phase2/index.html
```

| # | File | Topic | Type | Characters |
|---|---|---|---|---:|
| 1 | `chroma_introduction.md` | chroma | overview | 5112 |
| 2 | `chroma_usage_guide.md` | chroma | guide | 30529 |
| 3 | `docker_compose_readme.md` | docker | readme | 3693 |
| 4 | `fastapi_first_steps.md` | fastapi | tutorial | 13860 |
| 5 | `fastapi_tutorial_index.md` | fastapi | tutorial | 5408 |
| 6 | `langchain_text_splitters.md` | langchain | guide | 8587 |
| 7 | `qdrant_collections.md` | qdrant | manual | 86365 |
| 8 | `qdrant_points.md` | qdrant | manual | 107349 |
| 9 | `sentence_transformers_sts.md` | sentence_transformers | guide | 66755 |

## Metadata Schema

Mỗi chunk được gắn metadata:

| Field | Ví dụ | Mục đích |
|---|---|---|
| `source` | `data/downloaded_data/qdrant_points.md` | Trace chunk về file gốc |
| `filename` | `qdrant_points.md` | Nhận diện tài liệu |
| `parent_doc` | `qdrant_points` | Gom các chunk cùng document |
| `topic` | `qdrant` | Filter theo chủ đề benchmark |
| `doc_type` | `manual` | Phân loại document |
| `title` | `Qdrant points` | Tên hiển thị để đọc report |
| `language` | `en` | Lọc theo ngôn ngữ |
| `chunk_index` | `12` | Trace vị trí chunk |

## Baseline Chunking Comparison

| File | Fixed count / avg | Sentence count / avg | Recursive count / avg |
|---|---:|---:|---:|
| `chroma_usage_guide.md` | 49 / 691.61 | 32 / 951.34 | 52 / 585.17 |
| `fastapi_first_steps.md` | 22 / 696.82 | 22 / 626.23 | 22 / 622.55 |
| `langchain_text_splitters.md` | 14 / 678.36 | 6 / 1427.33 | 15 / 566.20 |
| `qdrant_collections.md` | 137 / 699.89 | 33 / 2612.48 | 129 / 548.88 |

Nhận xét:

- `SentenceChunker` tạo ít chunk hơn nhưng chunk dài hơn nhiều, đặc biệt với `qdrant_collections.md` có avg length lên 2612.48 ký tự.
- `RecursiveChunker` tạo nhiều chunk hơn, nhưng avg length ổn định hơn và gần mức `chunk_size=700`.
- Với documentation có markdown headings, code blocks và paragraph dài, recursive chunking phù hợp hơn để giữ section/context mà vẫn không làm chunk quá lớn.

## Benchmark Queries Và Gold Answers

| ID | Query | Gold answer | Expected topic |
|---|---|---|---|
| Q1 | What does Chroma provide for retrieval and metadata filtering? | Chroma provides retrieval infrastructure to store embeddings with metadata, search with dense/sparse vectors, filter by metadata, and retrieve across text, images, and other modalities. | chroma |
| Q2 | How do you run a FastAPI app locally and where can you open interactive API docs? | Copy the app code to `main.py`, run `fastapi dev`, open the app at `http://127.0.0.1:8000`, and open interactive docs at `/docs`. | fastapi |
| Q3 | Why is RecursiveCharacterTextSplitter a good default text splitting strategy? | It keeps larger units like paragraphs intact when possible, then falls back to smaller units such as sentences and words to manage chunk size while preserving context. | langchain |
| Q4 | In Qdrant, what is a collection and which distance metrics are supported? | A collection is a named set of points, each containing vectors and optional payload. Qdrant supports Dot, Cosine, Euclidean, and Manhattan distance metrics. | qdrant |
| Q5 | What is the quick start process for Docker Compose? | Define the app environment with a Dockerfile, define services in `compose.yaml`, then run `docker compose up`. | docker |
| Q6 | Which similarity functions are available in Sentence Transformers for semantic textual similarity? | Sentence Transformers supports cosine similarity, dot product, negative Euclidean distance, and negative Manhattan distance. | sentence_transformers |

## Kết Quả Nguyễn Thị Vang - 2A202600723

Strategy:

```text
SentenceChunker(max_sentences_per_chunk=4)
```

Lý do chọn:

Sentence-based chunking giữ nguyên câu hoàn chỉnh, giúp các tutorial và API docs dễ đọc khi inspect kết quả. Điểm yếu là một số file technical docs có câu dài/code block dài sẽ tạo chunk lớn, làm chunk có thể chứa nhiều ý khác nhau.

Thông số:

- Stored chunks: 151
- Average chunk length: 2165.61
- Unfiltered score: 3 / 12
- Filtered score: 12 / 12

| ID | Expected | Top-1 source unfiltered | Top-1 topic | Score | Top-3 relevant? | Filtered Top-1 source |
|---|---|---|---|---:|---|---|
| Q1 | chroma | `data/downloaded_data/qdrant_points.md` | qdrant | 1 | Yes | `data/downloaded_data/chroma_usage_guide.md` |
| Q2 | fastapi | `data/downloaded_data/docker_compose_readme.md` | docker | 0 | No | `data/downloaded_data/fastapi_first_steps.md` |
| Q3 | langchain | `data/downloaded_data/chroma_usage_guide.md` | chroma | 0 | No | `data/downloaded_data/langchain_text_splitters.md` |
| Q4 | qdrant | `data/downloaded_data/qdrant_collections.md` | qdrant | 2 | Yes | `data/downloaded_data/qdrant_collections.md` |
| Q5 | docker | `data/downloaded_data/chroma_usage_guide.md` | chroma | 0 | No | `data/downloaded_data/docker_compose_readme.md` |
| Q6 | sentence_transformers | `data/downloaded_data/fastapi_first_steps.md` | fastapi | 0 | No | `data/downloaded_data/sentence_transformers_sts.md` |

Nhận xét cá nhân:

- Không filter metadata, strategy này chỉ đạt 3/12 vì `_mock_embed` không biểu diễn semantic meaning thật sự tốt.
- Có filter theo `topic`, kết quả đạt 12/12 vì search space được thu hẹp đúng domain.
- Sentence chunking dễ đọc, nhưng chunk quá dài với Qdrant/Sentence Transformers docs nên có nguy cơ gom nhiều nội dung không liên quan trong cùng một chunk.

## Kết Quả Phạm Mai Hạnh - 2A202600883

Strategy:

```text
RecursiveChunker(chunk_size=700)
```

Lý do chọn:

Recursive chunking ưu tiên tách theo paragraph/line/ranh giới câu trước, sau đó mới tách nhỏ hơn. Strategy này hợp với downloaded docs vì các file là markdown/tutorial/manual có heading, paragraph và code block.

Thông số:

- Stored chunks: 490
- Average chunk length: 569.07
- Unfiltered score: 3 / 12
- Filtered score: 12 / 12

| ID | Expected | Top-1 source unfiltered | Top-1 topic | Score | Top-3 relevant? | Filtered Top-1 source |
|---|---|---|---|---:|---|---|
| Q1 | chroma | `data/downloaded_data/qdrant_collections.md` | qdrant | 0 | No | `data/downloaded_data/chroma_introduction.md` |
| Q2 | fastapi | `data/downloaded_data/qdrant_points.md` | qdrant | 0 | No | `data/downloaded_data/fastapi_first_steps.md` |
| Q3 | langchain | `data/downloaded_data/qdrant_points.md` | qdrant | 0 | No | `data/downloaded_data/langchain_text_splitters.md` |
| Q4 | qdrant | `data/downloaded_data/sentence_transformers_sts.md` | sentence_transformers | 1 | Yes | `data/downloaded_data/qdrant_points.md` |
| Q5 | docker | `data/downloaded_data/qdrant_collections.md` | qdrant | 0 | No | `data/downloaded_data/docker_compose_readme.md` |
| Q6 | sentence_transformers | `data/downloaded_data/sentence_transformers_sts.md` | sentence_transformers | 2 | Yes | `data/downloaded_data/sentence_transformers_sts.md` |

Nhận xét cá nhân:

- Recursive strategy tạo nhiều chunk hơn và chunk ngắn hơn, giúp context gọn hơn khi inspect top-k.
- Không filter metadata, điểm vẫn thấp do `_mock_embed` là deterministic fallback, không phải embedding semantic thực.
- Có filter theo `topic`, kết quả đạt 12/12 và top-1 đều về đúng topic/source mong đợi.

## So Sánh Hai Strategy

| Student | Strategy | Chunks | Avg length | Unfiltered score | Filtered score |
|---|---|---:|---:|---:|---:|
| Nguyễn Thị Vang | `SentenceChunker(max_sentences_per_chunk=4)` | 151 | 2165.61 | 3 / 12 | 12 / 12 |
| Phạm Mai Hạnh | `RecursiveChunker(chunk_size=700)` | 490 | 569.07 | 3 / 12 | 12 / 12 |

Kết luận so sánh:

- Nếu chỉ nhìn điểm filtered, hai strategy bằng nhau: 12/12.
- Nếu nhìn chất lượng chunk, `RecursiveChunker(chunk_size=700)` tốt hơn cho bộ downloaded docs vì chunk ngắn, ổn định và gần cấu trúc markdown hơn.
- `SentenceChunker(max_sentences_per_chunk=4)` có ưu điểm dễ đọc theo câu, nhưng với docs dài và nhiều code block, chunk trung bình quá lớn.
- Metadata filtering là yếu tố quan trọng nhất trong lần benchmark này. Khi filter theo `topic`, retrieval được thu hẹp vào đúng document family và kết quả tốt hơn rõ rệt.

## Failure Analysis

Failure case rõ nhất:

- Query Q2 hỏi về FastAPI nhưng unfiltered search của cả hai strategy đều trả về Qdrant/Docker document ở top-1.
- Nguyễn Thị Vang top-1: `docker_compose_readme.md`.
- Phạm Mai Hạnh top-1: `qdrant_points.md`.

Nguyên nhân:

- `_mock_embed` chỉ là embedding fallback deterministic, không hiểu semantic như embedding model thực.
- Dataset có nhiều tài liệu technical với nhiều từ chung như `run`, `server`, `API`, `client`, `docs`, nên unfiltered search dễ bị nhiễu.
- Các file Qdrant rất dài, tạo nhiều chunk nên có xác suất cao xuất hiện trong top-k.

Cải thiện:

- Dùng metadata filter theo `topic`, `doc_type`, hoặc `source`.
- Dùng embedder thật như `LocalEmbedder(all-MiniLM-L6-v2)` nếu môi trường cho phép.
- Thêm reranking hoặc hybrid search keyword + vector.
- Với docs dài như Qdrant, nên dùng recursive/header-aware chunking để tách theo section rõ hơn.

## Final Conclusion

Phase 2 với `downloaded_data` đã hoàn thành phần chạy data và so sánh cho Nguyễn Thị Vang - 2A202600723 và Phạm Mai Hạnh - 2A202600883.

Kết quả quan trọng nhất là metadata strategy ảnh hưởng mạnh đến retrieval quality. Trong điều kiện dùng `_mock_embed`, unfiltered vector search không ổn định; tuy nhiên khi có metadata filter theo `topic`, cả hai strategy đều retrieve đúng tài liệu cho 6/6 queries.
