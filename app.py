import streamlit as st

# ---------- Page setup ----------
st.set_page_config(
    page_title="Workforce Transition Portal",
    page_icon="🧭",
    layout="wide",
)

# ---------- Placeholder pages (we fill these in later) ----------
def employee_view():
    st.header("Employee View")
    st.write("Enter your job profile to see your automation risk and career paths.")
    st.info("Coming soon: profile form, risk prediction, reskilling recommendations.")

def leadership_view():
    st.header("Leadership View")
    st.write("Company-wide view of automation exposure for talent leaders.")
    st.info("Coming soon: risk distribution, most exposed roles, reskilling priorities.")

def about_page():
    st.header("About this project")
    st.write(
        "A tool that predicts which roles are most at risk from AI automation "
        "and recommends realistic career transition paths."
    )
    st.info("Coming soon: methodology, model performance, team.")

# ---------- Sidebar navigation ----------
st.title("🧭 Workforce Transition Portal")

page = st.sidebar.radio(
    "Go to",
    ["Employee View", "Leadership View", "About"],
)

if page == "Employee View":
    employee_view()
elif page == "Leadership View":
    leadership_view()
else:
    about_page()
