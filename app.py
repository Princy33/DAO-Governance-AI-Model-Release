import streamlit as st
import pandas as pd
import json
import hashlib
from pathlib import Path
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DAO AI Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RESULTS_PATH = (
    BASE_DIR
    / "ai"
    / "data"
    / "anomaly_detection_results.csv"
)

MANIFEST_DIR = BASE_DIR / "manifests"


# ============================================================
# SHA-256 HASHES
# ============================================================

EXPECTED_HASHES = {
    "2.0":
        "98b687886a77f68e3dca2770839344087b7d4847cbfb31176517cf61d53c11bd",

    "3.0":
        "bb8f51225c948c837c5e9bc1087cbc131b121a177b2af3c1889849c990cbccbf"
}


# ============================================================
# PROFESSIONAL VISUAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {

        background-image:
            linear-gradient(
                rgba(2, 12, 30, 0.64),
                rgba(3, 20, 45, 0.70)
            ),
            url(
                "https://images.unsplash.com/photo-1639322537228-f710d846310a?auto=format&fit=crop&w=2400&q=90"
            );

        background-size: cover;

        background-position: center center;

        background-attachment: fixed;

        background-repeat: no-repeat;

        min-height: 100vh;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .main {

        background: transparent !important;
    }


    .block-container {

        max-width: 1450px;

        padding-top: 2rem;

        padding-bottom: 3rem;

        background: transparent !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                rgba(2, 20, 43, 0.95),
                rgba(1, 8, 20, 0.98)
            );

        border-right:
            1px solid
            rgba(60, 190, 255, 0.30);
    }


    section[data-testid="stSidebar"] * {

        color: #EAF6FF;
    }


    /* =====================================================
       HEADINGS
       ===================================================== */

    h1 {

        color: #F4FAFF !important;

        font-weight: 800 !important;

        letter-spacing: -1px;

        text-shadow:
            0 3px 16px
            rgba(0, 0, 0, 0.60);
    }


    h2 {

        color: #EAF6FF !important;

        font-weight: 800 !important;

        text-shadow:
            0 2px 12px
            rgba(0, 0, 0, 0.50);
    }


    h3 {

        color: #DCEEFF !important;

        font-weight: 700 !important;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    [data-testid="metric-container"] {

        background:
            linear-gradient(
                145deg,
                rgba(8, 54, 94, 0.88),
                rgba(3, 27, 54, 0.92)
            );

        border:
            1px solid
            rgba(60, 195, 255, 0.34);

        border-radius: 18px;

        padding: 18px;

        box-shadow:
            0 12px 35px
            rgba(0, 0, 0, 0.30);

        backdrop-filter:
            blur(5px);
    }


    [data-testid="stMetricLabel"] {

        color: #9EBBD5 !important;
    }


    [data-testid="stMetricValue"] {

        color: #F2FAFF !important;

        font-weight: 800 !important;
    }


    /* =====================================================
       BORDERED STREAMLIT CARDS
       ===================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background:
            rgba(4, 28, 55, 0.80);

        border:
            1px solid
            rgba(70, 190, 255, 0.27);

        border-radius: 18px;

        box-shadow:
            0 12px 35px
            rgba(0, 0, 0, 0.26);

        backdrop-filter:
            blur(5px);
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton button {

        background:
            linear-gradient(
                90deg,
                #0878D1,
                #159CE8
            );

        color: white;

        border:
            1px solid
            #35CFFF;

        border-radius: 10px;

        font-weight: 700;
    }


    .stButton button:hover {

        background:
            linear-gradient(
                90deg,
                #0B8EEB,
                #20B4F2
            );

        box-shadow:
            0 0 18px
            rgba(53, 207, 255, 0.35);
    }


    /* =====================================================
       RADIO NAVIGATION
       ===================================================== */

    [role="radiogroup"] label {

        background:
            rgba(8, 42, 75, 0.55);

        border-radius: 10px;

        padding: 8px;

        margin-bottom: 5px;
    }


    [role="radiogroup"] label:hover {

        background:
            rgba(20, 76, 120, 0.70);
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {

        border-radius: 13px;
    }


    /* =====================================================
       TABLES
       ===================================================== */

    [data-testid="stDataFrame"] {

        border-radius: 14px;

        overflow: hidden;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {

        border-color:
            rgba(67, 171, 230, 0.20);
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    [data-testid="stExpander"] {

        background:
            rgba(5, 32, 60, 0.70);

        border:
            1px solid
            rgba(60, 180, 240, 0.22);

        border-radius: 12px;
    }


    /* =====================================================
       CODE BLOCKS
       ===================================================== */

    pre {

        border-radius: 12px !important;

        background:
            rgba(2, 15, 30, 0.90) !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA FUNCTIONS
# ============================================================

def load_results():

    if not RESULTS_PATH.exists():
        return pd.DataFrame()

    try:

        return pd.read_csv(
            RESULTS_PATH
        )

    except Exception:

        return pd.DataFrame()


def get_manifest_path(version):

    if version == "2.0":

        return MANIFEST_DIR / "manifest_v2.json"

    if version == "3.0":

        return MANIFEST_DIR / "manifest_v3.json"

    return None


def load_manifest(version):

    path = get_manifest_path(
        version
    )

    if path is None or not path.exists():

        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def calculate_hash(version):

    path = get_manifest_path(
        version
    )

    if path is None or not path.exists():

        return ""

    try:

        with open(
            path,
            "rb"
        ) as file:

            return hashlib.sha256(
                file.read()
            ).hexdigest()

    except Exception:

        return ""


results = load_results()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ DAO AI")

    st.subheader(
        "Governance Platform"
    )

    st.caption(
        "AI Model Release"
    )

    st.divider()

    page = st.radio(
        "PLATFORM NAVIGATION",
        [
            "🏠 Dashboard",
            "🤖 AI Evaluation",
            "📦 Model Manifests",
            "🗳️ DAO Governance",
            "🛡️ Security Tests",
            "⚙️ System Architecture"
        ]
    )

    st.divider()

    st.success(
        "● SYSTEM OPERATIONAL"
    )

    st.caption(
        "Project A9"
    )

    st.caption(
        "DAO Governance for AI Model Release"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "🛡️ DAO Governance for AI Model Release"
)

st.caption(
    "Decentralized AI governance combining "
    "off-chain model evaluation, cryptographic "
    "manifests and on-chain DAO voting."
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header(
        "📊 Governance Dashboard"
    )

    st.caption(
        "AI evaluation, model integrity and DAO governance overview."
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🗄️ Dataset Records",
            "200",
            "Synthetic"
        )

    with c2:

        st.metric(
            "⚠️ Anomalies",
            "5",
            "Injected"
        )

    with c3:

        st.metric(
            "👥 DAO Members",
            "5",
            "Registered"
        )

    with c4:

        st.metric(
            "🎯 Quorum",
            "3",
            "Required Votes"
        )

    st.divider()

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader(
        "🚀 AI Model Release Pipeline"
    )

    p1, p2, p3, p4, p5 = st.columns(5)

    with p1:

        st.info(
            "🤖 **AI Evaluation**\n\n"
            "Off-chain anomaly detection"
        )

    with p2:

        st.info(
            "📄 **Model Manifest**\n\n"
            "JSON evidence"
        )

    with p3:

        st.info(
            "🔐 **SHA-256**\n\n"
            "Integrity verification"
        )

    with p4:

        st.info(
            "⛓️ **DAO Voting**\n\n"
            "On-chain governance"
        )

    with p5:

        st.success(
            "🚀 **Model Release**\n\n"
            "Governance authorization"
        )

    st.divider()

    # --------------------------------------------------------
    # VOTING GRAPH
    # --------------------------------------------------------

    chart_col, status_col = st.columns(
        [1.7, 1]
    )

    with chart_col:

        st.subheader(
            "📊 Voting Distribution"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[
                    "Proposal 1",
                    "Proposal 3"
                ],

                y=[
                    4,
                    2
                ],

                name="YES",

                marker=dict(
                    color="#42B5FF",

                    line=dict(
                        color="#8CDEFF",
                        width=1
                    )
                ),

                hovertemplate=
                    "<b>%{x}</b><br>"
                    "YES Votes: %{y}"
                    "<extra></extra>"
            )
        )

        fig.add_trace(
            go.Bar(
                x=[
                    "Proposal 1",
                    "Proposal 3"
                ],

                y=[
                    1,
                    0
                ],

                name="NO",

                marker=dict(
                    color="#FF5F78",

                    line=dict(
                        color="#FF9AAA",
                        width=1
                    )
                ),

                hovertemplate=
                    "<b>%{x}</b><br>"
                    "NO Votes: %{y}"
                    "<extra></extra>"
            )
        )

        fig.update_layout(

            barmode="stack",

            height=430,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                family="Arial",
                color="#DCEEFF",
                size=13
            ),

            margin=dict(
                l=55,
                r=30,
                t=45,
                b=55
            ),

            legend=dict(
                orientation="h",

                yanchor="bottom",

                y=1.02,

                xanchor="right",

                x=1
            ),

            xaxis=dict(
                title="Proposal",

                color="#B8D0E8",

                showgrid=False
            ),

            yaxis=dict(
                title="Number of Votes",

                color="#B8D0E8",

                range=[
                    0,
                    5.5
                ],

                dtick=1,

                gridcolor=
                    "rgba(100,170,230,0.13)"
            ),

            hoverlabel=dict(
                bgcolor="#071B35",

                bordercolor="#35D5FF",

                font=dict(
                    color="white"
                )
            )
        )

        st.plotly_chart(
            fig,

            use_container_width=True,

            config={
                "displayModeBar": False,
                "responsive": True
            }
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    with status_col:

        st.subheader(
            "🗳️ Proposal Status"
        )

        st.success(
            "🟢 Proposal #1 — Model v2.0"
        )

        st.write(
            "**Votes:** 4 YES / 1 NO"
        )

        st.success(
            "✓ Quorum reached"
        )

        st.success(
            "✓ Proposal succeeded"
        )

        st.success(
            "✓ Proposal executed"
        )

        st.divider()

        st.error(
            "🔴 Proposal #3 — Model v3.1"
        )

        st.write(
            "**Votes:** 2 YES / 0 NO"
        )

        st.warning(
            "⚠ Quorum not reached"
        )

        st.error(
            "✕ Proposal defeated"
        )

    st.divider()

    # --------------------------------------------------------
    # GOVERNANCE TABLE
    # --------------------------------------------------------

    st.subheader(
        "📋 Governance Outcomes"
    )

    proposal_df = pd.DataFrame(
        {
            "Proposal": [
                "#1",
                "#3"
            ],

            "Model": [
                "v2.0",
                "v3.1"
            ],

            "YES": [
                4,
                2
            ],

            "NO": [
                1,
                0
            ],

            "Total Votes": [
                5,
                2
            ],

            "Quorum": [
                "✓ Reached",
                "✕ Not Reached"
            ],

            "Final State": [
                "Executed",
                "Defeated"
            ]
        }
    )

    st.dataframe(
        proposal_df,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# AI EVALUATION
# ============================================================

elif page == "🤖 AI Evaluation":

    st.header(
        "🤖 AI Model Evaluation"
    )

    st.caption(
        "Off-chain anomaly detection component."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🎯 Accuracy",
            "100%"
        )

    with c2:

        st.metric(
            "🔎 Precision",
            "100%"
        )

    with c3:

        st.metric(
            "📈 Recall",
            "100%"
        )

    with c4:

        st.metric(
            "⚡ F1 Score",
            "100%"
        )

    st.divider()

    left, right = st.columns(
        [1.6, 1]
    )

    with left:

        st.subheader(
            "📈 Anomaly Detection Results"
        )

        if not results.empty:

            if "anomaly_score" in results.columns:

                fig = go.Figure()

                if "is_anomaly" in results.columns:

                    if "record_id" in results.columns:

                        normal = results[
                            results["is_anomaly"] == 0
                        ]

                        anomalies = results[
                            results["is_anomaly"] == 1
                        ]

                        fig.add_trace(
                            go.Scatter(
                                x=normal[
                                    "record_id"
                                ],

                                y=normal[
                                    "anomaly_score"
                                ],

                                mode="markers",

                                name="Normal",

                                marker=dict(
                                    color="#42B5FF",
                                    size=7
                                )
                            )
                        )

                        fig.add_trace(
                            go.Scatter(
                                x=anomalies[
                                    "record_id"
                                ],

                                y=anomalies[
                                    "anomaly_score"
                                ],

                                mode="markers",

                                name="Anomaly",

                                marker=dict(
                                    color="#FF5F78",
                                    size=11,

                                    symbol="diamond"
                                )
                            )
                        )

                    else:

                        st.info(
                            "Record ID column not available."
                        )

                else:

                    x_values = (
                        results["record_id"]
                        if "record_id"
                        in results.columns
                        else results.index
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=x_values,

                            y=results[
                                "anomaly_score"
                            ],

                            mode="markers",

                            name="Anomaly Score",

                            marker=dict(
                                color="#42B5FF",
                                size=7
                            )
                        )
                    )

                fig.update_layout(

                    height=420,

                    paper_bgcolor=
                        "rgba(0,0,0,0)",

                    plot_bgcolor=
                        "rgba(0,0,0,0)",

                    font=dict(
                        color="#DCEEFF"
                    ),

                    xaxis=dict(
                        title="Record ID",

                        showgrid=False,

                        color="#B8D0E8"
                    ),

                    yaxis=dict(
                        title="Anomaly Score",

                        color="#B8D0E8",

                        gridcolor=
                            "rgba(100,170,230,0.12)"
                    ),

                    legend=dict(
                        font=dict(
                            color="#DCEEFF"
                        )
                    )
                )

                st.plotly_chart(
                    fig,

                    use_container_width=True,

                    config={
                        "displayModeBar": False
                    }
                )

            else:

                st.warning(
                    "Anomaly score column not found."
                )

        else:

            st.warning(
                "AI result file not found."
            )

    with right:

        st.subheader(
            "⚙️ Model Configuration"
        )

        st.info(
            "**Algorithm**\n\n"
            "Isolation Forest"
        )

        st.info(
            "**Estimators**\n\n"
            "200"
        )

        st.info(
            "**Contamination**\n\n"
            "2.5%"
        )

        st.info(
            "**Preprocessing**\n\n"
            "StandardScaler"
        )

        st.info(
            "**Random State**\n\n"
            "42"
        )

        st.success(
            "✓ 5 / 5 anomalies detected"
        )

    st.divider()

    st.subheader(
        "🧪 Experimental Evidence"
    )

    e1, e2, e3 = st.columns(3)

    with e1:

        st.metric(
            "Records",
            "200"
        )

    with e2:

        st.metric(
            "Injected Anomalies",
            "5"
        )

    with e3:

        st.metric(
            "Detected",
            "5"
        )


# ============================================================
# MODEL MANIFESTS
# ============================================================

elif page == "📦 Model Manifests":

    st.header(
        "📦 Model Manifest Registry"
    )

    st.caption(
        "Cryptographic integrity verification using SHA-256."
    )

    col1, col2 = st.columns(2)

    for col, version in [
        (col1, "2.0"),
        (col2, "3.0")
    ]:

        with col:

            manifest = load_manifest(
                version
            )

            actual_hash = calculate_hash(
                version
            )

            expected_hash = (
                EXPECTED_HASHES[
                    version
                ]
            )

            verified = (
                actual_hash != ""
                and
                actual_hash.lower()
                ==
                expected_hash.lower()
            )

            if verified:

                st.success(
                    f"✓ MODEL v{version} — SHA-256 VERIFIED"
                )

            else:

                st.error(
                    f"✕ MODEL v{version} — HASH MISMATCH"
                )

            st.subheader(
                f"🤖 AI Model v{version}"
            )

            filename = (
                "manifest_v2.json"
                if version == "2.0"
                else "manifest_v3.json"
            )

            st.caption(
                "Manifest file"
            )

            st.code(
                filename
            )

            st.markdown(
                "**SHA-256 Digest**"
            )

            if actual_hash:

                st.code(
                    actual_hash
                )

            else:

                st.warning(
                    "Manifest file not found."
                )

            with st.expander(
                "📄 View Complete Manifest JSON"
            ):

                if manifest:

                    st.json(
                        manifest
                    )

                else:

                    st.error(
                        "Manifest JSON could not be loaded."
                    )

    st.divider()

    st.info(
        "🔐 SHA-256 verifies the integrity of the manifest "
        "bytes. It does not independently prove that the "
        "underlying AI measurements are truthful."
    )


# ============================================================
# DAO GOVERNANCE
# ============================================================

elif page == "🗳️ DAO Governance":

    st.header(
        "🗳️ DAO Governance"
    )

    st.caption(
        "Solidity-based AI release governance on a local Ethereum-compatible chain."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "👥 DAO Members",
            "5"
        )

    with c2:

        st.metric(
            "🎯 Quorum",
            "3"
        )

    with c3:

        st.metric(
            "⏱️ Voting Window",
            "120 sec"
        )

    with c4:

        st.metric(
            "⚖️ Acceptance",
            "YES > NO"
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🔄 Proposal Lifecycle"
        )

        st.info(
            "🟢 Active"
        )

        st.info(
            "⬇️ Finalize"
        )

        st.info(
            "🔵 Succeeded / 🔴 Defeated"
        )

        st.info(
            "⬇️ Queue"
        )

        st.success(
            "🚀 Execute"
        )

    with right:

        st.subheader(
            "⚖️ Governance Rules"
        )

        st.write(
            "✓ Registered members only"
        )

        st.write(
            "✓ One vote per member"
        )

        st.write(
            "✓ Quorum = 3"
        )

        st.write(
            "✓ YES must exceed NO"
        )

        st.write(
            "✓ Tie = defeated"
        )

        st.write(
            "✓ Voting must close before finalization"
        )

        st.write(
            "✓ Successful proposals require queue before execution"
        )

        st.write(
            "✓ Duplicate proposals are rejected"
        )

    st.divider()

    st.subheader(
        "📊 Recorded Proposal Results"
    )

    dao_results = pd.DataFrame(
        {
            "Proposal": [
                1,
                3
            ],

            "Model": [
                "v2.0",
                "v3.1"
            ],

            "YES": [
                4,
                2
            ],

            "NO": [
                1,
                0
            ],

            "Total": [
                5,
                2
            ],

            "Quorum": [
                "Reached",
                "Not Reached"
            ],

            "State": [
                "Executed",
                "Defeated"
            ]
        }
    )

    st.dataframe(
        dao_results,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# SECURITY TESTS
# ============================================================

elif page == "🛡️ Security Tests":

    st.header(
        "🛡️ Security & Negative Tests"
    )

    st.caption(
        "Smart-contract validation and rejection tests."
    )

    security_df = pd.DataFrame(
        {
            "Test Case": [

                "Duplicate Vote",

                "Unregistered Voter",

                "Late Vote",

                "Early Finalization",

                "Duplicate Proposal"
            ],

            "Observed Result": [

                "Member has already voted",

                "Only registered members can vote",

                "Voting has ended",

                "Voting is still active",

                "Duplicate proposal"
            ],

            "Status": [

                "PASS",

                "PASS",

                "PASS",

                "PASS",

                "PASS"
            ]
        }
    )

    st.dataframe(
        security_df,

        use_container_width=True,

        hide_index=True
    )

    st.divider()

    a, b, c, d, e = st.columns(5)

    with a:

        st.success(
            "✓ Duplicate Vote"
        )

    with b:

        st.success(
            "✓ Unregistered"
        )

    with c:

        st.success(
            "✓ Late Vote"
        )

    with d:

        st.success(
            "✓ Early Finalize"
        )

    with e:

        st.success(
            "✓ Duplicate Proposal"
        )


# ============================================================
# SYSTEM ARCHITECTURE
# ============================================================

elif page == "⚙️ System Architecture":

    st.header(
        "⚙️ System Architecture"
    )

    st.caption(
        "Separation between AI computation and blockchain governance."
    )

    a, b, c, d, e = st.columns(5)

    with a:

        st.info(
            "🧠 **AI Module**\n\n"
            "Off-chain anomaly detection"
        )

    with b:

        st.info(
            "📄 **Model Manifest**\n\n"
            "JSON evidence"
        )

    with c:

        st.info(
            "🔐 **SHA-256**\n\n"
            "Integrity commitment"
        )

    with d:

        st.info(
            "⛓️ **DAO Contract**\n\n"
            "On-chain governance"
        )

    with e:

        st.success(
            "👥 **DAO Members**\n\n"
            "Voting and authorization"
        )

    st.divider()

    st.subheader(
        "👤 Actor & Permission Matrix"
    )

    permissions = pd.DataFrame(
        {
            "Action": [

                "Register Member",

                "Remove Member",

                "Create Proposal",

                "Vote",

                "Finalize",

                "Queue",

                "Execute",

                "Cancel / Pause"
            ],

            "Admin": [

                "✓",

                "✓",

                "✓",

                "—",

                "—",

                "✓",

                "✓",

                "✓"
            ],

            "Registered Member": [

                "—",

                "—",

                "—",

                "✓",

                "—",

                "—",

                "—",

                "—"
            ],

            "Unregistered Account": [

                "—",

                "—",

                "—",

                "✕",

                "—",

                "—",

                "—",

                "—"
            ]
        }
    )

    st.dataframe(
        permissions,

        use_container_width=True,

        hide_index=True
    )

    st.divider()

    st.subheader(
        "🔐 Security & Privacy"
    )

    st.info(
        "AI computation is performed off-chain. "
        "The blockchain stores governance information "
        "and the model-manifest digest rather than "
        "sensitive raw AI data."
    )

    st.warning(
        "SHA-256 provides integrity verification for "
        "the manifest bytes but does not independently "
        "authenticate the truth of the underlying AI evidence."
    )

    st.info(
        "Membership should remain fixed while an active "
        "ballot is running."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🛡️ DAO Governance for AI Model Release  •  "
    "Project A9  •  AI + Blockchain Governance"
)