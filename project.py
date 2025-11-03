import streamlit as st
import pandas as pd
import altair as alt

try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
except ImportError:
    get_script_run_ctx = None


def _is_streamlit_runtime():
    running_flag = getattr(st, "_is_running_with_streamlit", None)
    if callable(running_flag):
        try:
            if running_flag():
                return True
        except RuntimeError:
            return False
    if get_script_run_ctx is None:
        return False
    try:
        return get_script_run_ctx() is not None
    except RuntimeError:
        return False


class LinearCongruentialGenerator:
    def __init__(self, modulus, multiplier, increment, seed):  # fixed constructor
        if modulus <= 0:
            raise ValueError("Modulus must be positive")
        self.modulus = modulus
        self.multiplier = multiplier % modulus
        self.increment = increment % modulus
        self.state = seed % modulus

    def reseed(self, seed):
        self.state = seed % self.modulus

    def next_int(self):
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state

    def next_float(self):
        return self.next_int() / self.modulus


def main():
    if not _is_streamlit_runtime():
        print("Run this app with 'streamlit run project.py'")
        return

    st.set_page_config(page_title="Random Number Generator Studio", layout="wide")

    # ✅ FIXED: safer and more visible styling
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #000 !important;
        }
        .block-container {
            padding: 2.5rem 3rem 3rem;
            border-radius: 1.5rem;
            background-color: rgba(255, 255, 255, 0.97) !important;
            box-shadow: 0 32px 64px rgba(0, 0, 0, 0.15);
        }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2d1b69 0%, #11998e 100%);
            color: #f8fafc;
        }
        div[data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        .sidebar-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #ffffff;
        }
        .sidebar-subtitle {
            font-size: 1rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }
        .status-chip {
            margin-top: 1.5rem;
            padding: 1rem 1.5rem;
            border-radius: 50px;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            font-weight: 700;
            text-align: center;
            letter-spacing: 0.05em;
            color: #333;
            box-shadow: 0 8px 16px rgba(255, 154, 158, 0.3);
        }
        .hero {
            padding: 2rem 2.5rem;
            border-radius: 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            margin-bottom: 2.5rem;
            box-shadow: 0 16px 32px rgba(102, 126, 234, 0.3);
        }
        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 500;
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #2d1b69;
        }
        .metric-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 1rem;
            padding: 1.5rem;
            text-align: center;
            color: white;
            box-shadow: 0 12px 24px rgba(245, 87, 108, 0.3);
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # session setup
    if "generator" not in st.session_state:
        st.session_state.generator = None
    if "sequence" not in st.session_state:
        st.session_state.sequence = []
    if "status" not in st.session_state:
        st.session_state.status = "Awaiting configuration"
    if "params_snapshot" not in st.session_state:
        st.session_state.params_snapshot = None
    if "seed_snapshot" not in st.session_state:
        st.session_state.seed_snapshot = None

    # sidebar controls
    with st.sidebar:
        st.markdown("<div class='sidebar-title'>Generator Controls</div>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-subtitle'>Adjust parameters to craft your sequence.</div>", unsafe_allow_html=True)
        modulus = int(st.number_input("Modulus", value=2 ** 31, min_value=1, step=1, format="%d"))
        multiplier = int(st.number_input("Multiplier", value=1103515245, step=1, format="%d"))
        increment = int(st.number_input("Increment", value=12345, step=1, format="%d"))
        seed = int(st.number_input("Seed", value=42, step=1, format="%d"))
        count = int(st.slider("Sequence Length", min_value=1, max_value=500, value=50, step=1))
        st.markdown("---")
        config_col, generate_col = st.columns(2)
        configure_clicked = config_col.button("Apply Settings", use_container_width=True)
        generate_clicked = generate_col.button("Generate", use_container_width=True)
        next_clicked = st.button("Next Value", use_container_width=True)
        clear_clicked = st.button("Reset Output", use_container_width=True)

    def snapshots_match():
        return (
            st.session_state.params_snapshot == (modulus, multiplier, increment)
            and st.session_state.seed_snapshot == seed
        )

    def refresh_generator():
        generator = LinearCongruentialGenerator(modulus, multiplier, increment, seed)
        st.session_state.generator = generator
        st.session_state.params_snapshot = (modulus, multiplier, increment)
        st.session_state.seed_snapshot = seed
        return generator

    def populate_sequence(length):
        generator = refresh_generator()
        generator.reseed(seed)
        st.session_state.sequence = []
        for index in range(length):
            integer = generator.next_int()
            normalized = integer / generator.modulus
            st.session_state.sequence.append({"Index": index + 1, "Integer": integer, "Normalized": normalized})
        st.session_state.status = f"Generated {length} values"
        return generator

    # main logic
    if st.session_state.generator is None:
        refresh_generator()

    if not st.session_state.sequence and st.session_state.status == "Awaiting configuration":
        populate_sequence(count)

    if configure_clicked:
        refresh_generator()
        st.session_state.generator.reseed(seed)
        st.session_state.sequence = []
        st.session_state.status = "Generator ready"
        st.sidebar.success("Settings applied")

    if generate_clicked:
        populate_sequence(count)
        st.sidebar.success("Sequence refreshed")

    if next_clicked:
        if not snapshots_match():
            refresh_generator()
            st.session_state.sequence = []
        generator = st.session_state.generator or refresh_generator()
        if not st.session_state.sequence:
            generator.reseed(seed)
        integer = generator.next_int()
        normalized = integer / generator.modulus
        st.session_state.sequence.append({"Index": len(st.session_state.sequence) + 1, "Integer": integer, "Normalized": normalized})
        st.session_state.status = "Generated next value"
        st.sidebar.info("Appended one value")

    if clear_clicked:
        if not snapshots_match():
            refresh_generator()
        generator = st.session_state.generator or refresh_generator()
        generator.reseed(seed)
        st.session_state.sequence = []
        st.session_state.status = "Output cleared"
        st.sidebar.warning("Outputs cleared")

    st.sidebar.markdown(f"<div class='status-chip'>{st.session_state.status}</div>", unsafe_allow_html=True)

    # main UI
    st.markdown(
        """
        <div class='hero'>
            <div class='hero-title'>Linear Congruential Playground</div>
            <div class='hero-subtitle'>Visualize pseudo-random sequences and adjust parameters in real time.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    raw_values = st.session_state.sequence
    if raw_values:
        df = pd.DataFrame(raw_values)
        stats = df["Normalized"]
        std = stats.std(ddof=0) if not pd.isna(stats.std(ddof=0)) else 0
        spread = stats.max() - stats.min()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Count", len(df))
        col2.metric("Mean", f"{stats.mean():.5f}")
        col3.metric("Std Dev", f"{std:.5f}")
        col4.metric("Span", f"{spread:.5f}")

        st.markdown("### Sequence Visualization")
        chart = alt.Chart(df).mark_area(
            line={"color": "#667eea", "strokeWidth": 3},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="#f093fb", offset=0),
                    alt.GradientStop(color="#f5576c", offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0
            ),
            opacity=0.85,
        ).encode(
            x=alt.X("Index:Q", title="Step"),
            y=alt.Y("Normalized:Q", title="Normalized Value", scale=alt.Scale(domain=[0, 1])),
            tooltip=["Index", "Integer", alt.Tooltip("Normalized", format=".6f")]
        ).properties(height=340)
        st.altair_chart(chart.interactive(), use_container_width=True)

        st.markdown("### Sequence Details")
        df["Normalized"] = df["Normalized"].map(lambda x: f"{x:.10f}")
        st.dataframe(df, use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "lcg_sequence.csv", "text/csv")


if __name__ == "__main__":  # fixed main entry
    main()
