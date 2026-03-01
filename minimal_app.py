"""
EduSat AI - Minimal Working App
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="EduSat AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 EduSat AI - Eastern Cape")
st.markdown("### Rural Education Intelligence Platform")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data/Eastern_Cape_Education_Factors_Dataset.xlsx", sheet_name="data")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # Show basic stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Learners", len(df))
    
    with col2:
        at_risk = len(df[df['DropoutRisk'] == 'At Risk'])
        st.metric("At Risk", at_risk, f"{at_risk/len(df)*100:.1f}%")
    
    with col3:
        districts = df['District'].nunique()
        st.metric("Districts", districts)
    
    # Show data table
    st.subheader("📊 Learner Data")
    st.dataframe(df.head(100), use_container_width=True)
    
    # Simple chart
    st.subheader("📈 Risk by District")
    risk_district = df.groupby('District')['DropoutRisk'].apply(
        lambda x: (x == 'At Risk').mean() * 100
    ).reset_index()
    risk_district.columns = ['District', 'Risk %']
    
    fig = px.bar(risk_district, x='District', y='Risk %', 
                 color='Risk %', color_continuous_scale=['green', 'yellow', 'red'])
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.error("""
    ❌ Could not load data!
    
    Please make sure:
    1. The Excel file is in the 'data' folder
    2. File name is: Eastern_Cape_Education_Factors_Dataset.xlsx
    3. Sheet name is: 'data'
    """)

st.markdown("---")
st.markdown("🇿🇦 Built for Eastern Cape Rural Schools")
