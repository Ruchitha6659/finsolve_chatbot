import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rbac import get_allowed_roles


# ── LOAD ENV VARIABLES ────────────────────────────────────
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


# ── CONSTANTS ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

CHROMA_DIR = Path(C:/temp_chroma_db/finsolve)"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

COLLECTION_NAME = "finsolve"


# ── GLOBAL OBJECTS ────────────────────────────────────────
llm = None
vector_store = None


# ── INITIALIZE COMPONENTS ─────────────────────────────────
def initialize_components():

    global llm, vector_store

    print(f"\n📂 Loading ChromaDB from: {CHROMA_DIR}")

    if llm is None:

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=500,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    if vector_store is None:

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    import shutil

    try:
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR)
        )

    except Exception as e:

        print("⚠️ Corrupted ChromaDB detected. Rebuilding database...")

        if CHROMA_DIR.exists():
            shutil.rmtree(CHROMA_DIR)

        from ingest import ingest
        ingest()

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR)
        )


# ── PROMPT TEMPLATE ───────────────────────────────────────
PROMPT = PromptTemplate(
    template="""
You are an internal assistant for FinSolve Technologies.

Answer ONLY using the context below.
If answer not present → say:
"I don't have access to that information."

Mention sources at the end.

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)


# ── MAIN QUERY FUNCTION ───────────────────────────────────
def generate_answer(query: str, role: str):

    if vector_store is None:
        raise RuntimeError("Vector DB not initialized.")

    # Step 1: get allowed roles
    allowed_roles = get_allowed_roles(role)

    print(f"\nUser role: {role}")
    print(f" Allowed roles: {allowed_roles}")

    # Step 2: check what roles exist in DB
    all_docs = vector_store.get()

    db_roles = set(
        metadata.get("role")
        for metadata in all_docs["metadatas"]
    )

    print(f"Roles inside DB: {db_roles}")

    # Step 3: retrieve docs with RBAC filtering
    results = vector_store.similarity_search(
        query=query,
        k=5,
        filter={"role": {"$in": allowed_roles}}
    )

    print(f" Retrieved {len(results)} docs")

    # Step 4: handle no-results case
    if len(results) == 0:

        print(" RBAC BLOCK: role mismatch or no matching documents")

        return "I don't have access to that information.", []

    # Step 5: build context
    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    # Step 6: collect sources
    sources = list(set(
        doc.metadata.get("source", "unknown")
        for doc in results
    ))

    # Step 7: call LLM
    chain = PROMPT | llm | StrOutputParser()

    answer = chain.invoke({
        "context": context,
        "question": query
    })

    return answer, sources


# ── TEST ENTRY POINT ──────────────────────────────────────
if __name__ == "__main__":

    initialize_components()

    # check roles stored inside DB
    all_docs = vector_store.get()

    print(f"\n Total docs in DB: {len(all_docs['ids'])}")

    roles = set(
        metadata.get("role")
        for metadata in all_docs["metadatas"]
    )

    print(f" Unique roles in ChromaDB: {roles}")

    # test query
    answer, sources = generate_answer(
        query="What is the revenue for Q1 2024?",
        role="finance"
    )

    print("\n Answer:", answer)
    print("Sources:", sources)
