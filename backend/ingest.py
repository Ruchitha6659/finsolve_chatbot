import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# ── PATH CONFIGURATION ────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
CHROMA_DIR = BASE_DIR.parent / "chroma_db"


# ── FOLDER METADATA ───────────────────────────────────────
FOLDER_METADATA = {
    "finance": {
        "role": "finance",
        "owner": "Finance Team",
        "sensitivity": "high",
        "update_freq": "quarterly"
    },
    "hr": {
        "role": "hr",
        "owner": "HR & People Analytics",
        "sensitivity": "high",
        "update_freq": "monthly"
    },
    "marketing": {
        "role": "marketing",
        "owner": "Marketing Team",
        "sensitivity": "medium",
        "update_freq": "quarterly"
    },
    "engineering": {
        "role": "engineering",
        "owner": "Engineering Team",
        "sensitivity": "high",
        "update_freq": "quarterly"
    },
    "general": {
        "role": "general",  # 🔴 FIXED (was "employee")
        "owner": "Human Resources",
        "sensitivity": "low",
        "update_freq": "annually"
    },
}


# ── FILE LOADER FUNCTION ──────────────────────────────────
def load_file(filepath):

    ext = filepath.split(".")[-1].lower()

    try:

        if ext == "pdf":
            return PyPDFLoader(filepath).load()

        elif ext == "csv":
            return CSVLoader(filepath).load()

        elif ext in ["xls", "xlsx"]:
            return UnstructuredExcelLoader(filepath).load()

        elif ext in ["txt", "md"]:   # ✅ added markdown support
            return TextLoader(filepath, encoding="utf-8").load()

        else:
            print(f"Skipping unsupported file: {filepath}")
            return []

    except Exception as e:
        print(f"Skipping corrupted file {filepath}: {e}")
        return []
    except Exception as e:

        print(f"Skipping corrupted file {filepath}: {e}")
        return []


# ── INGESTION PIPELINE ────────────────────────────────────
def ingest():

    all_docs = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    print("\n🚀 Starting ingestion...")
    print(f"Reading data from: {DATA_DIR}\n")

    for folder, metadata in FOLDER_METADATA.items():

        folder_path = DATA_DIR / folder

        if not folder_path.exists():

            print(f"⚠️ Folder missing: {folder_path}")
            continue

        print(f"📂 Processing department: {folder}")

        for filename in os.listdir(folder_path):

            filepath = folder_path / filename

            docs = load_file(str(filepath))

            if not docs:
                continue

            chunks = splitter.split_documents(docs)

            for chunk in chunks:

                chunk.metadata["role"] = metadata["role"]
                chunk.metadata["owner"] = metadata["owner"]
                chunk.metadata["sensitivity"] = metadata["sensitivity"]
                chunk.metadata["update_freq"] = metadata["update_freq"]
                chunk.metadata["source"] = filename

            all_docs.extend(chunks)

            print(f"   ✅ {len(chunks)} chunks added from {filename}")

    if len(all_docs) == 0:

        print("\n❌ No documents ingested. Check your data folder.")
        return

    print(f"\n📊 Total chunks prepared: {len(all_docs)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="finsolve"
    )

    print("\n✅ Ingestion complete. ChromaDB ready.")


# ── ENTRY POINT ───────────────────────────────────────────
if __name__ == "__main__":

    ingest()