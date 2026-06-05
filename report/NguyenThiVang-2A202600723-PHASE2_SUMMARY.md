# Nguyễn Thị Vang - 2A202600723
# Tóm Tắt Cá Nhân Phase 2

## Bộ Dữ Liệu

Phase 2 sử dụng bộ tài liệu đã tải về trong:

```text
data/downloaded_data/
```

Domain:

```text
Technical Documentation Retrieval for AI Developer Tools
```

Bộ dữ liệu gồm 9 file về Chroma, Docker Compose, FastAPI, LangChain text splitters, Qdrant và Sentence Transformers.

## Strategy Cá Nhân

```text
SentenceChunker(max_sentences_per_chunk=4)
```

Lý do chọn:

- Giữ nguyên ranh giới câu, tránh cắt giữa câu.
- Dễ đọc khi kiểm tra các retrieved chunks.
- Phù hợp với tutorial docs và explanatory docs có câu văn rõ ràng.

Điểm yếu:

- Với technical docs dài, nhiều code block và câu dài, chunk có thể quá lớn.
- Average chunk length trong benchmark là 2165.61 ký tự, cao hơn mức lý tưởng cho retrieval gọn.

## Metadata Schema

Mỗi chunk được gắn metadata:

- `source`
- `filename`
- `parent_doc`
- `topic`
- `doc_type`
- `title`
- `language`
- `chunk_index`

Trong benchmark, `topic` được dùng để chạy `search_with_filter()`.

## Kết Quả Benchmark

| ID | Expected | Top-1 source unfiltered | Top-1 topic | Score | Top-3 relevant? | Filtered Top-1 source |
|---|---|---|---|---:|---|---|
| Q1 | chroma | `data/downloaded_data/qdrant_points.md` | qdrant | 1 | Yes | `data/downloaded_data/chroma_usage_guide.md` |
| Q2 | fastapi | `data/downloaded_data/docker_compose_readme.md` | docker | 0 | No | `data/downloaded_data/fastapi_first_steps.md` |
| Q3 | langchain | `data/downloaded_data/chroma_usage_guide.md` | chroma | 0 | No | `data/downloaded_data/langchain_text_splitters.md` |
| Q4 | qdrant | `data/downloaded_data/qdrant_collections.md` | qdrant | 2 | Yes | `data/downloaded_data/qdrant_collections.md` |
| Q5 | docker | `data/downloaded_data/chroma_usage_guide.md` | chroma | 0 | No | `data/downloaded_data/docker_compose_readme.md` |
| Q6 | sentence_transformers | `data/downloaded_data/fastapi_first_steps.md` | fastapi | 0 | No | `data/downloaded_data/sentence_transformers_sts.md` |

## Điểm Số

| Mode | Score |
|---|---:|
| Unfiltered search | 3 / 12 |
| Metadata-filtered search | 12 / 12 |

## Reflection

Kết quả cho thấy sentence chunking dễ đọc nhưng chưa đủ nếu search trên toàn bộ corpus mà không filter. Khi dùng `_mock_embed`, kết quả unfiltered bị nhiễu vì embedding fallback không hiểu semantic thật sự. Sau khi filter theo `topic`, retrieval trả đúng source cho tất cả 6 queries.

Nếu cải thiện tiếp, nên kết hợp sentence chunking với giới hạn chunk length hoặc recursive/header-aware chunking để tránh chunk quá dài.
