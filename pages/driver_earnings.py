import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

PLOT_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a0a8c0", family="DM Sans"),
    xaxis=dict(gridcolor="#1e1e2e", linecolor="#2a2a3a"),
    yaxis=dict(gridcolor="#1e1e2e", linecolor="#2a2a3a"),
)

def get_zone_earnings():
    return pd.DataFrame({
        "Zone": ["EWR (Newark)", "JFK Airport", "LaGuardia", "Midtown Manhattan", "Times Square", "Upper East Side", "Downtown BK", "Astoria QNS"],
        "Effective_$/hr": [648, 412, 387, 298, 276, 241, 198, 176],
        "Avg_Fare": [52.52, 48.30, 31.20, 18.40, 16.80, 22.10, 14.20, 13.80],
        "Avg_Duration_min": [28.4, 42.1, 21.6, 18.2, 14.1, 19.8, 14.4, 14.2],
        "Borough": ["EWR", "Queens", "Queens", "Manhattan", "Manhattan", "Manhattan", "Brooklyn", "Queens"],
    })

def get_trip_type_comparison():
    return pd.DataFrame({
        "Trip Type": ["Airport", "CBD Only", "Rush Hour", "Night (2-4am)", "Non-Airport"],
        "Avg Fare": [52.52, 19.80, 17.40, 15.20, 14.11],
        "Avg Tip %": [18.2, 16.8, 15.9, 14.2, 14.6],
        "Avg Duration (min)": [38.4, 22.1, 28.6, 18.2, 19.8],
    })

def get_hourly_earnings():
    hours = list(range(24))
    # Realistic earnings curve — peaks at AM rush, PM rush, and late night
    earnings = [
        28, 22, 31, 26, 29, 38, 48, 52, 49, 41, 38, 39,
        42, 44, 43, 46, 52, 58, 54, 47, 42, 39, 36, 33
    ]
    return pd.DataFrame({"Hour": hours, "Effective_$/hr": earnings})

def render():
    st.markdown("""
        <div style='margin-bottom:1.5rem;'>
            <h1 style='margin:0;'>🚗 Driver Earnings Analysis</h1>
            <p style='color:#888; margin-top:0.3rem;'>Zone-by-zone breakdown of effective driver earnings per hour</p>
        </div>
    """, unsafe_allow_html=True)

    # Top zones
    col1, col2, col3, col4 = st.columns(4)
    highlights = [
        ("$648/hr", "EWR Best Zone", "#ffd24c"),
        ("$52.52", "Avg Airport Fare", "#7aa0d4"),
        ("$14.11", "Avg Non-Airport Fare", "#d47a7a"),
        ("3.7×", "Airport Fare Premium", "#7ad4a0"),
    ]
    for col, (val, label, color) in zip([col1, col2, col3, col4], highlights):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style='font-size:1.6rem; color:{color};'>{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
            """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆 Top Zones", "✈️ Trip Type Breakdown", "🕐 Best Hours to Drive"])

    with tab1:
        df = get_zone_earnings().sort_values("Effective_$/hr", ascending=False)

        fig = go.Figure()
        colors_map = {
            "EWR": "#ffd24c", "Queens": "#7aa0d4",
            "Manhattan": "#7ad4a0", "Brooklyn": "#d47a7a"
        }
        bar_colors = [colors_map.get(b, "#888") for b in df["Borough"]]

        fig.add_trace(go.Bar(
            x=df["Zone"],
            y=df["Effective_$/hr"],
            marker_color=bar_colors,
            text=[f"${v}/hr" for v in df["Effective_$/hr"]],
            textposition="outside",
            textfont=dict(color="#e0e0f0", size=11),
        ))
        fig.update_layout(
            **PLOT_THEME, height=380,
            yaxis_title="Effective $/hr",
            showlegend=False,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Zone table
        df_display = df[["Zone", "Borough", "Effective_$/hr", "Avg_Fare", "Avg_Duration_min"]].copy()
        df_display.columns = ["Zone", "Borough", "Effective $/hr", "Avg Fare ($)", "Avg Duration (min)"]
        df_display["Effective $/hr"] = df_display["Effective $/hr"].apply(lambda x: f"${x}")
        df_display["Avg Fare ($)"] = df_display["Avg Fare ($)"].apply(lambda x: f"${x:.2f}")
        df_display["Avg Duration (min)"] = df_display["Avg Duration (min)"].apply(lambda x: f"{x:.1f}")
        st.dataframe(df_display.set_index("Zone"), use_container_width=True)

        st.markdown("""
            <div style='background:#1a1a0e; border:1px solid #4a4a1a; border-radius:10px; padding:1rem 1.5rem; font-size:0.85rem; color:#c8c840; margin-top:1rem;'>
                💡 <b>EWR Strategy:</b> Newark Airport trips command the highest effective hourly rate at <b>$648/hr</b>
                because of the high flat fare (~$52) and relatively short wait times at the EWR taxi stand. 
                JFK is second at $412/hr despite higher fares due to longer airport queue times.
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        df = get_trip_type_comparison()

        col_l, col_r = st.columns(2)
        with col_l:
            fig = go.Figure(go.Bar(
                x=df["Trip Type"],
                y=df["Avg Fare"],
                marker_color=["#ffd24c", "#7ad4a0", "#f5a623", "#7aa0d4", "#d47a7a"],
                text=[f"${v:.2f}" for v in df["Avg Fare"]],
                textposition="outside",
                textfont=dict(color="#e0e0f0"),
            ))
            fig.update_layout(**PLOT_THEME, height=320, title="Avg Fare by Trip Type",
                              yaxis_title="$", showlegend=False, margin=dict(t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            fig = go.Figure(go.Bar(
                x=df["Trip Type"],
                y=df["Avg Tip %"],
                marker_color=["#ffd24c", "#7ad4a0", "#f5a623", "#7aa0d4", "#d47a7a"],
                text=[f"{v:.1f}%" for v in df["Avg Tip %"]],
                textposition="outside",
                textfont=dict(color="#e0e0f0"),
            ))
            fig.update_layout(**PLOT_THEME, height=320, title="Avg Tip % by Trip Type",
                              yaxis_title="%", showlegend=False, margin=dict(t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        df = get_hourly_earnings()

        fig = px.area(
            df, x="Hour", y="Effective_$/hr",
            color_discrete_sequence=["#ffd24c"],
            labels={"Hour": "Hour of Day", "Effective_$/hr": "Effective $/hr"},
        )
        fig.update_traces(fillcolor="rgba(255,210,76,0.12)", line_width=2.5)
        fig.update_layout(**PLOT_THEME, height=360, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style='font-size:1.2rem; color:#ffd24c;'>17:00–19:00</div>
                    <div class="metric-label">Peak earnings (PM rush)</div>
                </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style='font-size:1.2rem; color:#7ad4a0;'>07:00–09:00</div>
                    <div class="metric-label">Strong AM rush earnings</div>
                </div>
            """, unsafe_allow_html=True)
        with col_c:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-value" style='font-size:1.2rem; color:#7aa0d4;'>02:00–04:00</div>
                    <div class="metric-label">Night premium (fewer cabs)</div>
                </div>
            """, unsafe_allow_html=True)
