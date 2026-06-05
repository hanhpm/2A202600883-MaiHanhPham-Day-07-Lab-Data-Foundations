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

const strategies = [
  {
    student: "Nguyễn Thị Vang",
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
  },
  {
    student: "Phạm Mai Hạnh",
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
  },
];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderScoreBars() {
  const root = document.querySelector("#scoreBars");
  strategies.forEach((item) => {
    const row = el("div", "student-row");
    const meta = el("div", "student-meta");
    meta.append(el("strong", "", `${item.student} · ${item.id}`));
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
    const avgFill = el("div", "chunk-fill");
    avgFill.style.width = `${Math.min(100, (item.avgLength / 2200) * 100)}%`;
    avgTrack.append(avgFill);
    avg.append(avgTrack);
    avg.append(el("div", "chunk-value", `${item.avgLength}`));
    root.append(avg);
  });
}

function renderQueryTable() {
  const body = document.querySelector("#queryTable tbody");
  strategies.forEach((strategy) => {
    strategy.results.forEach((row) => {
      const tr = document.createElement("tr");
      const cells = [
        `${strategy.student}`,
        row[0],
        row[1],
        row[2],
        row[3],
        `${row[4]}/2`,
      ];
      cells.forEach((cell) => {
        const td = document.createElement("td");
        if (String(cell).includes("data/downloaded_data")) {
          const code = document.createElement("code");
          code.textContent = cell;
          td.append(code);
        } else {
          td.textContent = cell;
        }
        tr.append(td);
      });

      const relevant = document.createElement("td");
      const pill = el("span", `pill ${row[5] ? "good" : "bad"}`, row[5] ? "Relevant" : "Not relevant");
      relevant.append(pill);
      tr.append(relevant);

      const filtered = document.createElement("td");
      const code = document.createElement("code");
      code.textContent = row[6];
      filtered.append(code);
      tr.append(filtered);

      body.append(tr);
    });
  });
}

function renderDataset() {
  const root = document.querySelector("#datasetList");
  dataset.forEach(([file, topic, type, chars]) => {
    const item = el("div", "doc-item");
    const left = document.createElement("div");
    left.append(el("strong", "", file));
    left.append(el("span", "", `${topic} · ${type}`));
    item.append(left);
    item.append(el("span", "", `${chars.toLocaleString()} chars`));
    root.append(item);
  });
}

renderScoreBars();
renderChunkChart();
renderQueryTable();
renderDataset();
