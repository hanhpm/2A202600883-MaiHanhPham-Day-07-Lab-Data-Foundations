# Phạm Mai Hạnh - 2A202600883
# Day 07 Lab: Data Foundations - Phase Summary

## Thông Tin Chung

- Sinh viên: Phạm Mai Hạnh
- MSSV: 2A202600883
- Lab: Day 07 - Data Foundations: Embedding & Vector Store
- Trạng thái hiện tại: Hoàn thành Phase 1 cá nhân và Phase 2 với downloaded data

## Phase 1 - Cá Nhân: Quá Trình Hoàn Thiện Code

### Mục Tiêu Phase 1

Phase 1 yêu cầu hoàn thiện các TODO trong package `src`, tập trung vào ba nhóm chức năng:

- Chunking: chia văn bản thành các chunk phù hợp cho embedding và retrieval.
- Vector store: lưu embedding, tìm kiếm theo similarity, filter metadata và delete document.
- RAG agent: lấy context từ vector store và đưa vào prompt để gọi LLM function.

### File Đã Hoàn Thiện

| File | Nội dung đã làm |
|---|---|
| `src/chunking.py` | Implement `SentenceChunker`, `RecursiveChunker`, `compute_similarity`, `ChunkingStrategyComparator` |
| `src/store.py` | Implement record normalization, add/search/filter/delete, collection size |
| `src/agent.py` | Implement `KnowledgeBaseAgent` với luồng retrieve context -> build prompt -> call `llm_fn` |

### Chi Tiết Implementation

#### 1. `SentenceChunker`

`SentenceChunker.chunk()` tách câu bằng regex dựa trên các dấu kết thúc câu như `.`, `!`, `?`, sau đó gom tối đa `max_sentences_per_chunk` câu vào một chunk. Cách này giúp chunk không bị cắt giữa câu, dễ đọc hơn và phù hợp với các tài liệu FAQ, support note, policy ngắn.

#### 2. `RecursiveChunker`

`RecursiveChunker` ưu tiên tách văn bản theo thứ tự separator lớn đến nhỏ:

```python
["\n\n", "\n", ". ", " ", ""]
```

Nếu một đoạn văn bản vẫn dài hơn `chunk_size`, hàm `_split()` tiếp tục thử separator tiếp theo. Nếu không còn separator phù hợp, code fallback sang cắt theo fixed-size để đảm bảo vẫn tạo được chunk. Cách này giữ được ngữ cảnh tốt hơn fixed-size trong nhiều tài liệu có cấu trúc paragraph/section.

#### 3. `compute_similarity`

`compute_similarity()` tính cosine similarity theo công thức:

```text
dot(a, b) / (||a|| * ||b||)
```

Code có guard cho zero vector: nếu một trong hai vector có magnitude bằng 0 thì trả về `0.0`, tránh lỗi chia cho 0.

#### 4. `ChunkingStrategyComparator`

Comparator chạy ba strategy có sẵn:

- `fixed_size`
- `by_sentences`
- `recursive`

Kết quả trả về gồm:

- `count`: số chunk tạo ra
- `avg_length`: độ dài trung bình
- `chunks`: danh sách chunk

Phần này dùng để so sánh baseline trước khi chọn strategy cho Phase 2.

#### 5. `EmbeddingStore`

`EmbeddingStore` lưu mỗi document thành record gồm:

- `id`
- `content`
- `metadata`
- `embedding`

Khi add document, code tạo embedding bằng `embedding_fn` và đưa vào in-memory store. Search embed query, tính dot product với từng record, sắp xếp score giảm dần và trả về top-k. Metadata filter được áp dụng trước khi search, đúng với yêu cầu lab vì filter trước giúp thu hẹp search space và tăng precision. Delete document xóa tất cả record có `metadata["doc_id"]` trùng với document id cần xóa.

#### 6. `KnowledgeBaseAgent`

`KnowledgeBaseAgent.answer()` thực hiện RAG pattern:

1. Gọi `store.search(question, top_k)`.
2. Ghép các chunk tìm được thành context block có source và score.
3. Tạo prompt yêu cầu trả lời dựa trên context.
4. Gọi `llm_fn(prompt)` và trả về câu trả lời.

## Kết Quả Kiểm Thử Phase 1

Đã chạy:

```bash
pytest tests/ -v
```

Kết quả:

```text
42 passed
```

## Phase 2 - Đã Chạy Với `downloaded_data`

Phase 2 đã được chạy với data thật trong:

```text
data/downloaded_data/
```

Các file kết quả chi tiết:

```text
report/PHASE2_DOWNLOADED_DATA_REPORT.md
report/PHASE2_BENCHMARK_RESULTS.md
report/phase2_benchmark_results.json
report/NguyenThiVang-2A202600723-PHASE2_SUMMARY.md
report/PhamMaiHanh-2A202600883-PHASE2_SUMMARY.md
```

Script có thể chạy lại:

```bash
python phase2_benchmark.py
```

### Thông Tin Cá Nhân Và Strategy Đã So Sánh

| Họ tên | MSSV | Strategy |
|---|---|---|
| Nguyễn Thị Vang | 2A202600723 | `SentenceChunker(max_sentences_per_chunk=4)` |
| Phạm Mai Hạnh | 2A202600883 | `RecursiveChunker(chunk_size=700)` |

### Kết Quả Tổng Hợp

| Student | Strategy | Chunks | Avg length | Unfiltered score | Filtered score |
|---|---|---:|---:|---:|---:|
| Nguyễn Thị Vang | `SentenceChunker(max_sentences_per_chunk=4)` | 151 | 2165.61 | 3 / 12 | 12 / 12 |
| Phạm Mai Hạnh | `RecursiveChunker(chunk_size=700)` | 490 | 569.07 | 3 / 12 | 12 / 12 |

### Kết Luận Phase 2

- Cả hai strategy đều đạt 12/12 khi dùng metadata filter theo `topic`.
- Khi không filter metadata, cả hai chỉ đạt 3/12 do `_mock_embed` không phải semantic embedding thật.
- `RecursiveChunker(chunk_size=700)` của Phạm Mai Hạnh tạo chunk ngắn và ổn định hơn, phù hợp hơn với markdown/tutorial/manual docs.
- `SentenceChunker(max_sentences_per_chunk=4)` của Nguyễn Thị Vang dễ đọc theo câu, nhưng chunk trung bình quá dài với tài liệu technical lớn.
- Metadata filtering là yếu tố quan trọng nhất trong lần benchmark này.

## Kết Luận Chung

Phase 1 cá nhân đã hoàn thành phần code cốt lõi cho embedding và vector store lab. Phase 2 đã hoàn thành phần chạy data, benchmark và so sánh hai strategy cá nhân trên bộ `downloaded_data`.
