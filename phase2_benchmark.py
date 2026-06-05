from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src import (
    Document,
    EmbeddingStore,
    EMBEDDING_PROVIDER_ENV,
    FixedSizeChunker,
    KnowledgeBaseAgent,
    OPENAI_EMBEDDING_MODEL,
    OpenAIEmbedder,
    RecursiveChunker,
    SentenceChunker,
    _mock_embed,
)


ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data" / "downloaded_data"
REPORT_DIR = ROOT / "report"


DATASET = [
    ("chroma_introduction.md", "chroma", "overview", "Chroma introduction"),
    ("chroma_usage_guide.md", "chroma", "guide", "Chroma usage guide"),
    ("docker_compose_readme.md", "docker", "readme", "Docker Compose readme"),
    ("fastapi_first_steps.md", "fastapi", "tutorial", "FastAPI first steps"),
    ("fastapi_tutorial_index.md", "fastapi", "tutorial", "FastAPI tutorial index"),
    ("langchain_text_splitters.md", "langchain", "guide", "LangChain text splitters"),
    ("qdrant_collections.md", "qdrant", "manual", "Qdrant collections"),
    ("qdrant_points.md", "qdrant", "manual", "Qdrant points"),
    ("sentence_transformers_sts.md", "sentence_transformers", "guide", "Sentence Transformers STS"),
]


QUERIES = [
    {
        "id": "Q1",
        "query": "What does Chroma provide for retrieval and metadata filtering?",
        "gold_answer": "Chroma provides retrieval infrastructure to store embeddings with metadata, search with dense/sparse vectors, filter by metadata, and retrieve across text, images, and other modalities.",
        "expected_topic": "chroma",
        "metadata_filter": {"topic": "chroma"},
    },
    {
        "id": "Q2",
        "query": "How do you run a FastAPI app locally and where can you open interactive API docs?",
        "gold_answer": "Copy the app code to main.py, run the development server with fastapi dev, open the app at http://127.0.0.1:8000, and open interactive docs at /docs.",
        "expected_topic": "fastapi",
        "metadata_filter": {"topic": "fastapi"},
    },
    {
        "id": "Q3",
        "query": "Why is RecursiveCharacterTextSplitter a good default text splitting strategy?",
        "gold_answer": "It keeps larger units like paragraphs intact when possible, then falls back to smaller units such as sentences and words to manage chunk size while preserving context.",
        "expected_topic": "langchain",
        "metadata_filter": {"topic": "langchain"},
    },
    {
        "id": "Q4",
        "query": "In Qdrant, what is a collection and which distance metrics are supported?",
        "gold_answer": "A collection is a named set of points, each containing vectors and optional payload. Qdrant supports Dot, Cosine, Euclidean, and Manhattan distance metrics.",
        "expected_topic": "qdrant",
        "metadata_filter": {"topic": "qdrant"},
    },
    {
        "id": "Q5",
        "query": "What is the quick start process for Docker Compose?",
        "gold_answer": "Define the app environment with a Dockerfile, define services in compose.yaml, then run docker compose up to start the application.",
        "expected_topic": "docker",
        "metadata_filter": {"topic": "docker"},
    },
    {
        "id": "Q6",
        "query": "Which similarity functions are available in Sentence Transformers for semantic textual similarity?",
        "gold_answer": "Sentence Transformers supports cosine similarity, dot product, negative Euclidean distance, and negative Manhattan distance.",
        "expected_topic": "sentence_transformers",
        "metadata_filter": {"topic": "sentence_transformers"},
    },
]


STRATEGIES = [
    {
        "student": "Nguyễn Thị Vang",
        "student_id": "2A202600723",
        "strategy_name": "SentenceChunker(max_sentences_per_chunk=4)",
        "chunker": SentenceChunker(max_sentences_per_chunk=4),
        "rationale": "Sentence-based chunks giữ câu hoàn chỉnh, giúp tutorial và API documentation dễ đọc khi kiểm tra kết quả.",
    },
    {
        "student": "Phạm Mai Hạnh",
        "student_id": "2A202600883",
        "strategy_name": "RecursiveChunker(chunk_size=700)",
        "chunker": RecursiveChunker(chunk_size=700),
        "rationale": "Recursive chunks giữ paragraph và section markdown trước, sau đó mới tách nhỏ hơn khi cần.",
    },
]


BASELINE_CHUNKERS = {
    "fixed_size": FixedSizeChunker(chunk_size=700, overlap=70),
    "by_sentences": SentenceChunker(max_sentences_per_chunk=4),
    "recursive": RecursiveChunker(chunk_size=700),
}


class CachedEmbedder:
    """Cache embedding calls during benchmark runs to avoid duplicate API requests."""

    def __init__(self, embedder: Any, max_input_chars: int | None = None) -> None:
        self.embedder = embedder
        self._backend_name = getattr(embedder, "_backend_name", embedder.__class__.__name__)
        self.max_input_chars = max_input_chars
        self._cache: dict[str, list[float]] = {}

    def __call__(self, text: str) -> list[float]:
        if text not in self._cache:
            embedding_text = text[: self.max_input_chars] if self.max_input_chars else text
            self._cache[text] = self.embedder(embedding_text)
        return self._cache[text]


def get_benchmark_embedder() -> tuple[Any, str]:
    load_dotenv(ROOT / ".env", override=False)
    provider = os.getenv(EMBEDDING_PROVIDER_ENV, "mock").strip().lower()
    if provider == "openai":
        try:
            model = os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL)
            return (
                CachedEmbedder(OpenAIEmbedder(model_name=model), max_input_chars=6000),
                f"openai:{model}:truncated_to_6000_chars",
            )
        except Exception as exc:
            print(f"[WARN] OpenAI embedder unavailable, falling back to mock: {exc}", file=sys.stderr)
    return CachedEmbedder(_mock_embed), "mock"


def load_texts() -> list[dict[str, str]]:
    rows = []
    for filename, topic, doc_type, title in DATASET:
        path = DATA_DIR / filename
        text = path.read_text(encoding="utf-8")
        rows.append(
            {
                "filename": filename,
                "topic": topic,
                "doc_type": doc_type,
                "title": title,
                "text": text,
                "chars": str(len(text)),
            }
        )
    return rows


def build_documents(rows: list[dict[str, str]], chunker: Any) -> list[Document]:
    documents: list[Document] = []
    for row in rows:
        chunks = chunker.chunk(row["text"])
        for index, chunk in enumerate(chunks):
            documents.append(
                Document(
                    id=f"{Path(row['filename']).stem}_{index}",
                    content=chunk,
                    metadata={
                        "source": f"data/downloaded_data/{row['filename']}",
                        "filename": row["filename"],
                        "parent_doc": Path(row["filename"]).stem,
                        "topic": row["topic"],
                        "doc_type": row["doc_type"],
                        "title": row["title"],
                        "language": "en",
                        "chunk_index": index,
                    },
                )
            )
    return documents


def is_relevant(results: list[dict[str, Any]], expected_topic: str) -> bool:
    return any(result["metadata"].get("topic") == expected_topic for result in results)


def score_result(results: list[dict[str, Any]], expected_topic: str) -> int:
    if not results:
        return 0
    if results[0]["metadata"].get("topic") == expected_topic:
        return 2
    if is_relevant(results, expected_topic):
        return 1
    return 0


def make_grounded_answer(prompt: str) -> str:
    question = ""
    context_preview = ""
    if "Question:\n" in prompt and "\n\nContext:\n" in prompt:
        question = prompt.split("Question:\n", 1)[1].split("\n\nContext:\n", 1)[0].strip()
    if "Context:\n" in prompt and "\n\nAnswer:" in prompt:
        context_preview = prompt.split("Context:\n", 1)[1].split("\n\nAnswer:", 1)[0]
        context_preview = " ".join(context_preview.split())[:260]
    return f"Grounded answer for: {question}. Evidence preview: {context_preview}"


def run_strategy(rows: list[dict[str, str]], strategy: dict[str, Any], embedding_fn: Any) -> dict[str, Any]:
    documents = build_documents(rows, strategy["chunker"])
    store = EmbeddingStore(
        collection_name=f"phase2_{strategy['student_id']}",
        embedding_fn=embedding_fn,
    )
    store.add_documents(documents)
    query_results = []
    for query in QUERIES:
        unfiltered = store.search(query["query"], top_k=3)
        filtered = store.search_with_filter(
            query["query"],
            top_k=3,
            metadata_filter=query["metadata_filter"],
        )
        filtered_store = EmbeddingStore(
            collection_name=f"phase2_filtered_{strategy['student_id']}_{query['id']}",
            embedding_fn=embedding_fn,
        )
        filtered_store.add_documents(
            [
                Document(
                    id=f"{query['id']}_{rank}",
                    content=result["content"],
                    metadata=result["metadata"],
                )
                for rank, result in enumerate(filtered, start=1)
            ]
        )
        agent = KnowledgeBaseAgent(store=filtered_store, llm_fn=make_grounded_answer)
        agent_answer = agent.answer(query["query"], top_k=3)
        query_results.append(
            {
                **query,
                "top3": [
                    {
                        "rank": rank,
                        "score": round(result["score"], 4),
                        "source": result["metadata"].get("source"),
                        "topic": result["metadata"].get("topic"),
                        "preview": " ".join(result["content"].split())[:220],
                    }
                    for rank, result in enumerate(unfiltered, start=1)
                ],
                "filtered_top3": [
                    {
                        "rank": rank,
                        "score": round(result["score"], 4),
                        "source": result["metadata"].get("source"),
                        "topic": result["metadata"].get("topic"),
                        "preview": " ".join(result["content"].split())[:220],
                    }
                    for rank, result in enumerate(filtered, start=1)
                ],
                "top3_relevant": is_relevant(unfiltered, query["expected_topic"]),
                "filtered_top3_relevant": is_relevant(filtered, query["expected_topic"]),
                "score_points": score_result(unfiltered, query["expected_topic"]),
                "filtered_score_points": score_result(filtered, query["expected_topic"]),
                "agent_answer": agent_answer,
                "agent_answer_verified": is_relevant(filtered, query["expected_topic"]),
            }
        )

    return {
        "student": strategy["student"],
        "student_id": strategy["student_id"],
        "strategy_name": strategy["strategy_name"],
        "rationale": strategy["rationale"],
        "chunk_count": len(documents),
        "avg_chunk_length": round(sum(len(doc.content) for doc in documents) / len(documents), 2),
        "results": query_results,
        "total_score": sum(item["score_points"] for item in query_results),
        "filtered_total_score": sum(item["filtered_score_points"] for item in query_results),
    }


def build_baseline(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    selected = [
        "chroma_usage_guide.md",
        "fastapi_first_steps.md",
        "langchain_text_splitters.md",
        "qdrant_collections.md",
    ]
    baseline: dict[str, dict[str, float]] = {}
    for row in rows:
        if row["filename"] not in selected:
            continue
        baseline[row["filename"]] = {}
        for name, chunker in BASELINE_CHUNKERS.items():
            chunks = chunker.chunk(row["text"])
            baseline[row["filename"]][f"{name}_count"] = len(chunks)
            baseline[row["filename"]][f"{name}_avg_length"] = round(
                sum(len(chunk) for chunk in chunks) / len(chunks), 2
            )
    return baseline


def markdown_report(
    rows: list[dict[str, str]],
    baseline: dict[str, Any],
    strategies: list[dict[str, Any]],
    embedding_backend: str,
) -> str:
    lines = [
        "# Phase 2 Benchmark Results",
        "",
        f"**Embedding backend:** `{embedding_backend}`",
        "",
        "## Dataset",
        "",
        "| File | Topic | Type | Characters |",
        "|---|---|---|---:|",
    ]
    for row in rows:
        lines.append(f"| `{row['filename']}` | {row['topic']} | {row['doc_type']} | {row['chars']} |")

    lines.extend(
        [
            "",
            "## Baseline Chunking Comparison",
            "",
            "| File | Fixed count / avg | Sentence count / avg | Recursive count / avg |",
            "|---|---:|---:|---:|",
        ]
    )
    for filename, stats in baseline.items():
        lines.append(
            "| `{}` | {} / {} | {} / {} | {} / {} |".format(
                filename,
                stats["fixed_size_count"],
                stats["fixed_size_avg_length"],
                stats["by_sentences_count"],
                stats["by_sentences_avg_length"],
                stats["recursive_count"],
                stats["recursive_avg_length"],
            )
        )

    lines.extend(
        [
            "",
            "## Query Set",
            "",
            "| ID | Query | Gold answer | Expected topic |",
            "|---|---|---|---|",
        ]
    )
    for query in QUERIES:
        lines.append(
            f"| {query['id']} | {query['query']} | {query['gold_answer']} | {query['expected_topic']} |"
        )

    for strategy in strategies:
        lines.extend(
            [
                "",
                f"## {strategy['student']} - {strategy['student_id']}",
                "",
                f"- Strategy: `{strategy['strategy_name']}`",
                f"- Rationale: {strategy['rationale']}",
                f"- Stored chunks: {strategy['chunk_count']}",
                f"- Average chunk length: {strategy['avg_chunk_length']}",
                f"- Unfiltered score: {strategy['total_score']} / {len(QUERIES) * 2}",
                f"- Filtered score: {strategy['filtered_total_score']} / {len(QUERIES) * 2}",
                "",
                "| ID | Expected | Top-1 source | Top-1 topic | Score | Top-3 relevant? | Filtered Top-1 source |",
                "|---|---|---|---|---:|---|---|",
            ]
        )
        for result in strategy["results"]:
            top1 = result["top3"][0] if result["top3"] else {}
            filtered_top1 = result["filtered_top3"][0] if result["filtered_top3"] else {}
            lines.append(
                "| {} | {} | `{}` | {} | {} | {} | `{}` |".format(
                    result["id"],
                    result["expected_topic"],
                    top1.get("source", "N/A"),
                    top1.get("topic", "N/A"),
                    result["score_points"],
                    "Yes" if result["top3_relevant"] else "No",
                    filtered_top1.get("source", "N/A"),
                )
            )

        lines.extend(
            [
                "",
                "| ID | Agent answer verification | Agent answer preview |",
                "|---|---|---|",
            ]
        )
        for result in strategy["results"]:
            lines.append(
                "| {} | {} | {} |".format(
                    result["id"],
                    "Verified against filtered top-3 context" if result["agent_answer_verified"] else "Needs review",
                    result["agent_answer"].replace("|", "/")[:260],
                )
            )

    lines.extend(
        [
            "",
            "## Comparison Summary",
            "",
            "| Student | Strategy | Chunks | Avg length | Unfiltered score | Filtered score |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for strategy in strategies:
        lines.append(
            f"| {strategy['student']} | `{strategy['strategy_name']}` | {strategy['chunk_count']} | {strategy['avg_chunk_length']} | {strategy['total_score']} / 12 | {strategy['filtered_total_score']} / 12 |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    embedder, embedding_backend = get_benchmark_embedder()
    rows = load_texts()
    baseline = build_baseline(rows)
    strategy_results = [run_strategy(rows, strategy, embedder) for strategy in STRATEGIES]
    output = {
        "embedding_backend": embedding_backend,
        "dataset": rows,
        "baseline": baseline,
        "strategies": strategy_results,
    }

    REPORT_DIR.mkdir(exist_ok=True)
    suffix = "_openai" if embedding_backend.startswith("openai:") else ""
    json_path = REPORT_DIR / f"phase2_benchmark_results{suffix}.json"
    md_path = REPORT_DIR / f"PHASE2_BENCHMARK_RESULTS{suffix.upper()}.md"

    json_path.write_text(
        json.dumps(output, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
    md_path.write_text(
        markdown_report(rows, baseline, strategy_results, embedding_backend),
        encoding="utf-8",
    )
    print(markdown_report(rows, baseline, strategy_results, embedding_backend))


if __name__ == "__main__":
    main()
