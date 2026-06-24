import asyncio
from typing import Any, Dict

from fastapi import APIRouter

from api.models import (
    AttackParams,
    AttackResponse,
    BaselineParams,
    BaselineResponse,
    DefenseParams,
    DefenseResponse,
    StatsResponse,
    DatasetStats,
    MetricsData,
    AttackExample,
)
from rag_simulator import AttackEngine
from core.cache_db import get_cached, set_cached
from core.defense_simulator import run_baseline, run_defense, get_all_baselines
from core.metric_calculator import asr_sweep, get_paper_metrics
from core.paper_data import DATASET_STATS

router = APIRouter(prefix="/api/v1")


def _to_metrics(data: Dict[str, float]) -> MetricsData:
    return MetricsData(
        asr=data["asr"],
        f1_score=data["f1_score"],
        precision=data["precision"],
        recall=data["recall"],
        queries_avg=data["queries_avg"],
        runtime_avg=data["runtime_avg"],
    )


@router.post("/attack", response_model=AttackResponse)
async def run_attack(params: AttackParams):
    cache_params = params.model_dump()
    cached = get_cached("attack", cache_params)
    if cached:
        return cached

    await asyncio.sleep(0.8)

    engine = AttackEngine()
    live = await asyncio.to_thread(
        engine.run_live,
        params.dataset,
        params.attack_type,
        params.n,
        params.k,
        params.llm,
        params.target_questions,
    )
    result = live or engine.run_simulation(
        params.dataset,
        params.attack_type,
        params.n,
        params.k,
        params.llm,
        params.target_questions,
    )

    response = AttackResponse(
        metrics=_to_metrics(result["metrics"]),
        examples=[AttackExample(**e) for e in result["examples"]],
        decomposition=result.get("decomposition"),
    )
    payload = response.model_dump()
    set_cached("attack", cache_params, payload)
    return payload


@router.post("/baseline", response_model=BaselineResponse)
async def run_baseline_endpoint(params: BaselineParams):
    cache_params = params.model_dump()
    cached = get_cached("baseline", cache_params)
    if cached:
        return cached

    await asyncio.sleep(0.5)
    result = run_baseline(params.dataset, params.baseline_type, params.n, params.k, params.llm)
    response = BaselineResponse(
        baseline_type=result["baseline_type"],
        metrics=_to_metrics(result["metrics"]),
    )
    payload = response.model_dump()
    set_cached("baseline", cache_params, payload)
    return payload


@router.get("/baseline/all")
async def get_all_baselines_endpoint(dataset: str = "nq", llm: str = "palm2", n: int = 5, k: int = 5):
    return get_all_baselines(dataset, llm, n, k)


@router.post("/defense", response_model=DefenseResponse)
async def run_defense_endpoint(params: DefenseParams):
    cache_params = params.model_dump()
    cached = get_cached("defense", cache_params)
    if cached:
        return cached

    await asyncio.sleep(0.5)
    result = run_defense(
        params.dataset,
        params.attack_type,
        params.defense,
        params.n,
        params.k,
        params.llm,
        params.expansion_k,
    )
    response = DefenseResponse(
        defense=result["defense"],
        metrics=_to_metrics(result["metrics"]),
        baseline_asr=result["baseline_asr"],
        asr_reduction=result["asr_reduction"],
    )
    payload = response.model_dump()
    set_cached("defense", cache_params, payload)
    return payload


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    return StatsResponse(
        nq=DatasetStats(**DATASET_STATS["nq"]),
        hotpotqa=DatasetStats(**DATASET_STATS["hotpotqa"]),
        msmarco=DatasetStats(**DATASET_STATS["msmarco"]),
    )


@router.get("/asr-sweep")
async def get_asr_sweep(dataset: str = "nq", llm: str = "palm2", attack_type: str = "blackbox"):
    base = get_paper_metrics(dataset, llm, attack_type)["asr"]
    return {"sweep": asr_sweep(list(range(1, 11)), base)}
