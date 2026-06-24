#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = REPO_ROOT / "src"
RAG_SIMULATOR_DIR = SRC_DIR / "rag_simulator"

def move_files():
    print("Moving files to rag_simulator...")
    RAG_SIMULATOR_DIR.mkdir(parents=True, exist_ok=True)
    
    # Items to move from src/ to src/rag_simulator/
    items_to_move = ["attack.py", "prompts.py", "utils.py", "models", "contriever_src"]
    
    for item in items_to_move:
        src_path = SRC_DIR / item
        dest_path = RAG_SIMULATOR_DIR / item
        if src_path.exists():
            print(f"Moving {src_path} -> {dest_path}")
            if dest_path.exists():
                if dest_path.is_dir():
                    shutil.rmtree(dest_path)
                else:
                    dest_path.unlink()
            shutil.move(src_path, dest_path)
        else:
            print(f"Warning: {src_path} does not exist.")

    # Create __init__.py in rag_simulator
    init_file = RAG_SIMULATOR_DIR / "__init__.py"
    if not init_file.exists():
        init_file.write_text('"""PoisonedRAG Core Attack Engine Simulator Module"""\n')
        print(f"Created {init_file}")

def update_imports():
    print("Updating import statements...")
    
    # Define replacement pairs
    replacements = {
        "from src.models": "from rag_simulator.models",
        "from src.utils": "from rag_simulator.utils",
        "from src.attack": "from rag_simulator.attack",
        "from src.prompts": "from rag_simulator.prompts",
        "from src.contriever_src": "from rag_simulator.contriever_src",
        "from .contriever_src": "from rag_simulator.contriever_src",
    }
    
    # Find all Python files under REPO_ROOT
    py_files = []
    
    # Root python files
    for f in REPO_ROOT.glob("*.py"):
        if f.name != "refactor_repo.py":
            py_files.append(f)
            
    # Files in src/rag_simulator
    for f in RAG_SIMULATOR_DIR.rglob("*.py"):
        py_files.append(f)
        
    for py_file in py_files:
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Could not read {py_file}: {e}")
            continue
            
        modified = False
        new_lines = []
        for line in content.splitlines():
            updated_line = line
            for old_imp, new_imp in replacements.items():
                if old_imp in updated_line:
                    updated_line = updated_line.replace(old_imp, new_imp)
            if updated_line != line:
                modified = True
            new_lines.append(updated_line)
            
        if modified:
            print(f"Updating imports in {py_file.relative_to(REPO_ROOT)}")
            py_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    move_files()
    update_imports()
    print("Refactoring complete!")
