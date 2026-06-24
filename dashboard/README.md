# PoisonedRAG – Attack & Defense Visualizer

Interactive security dashboard demonstrating knowledge corruption attacks on Retrieval-Augmented Generation (RAG) systems, based on the [PoisonedRAG paper](https://arxiv.org/abs/2402.07867) (USENIX Security 2025).

![Dashboard Preview](https://img.shields.io/badge/Stack-FastAPI%20%2B%20Next.js-00d4ff)

## Features

- **RAG Pipeline Visualization** — Animated SVG showing how malicious text P = S ⊕ I flows through retrieval
- **Attack Decomposition** — Split view of retrieval condition (S) and generation condition (I)
- **Metrics Dashboard** — ASR gauge, F1/Precision/Recall bars, ASR vs N trend chart
- **Baseline Comparison** — Grouped bar chart: Naive, Prompt Injection, Disinformation, Corpus Poisoning, GCG vs PoisonedRAG
- **Defense Simulation** — Toggle paraphrasing, perplexity detection, deduplication, knowledge expansion
- **Case Studies** — Real attack examples from the paper with failure mode analysis

## Project Structure

```
poisonedrag-dashboard/
├── backend/          # FastAPI API (attack, baseline, defense, stats)
├── frontend/         # Next.js 14 dashboard UI
├── scripts/          # setup_env.py, seed_cache.py
└── docker-compose.yml
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 20+
- The PoisonedRAG repo cloned at the parent directory (already present if you're in this monorepo)

### 1. Setup Environment

```bash
cd poisonedrag-dashboard
python scripts/setup_env.py --skip-datasets
```

For full dataset download (optional, ~several GB):

```bash
python scripts/setup_env.py
```

### 2. Seed Cache (instant load)

```bash
python scripts/seed_cache.py
```

This pre-populates SQLite with paper metric values and real adversarial text examples.

### 3. Start Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:3000

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/attack` | Run PoisonedRAG attack |
| POST | `/api/v1/baseline` | Run baseline attack comparison |
| POST | `/api/v1/defense` | Simulate defense against attack |
| GET | `/api/v1/stats` | Dataset statistics |
| GET | `/api/v1/baseline/all` | All baseline ASR values |
| GET | `/api/v1/asr-sweep` | ASR vs N sweep data |

### Example Attack Request

```bash
curl -X POST http://localhost:8000/api/v1/attack \
  -H "Content-Type: application/json" \
  -d '{
    "dataset": "nq",
    "attack_type": "blackbox",
    "n": 5,
    "k": 5,
    "llm": "palm2"
  }'
```

## Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Live Attack Mode (Optional)

By default the dashboard uses paper metrics and cached adversarial examples (no GPU/API keys required). To run live LLM attacks:

1. Configure API keys in `model_configs/` (see PoisonedRAG README)
2. Set `POISONEDRAG_LIVE=1` and ensure CUDA is available
3. Restart the backend

## Metric Sources

Static fallback values come from PoisonedRAG paper Tables 1, 4, and 12–13:

- **NQ + PaLM 2**: ASR 97%, F1 0.96
- **Defenses**: Paraphrasing → ~87% ASR, Perplexity → ~75% ASR
- **Baselines**: Naive ~18%, GCG ~58%, PoisonedRAG ~97%

## Citation

```bibtex
@inproceedings{zou2025poisonedrag,
  title={PoisonedRAG: Knowledge corruption attacks to Retrieval-Augmented Generation of Large Language Models},
  author={Zou, Wei and Geng, Runpeng and Wang, Binghui and Jia, Jinyuan},
  booktitle={34th USENIX Security Symposium (USENIX Security 25)},
  pages={3827--3844},
  year={2025}
}
```

## License

This dashboard wraps the [PoisonedRAG](https://github.com/sleeepeer/PoisonedRAG) codebase. See the parent repository LICENSE.
