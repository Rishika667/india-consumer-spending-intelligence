"""
ConsumerLens India — Reusable UI Components and Styling
Institutional, editorial styling for Streamlit with responsive layout helpers.
"""

import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    /* Global Container Adjustments */
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }
    
    /* Institutional Metric Card */
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .metric-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-subtitle {
        font-size: 0.82rem;
        color: #059669;
        font-weight: 500;
        margin-top: 0.35rem;
    }
    
    /* Editorial Callout Pill */
    .editorial-badge {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        margin-bottom: 0.5rem;
    }
    
    /* Quality Score Banner */
    .qc-badge-pass {
        background-color: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Warning & Methodology Box */
    .methodology-alert {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.85rem 1.1rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 1.25rem;
        color: #92400e;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1e293b;
        margin-top: 1.25rem;
        margin-bottom: 0.4rem;
    }
    .section-subtitle {
        font-size: 0.92rem;
        color: #64748b;
        margin-bottom: 1.25rem;
        line-height: 1.45;
    }

    /* Analytical Research Brief Card */
    .insight-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1e3a8a;
        border-radius: 6px;
        padding: 1.2rem 1.35rem;
        margin-bottom: 1.15rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }
    .insight-header {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-bottom: 0.65rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .insight-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: #0f172a;
    }
    .insight-tag {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background-color: #f1f5f9;
        color: #475569;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
    }
    .insight-body {
        font-size: 0.91rem;
        color: #334155;
        line-height: 1.6;
    }
    .insight-body p {
        margin-bottom: 0.65rem;
    }
    .insight-dim-label {
        font-weight: 600;
        color: #1e3a8a;
    }
    .insight-lim-label {
        font-weight: 600;
        color: #b45309;
    }
    </style>
    """, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, delta: str = "", delta_color: str = "#059669"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-subtitle" style="color: {delta_color};">{delta}</div>
    </div>
    """, unsafe_allow_html=True)


def render_disclaimer_banner(title: str, text: str):
    st.markdown(f"""
    <div class="methodology-alert">
        <strong>⚠️ {title}:</strong> {text}
    </div>
    """, unsafe_allow_html=True)


def render_insight_card(
    title: str,
    tag: str,
    finding_text: str,
    implication_text: str,
    limitation_text: str,
    border_color: str = "#1e3a8a"
):
    """
    Renders an editorial syndicated research brief card with natural narrative paragraphs:
    1. Finding & measured movement
    2. Analytical & commercial implication
    3. Methodological boundary & caveat
    """
    st.markdown(f"""
    <div class="insight-card" style="border-left-color: {border_color};">
        <div class="insight-header">
            <span class="insight-title">{title}</span>
            <span class="insight-tag">{tag}</span>
        </div>
        <div class="insight-body">
            <p>{finding_text}</p>
            <p><strong><span class="insight-dim-label">Analytical & Market Implications:</span></strong> {implication_text}</p>
            <p style="margin-bottom: 0;"><strong><span class="insight-lim-label">Methodological Boundary:</span></strong> {limitation_text}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
