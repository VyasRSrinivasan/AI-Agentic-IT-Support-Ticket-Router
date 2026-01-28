# scripts/seedKB.py

from pathlib import Path

from rag.indexKB import build_kb_index


def main():
    kb_dir = Path("data") / "kb"

    print(f"[seed_kb] Indexing knowledge base from: {kb_dir}")
    count = build_kb_index(kb_dir=kb_dir)

    print(f"[seed_kb] Done. Indexed {count} chunks.")


if __name__ == "__main__":
    main()