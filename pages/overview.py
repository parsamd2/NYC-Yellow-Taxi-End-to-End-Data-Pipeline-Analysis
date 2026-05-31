import streamlit as st

def render():
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">NYC TLC Fare Intelligence</div>
            <div class="hero-subtitle">End-to-end medallion pipeline · 151M trips · 2022–2026</div>
            <div style="margin-top: 1rem;">
                <span class="tag">Databricks</span>
                <span class="tag">Spark 4.1</span>
                <span class="tag">XGBoost</span>
                <span class="tag">R² 0.9659</span>
                <span class="tag">Medallion Architecture</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">151M</div>
                <div class="metric-label">Trips Processed</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">96.6%</div>
                <div class="metric-label">XGBoost R²</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">39.21%</div>
                <div class="metric-label">Avg Congestion Share</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">$1.68</div>
                <div class="metric-label">Congestion Pricing Impact</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### Pipeline Architecture")
        st.markdown("""
            <div style='background:#16161f; border:1px solid #2a2a3a; border-radius:12px; padding:1.5rem;'>
                <div style='display:flex; align-items:center; gap:1rem; margin-bottom:1rem;'>
                    <div style='background:#1e2a3a; border:1px solid #3a4a6a; border-radius:8px; padding:0.6rem 1rem; font-family:Space Mono,monospace; font-size:0.8rem; color:#7aa0d4;'>🟤 BRONZE</div>
                    <div style='color:#444;'>→</div>
                    <div style='font-size:0.8rem; color:#888;'>182M rows · 52 parquet files · Raw ingest</div>
                </div>
                <div style='display:flex; align-items:center; gap:1rem; margin-bottom:1rem;'>
                    <div style='background:#1e2a3a; border:1px solid #3a4a6a; border-radius:8px; padding:0.6rem 1rem; font-family:Space Mono,monospace; font-size:0.8rem; color:#c0c0e0;'>⚪ SILVER</div>
                    <div style='color:#444;'>→</div>
                    <div style='font-size:0.8rem; color:#888;'>151M rows · Cleaned & validated · Nulls removed</div>
                </div>
                <div style='display:flex; align-items:center; gap:1rem;'>
                    <div style='background:#2a2a1a; border:1px solid #5a5a2a; border-radius:8px; padding:0.6rem 1rem; font-family:Space Mono,monospace; font-size:0.8rem; color:#ffd24c;'>🟡 GOLD</div>
                    <div style='color:#444;'>→</div>
                    <div style='font-size:0.8rem; color:#888;'>45 features · Engineered · Model-ready</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Findings")
        findings = [
            ("14.48M hours", "lost to congestion across all trips"),
            ("35.57% → 42.29%", "congestion share worsening 2022–2026"),
            ("$52.52 vs $14.11", "airport vs non-airport average fare"),
            ("10.13 → 9.38 mph", "CBD speed decline (selection effect)"),
            ("$648/hr", "EWR best effective driver earnings zone"),
        ]
        for val, desc in findings:
            st.markdown(f"""
                <div style='display:flex; gap:1rem; align-items:flex-start; padding:0.6rem 0; border-bottom:1px solid #1a1a2a;'>
                    <div style='font-family:Space Mono,monospace; font-size:0.85rem; color:#ffd24c; min-width:140px;'>{val}</div>
                    <div style='font-size:0.85rem; color:#888;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### Model Comparison")
        models = [
            ("XGBoost", 0.9659, 2.93, 0.82, "#ffd24c"),
            ("Neural Network", 0.9555, 3.35, 0.83, "#7aa0d4"),
            ("Random Forest", 0.9581, 3.25, 1.15, "#7ad4a0"),
            ("Linear Regression", 0.9183, 4.54, 2.29, "#d47a7a"),
        ]
        for name, r2, rmse, mae, color in models:
            bar_width = int(r2 * 100)
            st.markdown(f"""
                <div style='background:#16161f; border:1px solid #2a2a3a; border-radius:10px; padding:1rem 1.2rem; margin-bottom:0.6rem;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
                        <span style='font-family:Space Mono,monospace; font-size:0.85rem; color:{color};'>{name}</span>
                        <span style='font-family:Space Mono,monospace; font-size:0.85rem; color:#fff;'>R² {r2}</span>
                    </div>
                    <div style='background:#1a1a2a; border-radius:4px; height:6px;'>
                        <div style='background:{color}; width:{bar_width}%; height:6px; border-radius:4px;'></div>
                    </div>
                    <div style='display:flex; gap:1.5rem; margin-top:0.5rem;'>
                        <span style='font-size:0.75rem; color:#666;'>RMSE ${rmse}</span>
                        <span style='font-size:0.75rem; color:#666;'>MAE ${mae}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("### Gold Layer Features")
        feature_groups = {
            "Trip Metrics": ["trip_duration_mins", "avg_speed_mph", "distance_ratio"],
            "Congestion": ["is_post_congestion", "congestion_share", "is_cbd_pickup"],
            "Trip Type": ["is_airport_trip", "is_rush_hour", "is_cbd_dropoff"],
            "Temporal": ["hour_sin/cos", "dow_sin/cos", "pickup_year/month"],
            "Route": ["route_mean_fare", "borough_zones"],
        }
        for group, features in feature_groups.items():
            st.markdown(f"""
                <div style='margin-bottom:0.5rem;'>
                    <span style='font-size:0.75rem; color:#666; text-transform:uppercase; letter-spacing:0.1em;'>{group}</span><br>
                    {''.join([f'<span class="tag">{f}</span>' for f in features])}
                </div>
            """, unsafe_allow_html=True)
