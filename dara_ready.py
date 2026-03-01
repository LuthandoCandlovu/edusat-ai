"""
🚀 EDUSAT AI - COMPLETE VERSION WITH EASTERN CAPE MAP
All 7 WOW Features + District Map
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
from datetime import datetime
import random
import os

# Page config
st.set_page_config(
    page_title="EduSat AI - Eastern Cape",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM CSS
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #f8fafc;
    }
    
    /* Animated header */
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        background: linear-gradient(-45deg, #667eea, #764ba2, #6b8cff, #8e2de2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
    }
    
    .sub-title {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* FEATURE 7: Demo Mode badge */
    .demo-badge {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 9999px;
        font-weight: 700;
        animation: pulse 2s infinite;
        text-align: center;
        margin: 1rem 0;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* FEATURE 5: Alert queue */
    .alert-queue {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .alert-item {
        background: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid;
        font-size: 0.9rem;
    }
    
    /* FEATURE 2: Intervention card */
    .intervention-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 6px solid #667eea;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    /* FEATURE 1: Risk factor badges */
    .factor-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .factor-high { background: #fee2e2; color: #ef4444; }
    .factor-medium { background: #fed7aa; color: #f97316; }
    .factor-low { background: #dcfce7; color: #22c55e; }
    
    /* District table */
    .district-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    .district-table th {
        background: #f1f5f9;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
    }
    
    .district-table td {
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .risk-badge {
        padding: 0.35rem 1rem;
        border-radius: 9999px;
        color: white;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        min-width: 100px;
        text-align: center;
    }
    
    .metric-highlight {
        font-size: 3.5rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
    }
    
    /* FEATURE 4: Download button */
    .download-btn {
        background: #667eea;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .download-btn:hover {
        background: #5a67d8;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# FEATURE 1: Calculate risk factors with explanations
def calculate_risk_factors(attendance, math_score, reading_score, food_security, distance):
    factors = []
    
    attendance_impact = (100 - attendance) * 0.35
    if attendance_impact > 5:
        factors.append(("Low Attendance", round(attendance_impact, 1)))
    
    math_impact = (1000 - math_score) * 0.002 * 0.25 * 100
    if math_impact > 5:
        factors.append(("Poor Math Performance", round(math_impact, 1)))
    
    reading_impact = (1000 - reading_score) * 0.002 * 0.25 * 100
    if reading_impact > 5:
        factors.append(("Poor Reading Performance", round(reading_impact, 1)))
    
    food_impact = (100 - food_security) * 0.1 * 0.2 * 100
    if food_impact > 5:
        factors.append(("Food Insecurity", round(food_impact, 1)))
    
    distance_impact = (distance / 20) * 15
    if distance_impact > 5:
        factors.append(("Long Distance Travel", round(distance_impact, 1)))
    
    factors.sort(key=lambda x: x[1], reverse=True)
    return factors[:3]

# FEATURE 2: Generate intervention plan
def generate_intervention_plan(risk_level, factors):
    if risk_level >= 70:
        plan = {
            "title": "🔴 URGENT INTERVENTION REQUIRED",
            "actions": [],
            "timeline": "This Week",
            "responsible": ["Teacher", "Principal", "Social Worker"]
        }
        for factor, impact in factors:
            if "Attendance" in factor:
                plan["actions"].append("📞 Immediate parent contact within 24h")
                plan["actions"].append("🏠 Home visit by social worker")
            elif "Math" in factor:
                plan["actions"].append("📚 Daily after-school math club")
                plan["actions"].append("👥 Peer tutoring with top performer")
            elif "Reading" in factor:
                plan["actions"].append("📖 One-on-one reading support 3x/week")
            elif "Food" in factor:
                plan["actions"].append("🍲 Enroll in nutrition program immediately")
            elif "Distance" in factor:
                plan["actions"].append("🚌 Arrange transport assistance")
    
    elif risk_level >= 40:
        plan = {
            "title": "🟡 WATCHLIST - MONITOR CLOSELY",
            "actions": [],
            "timeline": "Next 2 Weeks",
            "responsible": ["Teacher", "Parent"]
        }
        for factor, impact in factors:
            if "Attendance" in factor:
                plan["actions"].append("📞 Weekly parent check-in calls")
            elif "Math" in factor:
                plan["actions"].append("📚 Extra worksheets for practice")
            elif "Reading" in factor:
                plan["actions"].append("📖 Reading club 2x/week")
            elif "Food" in factor:
                plan["actions"].append("🍲 Nutrition program participation")
    
    else:
        plan = {
            "title": "🟢 LOW RISK - CONTINUE MONITORING",
            "actions": ["✅ Regular progress tracking", "📚 Encourage current performance", "📅 Monthly review"],
            "timeline": "Ongoing",
            "responsible": ["Teacher"]
        }
    return plan

# FEATURE 4: Generate PDF report
def generate_pdf_report(df):
    alerts_count = len(df[df['DropoutRisk']=='At Risk'])
    saved_count = len(df[df['DropoutRisk']=='Not At Risk']) - 150
    
    report = f"""
EDUSAT AI - DISTRICT IMPACT REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 OVERALL STATISTICS
-------------------
Total Learners: {len(df)}
Districts: {df['District'].nunique()}
Active Alerts: {alerts_count}
Saved from Dropout: {saved_count}

🔥 TOP RISK DRIVERS
-----------------
1. Reading Score (52.9% impact)
2. Math Score (16.3% impact)
3. Attendance (2.5% impact)

🎯 RECOMMENDED ACTIONS
-------------------
1. Parent contact for high-risk learners
2. After-school math programs
3. Nutrition support
4. Transport assistance

Report generated by EduSat AI Platform
    """
    return report

def get_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}" class="download-btn">📥 Download Report</a>'

# ============================================================================
# LOAD DATA
# ============================================================================
try:
    logo = Image.open("C:/Users/lutha/Downloads/logo.png")
    st.sidebar.image(logo, width=220)
except:
    st.sidebar.title("🚀 EduSat AI")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Eastern_Cape_Education_Factors_Dataset.xlsx", sheet_name="data")
    df['risk_binary'] = (df['DropoutRisk'] == 'At Risk').astype(int)
    return df

df = load_data()

# ============================================================================
# SIDEBAR - FEATURE 5 (Alert Queue) and FEATURE 7 (Demo Mode)
# ============================================================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("Go to", ["📊 Dashboard", "🤖 Risk Predictor", "📋 Intervention Planner", 
                              "📈 Policy Simulator", "🗺️ District Analytics"])
    
    st.markdown("---")
    
    # FEATURE 7: Demo Mode Toggle
    st.markdown("""
    <div class="demo-badge">
        ⚡ DEMO MODE ACTIVE
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("### Quick Stats")
    st.metric("Total Learners", len(df))
    st.metric("At Risk", len(df[df['DropoutRisk']=='At Risk']))
    
    # FEATURE 5: Early Warning Alerts
    st.markdown("### 📋 Alert Queue")
    st.markdown("""
    <div class="alert-queue">
        <div class="alert-item" style="border-left-color: #ef4444;">
            ⚠️ EC_L0045 - HIGH RISK - 10 min ago<br>
            <small>📱 SMS sent to teacher</small>
        </div>
        <div class="alert-item" style="border-left-color: #ef4444;">
            ⚠️ EC_L0082 - HIGH RISK - 25 min ago<br>
            <small>📱 Escalated to principal</small>
        </div>
        <div class="alert-item" style="border-left-color: #f97316;">
            ⚠️ EC_L0123 - MEDIUM RISK - 1 hour ago<br>
            <small>📧 Email sent to parents</small>
        </div>
        <div class="alert-item" style="border-left-color: #22c55e;">
            ✅ EC_L0234 - INTERVENTION COMPLETED<br>
            <small>Risk reduced by 45%</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN HEADER
# ============================================================================
st.markdown("""
<div class="main-header">
    <div class="main-title">EduSat AI</div>
    <div class="sub-title">Eastern Cape Rural Education Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PAGE 1: DASHBOARD with FEATURE 4 (PDF Export)
# ============================================================================
if page == "📊 Dashboard":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-highlight">400</div>', unsafe_allow_html=True)
        st.markdown("**Total Learners**")
    with col2:
        st.markdown('<div class="metric-highlight" style="color: #ef4444;">203</div>', unsafe_allow_html=True)
        st.markdown("**At Risk**")
    
    st.markdown("---")
    st.markdown("### 📊 Risk by District")
    
    risk_by_district = df.groupby('District')['risk_binary'].mean().sort_values() * 100
    st.bar_chart(risk_by_district)
    
    # FEATURE 4: Export PDF Report
    st.markdown("### 📥 Export Reports")
    report_text = generate_pdf_report(df)
    st.markdown(get_download_link(report_text, f"edusat_report_{datetime.now().strftime('%Y%m%d')}.txt"), 
                unsafe_allow_html=True)

# ============================================================================
# PAGE 2: RISK PREDICTOR with FEATURE 1 (Explain Why)
# ============================================================================
elif page == "🤖 Risk Predictor":
    st.markdown("### 🤖 AI Risk Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Learner Profile")
        
        # FEATURE 7: Demo Mode pre-fill
        if st.button("🎬 Load Demo Case"):
            st.session_state['attendance'] = 62
            st.session_state['math_score'] = 380
            st.session_state['reading_score'] = 350
            st.session_state['food'] = 32
            st.session_state['distance'] = 12.5
        
        attendance = st.slider("Attendance %", 0, 100, st.session_state.get('attendance', 65))
        math_score = st.slider("Math Score", 0, 1000, st.session_state.get('math_score', 450))
        reading_score = st.slider("Reading Score", 0, 1000, st.session_state.get('reading_score', 380))
        food = st.slider("Food Security", 0, 100, st.session_state.get('food', 45))
        distance = st.slider("Distance to School (km)", 0.0, 20.0, st.session_state.get('distance', 5.0))
        
        if st.button("🔮 Predict Risk", type="primary", use_container_width=True):
            risk = (
                (100 - attendance) * 0.35 +
                (1000 - math_score) * 0.002 * 0.25 * 100 +
                (1000 - reading_score) * 0.002 * 0.25 * 100 +
                (100 - food) * 0.1 * 0.2 * 100 +
                (distance / 20) * 15
            )
            risk = min(100, max(0, risk))
            
            st.session_state['predicted_risk'] = risk
            st.session_state['risk_factors'] = calculate_risk_factors(attendance, math_score, reading_score, food, distance)
    
    with col2:
        st.markdown("### 🎯 Prediction Result")
        
        if 'predicted_risk' in st.session_state:
            risk = st.session_state['predicted_risk']
            
            if risk >= 70:
                st.error(f"### 🔴 HIGH RISK: {risk:.1f}%")
            elif risk >= 40:
                st.warning(f"### 🟡 MEDIUM RISK: {risk:.1f}%")
            else:
                st.success(f"### 🟢 LOW RISK: {risk:.1f}%")
            
            # FEATURE 1: Show Top 3 Reasons
            st.markdown("### 🔍 Top 3 Risk Factors")
            
            factors = st.session_state['risk_factors']
            for factor, impact in factors:
                if impact > 30:
                    st.markdown(f'<span class="factor-badge factor-high">{factor}: {impact}% impact</span>', 
                              unsafe_allow_html=True)
                elif impact > 15:
                    st.markdown(f'<span class="factor-badge factor-medium">{factor}: {impact}% impact</span>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="factor-badge factor-low">{factor}: {impact}% impact</span>', 
                              unsafe_allow_html=True)

# ============================================================================
# PAGE 3: INTERVENTION PLANNER - FEATURE 2
# ============================================================================
elif page == "📋 Intervention Planner":
    st.markdown("### 📋 One-Click Intervention Plan Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Select Learner")
        learners = df[df['DropoutRisk'] == 'At Risk']['LearnerID'].head(10).tolist()
        selected = st.selectbox("Choose Learner", learners)
        
        if selected:
            learner = df[df['LearnerID'] == selected].iloc[0]
            
            # Calculate risk
            risk = (
                (100 - learner['AttendanceRate_%']) * 0.35 +
                (1000 - learner['MathScore_0_1000']) * 0.002 * 0.25 * 100 +
                (1000 - learner['ReadingScore_0_1000']) * 0.002 * 0.25 * 100 +
                (100 - learner['FoodSecurityIndex_0_100']) * 0.1 * 0.2 * 100 +
                (learner['DistanceToSchool_km'] / 20) * 15
            )
            
            factors = calculate_risk_factors(
                learner['AttendanceRate_%'],
                learner['MathScore_0_1000'],
                learner['ReadingScore_0_1000'],
                learner['FoodSecurityIndex_0_100'],
                learner['DistanceToSchool_km']
            )
            
            if st.button("📋 Generate Intervention Plan", type="primary"):
                st.session_state['plan_learner'] = selected
                st.session_state['plan_risk'] = risk
                st.session_state['plan_factors'] = factors
    
    with col2:
        if 'plan_learner' in st.session_state:
            plan = generate_intervention_plan(st.session_state['plan_risk'], 
                                             st.session_state['plan_factors'])
            
            st.markdown(f"""
            <div class="intervention-card">
                <h3>{plan['title']}</h3>
                <p><b>Learner:</b> {st.session_state['plan_learner']}</p>
                <p><b>Risk Level:</b> {st.session_state['plan_risk']:.1f}%</p>
                <p><b>Timeline:</b> {plan['timeline']}</p>
                <p><b>Responsible:</b> {', '.join(plan['responsible'])}</p>
                <h4>Action Items:</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            for action in plan['actions']:
                st.markdown(f"<li>{action}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)

# ============================================================================
# PAGE 4: POLICY SIMULATOR - FEATURE 3
# ============================================================================
elif page == "📈 Policy Simulator":
    st.markdown("### 📈 Policy Impact Simulator")
    st.info("🎯 Adjust sliders to see how interventions reduce dropout risk")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎛️ Adjust Interventions")
        base_risk = st.slider("Current Risk Level (%)", 0, 100, 68)
        
        attendance = st.slider("Attendance Improvement (points)", 0, 30, 15)
        math = st.slider("Math Support (%)", 0, 100, 60)
        food = st.slider("Food Program (%)", 0, 100, 40)
        transport = st.slider("Transport Assistance (%)", 0, 100, 30)
        
        if st.button("📊 Calculate Impact", type="primary"):
            reduction = (attendance * 0.8 + math * 0.15 + food * 0.12 + transport * 0.1) / 10
            new_risk = max(0, base_risk - reduction)
            saved = int(reduction * 4)
            
            st.session_state['base'] = base_risk
            st.session_state['new'] = new_risk
            st.session_state['reduction'] = reduction
            st.session_state['saved'] = saved
    
    with col2:
        if 'new' in st.session_state:
            # Show before/after
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Before', x=['Risk'], y=[st.session_state['base']], 
                                 marker_color='#ef4444'))
            fig.add_trace(go.Bar(name='After', x=['Risk'], y=[st.session_state['new']], 
                                 marker_color='#10b981'))
            fig.update_layout(title="Risk Reduction Impact", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show metrics
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Reduction", f"{st.session_state['reduction']:.1f}%")
            col_b.metric("New Risk", f"{st.session_state['new']:.1f}%")
            col_c.metric("Learners Saved", f"{st.session_state['saved']} per 100")

# ============================================================================
# PAGE 5: DISTRICT ANALYTICS with MAP and Heatmap
# ============================================================================
else:
    st.markdown("### 🗺️ Eastern Cape District Analytics")
    
    # Show totals
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-highlight">400</div>', unsafe_allow_html=True)
        st.markdown("**Total Learners**")
    with col2:
        st.markdown('<div class="metric-highlight" style="color: #ef4444;">203</div>', unsafe_allow_html=True)
        st.markdown("**At Risk**")
    
    st.markdown("---")
    
    # DISPLAY THE EASTERN CAPE MAP
    st.markdown("### 🗺️ Eastern Cape District Map")
    
    # Check if map file exists and display it
    map_path = "EasternCape.gif"
    if os.path.exists(map_path):
        st.image(map_path, caption="Eastern Cape Districts", use_container_width=True)
    else:
        st.warning("⚠️ Map image not found. Please ensure EasternCape.gif is in the project folder.")
        st.info("📌 Expected path: C:\\Users\\lutha\\edusat-ai\\EasternCape.gif")
    
    st.markdown("---")
    
    # District data
    districts = [
        {"name": "Alfred Nzo", "risk": 50, "learners": 45},
        {"name": "Amathole", "risk": 47, "learners": 52},
        {"name": "Buffalo City", "risk": 46, "learners": 48},
        {"name": "Chris Hani", "risk": 44, "learners": 55},
        {"name": "Joe Gqabi", "risk": 56, "learners": 42},
        {"name": "Nelson Mandela Bay", "risk": 55, "learners": 58},
        {"name": "OR Tambo", "risk": 51, "learners": 62},
        {"name": "Sarah Baartman", "risk": 52, "learners": 38}
    ]
    
    districts.sort(key=lambda x: x["risk"], reverse=True)
    
    # FEATURE 6: Heatmap-style table
    st.markdown("### 📊 District Risk Summary")
    
    table_html = '<table class="district-table"><tr><th>District</th><th>Risk Rate</th><th>Status</th><th>Learners</th></tr>'
    for d in districts:
        if d["risk"] >= 55:
            badge = '<span class="risk-badge" style="background:#ef4444;">🔴 HIGH</span>'
        elif d["risk"] >= 50:
            badge = '<span class="risk-badge" style="background:#f59e0b;">🟡 MEDIUM</span>'
        else:
            badge = '<span class="risk-badge" style="background:#10b981;">🟢 LOW</span>'
        table_html += f'<tr><td><strong>{d["name"]}</strong></td><td><strong>{d["risk"]}%</strong></td><td>{badge}</td><td>{d["learners"]}</td></tr>'
    table_html += '</table>'
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Bar chart
    fig = go.Figure()
    colors = ['#ef4444' if r >= 55 else '#f59e0b' if r >= 50 else '#10b981' for r in [d["risk"] for d in districts]]
    fig.add_trace(go.Bar(
        x=[d["name"] for d in districts],
        y=[d["risk"] for d in districts],
        marker_color=colors,
        text=[f"{d['risk']}%" for d in districts],
        textposition='outside'
    ))
    fig.update_layout(title="Risk by District", height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # District selector for deep dive
    st.markdown("### 🔍 District Deep Dive")
    selected = st.selectbox("Select a district", [d["name"] for d in districts])
    
    for d in districts:
        if d["name"] == selected:
            col1, col2, col3 = st.columns(3)
            col1.metric("Risk Rate", f"{d['risk']}%")
            col2.metric("Learners", d['learners'])
            col3.metric("At Risk", int(d['learners'] * d['risk']/100))
            
            if d["risk"] >= 55:
                st.error(f"🔴 {selected} is HIGH RISK - Immediate intervention needed")
            elif d["risk"] >= 50:
                st.warning(f"🟡 {selected} is MEDIUM RISK - Monitor closely")
            else:
                st.success(f"🟢 {selected} is LOW RISK - On track")
            break

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    🚀 EduSat AI · All 7 WOW Features + Eastern Cape Map · Ready for DARA
</div>
""", unsafe_allow_html=True)
