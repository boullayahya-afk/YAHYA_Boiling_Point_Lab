import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="YAHYA | Boiling Point Lab", page_icon="🧪", layout="wide")

# Antoine equation: log10(Psat in mmHg) = A - B / (T in °C + C)
DATA = {
    "Water": {"formula":"H₂O","A":8.07131,"B":1730.63,"C":233.426,"lo":1,"hi":100,"bp":100.00},
    "Ethanol": {"formula":"C₂H₆O","A":8.20417,"B":1642.89,"C":230.300,"lo":-2,"hi":80,"bp":78.37},
    "Methanol": {"formula":"CH₄O","A":8.08097,"B":1582.27,"C":239.700,"lo":-44,"hi":65,"bp":64.70},
    "Acetone": {"formula":"C₃H₆O","A":7.11714,"B":1210.59,"C":229.664,"lo":-55,"hi":55,"bp":56.05},
    "Benzene": {"formula":"C₆H₆","A":6.90565,"B":1211.033,"C":220.790,"lo":8,"hi":80,"bp":80.10},
    "Toluene": {"formula":"C₇H₈","A":6.95464,"B":1344.80,"C":219.480,"lo":6,"hi":100,"bp":110.60},
    "n-Hexane": {"formula":"C₆H₁₄","A":6.87630,"B":1171.53,"C":224.000,"lo":-25,"hi":69,"bp":68.70},
    "Chloroform": {"formula":"CHCl₃","A":6.95465,"B":1170.97,"C":226.232,"lo":-30,"hi":61,"bp":61.20},
}
MMHG_PER_KPA = 7.50061683

def psat(name, t):
    d = DATA[name]
    return 10 ** (d["A"] - d["B"] / (t + d["C"]))

def boiling_temp(name, p_mmhg):
    d = DATA[name]
    if p_mmhg <= 0:
        raise ValueError("La pression doit être strictement positive.")
    return d["B"] / (d["A"] - np.log10(p_mmhg)) - d["C"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:radial-gradient(circle at 8% 4%,#e7f3ff 0,transparent 27%),linear-gradient(135deg,#f5f9ff,#edf4fc)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#082b55,#104b82)}
[data-testid="stSidebar"] *{color:#f5f9ff!important}
.hero{padding:30px 34px;border-radius:22px;color:white;background:linear-gradient(115deg,#082b55,#1265ad 65%,#2995d6);box-shadow:0 12px 32px #0b3a7028;animation:rise .7s ease-out}
.hero h1{font-size:2.1rem;font-weight:800;margin:0 0 8px}
.hero p{margin:0;color:#dceeff}
.metric{background:white;border:1px solid #d8e8f8;border-radius:16px;padding:18px;box-shadow:0 7px 22px #0b3a700c}
.metric small{color:#64809b}.metric strong{display:block;font-size:1.8rem;color:#103d6b}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
div.stButton>button{background:linear-gradient(90deg,#0b4b87,#1686c9);color:white;border:0;border-radius:10px;font-weight:700}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧪 YAHYA LAB")
    st.caption("THERMODYNAMICS • PHASE EQUILIBRIUM")
    page = st.radio("NAVIGATION", ["Dashboard","Boiling point calculator","Vapour-pressure curve","Molecule comparison","Scientific method"])
    st.divider()
    st.markdown("**Created by YAHYA**")
    st.caption("Engineering project • Antoine model")

st.markdown('<div class="hero"><h1>🧪 YAHYA | BOILING POINT LAB</h1><p>Explore pure substances, calculate boiling temperatures and analyse the influence of pressure.</p></div>', unsafe_allow_html=True)

if page == "Dashboard":
    st.subheader("Welcome to your thermodynamics workspace")
    a,b,c = st.columns(3)
    for col,label,value,note in [(a,"COMPOUNDS IN DATABASE","08","Pure substances"),(b,"THERMODYNAMIC MODEL","Antoine","Empirical correlation"),(c,"REFERENCE PRESSURE","760 mmHg","≈ 101.325 kPa")]:
        with col:
            st.markdown(f'<div class="metric"><small>{label}</small><strong>{value}</strong><small>{note}</small></div>',unsafe_allow_html=True)
    st.subheader("Available compounds")
    st.dataframe(pd.DataFrame([{"Compound":n,"Formula":d["formula"],"Normal boiling point (°C)":d["bp"],"Validity range (°C)":f'{d["lo"]} to {d["hi"]}'} for n,d in DATA.items()]),use_container_width=True,hide_index=True)
    st.info("Choose a tool from the navigation panel.")
elif page == "Boiling point calculator":
    st.subheader("Boiling temperature at a specified absolute pressure")
    left,right=st.columns(2)
    with left:
        name=st.selectbox("Pure substance",list(DATA))
        unit=st.selectbox("Pressure unit",["kPa","mmHg","bar","atm"])
        defaults={"kPa":101.325,"mmHg":760.0,"bar":1.01325,"atm":1.0}
        p=st.number_input("Absolute pressure",min_value=0.001,value=defaults[unit])
        run=st.button("Calculate boiling temperature",use_container_width=True)
    with right:
        d=DATA[name]
        st.markdown(f"**{name} ({d['formula']})**")
        st.write(f"Antoine constants: A = {d['A']}, B = {d['B']}, C = {d['C']}")
        st.write(f"Validity range: {d['lo']} °C to {d['hi']} °C")
        st.latex(r"\\log_{10}(P_{sat})=A-\\frac{B}{T+C}")
        st.caption("P in mmHg; T in °C.")
    if run:
        factor={"kPa":MMHG_PER_KPA,"mmHg":1.0,"bar":750.061683,"atm":760.0}[unit]
        result=boiling_temp(name,p*factor)
        st.success(f"Estimated boiling temperature: {result:.2f} °C")
        x,y,z=st.columns(3)
        x.metric("Boiling temperature",f"{result:.2f} °C")
        y.metric("Input pressure",f"{p:g} {unit}")
        z.metric("Normal boiling point",f"{d['bp']:.2f} °C")
        if not d["lo"] <= result <= d["hi"]:
            st.warning("Result outside the stated Antoine validity range: this is an extrapolation.")
        st.latex(r"T=\\frac{B}{A-\\log_{10}(P)}-C")
elif page == "Vapour-pressure curve":
    st.subheader("Saturation pressure versus temperature")
    name=st.selectbox("Compound",list(DATA))
    d=DATA[name]
    lo,hi=st.slider("Temperature interval (°C)",int(d["lo"]),int(d["hi"]),(int(d["lo"]),int(d["hi"])))
    ts=np.linspace(lo,hi,250)
    fig=go.Figure(go.Scatter(x=ts,y=[psat(name,t) for t in ts],mode="lines",name=name,line=dict(width=3,color="#137fc1"),fill="tozeroy",fillcolor="rgba(19,127,193,.10)"))
    fig.add_hline(y=760,line_dash="dash",line_color="#e28a28",annotation_text="Atmospheric pressure (760 mmHg)")
    fig.update_layout(template="plotly_white",height=470,xaxis_title="Temperature (°C)",yaxis_title="Saturation pressure (mmHg)")
    st.plotly_chart(fig,use_container_width=True)
    st.caption("Boiling occurs when saturation pressure equals external absolute pressure.")
elif page == "Molecule comparison":
    st.subheader("Compare pure substances")
    selected=st.multiselect("Choose compounds",list(DATA),default=["Water","Ethanol","Acetone"])
    if selected:
        df=pd.DataFrame([{"Compound":n,"Formula":DATA[n]["formula"],"Normal boiling point (°C)":DATA[n]["bp"]} for n in selected]).sort_values("Normal boiling point (°C)")
        st.dataframe(df,use_container_width=True,hide_index=True)
        fig=go.Figure(go.Bar(x=df["Compound"],y=df["Normal boiling point (°C)"],text=df["Normal boiling point (°C)"],textposition="outside",marker_color="#147fbd"))
        fig.update_layout(template="plotly_white",height=430,yaxis_title="Normal boiling point (°C)")
        st.plotly_chart(fig,use_container_width=True)
else:
    st.subheader("Scientific method and model assumptions")
    st.write("Objective: estimate the boiling temperature of a pure substance at a specified absolute pressure.")
    st.latex(r"P_{sat}(T_{eb})=P_{ext}")
    st.latex(r"\\log_{10}(P_{sat})=A-\\frac{B}{T+C}")
    st.write("Procedure: select the substance, convert pressure to mmHg, invert the Antoine equation, then check the validity range.")
    st.warning("Antoine constants are empirical and valid only over stated temperature ranges. Verify all constants and ranges against the references required by your course before final submission.")
    st.write("Assumptions: pure substance, liquid-vapour equilibrium, absolute pressure (not gauge pressure).")
    st.write("Author: YAHYA BOULLA")

st.markdown("---")
st.caption("YAHYA BOULLA • BOILING POINT LAB • Educational thermodynamics tool")
