# Báo Cáo Lab 7: Embedding & Vector Store

## Thông Tin Chung

| Mục | Nội dung |
|---|---|
| Sinh viên chính | Phạm Mai Hạnh |
| MSSV | 2A202600883 |
| Thành viên so sánh Phase 2 | Nguyễn Thị Vang - 2A202600723 |
| Lab | Day 07 - Data Foundations: Embedding & Vector Store |
| Trạng thái | Hoàn thành Phase 1 và Phase 2 |

## Phase 1 - Cá Nhân

Phase 1 yêu cầu hoàn thiện các TODO trong package `src`, gồm chunking, vector store và RAG agent.

### File Đã Hoàn Thiện

| File | Nội dung |
|---|---|
| `src/chunking.py` | Implement `SentenceChunker`, `RecursiveChunker`, `compute_similarity`, `ChunkingStrategyComparator` |
| `src/store.py` | Implement `EmbeddingStore` với add/search/filter/delete/count |
| `src/agent.py` | Implement `KnowledgeBaseAgent` theo pattern retrieve context -> build prompt -> call LLM |

### Cách Tiếp Cận

`SentenceChunker` tách văn bản theo ranh giới câu, sau đó gom nhiều câu vào một chunk. Cách này giúp chunk dễ đọc và tránh cắt giữa câu.

`RecursiveChunker` ưu tiên tách theo separator lớn như paragraph, line break, sentence boundary, rồi mới fallback về tách nhỏ hơn. Cách này phù hợp với tài liệu markdown hoặc technical docs có cấu trúc rõ.

`compute_similarity` dùng cosine similarity với guard cho zero vector để tránh lỗi chia cho 0.

`EmbeddingStore` lưu record gồm `id`, `content`, `metadata`, `embedding`; khi search sẽ embed query, tính similarity, sort theo score giảm dần và trả về top-k. `search_with_filter()` lọc metadata trước rồi mới search, đúng với yêu cầu lab.

`KnowledgeBaseAgent` lấy top-k chunks từ store, ghép thành context block, tạo prompt và gọi `llm_fn`.

### Kết Quả Kiểm Thử

Đã chạy:

```bash
pytest tests/ -v
```

Kết quả:

```text
42 passed
```

## Phase 2 - Chạy Data Và So Sánh

Phase 2 sử dụng data đã tải về trong:

```text
data/downloaded_data/
```

Domain:

```text
Technical Documentation Retrieval for AI Developer Tools
```

Bộ dữ liệu gồm 9 file về Chroma, Docker Compose, FastAPI, LangChain text splitters, Qdrant và Sentence Transformers.

## Metadata Schema

Mỗi chunk được gắn metadata:

| Field | Ý nghĩa |
|---|---|
| `source` | Đường dẫn file gốc |
| `filename` | Tên file |
| `parent_doc` | Document gốc |
| `topic` | Chủ đề chính, dùng để filter |
| `doc_type` | Loại tài liệu |
| `title` | Tên hiển thị |
| `language` | Ngôn ngữ |
| `chunk_index` | Vị trí chunk |

## Strategy Của Từng Cá Nhân

| Họ tên | MSSV | Strategy | Lý do |
|---|---|---|---|
| Nguyễn Thị Vang | 2A202600723 | `SentenceChunker(max_sentences_per_chunk=4)` | Giữ câu hoàn chỉnh, dễ đọc khi inspect kết quả |
| Phạm Mai Hạnh | 2A202600883 | `RecursiveChunker(chunk_size=700)` | Giữ paragraph/section markdown tốt hơn và kiểm soát chunk size ổn định |

## Benchmark Queries

| ID | Query | Expected topic |
|---|---|---|
| Q1 | What does Chroma provide for retrieval and metadata filtering? | chroma |
| Q2 | How do you run a FastAPI app locally and where can you open interactive API docs? | fastapi |
| Q3 | Why is RecursiveCharacterTextSplitter a good default text splitting strategy? | langchain |
| Q4 | In Qdrant, what is a collection and which distance metrics are supported? | qdrant |
| Q5 | What is the quick start process for Docker Compose? | docker |
| Q6 | Which similarity functions are available in Sentence Transformers for semantic textual similarity? | sentence_transformers |

## Kết Quả So Sánh

| Student | Strategy | Chunks | Avg length | Unfiltered score | Filtered score |
|---|---|---:|---:|---:|---:|
| Nguyễn Thị Vang | `SentenceChunker(max_sentences_per_chunk=4)` | 151 | 2165.61 | 3 / 12 | 12 / 12 |
| Phạm Mai Hạnh | `RecursiveChunker(chunk_size=700)` | 490 | 569.07 | 3 / 12 | 12 / 12 |

## Nhận Xét

Khi không dùng metadata filter, cả hai strategy đều chỉ đạt 3/12. Nguyên nhân chính là lab đang dùng `_mock_embed`, đây là embedding fallback deterministic chứ không phải semantic embedding thật. Vì vậy, unfiltered search dễ bị nhiễu giữa các tài liệu technical có nhiều từ khóa chung như `API`, `client`, `server`, `docs`, `run`.

Khi dùng metadata filter theo `topic`, cả hai strategy đều đạt 12/12. Điều này cho thấy metadata filtering có tác động rất lớn đến retrieval quality trong bộ dữ liệu này.

Về chất lượng chunk, `RecursiveChunker(chunk_size=700)` phù hợp hơn với downloaded docs vì tạo chunk ngắn hơn, ổn định hơn và giữ cấu trúc markdown tốt hơn. `SentenceChunker(max_sentences_per_chunk=4)` dễ đọc nhưng chunk trung bình quá dài với các file manual lớn như Qdrant và Sentence Transformers.

## Failure Analysis

Failure case rõ nhất là Q2 hỏi về FastAPI, nhưng unfiltered search của hai strategy đều trả về tài liệu khác ở top-1:

- Nguyễn Thị Vang: top-1 là `docker_compose_readme.md`.
- Phạm Mai Hạnh: top-1 là `qdrant_points.md`.

Nguyên nhân:

- `_mock_embed` không hiểu semantic thật sự.
- Dataset có nhiều tài liệu dài và nhiều thuật ngữ technical giống nhau.
- Tài liệu Qdrant rất dài nên tạo nhiều chunk, làm tăng xác suất xuất hiện trong top-k.

Cải thiện:

- Dùng metadata filter theo `topic`, `doc_type`, hoặc `source`.
- Dùng embedder thật như `LocalEmbedder(all-MiniLM-L6-v2)` nếu môi trường cho phép.
- Thêm reranking hoặc hybrid search kết hợp keyword + vector.
- Với docs dài, nên dùng recursive/header-aware chunking để tách theo section rõ hơn.

## Kết Luận

Phase 1 đã hoàn thành đầy đủ và pass toàn bộ test. Phase 2 đã chạy với data thật trong `downloaded_data`, có benchmark queries, metadata schema, hai strategy cá nhân và bảng so sánh kết quả.

Bài học chính là retrieval quality không chỉ phụ thuộc vào chunking. Metadata strategy và embedding backend ảnh hưởng rất mạnh đến chất lượng kết quả.
