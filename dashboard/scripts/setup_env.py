#!/usr/bin/env python3
"""Setup script: clone PoisonedRAG repo, create env, install deps, download datasets."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

DASHBOARD_ROOT = Path(__file__).resolve().parent.parent
POISONEDRAG_ROOT = DASHBOARD_ROOT.parent
REPO_URL = "https://github.com/sleeepeer/PoisonedRAG.git"


def run_cmd(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"  $ {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd or POISONEDRAG_ROOT)


def clone_repo(target: Path) -> None:
    if (target / "main.py").exists():
        print(f"PoisonedRAG already present at {target}")
        return
    print(f"Cloning PoisonedRAG to {target}...")
    run_cmd(["git", "clone", REPO_URL, str(target)], cwd=target.parent)


def install_backend_deps() -> None:
    print("Installing dashboard backend dependencies...")
    run_cmd([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=DASHBOARD_ROOT / "backend")


def install_poisonedrag_deps() -> None:
    print("Installing PoisonedRAG dependencies (minimal for dashboard)...")
    deps = ["beir", "openai", "google-generativeai", "transformers", "sentence-transformers", "tqdm", "numpy"]
    run_cmd([sys.executable, "-m", "pip", "install"] + deps)


def download_datasets() -> None:
    prepare_script = POISONEDRAG_ROOT / "prepare_dataset.py"
    if prepare_script.exists():
        print("Downloading BEIR datasets (NQ, HotpotQA, MS-MARCO)...")
        run_cmd([sys.executable, str(prepare_script)])
    else:
        print("prepare_dataset.py not found — skipping dataset download")


def main():
    parser = argparse.ArgumentParser(description="Setup PoisonedRAG Dashboard environment")
    parser.add_argument("--clone", action="store_true", help="Clone PoisonedRAG repo if missing")
    parser.add_argument("--skip-datasets", action="store_true", help="Skip dataset download")
    args = parser.parse_args()

    print("=" * 60)
    print("PoisonedRAG Dashboard — Environment Setup")
    print("=" * 60)

    if args.clone:
        clone_repo(POISONEDRAG_ROOT)

    install_backend_deps()
    install_poisonedrag_deps()

    if not args.skip_datasets:
        download_datasets()

    print("\nSetup complete!")
    print("\nNext steps:")
    print("  1. python scripts/seed_cache.py")
    print("  2. cd backend && uvicorn main:app --reload --port 8000")
    print("  3. cd frontend && npm install && npm run dev")


if __name__ == "__main__":
    main()
