# Mai Hanh Pham - 2A202600883
# Day 07 Lab: Data Foundations - Phase Summary

## Thong tin chung

- Sinh vien: Mai Hanh Pham
- MSSV: 2A202600883
- Lab: Day 07 - Data Foundations: Embedding & Vector Store
- Trang thai hien tai: Hoan thanh code Phase 1 ca nhan

## Phase 1 - Ca nhan: Qua trinh hoan thien code

### Muc tieu Phase 1

Phase 1 yeu cau hoan thien cac TODO trong package `src`, tap trung vao ba nhom chuc nang:

- Chunking: chia van ban thanh cac chunk phu hop cho embedding va retrieval.
- Vector store: luu embedding, tim kiem theo similarity, filter metadata va delete document.
- RAG agent: lay context tu vector store va dua vao prompt de goi LLM function.

### File da hoan thien

| File | Noi dung da lam |
|---|---|
| `src/chunking.py` | Implement `SentenceChunker`, `RecursiveChunker`, `compute_similarity`, `ChunkingStrategyComparator` |
| `src/store.py` | Implement record normalization, add/search/filter/delete, collection size |
| `src/agent.py` | Implement `KnowledgeBaseAgent` voi luong retrieve context -> build prompt -> call `llm_fn` |

### Chi tiet implementation

#### 1. `SentenceChunker`

`SentenceChunker.chunk()` tach cau bang regex dua tren cac dau ket thuc cau nhu `.`, `!`, `?`, sau do gom toi da `max_sentences_per_chunk` cau vao mot chunk. Cach nay giup chunk khong bi cat giua cau, de doc hon va phu hop voi cac tai lieu FAQ, support note, policy ngan.

#### 2. `RecursiveChunker`

`RecursiveChunker` uu tien tach van ban theo thu tu separator lon den nho:

```python
["\n\n", "\n", ". ", " ", ""]
```

Neu mot doan van ban van dai hon `chunk_size`, ham `_split()` tiep tuc thu separator tiep theo. Neu khong con separator phu hop, code fallback sang cat theo fixed-size de dam bao van tao duoc chunk. Cach nay giu duoc ngu canh tot hon fixed-size trong nhieu tai lieu co cau truc paragraph/section.

#### 3. `compute_similarity`

`compute_similarity()` tinh cosine similarity theo cong thuc:

```text
dot(a, b) / (||a|| * ||b||)
```

Code co guard cho zero vector: neu mot trong hai vector co magnitude bang 0 thi tra ve `0.0`, tranh loi chia cho 0.

#### 4. `ChunkingStrategyComparator`

Comparator chay ba strategy co san:

- `fixed_size`
- `by_sentences`
- `recursive`

Ket qua tra ve gom:

- `count`: so chunk tao ra
- `avg_length`: do dai trung binh
- `chunks`: danh sach chunk

Phan nay dung de so sanh baseline truoc khi chon strategy cho Phase 2.

#### 5. `EmbeddingStore`

`EmbeddingStore` luu moi document thanh record gom:

- `id`
- `content`
- `metadata`
- `embedding`

Khi add document, code tao embedding bang `embedding_fn` va dua vao in-memory store. Search embed query, tinh dot product voi tung record, sap xep score giam dan va tra ve top-k. Metadata filter duoc ap dung truoc khi search, dung voi yeu cau lab vi filter truoc giup thu hep search space va tang precision. Delete document xoa tat ca record co `metadata["doc_id"]` trung voi document id can xoa.

#### 6. `KnowledgeBaseAgent`

`KnowledgeBaseAgent.answer()` thuc hien RAG pattern:

1. Goi `store.search(question, top_k)`.
2. Ghep cac chunk tim duoc thanh context block co source va score.
3. Tao prompt yeu cau tra loi dua tren context.
4. Goi `llm_fn(prompt)` va tra ve cau tra loi.

## Ket qua kiem thu Phase 1

Da chay lenh:

```bash
pytest tests/ -v
```

Ket qua:

```text
42 passed in 0.28s
```

Tat ca test trong `tests/test_solution.py` da pass, bao gom:

- Project structure
- Chunker interfaces
- Fixed-size chunking
- Sentence chunking
- Recursive chunking
- Embedding store add/search/sort/filter/delete
- Knowledge base agent
- Cosine similarity
- Strategy comparator

## Ghi chu ve du lieu mau da doc

Thu muc `data/` co cac tai lieu mau dung cho manual demo va Phase 2:

| File | Noi dung chinh |
|---|---|
| `python_intro.txt` | Gioi thieu Python, ung dung trong backend, data, AI va best practices |
| `vector_store_notes.md` | Workflow vector store, metadata va rui ro retrieval |
| `rag_system_design.md` | Thiet ke RAG system cho internal knowledge assistant |
| `customer_support_playbook.txt` | Huong dan support assistant, escalation va metadata access control |
| `chunking_experiment_report.md` | So sanh fixed-size, sentence-based va recursive chunking |
| `vi_retrieval_notes.md` | Ghi chu tieng Viet ve retrieval, chunking, metadata va failure cases |

## Phase 2 - Nhom: Khung report de cap nhat sau

Vi khong lam theo nhom, co the lam Phase 2 theo huong solo: dung bo data mau co san trong thu muc `data/`, tu dong vai "mot nhom mot nguoi", chon strategy ca nhan, tao benchmark queries va tu danh gia retrieval.

### Muc tieu Phase 2 solo

Phase 2 khong chi kiem tra code co chay hay khong. Muc tieu chinh la chung minh minh hieu retrieval strategy:

- Tai lieu nao duoc dua vao knowledge base?
- Metadata nao giup filter ket qua?
- Chunking strategy nao phu hop voi bo tai lieu?
- 5 benchmark queries co gold answer ro rang khong?
- Top-3 chunks tra ve co lien quan den query khong?
- Agent answer co dua tren retrieved context khong?

## Phase 2 Solo - Huong dan chi tiet de thuc hien

### Buoc 1 - Chon domain solo

Dung domain:

```text
Internal AI Knowledge Assistant Documentation
```

Ly do chon domain nay:

- Cac file data mau deu noi ve Python, vector store, RAG, retrieval, chunking va customer support.
- Domain nay phu hop voi lab vi cau hoi retrieval co the hoi ve pipeline, metadata, chunking, support escalation va RAG grounding.
- Data co ca tieng Anh va tieng Viet, giup kiem tra retrieval tren noi dung da ngon ngu.

### Buoc 2 - Chon bo tai lieu trong `data/`

Dung 6 file co san sau:

| # | File | Vai tro trong knowledge base | Noi dung chinh |
|---|---|---|---|
| 1 | `data/python_intro.txt` | Technical background | Python, backend, data, AI, testability |
| 2 | `data/vector_store_notes.md` | Vector store concept | Chunk, embed, store, metadata, risks |
| 3 | `data/rag_system_design.md` | RAG architecture | Ingestion, retrieval, prompt grounding, evaluation |
| 4 | `data/customer_support_playbook.txt` | Support operations | Support assistant, escalation, safe answers |
| 5 | `data/chunking_experiment_report.md` | Chunking comparison | Fixed-size vs sentence vs recursive chunking |
| 6 | `data/vi_retrieval_notes.md` | Vietnamese retrieval notes | Retrieval, chunk quality, metadata, failure cases |

### Buoc 3 - Metadata schema nen dung

Moi document nen co metadata toi thieu:

| Truong | Kieu | Vi du | Tac dung |
|---|---|---|---|
| `doc_id` | string | `python_intro` | Dung de trace va delete document |
| `source` | string | `data/python_intro.txt` | Biet chunk den tu file nao |
| `doc_type` | string | `technical_note`, `support_playbook`, `experiment_report` | Filter theo loai tai lieu |
| `language` | string | `en`, `vi` | Filter noi dung tieng Anh/tieng Viet |
| `topic` | string | `python`, `vector_store`, `rag`, `support`, `chunking`, `retrieval` | Filter theo chu de |

Metadata goi y cho tung file:

| File | `doc_type` | `language` | `topic` |
|---|---|---|---|
| `python_intro.txt` | `technical_note` | `en` | `python` |
| `vector_store_notes.md` | `technical_note` | `en` | `vector_store` |
| `rag_system_design.md` | `design_doc` | `en` | `rag` |
| `customer_support_playbook.txt` | `support_playbook` | `en` | `support` |
| `chunking_experiment_report.md` | `experiment_report` | `en` | `chunking` |
| `vi_retrieval_notes.md` | `technical_note` | `vi` | `retrieval` |

### Buoc 4 - Chon strategy ca nhan

Strategy de xuat cho Mai Hanh Pham:

```text
RecursiveChunker(chunk_size=500)
```

Ly do:

- Bo data co cau truc paragraph va markdown heading, nen recursive chunking giu ngu canh tot hon fixed-size.
- Strategy nay thu tach theo paragraph truoc, neu doan qua dai moi tach theo cau/tu.
- Phu hop voi tai lieu RAG va vector store vi moi paragraph thuong trinh bay mot y hoan chinh.
- Trong file `chunking_experiment_report.md`, recursive chunking cung duoc mo ta la strategy co balance tot.

Baseline can so sanh:

- `FixedSizeChunker(chunk_size=500, overlap=50)`
- `SentenceChunker(max_sentences_per_chunk=3)`
- `RecursiveChunker(chunk_size=500)`

### Buoc 5 - 5 benchmark queries va gold answers

Dung 5 queries sau de lam benchmark solo:

| # | Query | Gold answer | Tai lieu nen retrieve |
|---|---|---|---|
| 1 | What are the four stages of a typical vector search pipeline? | Chunk documents, embed each chunk, store vectors with metadata, embed query and rank by similarity. | `vector_store_notes.md` |
| 2 | Why is recursive chunking a strong default for mixed technical documentation? | It splits first by larger structures like paragraphs, then falls back to smaller separators, preserving context while keeping chunks within target size. | `chunking_experiment_report.md` |
| 3 | How should a RAG assistant behave when retrieval results are weak or contradictory? | It should say that context is weak or incomplete instead of pretending the answer is complete. | `rag_system_design.md` |
| 4 | Why should support content avoid vague instructions such as "check the settings"? | Specific instructions with exact pages, buttons, or logs make chunks easier to retrieve and safer for support agents. | `customer_support_playbook.txt` |
| 5 | Metadata co the giup retrieval tieng Viet nhu the nao? | Metadata co the loc theo phong ban, ngon ngu, do nhay cam hoac ngay cap nhat de tranh lay nham tai lieu khong lien quan. | `vi_retrieval_notes.md` |

Trong 5 queries nay, query #5 nen chay them voi metadata filter:

```python
metadata_filter={"language": "vi"}
```

### Buoc 6 - Code mau de chay Phase 2 solo

Tao file tam hoac chay trong Python shell tu thu muc lab:

```python
from pathlib import Path

from src import (
    Document,
    EmbeddingStore,
    KnowledgeBaseAgent,
    RecursiveChunker,
    ChunkingStrategyComparator,
    _mock_embed,
)

DATASET = [
    ("data/python_intro.txt", {"doc_type": "technical_note", "language": "en", "topic": "python"}),
    ("data/vector_store_notes.md", {"doc_type": "technical_note", "language": "en", "topic": "vector_store"}),
    ("data/rag_system_design.md", {"doc_type": "design_doc", "language": "en", "topic": "rag"}),
    ("data/customer_support_playbook.txt", {"doc_type": "support_playbook", "language": "en", "topic": "support"}),
    ("data/chunking_experiment_report.md", {"doc_type": "experiment_report", "language": "en", "topic": "chunking"}),
    ("data/vi_retrieval_notes.md", {"doc_type": "technical_note", "language": "vi", "topic": "retrieval"}),
]

chunker = RecursiveChunker(chunk_size=500)
docs = []

for file_path, metadata in DATASET:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    for index, chunk in enumerate(chunker.chunk(text)):
        docs.append(
            Document(
                id=f"{path.stem}_chunk_{index}",
                content=chunk,
                metadata={
                    **metadata,
                    "source": file_path,
                    "parent_doc": path.stem,
                    "chunk_index": index,
                },
            )
        )

store = EmbeddingStore(collection_name="phase2_solo", embedding_fn=_mock_embed)
store.add_documents(docs)

print("Stored chunks:", store.get_collection_size())

queries = [
    "What are the four stages of a typical vector search pipeline?",
    "Why is recursive chunking a strong default for mixed technical documentation?",
    "How should a RAG assistant behave when retrieval results are weak or contradictory?",
    'Why should support content avoid vague instructions such as "check the settings"?',
    "Metadata co the giup retrieval tieng Viet nhu the nao?",
]

for q in queries:
    print("\nQUERY:", q)
    results = store.search(q, top_k=3)
    for rank, result in enumerate(results, start=1):
        print(rank, round(result["score"], 4), result["metadata"].get("source"))
        print(result["content"][:180].replace("\n", " "), "...")

print("\nFILTERED VI QUERY")
filtered = store.search_with_filter(
    "Metadata co the giup retrieval tieng Viet nhu the nao?",
    top_k=3,
    metadata_filter={"language": "vi"},
)
for rank, result in enumerate(filtered, start=1):
    print(rank, round(result["score"], 4), result["metadata"].get("source"))
```

### Buoc 7 - Code mau de so sanh chunking baseline

Chay comparator tren 2-3 tai lieu:

```python
from pathlib import Path
from src import ChunkingStrategyComparator

files = [
    "data/vector_store_notes.md",
    "data/rag_system_design.md",
    "data/chunking_experiment_report.md",
]

for file_path in files:
    text = Path(file_path).read_text(encoding="utf-8")
    result = ChunkingStrategyComparator().compare(text, chunk_size=500)
    print("\nFILE:", file_path)
    for strategy, stats in result.items():
        print(strategy, "count=", stats["count"], "avg_length=", round(stats["avg_length"], 2))
```

### Buoc 8 - Bang ket qua can dien vao report

Sau khi chay benchmark, dien bang nay:

| # | Query | Expected source | Top-1 source | Top-1 score | Top-3 co relevant chunk? | Nhan xet |
|---|---|---|---|---|---|---|
| 1 | Vector search pipeline | `vector_store_notes.md` | TBD | TBD | Yes/No | TBD |
| 2 | Recursive chunking default | `chunking_experiment_report.md` | TBD | TBD | Yes/No | TBD |
| 3 | Weak RAG retrieval | `rag_system_design.md` | TBD | TBD | Yes/No | TBD |
| 4 | Support vague instructions | `customer_support_playbook.txt` | TBD | TBD | Yes/No | TBD |
| 5 | Vietnamese metadata retrieval | `vi_retrieval_notes.md` | TBD | TBD | Yes/No | TBD |

### Buoc 9 - Cach danh gia ket qua

Danh gia tung query theo rubric:

- 2 diem: Top-3 co chunk dung va cau tra loi agent dung voi gold answer.
- 1 diem: Top-3 co chunk gan dung nhung thieu chi tiet, hoac chunk dung khong nam top-1.
- 0 diem: Khong retrieve duoc chunk lien quan trong top-3.

Voi solo report, nen ghi them:

- Query nao retrieve tot nhat?
- Query nao retrieve yeu nhat?
- Metadata filter co cai thien query tieng Viet khong?
- Recursive chunking co giu context tot hon fixed-size khong?
- Neu lam lai, co can them metadata nao khong?

### Buoc 10 - Cau truc phan viet trong report

Co the viet Phase 2 theo format sau:

```text
Toi thuc hien Phase 2 theo hinh thuc solo voi domain Internal AI Knowledge Assistant Documentation.
Bo du lieu gom 6 file mau trong thu muc data, bao phu cac chu de Python, vector store, RAG,
support playbook, chunking experiment va retrieval tieng Viet.

Strategy ca nhan cua toi la RecursiveChunker(chunk_size=500). Toi chon strategy nay vi bo tai
lieu co nhieu paragraph va heading markdown; recursive chunking giup uu tien giu nguyen ngu canh
truoc khi tach nho hon.

Toi thiet ke metadata gom source, doc_type, language, topic, parent_doc va chunk_index.
Metadata language duoc dung de test query tieng Viet voi search_with_filter(language='vi').

Sau khi chay 5 benchmark queries, toi danh gia ket qua dua tren viec top-3 co chua chunk lien
quan hay khong, score co hop ly khong va agent answer co bam vao retrieved context khong.
```

### Viec can lam cho Phase 2

- [x] Chon domain solo: Internal AI Knowledge Assistant Documentation.
- [x] Chon 6 tai lieu `.txt`/`.md` trong `data/`.
- [x] Thiet ke metadata schema toi thieu 2 truong huu ich.
- [x] Tao 5 benchmark queries va gold answers.
- [x] Chon strategy ca nhan: `RecursiveChunker(chunk_size=500)`.
- [ ] Chay `ChunkingStrategyComparator` tren 2-3 tai lieu.
- [ ] Chay retrieval benchmark top-3 cho 5 queries.
- [ ] Ghi ket qua vao bang benchmark.
- [ ] Viet nhan xet failure case va de xuat cai thien.

### Bang dien sau cho Phase 2

| Hang muc | Ket qua se cap nhat |
|---|---|
| Domain solo | Internal AI Knowledge Assistant Documentation |
| Tai lieu solo | 6 file trong `data/` |
| Metadata schema | `source`, `doc_type`, `language`, `topic`, `parent_doc`, `chunk_index` |
| Strategy ca nhan | `RecursiveChunker(chunk_size=500)` |
| 5 benchmark queries | Da de xuat trong muc Phase 2 Solo |
| Top-3 retrieval results | TBD |
| Strategy tot nhat trong so sanh baseline | TBD |
| Failure case | TBD |

## Ket luan hien tai

Phase 1 ca nhan da hoan thanh phan code cot loi cho embedding va vector store lab. Implementation hien tai co the dung lam nen tang cho Phase 2: chon data, thu strategy chunking rieng, chay benchmark retrieval va so sanh ket qua trong nhom.
