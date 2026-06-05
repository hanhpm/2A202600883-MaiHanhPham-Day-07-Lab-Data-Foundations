from pathlib import Path
import requests
import html2text

DOCS = {
    "langchain_text_splitters.md": "https://docs.langchain.com/oss/python/integrations/splitters",
    "chroma_introduction.md": "https://docs.trychroma.com/docs/overview/introduction",
    "qdrant_collections.md": "https://qdrant.tech/documentation/manage-data/collections/",
    "qdrant_points.md": "https://qdrant.tech/documentation/manage-data/points/",
    "sentence_transformers_sts.md": "https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html",
}

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

converter = html2text.HTML2Text()
converter.ignore_links = False
converter.body_width = 0

headers = {
    "User-Agent": "Mozilla/5.0"
}

for filename, url in DOCS.items():
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    markdown = converter.handle(response.text)
    output_path = output_dir / filename
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Saved {output_path}")