# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Phạm Mai Hạnh  
**MSSV:** 2A202600883  
**Nhóm:** Technical Documentation Retrieval  
**Thành viên so sánh:** Nguyễn Thị Vang - 2A202600723  
**Ngày:** 05/06/2026  

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**

High cosine similarity nghĩa là hai vector embedding có hướng gần giống nhau, tức là hai đoạn văn bản có ý nghĩa hoặc ngữ cảnh tương tự nhau. Trong retrieval, điểm cosine similarity cao thường cho thấy chunk đó có khả năng liên quan đến query.

**Ví dụ HIGH similarity:**

- Sentence A: "Chroma stores embeddings with metadata for retrieval."
- Sentence B: "A vector database can save embeddings and metadata for search."
- Tại sao tương đồng: Cả hai câu đều nói về việc lưu embeddings, metadata và phục vụ retrieval/search.

**Ví dụ LOW similarity:**

- Sentence A: "FastAPI provides interactive API documentation."
- Sentence B: "Docker Compose can run multi-container applications."
- Tại sao khác: Hai câu thuộc hai chủ đề khác nhau, một câu nói về API documentation, câu còn lại nói về container orchestration.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**

Cosine similarity tập trung vào hướng của vector thay vì độ lớn tuyệt đối, nên phù hợp hơn với embeddings đã biểu diễn ý nghĩa văn bản. Với text embeddings, hai câu có nghĩa gần nhau thường có vector cùng hướng dù độ dài hoặc magnitude có thể khác nhau.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, `chunk_size=500`, `overlap=50`. Bao nhiêu chunks?**

Công thức:

```text
num_chunks = ceil((doc_length - overlap) / (chunk_size - overlap))
```

Tính:

```text
ceil((10000 - 50) / (500 - 50))
= ceil(9950 / 450)
= ceil(22.11)
= 23 chunks
```

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**

```text
ceil((10000 - 100) / (500 - 100))
= ceil(9900 / 400)
= ceil(24.75)
= 25 chunks
```

Overlap tăng làm số chunk tăng vì bước nhảy giữa hai chunk nhỏ hơn. Overlap nhiều hơn giúp giữ ngữ cảnh giữa các chunk liền kề, nhưng đổi lại index lớn hơn và retrieval có thể có nhiều chunk trùng nội dung hơn.

---

## 2. Document Selection - Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Technical Documentation Retrieval for AI Developer Tools

Nhóm chọn domain này vì bộ dữ liệu `downloaded_data` gồm các tài liệu kỹ thuật thực tế về Chroma, Docker Compose, FastAPI, LangChain text splitters, Qdrant và Sentence Transformers. Đây là domain phù hợp với lab vì có nhiều khái niệm liên quan trực tiếp đến embedding, vector store, chunking, metadata filtering và semantic search.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|---|---|---:|---|
| 1 | `chroma_introduction.md` | `data/downloaded_data/` | 5112 | `topic=chroma`, `doc_type=overview`, `language=en` |
| 2 | `chroma_usage_guide.md` | `data/downloaded_data/` | 30529 | `topic=chroma`, `doc_type=guide`, `language=en` |
| 3 | `docker_compose_readme.md` | `data/downloaded_data/` | 3693 | `topic=docker`, `doc_type=readme`, `language=en` |
| 4 | `fastapi_first_steps.md` | `data/downloaded_data/` | 13860 | `topic=fastapi`, `doc_type=tutorial`, `language=en` |
| 5 | `fastapi_tutorial_index.md` | `data/downloaded_data/` | 5408 | `topic=fastapi`, `doc_type=tutorial`, `language=en` |
| 6 | `langchain_text_splitters.md` | `data/downloaded_data/` | 8587 | `topic=langchain`, `doc_type=guide`, `language=en` |
| 7 | `qdrant_collections.md` | `data/downloaded_data/` | 86365 | `topic=qdrant`, `doc_type=manual`, `language=en` |
| 8 | `qdrant_points.md` | `data/downloaded_data/` | 107349 | `topic=qdrant`, `doc_type=manual`, `language=en` |
| 9 | `sentence_transformers_sts.md` | `data/downloaded_data/` | 66755 | `topic=sentence_transformers`, `doc_type=guide`, `language=en` |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|---|---|---|---|
| `source` | string | `data/downloaded_data/qdrant_points.md` | Trace chunk về file gốc |
| `filename` | string | `qdrant_points.md` | Nhận diện tài liệu cụ thể |
| `parent_doc` | string | `qdrant_points` | Gom các chunk thuộc cùng document |
| `topic` | string | `qdrant` | Filter theo chủ đề benchmark |
| `doc_type` | string | `manual` | Phân biệt guide, tutorial, manual, readme |
| `language` | string | `en` | Có thể lọc theo ngôn ngữ |
| `chunk_index` | int | `12` | Trace vị trí chunk trong tài liệu |

---

## 3. Chunking Strategy - Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy baseline comparison trên các tài liệu đại diện:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|---|---|---:|---:|---|
| `chroma_usage_guide.md` | FixedSizeChunker (`fixed_size`) | 49 | 691.61 | Trung bình, có thể cắt ngang câu |
| `chroma_usage_guide.md` | SentenceChunker (`by_sentences`) | 32 | 951.34 | Tốt ở mức câu, nhưng chunk khá dài |
| `chroma_usage_guide.md` | RecursiveChunker (`recursive`) | 52 | 585.17 | Tốt, giữ paragraph/section ổn định |
| `fastapi_first_steps.md` | FixedSizeChunker (`fixed_size`) | 22 | 696.82 | Trung bình |
| `fastapi_first_steps.md` | SentenceChunker (`by_sentences`) | 22 | 626.23 | Tốt |
| `fastapi_first_steps.md` | RecursiveChunker (`recursive`) | 22 | 622.55 | Tốt |
| `langchain_text_splitters.md` | FixedSizeChunker (`fixed_size`) | 14 | 678.36 | Trung bình |
| `langchain_text_splitters.md` | SentenceChunker (`by_sentences`) | 6 | 1427.33 | Dễ đọc nhưng quá dài |
| `langchain_text_splitters.md` | RecursiveChunker (`recursive`) | 15 | 566.20 | Tốt |
| `qdrant_collections.md` | FixedSizeChunker (`fixed_size`) | 137 | 699.89 | Trung bình |
| `qdrant_collections.md` | SentenceChunker (`by_sentences`) | 33 | 2612.48 | Chunk quá dài |
| `qdrant_collections.md` | RecursiveChunker (`recursive`) | 129 | 548.88 | Tốt nhất cho tài liệu dài |

### Strategy Của Tôi

**Loại:** `RecursiveChunker(chunk_size=700)`

**Mô tả cách hoạt động:**

Strategy này ưu tiên tách văn bản theo ranh giới lớn trước như paragraph, line break và câu. Nếu một đoạn vẫn vượt quá `chunk_size`, thuật toán tiếp tục dùng separator nhỏ hơn cho đến khi chunk đủ gọn. Nếu không còn separator phù hợp, nó fallback sang cắt theo fixed-size để tránh bỏ sót nội dung.

**Tại sao tôi chọn strategy này cho domain nhóm?**

Bộ dữ liệu của nhóm là technical documentation dạng markdown/manual/tutorial, thường có heading, paragraph, code block và section dài. Recursive chunking phù hợp vì nó giữ được cấu trúc tự nhiên của tài liệu tốt hơn fixed-size, đồng thời tránh tạo chunk quá dài như sentence chunking trên các file Qdrant hoặc Sentence Transformers.

**Code snippet:**

```python
chunker = RecursiveChunker(chunk_size=700)
```

### So Sánh: Strategy Của Tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|---|---|---:|---:|---|
| `qdrant_collections.md` | SentenceChunker baseline | 33 | 2612.48 | Chunk quá dài, dễ chứa nhiều ý |
| `qdrant_collections.md` | **RecursiveChunker của tôi** | 129 | 548.88 | Chunk gọn hơn, dễ retrieve đúng section |
| `langchain_text_splitters.md` | SentenceChunker baseline | 6 | 1427.33 | Ít chunk nhưng mỗi chunk quá rộng |
| `langchain_text_splitters.md` | **RecursiveChunker của tôi** | 15 | 566.20 | Cân bằng tốt hơn giữa context và size |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/12) | Điểm mạnh | Điểm yếu |
|---|---|---:|---|---|
| Phạm Mai Hạnh | `RecursiveChunker(chunk_size=700)` | 12/12 filtered | Chunk ngắn, ổn định, hợp markdown/manual docs | Tạo nhiều chunk hơn |
| Nguyễn Thị Vang | `SentenceChunker(max_sentences_per_chunk=4)` | 12/12 filtered | Dễ đọc, giữ câu hoàn chỉnh | Chunk trung bình dài, dễ gom nhiều ý |

**Strategy nào tốt nhất cho domain này? Tại sao?**

`RecursiveChunker(chunk_size=700)` phù hợp hơn cho domain này vì tài liệu technical có cấu trúc markdown và nhiều section dài. Strategy này giữ context tốt nhưng vẫn kiểm soát chunk length, giúp kết quả retrieval dễ kiểm tra hơn.

---

## 4. My Approach - Cá nhân (10 điểm)

### Chunking Functions

**`SentenceChunker.chunk` - approach:**

Tôi dùng regex `(?<=[.!?])\s+` để tách câu sau các dấu kết thúc câu. Sau đó gom tối đa `max_sentences_per_chunk` câu vào một chunk và bỏ các phần rỗng để xử lý edge case văn bản trống hoặc nhiều khoảng trắng.

**`RecursiveChunker.chunk` / `_split` - approach:**

Thuật toán kiểm tra base case trước: nếu text rỗng thì trả về list rỗng, nếu text ngắn hơn `chunk_size` thì trả về một chunk. Nếu text dài, `_split()` thử separator theo thứ tự ưu tiên từ paragraph đến word, gom các piece vào buffer và recurse với separator nhỏ hơn nếu piece vẫn quá dài.

### EmbeddingStore

**`add_documents` + `search` - approach:**

Mỗi document được chuẩn hóa thành record gồm `id`, `content`, `metadata`, `embedding`. Khi search, query được embed bằng cùng `embedding_fn`, sau đó tính dot product với từng record, sort theo score giảm dần và trả về top-k.

**`search_with_filter` + `delete_document` - approach:**

`search_with_filter()` lọc metadata trước, sau đó mới search trong tập record đã lọc. Cách này đúng với yêu cầu retrieval vì filter trước giúp giảm nhiễu và tăng precision. `delete_document()` xóa tất cả chunk có `metadata["doc_id"]` trùng với document id cần xóa.

### KnowledgeBaseAgent

**`answer` - approach:**

Agent retrieve top-k chunks từ `EmbeddingStore`, ghép context theo dạng block có source và score, sau đó tạo prompt yêu cầu LLM trả lời dựa trên context. Cuối cùng gọi `llm_fn(prompt)` để lấy answer.

### Test Results

```text
pytest tests/ -v
42 passed
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions - Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|---|---|---|---|---:|---|
| 1 | Chroma stores embeddings with metadata. | Vector databases store vectors and metadata. | high | -0.0965 | Không |
| 2 | FastAPI creates interactive API docs. | FastAPI provides Swagger UI documentation. | high | -0.0259 | Không |
| 3 | Docker Compose runs multi-container apps. | A guitar player performs on stage. | low | 0.1510 | Không |
| 4 | Qdrant collections contain points and vectors. | Sentence Transformers computes text embeddings. | medium | -0.0853 | Không |
| 5 | Recursive splitting preserves paragraph context. | Chunking can keep sections coherent. | high | -0.1959 | Không |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**

Kết quả bất ngờ nhất là các cặp dự đoán high lại có điểm âm hoặc rất thấp. Nguyên nhân là lab đang dùng `_mock_embed`, đây là embedding fallback deterministic để phục vụ test chứ không phải semantic embedding thật. Điều này cho thấy khi đánh giá ý nghĩa văn bản, backend embedding ảnh hưởng rất lớn; nếu dùng `LocalEmbedder(all-MiniLM-L6-v2)` thì các dự đoán semantic có thể hợp lý hơn.

---

## 6. Results - Cá nhân (10 điểm)

Chạy benchmark queries trên implementation cá nhân với data trong `data/downloaded_data/`.

### Benchmark Queries & Gold Answers

| # | Query | Gold Answer |
|---|---|---|
| 1 | What does Chroma provide for retrieval and metadata filtering? | Chroma stores embeddings with metadata, supports dense/sparse search, metadata filtering and multimodal retrieval. |
| 2 | How do you run a FastAPI app locally and where can you open interactive API docs? | Copy code to `main.py`, run `fastapi dev`, open app at `http://127.0.0.1:8000`, and docs at `/docs`. |
| 3 | Why is RecursiveCharacterTextSplitter a good default text splitting strategy? | It keeps larger units like paragraphs intact, then falls back to sentences and words when needed. |
| 4 | In Qdrant, what is a collection and which distance metrics are supported? | A collection is a named set of points with vectors and payload; metrics include Dot, Cosine, Euclidean and Manhattan. |
| 5 | What is the quick start process for Docker Compose? | Define environment with Dockerfile, define services in `compose.yaml`, then run `docker compose up`. |
| 6 | Which similarity functions are available in Sentence Transformers for semantic textual similarity? | Cosine, dot product, negative Euclidean distance and negative Manhattan distance. |

### Kết Quả Của Tôi

Agent answer được tạo bằng `KnowledgeBaseAgent.answer()` với một mock grounded LLM. Mock LLM không tự bịa câu trả lời mới; nó nhận prompt có retrieved context, trích evidence preview và dùng filtered top-3 context để verify với gold answer.

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|---|---|---:|---|---|
| 1 | Chroma retrieval | Unfiltered top-1 là Qdrant; filtered top-1 là Chroma introduction | 0 | Có khi filter | Verified: context Chroma có embeddings, metadata, retrieval |
| 2 | FastAPI local docs | Unfiltered top-1 là Qdrant; filtered top-1 là FastAPI first steps | 0 | Có khi filter | Verified: context FastAPI có `fastapi dev`, `/docs` |
| 3 | Recursive splitter | Unfiltered top-1 là Qdrant; filtered top-1 là LangChain text splitters | 0 | Có khi filter | Verified: context LangChain nói recursive splitter giữ paragraph rồi tách nhỏ |
| 4 | Qdrant collection | Top-3 có Qdrant; filtered top-1 là Qdrant points | 1 | Có | Verified: context Qdrant mô tả points/collections/vectors/payload |
| 5 | Docker Compose quick start | Unfiltered top-1 là Qdrant; filtered top-1 là Docker Compose readme | 0 | Có khi filter | Verified: context Docker Compose có Dockerfile, `compose.yaml`, `docker compose up` |
| 6 | Sentence Transformers similarity | Top-1 là Sentence Transformers STS | 2 | Có | Verified: context Sentence Transformers có cosine, dot, Euclidean, Manhattan |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 6 / 6 khi dùng metadata filter theo `topic`.

### UI/UX Metrics Dashboard

Nhóm có thêm dashboard để hiển thị trực quan metrics so sánh:

```text
report_ui_phase2/index.html
```

Dashboard hiển thị dataset inventory, score unfiltered/filtered, chunk profile, actual similarity predictions, query result matrix, agent answer verification, rubric coverage và key findings.

### Optional OpenAI Embedding Run

Nhóm chạy thêm benchmark bằng OpenAI `text-embedding-3-small` để so sánh với `_mock_embed`. Vì một số chunk dài vượt giới hạn input của OpenAI embedding, script benchmark truncate phần text dùng để tạo embedding xuống tối đa 6000 ký tự, còn metadata/source vẫn giữ nguyên.

| Backend | Nguyễn Thị Vang - SentenceChunker | Phạm Mai Hạnh - RecursiveChunker | Nhận xét |
|---|---:|---:|---|
| `_mock_embed` unfiltered | 3 / 12 | 3 / 12 | Mock không hiểu nghĩa semantic nên dễ retrieve nhầm topic |
| `_mock_embed` filtered | 12 / 12 | 12 / 12 | Metadata filter giúp sửa lỗi retrieval |
| OpenAI unfiltered | 12 / 12 | 12 / 12 | Semantic embedding thật retrieve đúng topic ngay cả khi chưa filter |
| OpenAI filtered | 12 / 12 | 12 / 12 | Filter vẫn hữu ích để giới hạn search space |

File chi tiết: `report/PHASE2_BENCHMARK_RESULTS_OPENAI.md` và `report/OPENAI_EMBEDDING_COMPARISON.md`.

---

## 7. What I Learned (5 điểm - Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**

Từ strategy của Nguyễn Thị Vang, tôi thấy sentence-based chunking rất dễ đọc khi inspect kết quả, đặc biệt với tutorial docs có câu văn rõ ràng. Tuy nhiên, khi tài liệu dài và nhiều code block, cần thêm giới hạn chunk length để tránh chunk quá lớn.

**Điều hay nhất tôi học được từ nhóm khác hoặc phần demo:**

Điểm quan trọng nhất là retrieval quality không chỉ phụ thuộc vào model hay vector store. Data strategy, metadata schema và cách chunk tài liệu ảnh hưởng rất mạnh đến kết quả cuối cùng.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**

Tôi sẽ thêm metadata chi tiết hơn như `section_title`, `tool_name`, `api_area` và `difficulty`. Với các file dài như Qdrant, tôi sẽ dùng header-aware chunking để tách theo section thay vì chỉ recursive theo ký tự.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|---|---|---:|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 10 / 10 |
| Chunking strategy | Nhóm | 15 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo / UI metrics dashboard | Nhóm | 5 / 5 |
| **Tổng** | | **100 / 100** |
