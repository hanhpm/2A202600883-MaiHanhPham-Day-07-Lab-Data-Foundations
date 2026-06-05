# OpenAI Embedding Comparison - Phase 2

**Mục đích:** chạy lại benchmark Phase 2 bằng OpenAI embeddings để so sánh với `_mock_embed`.

**Backend đã chạy:**

```text
openai:text-embedding-3-small:truncated_to_6000_chars
```

Ghi chú: một số chunk dài vượt giới hạn input của OpenAI embedding, nên benchmark chỉ truncate phần text dùng để tạo embedding xuống tối đa 6000 ký tự. Nội dung chunk, metadata và source trong kết quả vẫn giữ nguyên để trace.

---

## Kết quả tổng quan

| Backend | Nguyễn Thị Vang - SentenceChunker | Phạm Mai Hạnh - RecursiveChunker | Nhận xét |
|---|---:|---:|---|
| `_mock_embed` - unfiltered | 3 / 12 | 3 / 12 | Dễ retrieve nhầm topic vì mock không hiểu nghĩa semantic |
| `_mock_embed` - filtered by `topic` | 12 / 12 | 12 / 12 | Metadata filter sửa phần lớn lỗi retrieval |
| OpenAI - unfiltered | 12 / 12 | 12 / 12 | Embedding semantic thật retrieve đúng topic ngay cả khi chưa filter |
| OpenAI - filtered by `topic` | 12 / 12 | 12 / 12 | Filter vẫn hữu ích để giới hạn search space và ổn định context |

---

## Nhận xét chính

1. OpenAI embedding cải thiện mạnh phần **unfiltered retrieval**: từ 3/12 lên 12/12 cho cả hai strategy.
2. Metadata filtering vẫn có giá trị, nhưng với embedding thật, nó không còn là yếu tố duy nhất giúp hệ thống đúng.
3. Kết quả này xác nhận failure analysis trong report: lỗi lớn của mock benchmark không phải do chunking hay store, mà do `_mock_embed` không biểu diễn nghĩa văn bản.
4. `RecursiveChunker(chunk_size=700)` vẫn phù hợp với technical docs vì chunk ngắn hơn, dễ inspect hơn và trace source rõ hơn.
5. Nếu triển khai thật, nên dùng OpenAI hoặc local semantic embedder, còn `_mock_embed` chỉ nên dùng cho unit test và classroom fallback.

---

## File kết quả

| File | Nội dung |
|---|---|
| `report/PHASE2_BENCHMARK_RESULTS.md` | Benchmark cũ bằng `_mock_embed` |
| `report/phase2_benchmark_results.json` | JSON kết quả mock |
| `report/PHASE2_BENCHMARK_RESULTS_OPENAI.md` | Benchmark mới bằng OpenAI embeddings |
| `report/phase2_benchmark_results_openai.json` | JSON kết quả OpenAI |

---

## Câu nói ngắn khi thuyết trình

Khi dùng `_mock_embed`, unfiltered retrieval chỉ đạt 3/12 vì embedding không hiểu nghĩa thật và dễ retrieve nhầm topic. Sau khi chuyển sang OpenAI `text-embedding-3-small`, unfiltered retrieval tăng lên 12/12 cho cả hai strategy. Điều này chứng minh chất lượng embedding backend ảnh hưởng trực tiếp đến retrieval quality. Metadata filter vẫn hữu ích, nhưng với semantic embedding thật, hệ thống đã retrieve đúng hơn ngay từ bước search ban đầu.
