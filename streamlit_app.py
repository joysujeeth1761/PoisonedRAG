import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure src/ is on system path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "src"))

try:
    from rag_simulator import AttackEngine
except ImportError:
    # Fallback to local import if src is not initialized
    sys.path.insert(0, str(ROOT_DIR))
    from src.rag_simulator import AttackEngine

# -------------------------------------------------------------
# Configuration & Theme Setup
# -------------------------------------------------------------
st.set_page_config(
    page_title="RAG Attack Visualizer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Glassmorphism & Sleek Dark theme elements)
st.markdown(
    """
    <style>
    .main {
        background-color: #0f111a;
        color: #ffffff;
    }
    .stApp {
        background: linear-gradient(135deg, #0f111a 0%, #151824 100%);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 5px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8b9bb4;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Engine
engine = AttackEngine(repo_root=ROOT_DIR)

# -------------------------------------------------------------
# Sidebar Controls
# -------------------------------------------------------------
st.sidebar.image("https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge", use_container_width=False)
st.sidebar.title("🛡️ Controls Panel")

st.sidebar.markdown("### 📊 Experiment Settings")
dataset = st.sidebar.selectbox("BEIR Dataset", ["nq", "hotpotqa", "msmarco"], format_func=lambda x: x.upper())
llm_model = st.sidebar.selectbox("LLM Target", ["palm2", "gpt4", "llama2", "vicuna"], format_func=lambda x: {
    "palm2": "PaLM 2", "gpt4": "GPT-4", "llama2": "LLaMA-2 7B", "vicuna": "Vicuna 7B"
}.get(x, x))
attack_type = st.sidebar.selectbox("Attack Strategy", ["blackbox", "whitebox"], format_func=lambda x: {
    "blackbox": "Black-Box (LM-targeted)", "whitebox": "White-Box (HotFlip)"
}.get(x, x))

n_value = st.sidebar.slider("N (Adv Texts per Query)", 1, 10, 5)
k_value = st.sidebar.slider("K (Top-K Retrieval Limit)", 1, 20, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛡️ Defenses Enabled")
paraphrase_def = st.sidebar.checkbox("Paraphrasing Defense", value=False, help="Reduces ASR by ~10%")
perplexity_def = st.sidebar.checkbox("Perplexity Detection", value=False, help="Filters out highly anomalous text snippets")
dedup_def = st.sidebar.checkbox("Duplicate Filtering", value=False, help="Deduplicates corpus entries")
expansion_def = st.sidebar.checkbox("Knowledge Expansion", value=False, help="Increases K to dilute poison texts")

expansion_k = 20
if expansion_def:
    expansion_k = st.sidebar.slider("Expansion Limit (Effective K)", 10, 50, 20)

# Run Simulation
sim_data = engine.run_simulation(dataset, attack_type, n_value, k_value, llm_model)
base_metrics = sim_data["metrics"]

# Apply defenses dynamically
defended_metrics = dict(base_metrics)
defense_descriptions = []

if paraphrase_def:
    defended_metrics["asr"] = round(defended_metrics["asr"] * 0.897, 3)
    defense_descriptions.append("Paraphrasing Active (-10% ASR)")
if perplexity_def:
    defended_metrics["asr"] = round(defended_metrics["asr"] * 0.75, 3)
    defense_descriptions.append("Perplexity Filter Active (-25% ASR)")
if dedup_def:
    defended_metrics["asr"] = round(defended_metrics["asr"] * 0.98, 3)
    defense_descriptions.append("Deduplication Active (-2% ASR)")
if expansion_def:
    reduction = min(0.5, (expansion_k - k_value) * 0.015)
    defended_metrics["asr"] = max(0.1, round(defended_metrics["asr"] - reduction, 3))
    defense_descriptions.append(f"Knowledge Expansion Active (K={expansion_k})")

# Ensure bounds
defended_metrics["asr"] = max(0.0, min(1.0, defended_metrics["asr"]))
asr_reduction = round(base_metrics["asr"] - defended_metrics["asr"], 3)

# Update F1/Precision/Recall based on ASR updates
if defended_metrics["asr"] < base_metrics["asr"]:
    ratio = defended_metrics["asr"] / max(base_metrics["asr"], 1e-9)
    defended_metrics["f1_score"] = round(defended_metrics["f1_score"] * ratio, 3)
    defended_metrics["precision"] = round(defended_metrics["precision"] * ratio, 3)

# -------------------------------------------------------------
# Main Visualizer Header
# -------------------------------------------------------------
st.title("🛡️ RAG Attack & Defense Visualizer")
st.markdown(
    """
    **Interactive demonstration of knowledge database corruption attacks on Retrieval-Augmented Generation (RAG) systems.**
    
    *This dashboard showcases the vulnerability of LLM-based QA systems to adversarial insertions.*
    """
)

# Attribution Alert
st.info(
    "💡 **Acknowledgements**: This codebase is built upon the research and core implementation of **'PoisonedRAG'** "
    "by Wei Zou, Runpeng Geng, Binghui Wang, and Jinyuan Jia (Penn State & IIT)."
)

st.markdown("---")

# -------------------------------------------------------------
# Layout Tabs
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Metrics & Sweeps", "🔄 RAG Flow Visualization", "📖 Case Studies"])

with tab1:
    st.header("📈 Attack Performance & Metrics")
    
    # Large Metrics Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{defended_metrics['asr'] * 100:.1f}%</div>
                <div class="metric-label">Attack Success Rate (ASR)</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{defended_metrics['f1_score']:.3f}</div>
                <div class="metric-label">Retrieval F1 Score</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{defended_metrics['precision']:.3f}</div>
                <div class="metric-label">Retrieval Precision</div>
            </div>
            """, unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{asr_reduction * 100:.1f}%</div>
                <div class="metric-label">ASR Reduction (Defense Effect)</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("### 📊 Baseline Comparison")
    
    # Baseline comparison data
    baselines = {
        "nq": {"Naive": 0.18, "Prompt Injection": 0.32, "Disinformation": 0.41, "Corpus Poisoning": 0.52, "GCG": 0.58, "PoisonedRAG": base_metrics["asr"]},
        "hotpotqa": {"Naive": 0.15, "Prompt Injection": 0.28, "Disinformation": 0.38, "Corpus Poisoning": 0.48, "GCG": 0.54, "PoisonedRAG": base_metrics["asr"]},
        "msmarco": {"Naive": 0.12, "Prompt Injection": 0.25, "Disinformation": 0.35, "Corpus Poisoning": 0.45, "GCG": 0.50, "PoisonedRAG": base_metrics["asr"]},
    }
    
    current_baselines = baselines.get(dataset, baselines["nq"])
    baseline_df = pd.DataFrame({
        "Attack Type": list(current_baselines.keys()),
        "Attack Success Rate (ASR)": list(current_baselines.values())
    })
    
    fig_bar = px.bar(
        baseline_df,
        x="Attack Type",
        y="Attack Success Rate (ASR)",
        color="Attack Type",
        title=f"Attack Success Rate vs Alternative Baselines (Dataset: {dataset.upper()})",
        labels={"Attack Success Rate (ASR)": "ASR (Ratio)"},
        color_discrete_sequence=px.colors.sequential.Teal_r
    )
    fig_bar.update_layout(showlegend=False, template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ASR vs N Sweep Chart
    st.markdown("### 📈 ASR Trend over N (Number of inserted adversarial texts)")
    
    n_sweep = list(range(1, 11))
    sweep_asr = [engine._interpolate_asr_for_n(base_metrics["asr"], n) for n in n_sweep]
    
    sweep_df = pd.DataFrame({
        "Number of Ads (N)": n_sweep,
        "ASR": sweep_asr
    })
    
    fig_line = px.line(
        sweep_df,
        x="Number of Ads (N)",
        y="ASR",
        title="ASR Diminishing Returns Curve (ASR vs N)",
        markers=True,
        color_discrete_sequence=["#00d4ff"]
    )
    fig_line.update_layout(template="plotly_dark")
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.header("🔄 RAG Pipeline Flow & Visualization")
    st.markdown("This section details how PoisonedRAG constructs the attack context.")
    
    st.subheader("Structure of Malicious Text Insertion")
    st.latex(r"P = S \oplus I")
    
    st.markdown(
        """
        - **Retrieval Condition ($S$)**: Standard text snippet (usually identical to the target query) designed to rank highly during semantic embedding matching.
        - **Generation Condition ($I$)**: authoritative-sounding, factually-incorrect context designed to bias the generator LLM into generating the target incorrect answer.
        """
    )
    
    # Mermaid diagram replacement via styled visual block
    st.markdown(
        """
        <div style="background: rgba(255, 255, 255, 0.02); padding: 30px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); text-align: center;">
            <span style="font-size: 1.2rem; font-weight: bold; color: #ff007f;">1. Malicious Document Generation</span>
            <br>
            <code style="background: #1e1e2e; color: #abe9b3; padding: 5px 10px; border-radius: 4px; display: inline-block; margin-top: 10px;">
                P = [Target Query] + [Synthesized Incorrect Context]
            </code>
            <div style="margin: 15px 0; color: #8b9bb4;">↓ inserted into Database</div>
            <span style="font-size: 1.2rem; font-weight: bold; color: #00d4ff;">2. Knowledge Database Retrieval</span>
            <br>
            <span style="color: #8b9bb4; font-size: 0.9rem;">The embedding model ranks the document highly because it matches the query's vector projection.</span>
            <div style="margin: 15px 0; color: #8b9bb4;">↓ Top-K contexts retrieved</div>
            <span style="font-size: 1.2rem; font-weight: bold; color: #f8bd96;">3. LLM Generation Biasing</span>
            <br>
            <span style="color: #8b9bb4; font-size: 0.9rem;">The generator LLM integrates the injected context and answers with the targeted incorrect answer.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab3:
    st.header("📖 Case Studies & Decomposition")
    
    examples = sim_data["examples"]
    for i, ex in enumerate(examples):
        with st.expander(f"Case Study {i+1}: {ex['target_question']}"):
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown(f"**🎯 Target Question:** `{ex['target_question']}`")
                st.markdown(f"**✅ Correct Answer:** `<span style='color: #4e9a06;'>{ex['correct_answer']}</span>`", unsafe_allow_html=True)
                st.markdown(f"**❌ Target Incorrect Answer:** `<span style='color: #cc0000;'>{ex['target_answer']}</span>`", unsafe_allow_html=True)
                st.markdown(f"**⚠️ Failure Mode:** `{ex['failure_mode'] or 'Attack Succeeded'}`")
            
            with col_r:
                st.markdown("**🛡️ Adversarial Context Decomposition:**")
                st.markdown(
                    f"""
                    <div style="border: 1px solid rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; font-family: monospace; background: #1e1e2e;">
                        <span style="background: rgba(0,212,255,0.2); padding: 2px 4px; border-radius: 3px; border: 1px solid #00d4ff;">{ex['retrieval_part']}</span>
                        <span style="background: rgba(255,0,127,0.2); padding: 2px 4px; border-radius: 3px; border: 1px solid #ff007f;">{ex['generation_part']}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.8rem; color: #8b9bb4;">
                        <span style="color: #00d4ff;">■</span> Retrieval Condition (S) | <span style="color: #ff007f;">■</span> Generation Condition (I)
                    </div>
                    """,
                    unsafe_allow_html=True
                )
