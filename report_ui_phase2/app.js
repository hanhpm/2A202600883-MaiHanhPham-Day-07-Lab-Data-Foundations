const dataset = [
  ["chroma_introduction.md", "chroma", "overview", 5112],
  ["chroma_usage_guide.md", "chroma", "guide", 30529],
  ["docker_compose_readme.md", "docker", "readme", 3693],
  ["fastapi_first_steps.md", "fastapi", "tutorial", 13860],
  ["fastapi_tutorial_index.md", "fastapi", "tutorial", 5408],
  ["langchain_text_splitters.md", "langchain", "guide", 8587],
  ["qdrant_collections.md", "qdrant", "manual", 86365],
  ["qdrant_points.md", "qdrant", "manual", 107349],
  ["sentence_transformers_sts.md", "sentence_transformers", "guide", 66755],
];

const similarityPairs = [
  ["P1", "high", -0.0965, "Chroma stores embeddings...", "Vector databases store vectors..."],
  ["P2", "high", -0.0259, "FastAPI creates interactive API docs.", "FastAPI provides Swagger UI documentation."],
  ["P3", "low", 0.1510, "Docker Compose runs multi-container apps.", "A guitar player performs on stage."],
  ["P4", "medium", -0.0853, "Qdrant collections contain points and vectors.", "Sentence Transformers computes text embeddings."],
  ["P5", "high", -0.1959, "Recursive splitting preserves paragraph context.", "Chunking can keep sections coherent."],
];

const strategies = [
  {
    student: "Nguyen Thi Vang",
    id: "2A202600723",
    strategy: "SentenceChunker(max_sentences_per_chunk=4)",
    chunks: 151,
    avgLength: 2165.61,
    unfiltered: 3,
    filtered: 12,
    results: [
      ["Q1", "chroma", "data/downloaded_data/qdrant_points.md", "qdrant", 1, true, "data/downloaded_data/chroma_usage_guide.md"],
      ["Q2", "fastapi", "data/downloaded_data/docker_compose_readme.md", "docker", 0, false, "data/downloaded_data/fastapi_first_steps.md"],
      ["Q3", "langchain", "data/downloaded_data/chroma_usage_guide.md", "chroma", 0, false, "data/downloaded_data/langchain_text_splitters.md"],
      ["Q4", "qdrant", "data/downloaded_data/qdrant_collections.md", "qdrant", 2, true, "data/downloaded_data/qdrant_collections.md"],
      ["Q5", "docker", "data/downloaded_data/chroma_usage_guide.md", "chroma", 0, false, "data/downloaded_data/docker_compose_readme.md"],
      ["Q6", "sentence_transformers", "data/downloaded_data/fastapi_first_steps.md", "fastapi", 0, false, "data/downloaded_data/sentence_transformers_sts.md"],
    ],
    agent: [
      ["Q1", "data/downloaded_data/chroma_usage_guide.md", "Verified", "Evidence context Chroma has embeddings, metadata, and retrieval."],
      ["Q2", "data/downloaded_data/fastapi_first_steps.md", "Verified", "Evidence context FastAPI has a local server and interactive docs."],
      ["Q3", "data/downloaded_data/langchain_text_splitters.md", "Verified", "Evidence context LangChain keeps paragraphs before splitting into smaller chunks."],
      ["Q4", "data/downloaded_data/qdrant_collections.md", "Verified", "Evidence context Qdrant describes collections, vectors, and metrics."],
      ["Q5", "data/downloaded_data/docker_compose_readme.md", "Verified", "Evidence context Docker Compose includes Dockerfile, compose.yaml, and docker compose up."],
      ["Q6", "data/downloaded_data/sentence_transformers_sts.md", "Verified", "Evidence context Sentence Transformers includes cosine, dot, Euclidean, and Manhattan similarity."],
    ],
  },
  {
    student: "Pham Mai Hanh",
    id: "2A202600883",
    strategy: "RecursiveChunker(chunk_size=700)",
    chunks: 490,
    avgLength: 569.07,
    unfiltered: 3,
    filtered: 12,
    results: [
      ["Q1", "chroma", "data/downloaded_data/qdrant_collections.md", "qdrant", 0, false, "data/downloaded_data/chroma_introduction.md"],
      ["Q2", "fastapi", "data/downloaded_data/qdrant_points.md", "qdrant", 0, false, "data/downloaded_data/fastapi_first_steps.md"],
      ["Q3", "langchain", "data/downloaded_data/qdrant_points.md", "qdrant", 0, false, "data/downloaded_data/langchain_text_splitters.md"],
      ["Q4", "qdrant", "data/downloaded_data/sentence_transformers_sts.md", "sentence_transformers", 1, true, "data/downloaded_data/qdrant_points.md"],
      ["Q5", "docker", "data/downloaded_data/qdrant_collections.md", "qdrant", 0, false, "data/downloaded_data/docker_compose_readme.md"],
      ["Q6", "sentence_transformers", "data/downloaded_data/sentence_transformers_sts.md", "sentence_transformers", 2, true, "data/downloaded_data/sentence_transformers_sts.md"],
    ],
    agent: [
      ["Q1", "data/downloaded_data/chroma_introduction.md", "Verified", "Evidence context Chroma introduction mentions retrieval and metadata."],
      ["Q2", "data/downloaded_data/fastapi_first_steps.md", "Verified", "Evidence context FastAPI first steps uses fastapi dev and /docs."],
      ["Q3", "data/downloaded_data/langchain_text_splitters.md", "Verified", "Evidence context LangChain text splitters describe recursive splitting."],
      ["Q4", "data/downloaded_data/qdrant_points.md", "Verified", "Evidence context Qdrant includes points, vectors, and payload."],
      ["Q5", "data/downloaded_data/docker_compose_readme.md", "Verified", "Evidence context Docker Compose describes the quick start process."],
      ["Q6", "data/downloaded_data/sentence_transformers_sts.md", "Verified", "Evidence context STS lists available similarity functions."],
    ],
  },
];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function appendCodeCell(tr, text) {
  const td = document.createElement("td");
  const code = document.createElement("code");
  code.textContent = text;
  td.append(code);
  tr.append(td);
}

function renderScoreBars() {
  const root = document.querySelector("#scoreBars");
  strategies.forEach((item) => {
    const row = el("div", "student-row");
    const meta = el("div", "student-meta");
    meta.append(el("strong", "", `${item.student} - ${item.id}`));
    meta.append(el("span", "", item.strategy));

    const pair = el("div", "bar-pair");
    [
      ["Unfiltered", item.unfiltered, "unfiltered"],
      ["Filtered", item.filtered, "filtered"],
    ].forEach(([label, value, kind]) => {
      const labelNode = el("div", "bar-label", `${label}: ${value}/12`);
      const track = el("div", "bar-track");
      const fill = el("div", `bar-fill ${kind}`);
      fill.style.width = `${(value / 12) * 100}%`;
      track.append(fill);
      pair.append(labelNode, track);
    });

    row.append(meta, pair);
    root.append(row);
  });
}

function renderChunkChart() {
  const root = document.querySelector("#chunkChart");
  const maxChunks = Math.max(...strategies.map((item) => item.chunks));
  strategies.forEach((item) => {
    const row = el("div", "chunk-row");
    row.append(el("div", "chunk-name", item.student));
    const track = el("div", "chunk-track");
    const fill = el("div", "chunk-fill");
    fill.style.width = `${(item.chunks / maxChunks) * 100}%`;
    track.append(fill);
    row.append(track);
    row.append(el("div", "chunk-value", `${item.chunks} chunks`));
    root.append(row);

    const avg = el("div", "chunk-row");
    avg.append(el("div", "chunk-name", "Avg length"));
    const avgTrack = el("div", "chunk-track");
    const avgFill = el("div", "chunk-fill amber-fill");
    avgFill.style.width = `${Math.min(100, (item.avgLength / 2200) * 100)}%`;
    avgTrack.append(avgFill);
    avg.append(avgTrack);
    avg.append(el("div", "chunk-value", `${item.avgLength}`));
    root.append(avg);
  });
}

function renderSimilarity() {
  const root = document.querySelector("#similarityList");
  similarityPairs.forEach(([id, prediction, score, a, b]) => {
    const item = el("div", "similarity-item");
    const top = el("div", "similarity-top");
    top.append(el("strong", "", `${id} - predicted ${prediction}`));
    top.append(el("span", score < 0 ? "score negative" : "score positive", Number(score).toFixed(4)));
    const text = el("p", "", `${a} <-> ${b}`);
    const note = el("span", "note", "Actual score from code. Mock embedder explains the mismatch with semantic prediction.");
    item.append(top, text, note);
    root.append(item);
  });
}

function renderQueryTable() {
  const body = document.querySelector("#queryTable tbody");
  strategies.forEach((strategy) => {
    strategy.results.forEach((row) => {
      const tr = document.createElement("tr");
      [strategy.student, row[0], row[1]].forEach((cell) => {
        const td = document.createElement("td");
        td.textContent = cell;
        tr.append(td);
      });
      appendCodeCell(tr, row[2]);

      const topic = document.createElement("td");
      topic.textContent = row[3];
      tr.append(topic);

      const score = document.createElement("td");
      score.textContent = `${row[4]}/2`;
      score.className = "score-cell";
      tr.append(score);

      const relevant = document.createElement("td");
      relevant.append(el("span", `pill ${row[5] ? "good" : "bad"}`, row[5] ? "Relevant" : "Not relevant"));
      tr.append(relevant);
      appendCodeCell(tr, row[6]);
      body.append(tr);
    });
  });
}

function renderAgentGrid() {
  const root = document.querySelector("#agentGrid");
  strategies.forEach((strategy) => {
    const card = el("article", "agent-card");
    card.append(el("h3", "", `${strategy.student} - ${strategy.strategy}`));
    strategy.agent.forEach(([query, source, status, summary]) => {
      const item = el("div", "agent-item");
      item.append(el("span", "pill good", status));
      item.append(el("strong", "", query));
      const code = document.createElement("code");
      code.textContent = source;
      item.append(code);
      item.append(el("p", "", summary));
      card.append(item);
    });
    root.append(card);
  });
}

function renderDataset() {
  const root = document.querySelector("#datasetList");
  dataset.forEach(([file, topic, type, chars]) => {
    const item = el("div", "doc-item");
    const left = document.createElement("div");
    left.append(el("strong", "", file));
    left.append(el("span", "", `${topic} - ${type}`));
    item.append(left);
    item.append(el("span", "", `${chars.toLocaleString()} chars`));
    root.append(item);
  });
}

renderScoreBars();
renderChunkChart();
renderSimilarity();
renderQueryTable();
renderAgentGrid();
renderDataset();
