# Phạm Mai Hạnh - 2A202600883
# Day 07 Lab: Data Foundations - Summary Log

## Thông Tin Chung

- Sinh viên: Phạm Mai Hạnh
- MSSV: 2A202600883
- Lab: Day 07 - Data Foundations: Embedding & Vector Store
- Trạng thái: Hoàn thành Phase 1, Phase 2 và dashboard UI/UX metrics.

## Phase 1

Phase 1 đã hoàn thiện các TODO trong:

- `src/chunking.py`
- `src/store.py`
- `src/agent.py`

Các chức năng đã làm:

- `SentenceChunker`
- `RecursiveChunker`
- `compute_similarity`
- `ChunkingStrategyComparator`
- `EmbeddingStore.add_documents`
- `EmbeddingStore.search`
- `EmbeddingStore.search_with_filter`
- `EmbeddingStore.delete_document`
- `KnowledgeBaseAgent.answer`

Kết quả kiểm thử:

```text
pytest tests/ -v
42 passed
```

## Phase 2

Phase 2 đã chạy với data thật trong:

```text
data/downloaded_data/
```

Dashboard UI/UX hiển thị metrics so sánh:

```text
report_ui_phase2/index.html
```

Các report kết quả:

```text
report/REPORT.md
report/PHASE2_DOWNLOADED_DATA_REPORT.md
report/PHASE2_BENCHMARK_RESULTS.md
report/NguyenThiVang-2A202600723-PHASE2_SUMMARY.md
report/PhamMaiHanh-2A202600883-PHASE2_SUMMARY.md
report/phase2_benchmark_results.json
```

Script benchmark:

```bash
python phase2_benchmark.py
```

## So Sánh Strategy

| Họ tên | MSSV | Strategy | Chunks | Avg length | Unfiltered score | Filtered score |
|---|---|---|---:|---:|---:|---:|
| Nguyễn Thị Vang | 2A202600723 | `SentenceChunker(max_sentences_per_chunk=4)` | 151 | 2165.61 | 3 / 12 | 12 / 12 |
| Phạm Mai Hạnh | 2A202600883 | `RecursiveChunker(chunk_size=700)` | 490 | 569.07 | 3 / 12 | 12 / 12 |

## Kết Luận

Metadata filtering theo `topic` là yếu tố cải thiện retrieval rõ nhất trong benchmark này. Khi không filter, cả hai strategy chỉ đạt 3/12 do `_mock_embed` không phải semantic embedding thật. Khi filter theo `topic`, cả hai đạt 12/12.

Về chunking, `RecursiveChunker(chunk_size=700)` phù hợp hơn với bộ downloaded docs vì chunk ngắn, ổn định và gần cấu trúc markdown/manual docs hơn. `SentenceChunker(max_sentences_per_chunk=4)` dễ đọc theo câu nhưng chunk trung bình quá dài với các tài liệu technical lớn.
