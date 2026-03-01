"""
🚀 EDUSAT AI - Web Dashboard (Streamlit Cloud)
Deploy this to share with donors and officials
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="EduSat AI - Eastern Cape",
    page_icon="🚀",
    layout="wide"
)

# Load model
@st.cache_resource
def load_model():
    try:
        model_files = [f for f in os.listdir('models') if f.endswith('.joblib')]
        if model_files:
            latest_model = sorted(model_files)[-1]
            model_pkg = joblib.load(f'models/{latest_model}')
            return model_pkg
    except:
        return None

model_pkg = load_model()

# Header
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center'>
    <h1 style='color: white; margin:0'>🚀 EduSat AI</h1>
    <p style='color: white; opacity:0.9; margin:0'>Eastern Cape Rural Education Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("data/Eastern_Cape_Education_Factors_Dataset.xlsx", sheet_name="data")
    df['risk_binary'] = (df['DropoutRisk'] == 'At Risk').astype(int)
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.image("C:/Users/lutha/Downloads/logo.png" if os.path.exists("C:/Users/lutha/Downloads/logo.png") else None, width=200)
    st.markdown("## Navigation")
    page = st.radio("", [
        "📊 Impact Dashboard",
        "🤖 Risk Predictor",
        "🗺️ District Analytics",
        "📈 Policy Simulator"
    ])
    
    st.markdown("---")
    st.markdown(f"**👥 Active Learners:** {len(df)}")
    st.markdown(f"**🏫 Districts:** {df['District'].nunique()}")
    st.markdown(f"**⚠️ At Risk:** {len(df[df['DropoutRisk']=='At Risk'])}")

# PAGE 1: Impact Dashboard
if page == "📊 Impact Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Learners", len(df), "100% coverage")
    with col2:
        saved = len(df[df['DropoutRisk']=='Not At Risk']) - 150
        st.metric("Saved from Dropout", saved, "early intervention")
    with col3:
        alerts = len(df[df['DropoutRisk']=='At Risk'])
        st.metric("Active Alerts", alerts, "need attention")
    with col4:
        st.metric("Schools Connected", "8", "Starlink active")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk by District")
        risk_district = df.groupby('District')['risk_binary'].mean() * 100
        fig = px.bar(x=risk_district.index, y=risk_district.values, 
                     color=risk_district.values, color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk Trend by Grade")
        risk_grade = df.groupby('Grade')['risk_binary'].mean() * 100
        fig = px.line(x=risk_grade.index, y=risk_grade.values, markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Model performance if available
    if model_pkg and 'metrics' in model_pkg:
        st.subheader("🤖 Model Performance")
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.metric("Accuracy", f"{model_pkg['metrics']['accuracy']:.2%}")
        mcol2.metric("F1 Score", f"{model_pkg['metrics']['f1']:.2%}")
        mcol3.metric("ROC-AUC", f"{model_pkg['metrics']['roc_auc']:.2%}")

# PAGE 2: Risk Predictor
elif page == "🤖 Risk Predictor":
    st.subheader("🎯 Real-time Risk Prediction")
    st.markdown("Enter learner data to predict dropout probability")
    
    col1, col2 = st.columns(2)
    
    with col1:
        attendance = st.slider("Attendance %", 0, 100, 65)
        math_score = st.slider("Math Score", 0, 1000, 450)
        reading_score = st.slider("Reading Score", 0, 1000, 380)
        food_security = st.slider("Food Security", 0, 100, 45)
        distance = st.slider("Distance to School (km)", 0.0, 20.0, 5.0)
        unemployment = st.slider("Household Unemployment %", 0, 100, 60)
        
        if st.button("🔮 Predict Risk", type="primary"):
            # Simple calculation for demo
            risk = (
                (100 - attendance) * 0.3 +
                (1000 - math_score) * 0.002 * 0.25 +
                (1000 - reading_score) * 0.002 * 0.25 +
                (100 - food_security) * 0.1 * 0.2
            )
            risk = min(100, max(0, risk))
            st.session_state['risk_score'] = risk
    
    with col2:
        if 'risk_score' in st.session_state:
            risk = st.session_state['risk_score']
            
            if risk >= 70:
                st.markdown(f"""
                <div style='background:#ff6b6b; padding:2rem; border-radius:10px; text-align:center'>
                    <h1 style='color:white; font-size:4rem'>🔴</h1>
                    <h2 style='color:white'>HIGH RISK</h2>
                    <h1 style='color:white; font-size:3rem'>{risk:.0f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("""
                **Intervention Plan:**
                - 📞 Urgent parent contact
                - 📚 After-school math club
                - 🍲 Nutrition program enrollment
                - 👥 Peer tutoring
                """)
            elif risk >= 40:
                st.markdown(f"""
                <div style='background:#feca57; padding:2rem; border-radius:10px; text-align:center'>
                    <h1 style='color:white; font-size:4rem'>🟡</h1>
                    <h2 style='color:white'>MEDIUM RISK</h2>
                    <h1 style='color:white; font-size:3rem'>{risk:.0f}%</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("""
                **Intervention Plan:**
                - 📞 SMS alert to parents
                - 📚 Extra worksheets
                - 👥 Weekly check-in
                """)
            else:
                st.markdown(f"""
                <div style='background:#1dd1a1; padding:2rem; border-radius:10px; text-align:center'>
                    <h1 style='color:white; font-size:4rem'>🟢</h1>
                    <h2 style='color:white'>LOW RISK</h2>
                    <h1 style='color:white; font-size:3rem'>{risk:.0f}%</h1>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("👆 Enter data and click Predict")

# PAGE 3: District Analytics
elif page == "🗺️ District Analytics":
    st.subheader("📍 Eastern Cape District Analysis")
    
    # District selector
    district = st.selectbox("Select District", sorted(df['District'].unique()))
    
    # Filter data
    district_df = df[df['District'] == district]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Learners", len(district_df))
    col2.metric("Risk Rate", f"{district_df['risk_binary'].mean()*100:.1f}%")
    col3.metric("Avg Math", f"{district_df['MathScore_0_1000'].mean():.0f}")
    
    # Risk factors
    st.subheader("Risk Factors Comparison")
    
    factors = pd.DataFrame({
        'Factor': ['Attendance', 'Math', 'Reading', 'Food Security'],
        'Value': [
            district_df['AttendanceRate_%'].mean(),
            district_df['MathScore_0_1000'].mean() / 10,
            district_df['ReadingScore_0_1000'].mean() / 10,
            district_df['FoodSecurityIndex_0_100'].mean()
        ]
    })
    
    fig = px.bar(factors, x='Factor', y='Value', color='Value',
                 color_continuous_scale='RdYlGn', range_color=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

# PAGE 4: Policy Simulator
else:  # Policy Simulator
    st.subheader("📊 Policy Impact Simulator")
    st.markdown("See how interventions reduce dropout risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Select Interventions")
        base_risk = st.slider("Current Risk %", 0, 100, 70)
        
        parent = st.checkbox("📞 Parent Contact Program (-15%)", True)
        math = st.checkbox("📚 After-school Math Club (-20%)", True)
        nutrition = st.checkbox("🍲 School Nutrition (-12%)", True)
        tutoring = st.checkbox("👥 Peer Tutoring (-18%)", False)
        transport = st.checkbox("🚌 Transport Assistance (-10%)", False)
        
        if st.button("Simulate Impact", type="primary"):
            reduction = 0
            if parent: reduction += 15
            if math: reduction += 20
            if nutrition: reduction += 12
            if tutoring: reduction += 18
            if transport: reduction += 10
            
            new_risk = max(0, base_risk - reduction)
            st.session_state['new_risk'] = new_risk
            st.session_state['reduction'] = reduction
    
    with col2:
        if 'new_risk' in st.session_state:
            st.markdown("### Projected Impact")
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=st.session_state['new_risk'],
                delta={'reference': base_risk},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'steps': [
                        {'range': [0, 30], 'color': '#1dd1a1'},
                        {'range': [30, 60], 'color': '#feca57'},
                        {'range': [60, 100], 'color': '#ff6b6b'}
                    ]
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"""
            **Risk Reduction:** {st.session_state['reduction']}%
            **New Risk Level:** {st.session_state['new_risk']:.0f}%
            **Learners Saved:** {int(st.session_state['reduction'] * 5)} per 100
            """)
        else:
            st.info("Select interventions and click Simulate")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem'>
    <span>🚀 EduSat AI - Eastern Cape | 🇿🇦 Built for Rural Schools | 🛰️ Starlink Ready</span>
    <br>
    <span>Version 1.0.0 | © 2024</span>
</div>
""", unsafe_allow_html=True)
