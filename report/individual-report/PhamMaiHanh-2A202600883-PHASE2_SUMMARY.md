# Phạm Mai Hạnh - 2A202600883
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
RecursiveChunker(chunk_size=700)
```

Lý do chọn:

- Tài liệu downloaded chủ yếu là markdown/tutorial/manual docs có heading, paragraph và code block.
- Recursive chunking tách theo paragraph/line trước, giữ ngữ cảnh tốt hơn fixed-size.
- Khi paragraph quá dài, strategy mới fallback sang separator nhỏ hơn, giúp chunk không quá lớn.

Điểm yếu:

- Tạo nhiều chunk hơn sentence strategy, nên index lớn hơn.
- Nếu dùng `_mock_embed`, nhiều chunk hơn có thể làm unfiltered search dễ bị nhiễu hơn nếu không có metadata filter.

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
| Q1 | chroma | `data/downloaded_data/qdrant_collections.md` | qdrant | 0 | No | `data/downloaded_data/chroma_introduction.md` |
| Q2 | fastapi | `data/downloaded_data/qdrant_points.md` | qdrant | 0 | No | `data/downloaded_data/fastapi_first_steps.md` |
| Q3 | langchain | `data/downloaded_data/qdrant_points.md` | qdrant | 0 | No | `data/downloaded_data/langchain_text_splitters.md` |
| Q4 | qdrant | `data/downloaded_data/sentence_transformers_sts.md` | sentence_transformers | 1 | Yes | `data/downloaded_data/qdrant_points.md` |
| Q5 | docker | `data/downloaded_data/qdrant_collections.md` | qdrant | 0 | No | `data/downloaded_data/docker_compose_readme.md` |
| Q6 | sentence_transformers | `data/downloaded_data/sentence_transformers_sts.md` | sentence_transformers | 2 | Yes | `data/downloaded_data/sentence_transformers_sts.md` |

## Điểm Số

| Mode | Score |
|---|---:|
| Unfiltered search | 3 / 12 |
| Metadata-filtered search | 12 / 12 |

## Reflection

Recursive chunking tạo 490 chunks với average length 569.07 ký tự, gần với mức `chunk_size=700` và gọn hơn sentence strategy. Khi có metadata filter, strategy này trả đúng source cho tất cả benchmark queries.

Kết quả unfiltered thấp vì `_mock_embed` không phải semantic embedder thật. Điểm học được là retrieval quality không chỉ phụ thuộc chunking; metadata filtering và embedding backend ảnh hưởng rất mạnh đến kết quả.
