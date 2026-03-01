"""
EduSat AI - Fixed Version
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="EduSat AI - Eastern Cape",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .big-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>📚 EduSat AI - Eastern Cape</h1><p>Rural Education Intelligence Platform</p></div>', 
            unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data/Eastern_Cape_Education_Factors_Dataset.xlsx", sheet_name="data")
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

df = load_data()

if df is not None:
    # Sidebar filters
    with st.sidebar:
        st.header("🎯 Filters")
        
        # District filter
        districts = ['All'] + sorted(df['District'].unique().tolist())
        selected_district = st.selectbox("Select District", districts)
        
        # Grade filter
        grades = ['All'] + sorted(df['Grade'].unique().tolist())
        selected_grade = st.selectbox("Select Grade", grades)
        
        st.markdown("---")
        st.markdown(f"### 📊 Dataset Stats")
        st.markdown(f"Total Learners: **{len(df)}**")
        st.markdown(f"At Risk: **{len(df[df['DropoutRisk']=='At Risk'])}**")
        st.markdown(f"Districts: **{df['District'].nunique()}**")
    
    # Filter data
    filtered_df = df.copy()
    if selected_district != 'All':
        filtered_df = filtered_df[filtered_df['District'] == selected_district]
    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['Grade'] == selected_grade]
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Total Learners")
        st.markdown(f'<div class="big-number">{len(filtered_df)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 🔴 At Risk")
        at_risk = len(filtered_df[filtered_df['DropoutRisk'] == 'At Risk'])
        st.markdown(f'<div class="big-number" style="color:#dc3545;">{at_risk}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Risk Rate")
        risk_rate = at_risk / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
        st.markdown(f'<div class="big-number" style="color:#fd7e14;">{risk_rate:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 Avg Attendance")
        avg_att = filtered_df['AttendanceRate_%'].mean()
        st.markdown(f'<div class="big-number" style="color:#28a745;">{avg_att:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏫 Risk by District")
        risk_district = df.groupby('District')['DropoutRisk'].apply(
            lambda x: (x == 'At Risk').mean() * 100
        ).reset_index()
        risk_district.columns = ['District', 'Risk %']
        
        fig = px.bar(risk_district, x='District', y='Risk %', 
                     color='Risk %', 
                     color_continuous_scale=['#28a745', '#fd7e14', '#dc3545'],
                     title="Risk Percentage by District")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)  # Fixed: use_container_width=True is correct
    
    with col2:
        st.subheader("📚 Risk by Grade")
        risk_grade = df.groupby('Grade')['DropoutRisk'].apply(
            lambda x: (x == 'At Risk').mean() * 100
        ).reset_index()
        risk_grade.columns = ['Grade', 'Risk %']
        
        fig = px.line(risk_grade, x='Grade', y='Risk %', 
                      markers=True,
                      title="Risk Trend Across Grades")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)  # Fixed: use_container_width=True is correct
    
    # At Risk Learners Table
    st.subheader("🚨 At-Risk Learners")
    at_risk_df = filtered_df[filtered_df['DropoutRisk'] == 'At Risk'].copy()
    
    if len(at_risk_df) > 0:
        # Calculate risk score
        at_risk_df['Risk Score'] = (
            (100 - at_risk_df['AttendanceRate_%']) * 0.3 +
            (1000 - at_risk_df['MathScore_0_1000']) * 0.002 * 0.35 +
            (1000 - at_risk_df['ReadingScore_0_1000']) * 0.002 * 0.35
        ).round(2)
        
        display_cols = ['LearnerID', 'Grade', 'District', 'RuralStatus',
                        'AttendanceRate_%', 'MathScore_0_1000', 'ReadingScore_0_1000',
                        'Risk Score']
        
        # Fixed: use_container_width=True is correct for st.dataframe
        st.dataframe(
            at_risk_df[display_cols].sort_values('Risk Score', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Export button
        if st.button("📥 Export At-Risk List"):
            csv = at_risk_df[display_cols].to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="at_risk_learners.csv",
                mime="text/csv"
            )
    else:
        st.info("No at-risk learners in current filter")
    
    # Quick stats in expander
    with st.expander("📊 View Detailed Statistics"):
        st.write("### District Summary")
        district_summary = df.groupby('District').agg({
            'LearnerID': 'count',
            'risk_binary': 'mean',
            'MathScore_0_1000': 'mean',
            'ReadingScore_0_1000': 'mean',
            'AttendanceRate_%': 'mean'
        }).round(2)
        district_summary.columns = ['Count', 'Risk Rate', 'Avg Math', 'Avg Reading', 'Avg Attendance']
        district_summary['Risk Rate'] = (district_summary['Risk Rate'] * 100).round(1)
        st.dataframe(district_summary, use_container_width=True)  # Fixed

else:
    st.error("""
    ## ❌ Could not load data!
    
    Please check:
    1. The Excel file is in the **data** folder
    2. File name is exactly: **Eastern_Cape_Education_Factors_Dataset.xlsx**
    3. The sheet name is: **data**
    
    Current directory contents:
    """)
    
    import os
    st.code(os.listdir('.'))

# Footer
st.markdown("---")
st.markdown("🇿🇦 **Built for Eastern Cape Rural Schools** | © 2024 EduSat AI")
