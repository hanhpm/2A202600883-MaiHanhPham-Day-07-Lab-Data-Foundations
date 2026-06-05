> ## Documentation Index
> 
> Fetch the complete documentation index at: [/llms.txt](/llms.txt)
> 
> Use this file to discover all available pages before exploring further.

Skip to main content

[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)](/)

![https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/images/brand/langchain-icon.png)Open source

Search...

⌘K

  * [Ask AI](https://chat.langchain.com/)
  * [GitHub](https://github.com/langchain-ai)
  * [Try LangSmith](https://smith.langchain.com/)
  * [Try LangSmith](https://smith.langchain.com/)



Search...

Navigation

Integrations by component

Text splitter integrations

[Deep Agents](/oss/python/deepagents/overview)[LangChain](/oss/python/langchain/overview)[LangGraph](/oss/python/langgraph/overview)[Integrations](/oss/python/integrations/providers/overview)[Learn](/oss/python/learn)[Reference](/oss/python/reference/overview)[Contribute](/oss/python/contributing/overview)

Python



  * [LangChain integrations](/oss/python/integrations/providers/overview)


  * [All providers](/oss/python/integrations/providers/all_providers)



### Popular Providers

  * [OpenAI](/oss/python/integrations/providers/openai)
  * [Anthropic](/oss/python/integrations/providers/anthropic)
  * [Google](/oss/python/integrations/providers/google)
  * [AWS](/oss/python/integrations/providers/aws)
  * [NVIDIA](/oss/python/integrations/providers/nvidia)
  * [Hugging Face](/oss/python/integrations/providers/huggingface)
  * [Microsoft](/oss/python/integrations/providers/microsoft)
  * [Ollama](/oss/python/integrations/providers/ollama)
  * [Groq](/oss/python/integrations/providers/groq)
  * [Fireworks](/oss/python/integrations/providers/fireworks)



### Integrations by component

  * [Chat models](/oss/python/integrations/chat)
  * [Tools and toolkits](/oss/python/integrations/tools)
  * [Middleware](/oss/python/integrations/middleware)
  * [Sandboxes](/oss/python/integrations/sandboxes)
  * [Checkpointers](/oss/python/integrations/checkpointers)
  * [Retrievers](/oss/python/integrations/retrievers)
  * [Text splitters](/oss/python/integrations/splitters)
  * [Embedding models](/oss/python/integrations/embeddings)
  * [Vector stores](/oss/python/integrations/vectorstores)
  * [Document loaders](/oss/python/integrations/document_loaders)



## On this page

  * Text structure-based
  * Length-based
  * Document structure-based



[Integrations by component](/oss/python/integrations/chat/index)

# Text splitter integrations

Copy page

Integrate with text splitters using LangChain.

Copy page

pip

uv
    
    
    pip install -U langchain-text-splitters
    

**Text splitters** break large docs into smaller chunks that will be retrievable individually and fit within model context window limit. There are several strategies for splitting documents, each with its own advantages.

For most use cases, start with the [`RecursiveCharacterTextSplitter`](/oss/python/integrations/splitters/recursive_text_splitter). It provides a solid balance between keeping context intact and managing chunk size. This default strategy works well out of the box, and you should only consider adjusting it if you need to fine-tune performance for your specific application.

## 

​

Text structure-based

Text is naturally organized into hierarchical units such as paragraphs, sentences, and words. We can leverage this inherent structure to inform our splitting strategy, creating split that maintain natural language flow, maintain semantic coherence within split, and adapts to varying levels of text granularity. LangChain’s `RecursiveCharacterTextSplitter` implements this concept:

  * The [`RecursiveCharacterTextSplitter`](/oss/python/integrations/splitters/recursive_text_splitter) attempts to keep larger units (e.g., paragraphs) intact.
  * If a unit exceeds the chunk size, it moves to the next level (e.g., sentences).
  * This process continues down to the word level if necessary.

Example usage:
    
    
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_text(document)
    

**Available text splitters** :

  * [Recursively split text](/oss/python/integrations/splitters/recursive_text_splitter)



## 

​

Length-based

An intuitive strategy is to split documents based on their length. This simple yet effective approach ensures that each chunk doesn’t exceed a specified size limit. Key benefits of length-based splitting:

  * Straightforward implementation
  * Consistent chunk sizes
  * Easily adaptable to different model requirements

Types of length-based splitting:

  * Token-based: Splits text based on the number of tokens, which is useful when working with language models.
  * Character-based: Splits text based on the number of characters, which can be more consistent across different types of text.

Example implementation using LangChain’s `CharacterTextSplitter` with token-based splitting:
    
    
    from langchain_text_splitters import CharacterTextSplitter
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=100, chunk_overlap=0
    )
    texts = text_splitter.split_text(document)
    

**Available text splitters** :

  * [Split by tokens](/oss/python/integrations/splitters/split_by_token)
  * [Split by characters](/oss/python/integrations/splitters/character_text_splitter)



## 

​

Document structure-based

Some documents have an inherent structure, such as HTML, Markdown, or JSON files. In these cases, it’s beneficial to split the document based on its structure, as it often naturally groups semantically related text. Key benefits of structure-based splitting:

  * Preserves the logical organization of the document
  * Maintains context within each chunk
  * Can be more effective for downstream tasks like retrieval or summarization

Examples of structure-based splitting:

  * Markdown: Split based on headers (e.g., `#`, `##`, `###`)
  * HTML: Split using tags
  * JSON: Split by object or array elements
  * Code: Split by functions, classes, or logical blocks

**Available text splitters** :

  * [Split Markdown](/oss/python/integrations/splitters/markdown_header_metadata_splitter)
  * [Split JSON](/oss/python/integrations/splitters/recursive_json_splitter)
  * [Split code](/oss/python/integrations/splitters/code_splitter)
  * [Split HTML](/oss/python/integrations/splitters/split_html)



* * *

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/integrations/splitters/index.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

Was this page helpful?

YesNo

[Retriever integrationsPrevious](/oss/python/integrations/retrievers)[Embedding model integrationsNext](/oss/python/integrations/embeddings)

⌘I

[Docs by LangChain home page![light logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-dark-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=5babf1a1962208fd7eed942fa2432ecb)![dark logo](https://mintcdn.com/langchain-5e9cc07a/nQm-sjd_MByLhgeW/images/brand/langchain-docs-light-blue.png?fit=max&auto=format&n=nQm-sjd_MByLhgeW&q=85&s=0bcd2a1f2599ed228bcedf0f535b45b1)](/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChain)[linkedin](https://www.linkedin.com/company/langchain)[youtube](https://www.youtube.com/@LangChain)

Resources

[Forum](https://forum.langchain.com/)[Changelog](https://changelog.langchain.com/)[LangChain Academy](https://academy.langchain.com/)[Contact Sales](https://www.langchain.com/contact-sales)

Company

[Home](https://langchain.com/)[Trust Center](https://trust.langchain.com/)[Careers](https://langchain.com/careers)[Blog](https://blog.langchain.com/)

[github](https://github.com/langchain-ai)[x](https://x.com/LangChain)[linkedin](https://www.linkedin.com/company/langchain)[youtube](https://www.youtube.com/@LangChain)
