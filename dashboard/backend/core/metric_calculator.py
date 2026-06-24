from typing import Dict, List

from .paper_data import ASR_VS_N, PAPER_METRICS


def interpolate_asr_for_n(base_asr: float, n: int) -> float:
    """Scale ASR based on N using paper's diminishing-returns curve."""
    reference = ASR_VS_N.get(5, 0.97)
    target = ASR_VS_N.get(n, reference)
    if reference == 0:
        return base_asr
    return min(0.999, round(base_asr * (target / reference), 3))


def scale_metrics_for_k(metrics: Dict[str, float], k: int, default_k: int = 5) -> Dict[str, float]:
    """Adjust retrieval metrics when k changes."""
    if k == default_k:
        return metrics
    factor = min(1.0, default_k / max(k, 1))
    scaled = dict(metrics)
    scaled["precision"] = round(metrics["precision"] * factor, 3)
    scaled["recall"] = round(min(1.0, metrics["recall"] * (k / default_k)), 3)
    scaled["f1_score"] = round(
        2 * scaled["precision"] * scaled["recall"] / max(scaled["precision"] + scaled["recall"], 1e-9),
        3,
    )
    return scaled


def get_paper_metrics(dataset: str, llm: str, attack_type: str, n: int = 5, k: int = 5) -> Dict[str, float]:
    base = PAPER_METRICS.get(dataset, PAPER_METRICS["nq"]).get(llm, PAPER_METRICS["nq"]["palm2"]).get(
        attack_type, PAPER_METRICS["nq"]["palm2"]["blackbox"]
    )
    metrics = dict(base)
    metrics["asr"] = interpolate_asr_for_n(metrics["asr"], n)
    metrics = scale_metrics_for_k(metrics, k)
    return metrics


def asr_sweep(n_values: List[int], base_asr: float = 0.97) -> List[Dict[str, float]]:
    return [{"n": n, "asr": interpolate_asr_for_n(base_asr, n)} for n in n_values]
