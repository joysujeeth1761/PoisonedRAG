# RAG Attack Visualizer (PoisonedRAG Fork)

RAG Attack Visualizer (rebranded from the original `PoisonedRAG` package) is an interactive, full-stack security dashboard designed to demonstrate and visualize knowledge corruption attacks on Retrieval-Augmented Generation (RAG) systems. It is built upon the USENIX Security 2025 paper: [PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models](https://arxiv.org/abs/2402.07867).

This repository has been enhanced with:
- A clean, package-ready `src/` layout under the module name `rag_simulator` (rebranded as `rag-attack-visualizer`).
- A unified Python wrapper (`AttackEngine`) abstracting attack logic (with automated simulations and live execution modes).
- A full-stack web dashboard (FastAPI backend + Next.js frontend) to visualize the attack flow, inspect query decomposition ($P = S \oplus I$), and run interactive defense scenarios.

---

## 🚀 Quick Start & Installation

### 1. Setup Environment
First, create and activate a Python 3.10 environment:
```bash
conda create -n PoisonedRAG python=3.10
conda activate PoisonedRAG
```

Install core dependencies (including backend/dashboard dependencies):
```bash
pip install -e .
pip install fastapi uvicorn pydantic python-multipart
```

### 2. Download BEIR Datasets (Optional)
If you wish to run live/real-time attacks instead of simulated paper results:
```bash
python prepare_dataset.py
```

### 3. Run the Dashboard

#### Start the FastAPI Backend:
```bash
cd dashboard/backend
python -m uvicorn main:app --reload --port 8000
```
API Documentation is available at https://ragispoisoned.streamlit.app.

#### Start the Next.js Frontend:
Ensure you have Node.js 18+ installed:
```bash
cd dashboard/frontend
npm install
npm run dev
```
Open [https://ragispoisoned.streamlit.app](https://ragispoisoned.streamlit.app) in your browser to view the interactive dashboard.

---

## 🛠️ Package Layout & Wrapper API

The core simulation code has been reorganized into the `rag_simulator` module:
- `rag_simulator.engine.AttackEngine`: Main wrapper class to invoke attacks.
- `rag_simulator.attack`: Attack algorithms (hotflip, LM_targeted).
- `rag_simulator.models`: Large Language Model wrappers.

### Python API Example:
```python
from rag_simulator import AttackEngine

engine = AttackEngine()

# Run simulated metrics using paper benchmarks
sim_results = engine.run_simulation(
    dataset="nq",
    attack_type="blackbox",
    n=5,
    k=5,
    llm="palm2"
)
print("ASR Mean:", sim_results["metrics"]["asr"])
```



## Citation

If you use this work, please cite the original authors' paper:

```bib
@inproceedings{zou2025poisonedrag,
  title={$\{$PoisonedRAG$\}$: Knowledge corruption attacks to $\{$Retrieval-Augmented$\}$ generation of large language models},
  author={Zou, Wei and Geng, Runpeng Geng and Wang, Binghui and Jia, Jinyuan},
  booktitle={34th USENIX Security Symposium (USENIX Security 25)},
  pages={3827--3844},
  year={2025}
}
```
