from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AttackParams(BaseModel):
    dataset: str = Field(..., description="nq, hotpotqa, or msmarco")
    attack_type: str = Field(..., description="blackbox or whitebox")
    n: int = Field(5, ge=1, le=10)
    k: int = Field(5, ge=1, le=50)
    llm: str = Field("palm2", description="palm2, gpt4, llama2, vicuna")
    defense: Optional[str] = None
    target_questions: Optional[List[str]] = None


class BaselineParams(BaseModel):
    dataset: str
    baseline_type: str = Field(
        ..., description="naive, prompt_injection, disinformation, corpus, gcg"
    )
    n: int = 5
    k: int = 5
    llm: str = "palm2"


class DefenseParams(BaseModel):
    dataset: str
    attack_type: str = "blackbox"
    defense: str = Field(..., description="paraphrase, perplexity, dedup, expansion")
    n: int = 5
    k: int = 5
    llm: str = "palm2"
    expansion_k: Optional[int] = None


class MetricsData(BaseModel):
    asr: float
    f1_score: float
    precision: float
    recall: float
    queries_avg: float
    runtime_avg: float


class AttackExample(BaseModel):
    target_question: str
    correct_answer: str
    target_answer: str
    malicious_text: str
    retrieval_part: str = ""
    generation_part: str = ""
    failure_mode: Optional[str] = None


class AttackResponse(BaseModel):
    metrics: MetricsData
    examples: List[AttackExample]
    decomposition: Optional[Dict[str, Any]] = None


class BaselineResponse(BaseModel):
    baseline_type: str
    metrics: MetricsData


class DefenseResponse(BaseModel):
    defense: str
    metrics: MetricsData
    baseline_asr: float
    asr_reduction: float


class DatasetStats(BaseModel):
    texts: int
    questions: int


class StatsResponse(BaseModel):
    nq: DatasetStats
    hotpotqa: DatasetStats
    msmarco: DatasetStats
