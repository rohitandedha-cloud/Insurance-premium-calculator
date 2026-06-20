import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# ==========================================
# 1. SETUP & SIMULATED MODEL (TRAIN YOURS HERE)
# ==========================================
# For demonstration, we create a dummy model so the app runs standalone.
# Replace this block with your actual loaded model (e.g., via pickle or joblib).
@st.cache_resource
def load_model():
    # Simulating the exact 6 features your model expects
    features = ['age', 'bmi', 'children', 'is_smoker', 'is_female', 'bmi_category_Obese']
    X_dummy = pd.DataFrame(np.random.rand(100, 6), columns=features)
    y_dummy = np.random.rand(100) * 25000 + 5000  # US scale charges
    
    mock_model = RandomForestRegressor(n_estimators=10, random_state=42)
    mock_model.fit(X_dummy, y_dummy)
    return mock_model

model = load_model()

# ==========================================
# 2. BEAUTIFUL FLOATING UI STYLES (CSS)
# ==========================================
st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translatey(0px); }
        50% { transform: translatey(-10px); }
        100% { transform: translatey(0px); }
    }
    .floating-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #1E3A8A;
        animation: float 4s ease-in-out infinite;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0 is the Welcome Screen

# Dictionary to hold user responses
if 'inputs' not in st.session_state:
    st.session_state.inputs = {
        'age': 30, 'bmi': 24.0, 'children': 0,
        'is_smoker': 'no', 'is_female': 'no'
    }

# Helper functions to change steps
def next_step(): st.session_state.step += 1
def restart(): st.session_state.step = 0

# ==========================================
# 4. MULTI-STEP WIZARD UI
# ==========================================

# --- STEP 0: START LANDING PAGE ---
if st.session_state.step == 0:
    st.markdown('<div class="floating-title">✨ Insurance Premium Calculator ✨</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:1.2rem; color:#6B7280;'>Get an instant, customized medical insurance estimate tailored to your health profile.</p>", unsafe_allow_html=True)
    
    st.write("---")
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        st.button("🚀 Get Started", on_click=next_step)

# --- STEP 1: AGE QUESTION ---
elif st.session_state.step == 1:
    st.subheader("Step 1 of 5: Age Assessment")
    st.session_state.inputs['age'] = st.slider("Enter the client's age:", 18, 100, int(st.session_state.inputs['age']))
    st.button("Next ➡️", on_click=next_step)

# --- STEP 2: BMI QUESTION ---
elif st.session_state.step == 2:
    st.subheader("Step 2 of 5: Body Mass Index (BMI)")
    st.session_state.inputs['bmi'] = st.number_input("Enter the client's BMI:", min_value=10.0, max_value=60.0, value=float(st.session_state.inputs['bmi']), step=0.1)
    st.button("Next ➡️", on_click=next_step)

# --- STEP 3: DEPENDENTS ---
elif st.session_state.step == 3:
    st.subheader("Step 3 of 5: Family & Dependents")
    st.session_state.inputs['children'] = st.selectbox("Number of children/dependents:", [0, 1, 2, 3, 4, 5], index=int(st.session_state.inputs['children']))
    st.button("Next ➡️", on_click=next_step)

# --- STEP 4: TOBACCO USE ---
elif st.session_state.step == 4:
    st.subheader("Step 4 of 5: Health & Lifestyle")
    st.session_state.inputs['is_smoker'] = st.radio("Do you smoke tobacco?", ['no', 'yes'], index=0 if st.session_state.inputs['is_smoker']=='no' else 1)
    st.button("Next ➡️", on_click=next_step)

# --- STEP 5: GENDER ---
elif st.session_state.step == 5:
    st.subheader("Step 5 of 5: Demographics")
    st.session_state.inputs['is_female'] = st.radio("Gender?", ['Male', 'Female'], index=0 if st.session_state.inputs['is_female']=='Male' else 1)
    st.button("Generate Calculation 🎯", on_click=next_step)

# --- STEP 6: REALISTIC FINAL RESULTS PAGE ---
elif st.session_state.step == 6:
    st.balloons()
    st.markdown("<h2 style='text-align: center; color: #10B981;'>📊 Premium Assessment Complete</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # 1. Process client parameters to match ML formatting
    age = st.session_state.inputs['age']
    bmi = st.session_state.inputs['bmi']
    children = st.session_state.inputs['children']
    is_smoker = 1 if st.session_state.inputs['is_smoker'] == 'yes' else 0
    is_female = 1 if st.session_state.inputs['is_female'] == 'yes' else 0
    bmi_category_Obese = 1 if bmi >= 30.0 else 0

    input_df = pd.DataFrame([{
        'age': age, 'bmi': bmi, 'children': children,
        'is_smoker': is_smoker, 'is_female': is_female,
        'bmi_category_Obese': bmi_category_Obese
    }])

    # 2. Predict and Apply Indian Market Scaling
    pred_usd = model.predict(input_df)[0]
    INDIAN_MARKET_SCALING_FACTOR = 1.25
    final_premium_inr = max(6000, pred_usd * INDIAN_MARKET_SCALING_FACTOR)

    # 3. Render the client data summary table
    st.write("### 📋 Client Profile Summary")
    summary_data = {
        "Metric": ["Age", "BMI", "Children", "Smoker", "Female Status", "Obesity Marker"],
        "Provided Value": [f"{age} years", f"{bmi}", f"{children}", st.session_state.inputs['is_smoker'].capitalize(), st.session_state.inputs['is_female'].capitalize(), "Yes" if bmi_category_Obese else "No"]
    }
    st.table(pd.DataFrame(summary_data))

    # 4. Generate Interactive Risk Distribution Graph
    st.write("### 📈 Premium Distribution Curve")
    x_axis = np.linspace(5000, 50000, 100)
    # Create a bell curve distribution focused around the median market rates
    y_axis = np.exp(-((x_axis - 18000) ** 2) / (2 * 8000 ** 2))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_axis, y=y_axis, mode='lines', name='Market Baseline', line=dict(color='gray', width=2)))
    # Drop a vertical pin showing exactly where this specific client lands on the curve
    fig.add_trace(go.Scatter(x=[final_premium_inr, final_premium_inr], y=[0, max(y_axis)], mode='lines+markers', name='Your Quote', line=dict(color='red', width=4, dash='dash')))
    
    fig.update_layout(title="Where You Stand in the Insurance Pool", xaxis_title="Premium Cost (₹ INR)", yaxis_title="Risk Density Group", showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

    # 5. Display the Highlighted Final Premium Amount Box
    st.markdown(f"""
        <div style="background-color: #ECFDF5; border-left: 6px solid #10B981; padding: 20px; border-radius: 8px; text-align: center;">
            <p style="margin: 0; font-size: 1.1rem; color: #065F46; font-weight: bold;">Estimated Domestic Premium Quote</p>
            <h1 style="margin: 5px 0 0 0; color: #047857; font-size: 2.8rem;">₹{final_premium_inr:,.2f} <span style="font-size: 1.2rem;">INR / year</span></h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("\n")
    st.button("🔄 Calculate New Premium", on_click=restart)
