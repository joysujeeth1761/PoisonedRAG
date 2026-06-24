#!/usr/bin/env python3
"""Pre-run default experiments and cache results in SQLite for instant dashboard loading."""

import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from core.attack_engine import run_attack_simulation
from core.cache_db import set_cached
from core.defense_simulator import run_baseline, run_defense, get_all_baselines
from core.metric_calculator import asr_sweep, get_paper_metrics

DATASETS = ["nq", "hotpotqa", "msmarco"]
LLMS = ["palm2", "gpt4", "llama2", "vicuna"]
ATTACK_TYPES = ["blackbox", "whitebox"]
DEFENSES = ["paraphrase", "perplexity", "dedup", "expansion"]
BASELINES = ["naive", "prompt_injection", "disinformation", "corpus", "gcg", "poisonedrag"]


def seed_attacks():
    count = 0
    for dataset in DATASETS:
        for llm in LLMS:
            for attack_type in ATTACK_TYPES:
                for n in [5]:
                    for k in [5]:
                        params = {
                            "dataset": dataset,
                            "attack_type": attack_type,
                            "n": n,
                            "k": k,
                            "llm": llm,
                            "defense": None,
                            "target_questions": None,
                        }
                        result = run_attack_simulation(dataset, attack_type, n, k, llm)
                        set_cached("attack", params, {
                            "metrics": result["metrics"],
                            "examples": result["examples"],
                            "decomposition": result.get("decomposition"),
                        })
                        count += 1
    return count


def seed_baselines():
    count = 0
    for dataset in DATASETS:
        for baseline in BASELINES:
            params = {"dataset": dataset, "baseline_type": baseline, "n": 5, "k": 5, "llm": "palm2"}
            result = run_baseline(dataset, baseline, 5, 5, "palm2")
            set_cached("baseline", params, {
                "baseline_type": result["baseline_type"],
                "metrics": result["metrics"],
            })
            count += 1
        all_b = get_all_baselines(dataset, "palm2", 5, 5)
        set_cached("baseline_all", {"dataset": dataset, "llm": "palm2", "n": 5, "k": 5}, all_b)
    return count


def seed_defenses():
    count = 0
    for dataset in DATASETS:
        for defense in DEFENSES:
            params = {
                "dataset": dataset,
                "attack_type": "blackbox",
                "defense": defense,
                "n": 5,
                "k": 5,
                "llm": "palm2",
                "expansion_k": 20 if defense == "expansion" else None,
            }
            result = run_defense(dataset, "blackbox", defense, 5, 5, "palm2", params["expansion_k"])
            set_cached("defense", params, {
                "defense": result["defense"],
                "metrics": result["metrics"],
                "baseline_asr": result["baseline_asr"],
                "asr_reduction": result["asr_reduction"],
            })
            count += 1
    return count


def seed_asr_sweeps():
    for dataset in DATASETS:
        base = get_paper_metrics(dataset, "palm2", "blackbox")["asr"]
        sweep = {"sweep": asr_sweep(list(range(1, 11)), base)}
        set_cached("asr_sweep", {"dataset": dataset, "llm": "palm2", "attack_type": "blackbox"}, sweep)


def main():
    print("Seeding SQLite cache with paper-based experiment data...")
    a = seed_attacks()
    b = seed_baselines()
    d = seed_defenses()
    seed_asr_sweeps()
    print(f"  Cached {a} attack configs, {b} baselines, {d} defense configs")
    print(f"  Database: {BACKEND_DIR / 'data' / 'cache.db'}")
    print("Done!")


if __name__ == "__main__":
    main()
