"""RAG pipeline: retrieval + generation with Claude."""
from langchain_anthropic import ChatAnthropic
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from app.config import get_settings
from app.core import vector_store as vs
from app.models import QueryResponse, SourceChunk

SYSTEM_PROMPT = """\
You are a helpful assistant that answers questions using only the provided context.
If the context does not contain enough information to answer the question, say so clearly.
Do not hallucinate or make up information.

Context:
{context}
"""


def _build_rag_chain(k: int):
    settings = get_settings()
    llm = ChatAnthropic(
        model=settings.claude_model,
        anthropic_api_key=settings.anthropic_api_key,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
    ])

    vector_store = vs.get_vector_store()
    if vector_store is None:
        raise RuntimeError("Knowledge base is empty — ingest documents before querying.")
    retriever = vector_store.as_retriever(search_kwargs={"k": k})

    doc_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, doc_chain), retriever


def run_rag_query(question: str, k: int, include_sources: bool) -> QueryResponse:
    settings = get_settings()
    effective_k = k or settings.retrieval_k

    chain, retriever = _build_rag_chain(effective_k)

    # Run the chain (retrieval + generation in one call)
    result = chain.invoke({"input": question})
    answer: str = result["answer"]
    context_docs: list[Document] = result.get("context", [])

    sources: list[SourceChunk] = []
    if include_sources:
        for doc in context_docs:
            sources.append(SourceChunk(
                content=doc.page_content,
                source=doc.metadata.get("source"),
                metadata=doc.metadata,
            ))

    return QueryResponse(
        question=question,
        answer=answer,
        sources=sources,
        model=settings.claude_model,
    )
