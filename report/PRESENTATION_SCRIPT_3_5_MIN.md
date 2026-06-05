# Script thuyết trình 3-5 phút - Lab 7 Embedding & Vector Store

**Sinh viên:** Phạm Mai Hạnh - 2A202600883  
**Thành viên so sánh:** Nguyễn Thị Vang - 2A202600723  
**Domain:** Technical Documentation Retrieval for AI Developer Tools  
**File hỗ trợ demo:** `report_ui_phase2/index.html`

---

## 1. Mục tiêu bài làm (khoảng 30 giây)

Kính chào thầy/cô và các bạn.  
Phần trình bày của em là Lab 7 về **Embedding & Vector Store**. Mục tiêu của bài là xây dựng một pipeline retrieval đơn giản theo hướng RAG: đầu tiên chia tài liệu thành chunks, sau đó embed và lưu vào vector store, cuối cùng dùng agent để trả lời câu hỏi dựa trên context đã retrieve.

Bài làm có 2 phase.  
**Phase 1** là phần cá nhân, em hoàn thiện code trong package `src`, gồm chunking, vector store, metadata filtering, delete document, cosine similarity và KnowledgeBaseAgent.  
**Phase 2** là phần so sánh strategy trên bộ dữ liệu nhóm, dùng cùng một bộ query để đánh giá retrieval quality.

---

## 2. Phase 1 - Core implementation (khoảng 60 giây)

Ở Phase 1, em implement các thành phần chính.

Thứ nhất là **chunking** trong `src/chunking.py`.  
Em có ba cách chunk:

- `FixedSizeChunker`: chia theo số ký tự cố định và có overlap.
- `SentenceChunker`: dùng regex để tách theo ranh giới câu, sau đó gom tối đa một số câu vào mỗi chunk.
- `RecursiveChunker`: ưu tiên tách theo paragraph, xuống dòng, câu, khoảng trắng, rồi fallback về cắt ký tự nếu đoạn vẫn quá dài.

Strategy cá nhân của em trong Phase 2 là `RecursiveChunker(chunk_size=700)` vì tài liệu nhóm chủ yếu là markdown, tutorial và manual kỹ thuật. Kiểu recursive giúp giữ paragraph và section tốt hơn, đồng thời tránh chunk quá dài.

Thứ hai là **EmbeddingStore** trong `src/store.py`.  
Store hỗ trợ `add_documents`, `search`, `search_with_filter`, `get_collection_size` và `delete_document`. Khi search, hệ thống embed query, tính score với từng chunk, sort giảm dần và trả về top-k. Phần quan trọng nhất là `search_with_filter`: hệ thống lọc metadata trước, rồi mới search trên tập chunk đã lọc.

Thứ ba là **KnowledgeBaseAgent** trong `src/agent.py`.  
Agent retrieve top-k context từ store, ghép thành prompt có source và score, sau đó gọi `llm_fn`. Trong benchmark, em dùng mock grounded LLM để kiểm chứng câu trả lời có dựa trên filtered context hay không.

Kết quả kiểm thử: toàn bộ test suite pass, **42/42 tests passed**.

---

## 3. Phase 2 - Data và chiến lược so sánh (khoảng 75 giây)

Ở Phase 2, nhóm chọn domain là **Technical Documentation Retrieval for AI Developer Tools**. Bộ dữ liệu nằm trong `data/downloaded_data`, gồm 9 tài liệu:

- Chroma introduction và Chroma usage guide.
- Docker Compose readme.
- FastAPI first steps và tutorial index.
- LangChain text splitters.
- Qdrant collections và Qdrant points.
- Sentence Transformers semantic textual similarity.

Metadata được gán cho từng chunk gồm `source`, `filename`, `parent_doc`, `topic`, `doc_type`, `language` và `chunk_index`. Trong đó metadata quan trọng nhất cho benchmark là `topic`, ví dụ `chroma`, `fastapi`, `qdrant`, `docker`, `langchain`, hoặc `sentence_transformers`.

Nhóm so sánh hai strategy:

| Thành viên | Strategy | Số chunk | Avg length |
|---|---|---:|---:|
| Nguyễn Thị Vang - 2A202600723 | `SentenceChunker(max_sentences_per_chunk=4)` | 151 | 2165.61 |
| Phạm Mai Hạnh - 2A202600883 | `RecursiveChunker(chunk_size=700)` | 490 | 569.07 |

Nhận xét chính là strategy của bạn Vang dễ đọc vì giữ câu hoàn chỉnh, nhưng chunk trung bình khá dài. Strategy của em tạo nhiều chunk hơn, nhưng mỗi chunk gọn hơn và phù hợp hơn với tài liệu markdown/manual dài.

Nhóm dùng 6 benchmark queries, bao phủ các topic: Chroma, FastAPI, LangChain, Qdrant, Docker Compose và Sentence Transformers. Mỗi query có gold answer và expected topic để đánh giá top-3 retrieval.

---

## 4. Kết quả benchmark và nhận xét (khoảng 90 giây)

Kết quả quan trọng nhất là khi **không dùng metadata filter**, cả hai strategy chỉ đạt **3/12 điểm**. Lý do là hệ thống đang dùng `_mock_embed`, đây là embedding deterministic để phục vụ test, không phải semantic embedding thật. Vì vậy unfiltered search dễ retrieve nhầm topic. Ví dụ query FastAPI có thể retrieve Docker hoặc Qdrant.

Khi dùng `search_with_filter` theo `topic`, cả hai strategy đều đạt **12/12 điểm**. Điều này cho thấy metadata filtering cải thiện retrieval rất rõ. Nó giúp giảm search space từ toàn bộ tài liệu xuống đúng nhóm chủ đề, nên top-3 context ổn định hơn và agent answer cũng dễ verify hơn.

Về failure analysis, điểm yếu lớn nhất không nằm ở code chạy sai, mà nằm ở backend embedding. `_mock_embed` không hiểu nghĩa câu như embedding thật, nên phần Similarity Predictions có nhiều kết quả lệch với dự đoán semantic. Ví dụ các cặp câu dự đoán high similarity lại có actual score âm. Đây là bằng chứng cho thấy trong retrieval system, chất lượng embedding backend ảnh hưởng trực tiếp đến chất lượng kết quả.

Về so sánh strategy, cả hai đều đạt 12/12 khi có filter. Tuy nhiên em đánh giá `RecursiveChunker(chunk_size=700)` phù hợp hơn với domain này vì tài liệu kỹ thuật có nhiều heading, paragraph và code block. Recursive chunking giữ cấu trúc tự nhiên tốt hơn, chunk ngắn hơn và dễ trace nguồn hơn.

---

## 5. UI/UX dashboard và demo (khoảng 45 giây)

Để hỗ trợ phần demo, nhóm có thêm dashboard ở:

```text
report_ui_phase2/index.html
```

Dashboard này hiển thị trực quan các phần chính:

- Dataset inventory: danh sách 9 tài liệu và topic.
- Score comparison: so sánh unfiltered 3/12 với filtered 12/12.
- Chunk profile: số chunk và độ dài trung bình của từng strategy.
- Similarity predictions: actual scores từ code.
- Query result matrix: top-1 source, top-1 topic, score, top-3 relevance và filtered top-1.
- Agent answer verification: câu trả lời được tạo bằng `KnowledgeBaseAgent.answer()` trên filtered top-3 context.
- Rubric coverage: nhắc lại test pass, data đủ 5-10 docs, metadata utility và grounding quality.

Khi demo, em sẽ mở dashboard để chỉ ra trực tiếp sự khác biệt giữa search thường và search có metadata filter.

---

## 6. Kết luận và bài học (khoảng 45 giây)

Qua bài lab này, em rút ra ba điểm chính.

Thứ nhất, chunking strategy ảnh hưởng lớn đến khả năng retrieve đúng section. Với tài liệu kỹ thuật dài, recursive chunking là lựa chọn tốt vì cân bằng giữa context và độ dài chunk.

Thứ hai, metadata không chỉ là thông tin phụ. Trong benchmark này, metadata filter theo `topic` đã tăng kết quả từ **3/12 lên 12/12** cho cả hai strategy.

Thứ ba, embedding backend quyết định chất lượng semantic search. Mock embedder đủ để test code, nhưng nếu triển khai thật thì nên dùng local embedder như `all-MiniLM-L6-v2` hoặc OpenAI embedding để similarity phản ánh nghĩa văn bản tốt hơn.

Nếu làm tiếp, em sẽ cải thiện bằng cách thêm metadata chi tiết hơn như `section_title`, `tool_name`, `api_area`, và dùng header-aware chunking cho các file dài như Qdrant.

Em xin hết phần trình bày. Em cảm ơn thầy/cô và các bạn đã lắng nghe.

---

## Bản nói siêu ngắn nếu chỉ có 3 phút

Em trình bày Lab 7 về Embedding & Vector Store. Bài gồm hai phase. Phase 1 em hoàn thiện code trong `src`: ba chunker, cosine similarity, EmbeddingStore có search/filter/delete, và KnowledgeBaseAgent theo pattern RAG. Toàn bộ test pass 42/42.

Phase 2 nhóm chọn domain Technical Documentation Retrieval, gồm 9 tài liệu trong `data/downloaded_data`: Chroma, Docker Compose, FastAPI, LangChain, Qdrant và Sentence Transformers. Metadata chính là `topic`, `doc_type`, `source`, `filename`, `chunk_index`.

Nhóm so sánh hai strategy. Bạn Nguyễn Thị Vang dùng `SentenceChunker(max_sentences_per_chunk=4)`, tạo 151 chunks, avg length 2165.61. Em dùng `RecursiveChunker(chunk_size=700)`, tạo 490 chunks, avg length 569.07. Strategy của em tạo nhiều chunk hơn nhưng chunk gọn hơn, phù hợp với markdown/manual docs.

Benchmark có 6 queries. Khi không filter, cả hai strategy chỉ đạt 3/12 vì `_mock_embed` không hiểu nghĩa semantic thật, nên retrieve nhầm topic. Khi dùng metadata filter theo `topic`, cả hai đạt 12/12. Điều này chứng minh metadata filtering giúp tăng precision rất mạnh.

Agent answer được tạo bằng `KnowledgeBaseAgent.answer()` trên filtered top-3 context, nên có thể trace evidence theo source. Nhóm cũng có dashboard `report_ui_phase2/index.html` để demo score comparison, chunk profile, similarity predictions, query matrix và agent verification.

Bài học chính của em là: chunking giúp giữ context, metadata filter giúp giảm nhiễu, còn embedding backend quyết định chất lượng semantic search. Nếu cải thiện tiếp, em sẽ thêm metadata theo section và dùng embedding thật thay cho mock embedder.

---

## Gợi ý trả lời câu hỏi sau trình bày

**Hỏi: Vì sao unfiltered chỉ 3/12 nhưng filtered 12/12?**  
Vì unfiltered search chạy trên toàn bộ chunk của 9 tài liệu, trong khi `_mock_embed` không hiểu nghĩa semantic thật nên dễ retrieve nhầm topic. Filter theo `topic` giới hạn search space đúng chủ đề, nên top-3 chính xác hơn.

**Hỏi: Strategy nào tốt hơn?**  
Cả hai đạt 12/12 khi có filter, nhưng với domain technical markdown/manual, em chọn `RecursiveChunker(chunk_size=700)` vì chunk ngắn, giữ paragraph/section tốt và dễ trace source hơn.

**Hỏi: Agent answer được kiểm chứng thế nào?**  
Benchmark tạo filtered top-3 context, đưa vào `KnowledgeBaseAgent.answer()`, rồi mock grounded LLM trả lời kèm evidence preview. Nếu filtered top-3 đúng expected topic thì answer được đánh dấu verified.

**Hỏi: Điểm hạn chế lớn nhất là gì?**  
Hạn chế lớn nhất là đang dùng `_mock_embed`, không phải embedding semantic thật. Vì vậy similarity scores và unfiltered retrieval chưa phản ánh đúng nghĩa văn bản.

**Hỏi: Nếu nâng cấp hệ thống thì làm gì?**  
Em sẽ dùng real embedding backend, thêm metadata `section_title` và `api_area`, đồng thời dùng header-aware chunking cho tài liệu dài.
