import streamlit as st
import plotly.express as px
from utils.data_loader import load_student_data,validate_columns
from utils.metrics import get_metric
from utils.charts import (
    department_distribution,
    average_cgpa_by_department,
    placement_distribution
)

# Page configuration
st.set_page_config(
    page_title="Voyage | Travel Management",
    page_icon=":airplane:",
    layout="wide"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap');

    :root {
        --navy: #102a43;
        --blue: #1677ff;
        --sky: #eaf4ff;
        --ink: #203040;
        --muted: #6d7f90;
        --line: #d9e5ef;
        --white: #ffffff;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5faff 0%, #ffffff 45%, #eef8f6 100%);
    }

    [data-testid="stHeader"] { background: transparent; }

    .brand-mark {
        color: var(--navy);
        font-family: 'Manrope', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.25rem;
    }

    .brand-mark span { color: var(--blue); }

    .login-card {
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid var(--line);
        border-radius: 18px;
        box-shadow: 0 18px 50px rgba(16, 42, 67, 0.1);
        margin: 6vh auto 0;
        max-width: 680px;
        padding: 2.5rem;
    }

    .login-eyebrow {
        color: var(--blue);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .login-title {
        color: var(--navy);
        font-family: 'Manrope', sans-serif;
        font-size: 2.4rem;
        line-height: 1.1;
        margin: 0.55rem 0 0.75rem;
    }

    .login-copy { color: var(--muted); font-size: 1rem; }
    .stButton > button[kind="primary"] {
        background: var(--blue);
        border: 0;
        border-radius: 9px;
        color: var(--white);
        font-weight: 700;
        min-height: 2.8rem;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--navy);
        border: 0;
        color: var(--white);
    }
    </style>
    """,
    unsafe_allow_html=True
)


def show_login_page():
    """Render and validate the travel management login form."""
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="brand-mark">voyage<span>.</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-eyebrow">Travel operations platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Welcome back, traveler.</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="login-copy">Sign in to coordinate itineraries, bookings, and guest journeys from one calm workspace.</p>',
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign in", type="primary", use_container_width=True)

    if submitted:
        valid_users = {
            "travel.admin": "Travel@123",
            "demo": "demo123"
        }
        if not username.strip() or not password:
            st.error("Enter both your username and password to continue.")
        elif valid_users.get(username.strip()) != password:
            st.error("That username or password is not valid. Please try again.")
        else:
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.just_logged_in = True
            st.rerun()

    st.caption("Demo access: travel.admin / Travel@123")
    st.markdown('</div>', unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Application Title
st.title("Voyage Travel Management")

if st.session_state.just_logged_in:
    st.success(f"Login successful. Welcome, {st.session_state.username}.")
    st.session_state.just_logged_in = False

st.sidebar.success(f"Signed in as {st.session_state.username}")
if st.sidebar.button("Sign out", type="secondary", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.just_logged_in = False
    st.rerun()

st.write("""
    Welcome to your travel operations workspace.

    Coordinate guest journeys, review performance, and keep every booking moving.
""")

st.sidebar.header("Dashboard Controls")

st.sidebar.info(""" 
Filters and controls will appear here"""
)

# Main sections

st.header("Student Data Overview")

st.info("""
Student dataset will be loaded here"""
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Student CSV File",
    type=["csv"]
)

if uploaded_file is not None:
    df_student = load_student_data(uploaded_file)
    st.sidebar.success(
        "Using uploaded dataset"
    )
else:
    DATA_FILE = "student_dashboard/data/students.csv"
    df_student = load_student_data(DATA_FILE)
    st.sidebar.info(
        "using sample dataset"
    )

valid,missing = validate_columns(df=df_student)

if not valid:
    st.error(
        f"Missing columns:{missing}"
    )
    st.stop()

st.sidebar.header("Filters")

if df_student is not None:
    departments = [
        "All"
    ] + sorted(
        df_student["Department"].unique().tolist()
    )

    selected_department = st.sidebar.selectbox(
        "Select Department",
        departments
    )

    semesters = [
        "All"
    ]+ sorted(
        df_student["Semester"].unique().tolist()
    )
    selected_semester = st.sidebar.selectbox(
        "Select a Semester",
        semesters
    )

df_filtered = df_student.copy()

if selected_department != "All":
    df_filtered = df_filtered[
        df_filtered["Department"] == selected_department
    ]

if selected_semester != "All":
    df_filtered = df_filtered[
        df_filtered["Semester"] == selected_semester
    ]


min_cgpa = st.sidebar.slider(
    "Minimum CGPA",
    min_value=float(df_filtered["CGPA"].min()),
    max_value=float(df_filtered["CGPA"].max()),
    value=7.0
)

df_filtered = df_filtered[
    df_filtered["CGPA"] >= min_cgpa
]

st.header("Analytics")

st.dataframe(df_filtered,use_container_width=True)

dict_metrics = get_metric(df=df_filtered)

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Students",
        value= dict_metrics.get("total_students","--")
    )

with col2:
    st.metric(
        label="Average CGPA",
        value= dict_metrics.get("average_cgpa","--")
    )

with col3:
    st.metric(
        label="Placement %",
        value= dict_metrics.get("placement_status","--")
    )

st.header("Visualizations")
st.write(
    "Charts will be deplayed here"
)

st.subheader("Students by Department")

chart_distribution = department_distribution(
    df=df_filtered
)

st.plotly_chart(
    chart_distribution,
    use_container_width=True
)

st.subheader("Average CGPA by Department")

chart_cgpa = average_cgpa_by_department(
    df=df_filtered
)


st.plotly_chart(
    chart_cgpa,
    use_container_width=True
)


st.subheader("Placement Status")

chart_placement = placement_distribution(
    df=df_filtered
)


st.plotly_chart(
    chart_placement,
    use_container_width=True
)

# Footer
st.divider()

st.caption(
    "Built using Python and Streamlit"
)