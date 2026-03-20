#!/usr/bin/env python3
"""
Memory wipe utility for Robot4Henry.
Clears all memory stores: SQLite DB, ChromaDB, and optionally raw logs.
"""

import os
import sys
import sqlite3
import shutil
import argparse


def wipe_sqlite(db_path: str):
    if not os.path.exists(db_path):
        print(f"  [skip] {db_path} not found")
        return
    conn = sqlite3.connect(db_path)
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    for (table,) in tables:
        conn.execute(f"DELETE FROM {table}")
    conn.commit()
    conn.close()
    print(f"  [ok] Cleared all tables in {db_path}")


def wipe_chroma(chroma_path: str):
    if not os.path.exists(chroma_path):
        print(f"  [skip] {chroma_path} not found")
        return
    shutil.rmtree(chroma_path)
    os.makedirs(chroma_path)
    print(f"  [ok] Wiped and recreated {chroma_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Wipe Qbot memory stores"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Wipe everything including raw conversation logs"
    )
    parser.add_argument(
        "--facts-only", action="store_true",
        help="Wipe key facts only"
    )
    parser.add_argument(
        "--long-term-only", action="store_true",
        help="Wipe long term ChromaDB only"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be wiped without doing it"
    )
    args = parser.parse_args()

    # Load paths from settings
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from config.settings import DB_PATH, CHROMA_PATH
    except ImportError:
        DB_PATH = "storage/robot.db"
        CHROMA_PATH = "storage/chroma_db"

    print("\nQbot Memory Wipe")
    print("=" * 40)

    if args.dry_run:
        print("[DRY RUN] No changes will be made\n")

    if args.facts_only:
        print("Wiping key facts...")
        if not args.dry_run:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("DELETE FROM key_facts")
            conn.commit()
            conn.close()
            print("  [ok] Key facts cleared")

    elif args.long_term_only:
        print("Wiping long term memory...")
        if not args.dry_run:
            wipe_chroma(CHROMA_PATH)

    else:
        # Default — wipe working memory but preserve raw logs
        print("Wiping working memory (key facts + long term)...")
        if not args.dry_run:
            # Clear key facts
            if os.path.exists(DB_PATH):
                conn = sqlite3.connect(DB_PATH)
                conn.execute("DELETE FROM key_facts")
                conn.execute("DELETE FROM conversation_summary")
                conn.execute("DELETE FROM raw_conversations")
                conn.execute("DELETE FROM sessions") 
                conn.commit()
                conn.close()
                print(f"  [ok] Key facts and summary cleared in {DB_PATH}")

            # Wipe ChromaDB
            wipe_chroma(CHROMA_PATH)

        if args.all:
            print("Wiping raw conversation logs...")
            if not args.dry_run:
                conn = sqlite3.connect(DB_PATH)
                conn.execute("DELETE FROM raw_conversations")
                conn.execute("DELETE FROM sessions")
                conn.commit()
                conn.close()
                print(f"  [ok] Raw logs cleared")

    print("\nDone.")
    if not args.dry_run:
        print("Qbot's memory has been wiped.")
    else:
        print("Dry run complete — nothing was changed.")
    print()


if __name__ == "__main__":
    main()
