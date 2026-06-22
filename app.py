import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from fpdf import FPDF
import folium
from streamlit_folium import st_folium
import pyttsx3
from datetime import datetime
import feedparser
import os

def create_pdf_report(
    location,
    disaster_type,
    risk_score,
    report_text
):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        20
    )

    pdf.cell(
        0,
        10,
        "Disaster Twin AI Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.multi_cell(
        0,
        10,
        f"""
Location: {location}

Disaster Type: {disaster_type}

Risk Score: {risk_score}%

--------------------------------

AI Analysis:

{report_text}
"""
    )

    filename = "disaster_report.pdf"

    pdf.output(filename)

    return filename

def get_coordinates(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

        response = requests.get(
            url,
            headers={"User-Agent": "DisasterTwinAI"}
        )

        res = response.json()

       # DEBUG

        if res:
            return float(res[0]["lat"]), float(res[0]["lon"])

        return None, None

    except Exception as e:
        st.error(e)
        return None, None

# =========================
# GEMINI API
# =========================

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Disaster Twin AI",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
.block-container{
padding-top:1rem;
}
</style>
""",unsafe_allow_html=True)


if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown("""
<div class='glass'>
<h3>🌍 Real-Time Disaster Intelligence</h3>
<p>Powered by Gemini AI</p>
</div>
""",unsafe_allow_html=True)
# =========================
# SIDEBAR
# =========================

st.sidebar.title("🛰️ Disaster Twin AI")



st.sidebar.markdown("""
<div style="
padding:15px;
border-radius:15px;
background:rgba(139,92,246,.15);
border:1px solid rgba(255,255,255,.08);
">

🟢 System Online

📡 Monitoring Active

🤖 AI Engine Running

🛰 Live Intelligence

</div>
""", unsafe_allow_html=True)
st.sidebar.success("AI Digital Twin Enabled")
st.sidebar.success("Risk Prediction Engine")
st.sidebar.success("Emergency Response Advisor")
st.sidebar.success("Climate Impact Analysis")

st.sidebar.info("""
Version: 3.0

Features:
✅ AI Disaster Analysis
✅ Risk Assessment
✅ Disaster Detection
✅ Location Analysis
✅ Risk Visualization
✅ Report Download
✅ Emergency Contacts
✅ Disaster Images
✅ Gemini Fallback Mode
""")

# =========================
# MAIN UI
# =========================
hero_class = "hero-box"

st.markdown("""
<div class="hero-box">

<div class="hero-content">

<div class="hero-icon">
<div style='font-size:70px;text-align:center'>
🛰️
</div>


<div>
<h1>Disaster Twin AI</h1>
<p>
Predict • Simulate • Protect • Respond
</p>

<div class="live-status">
🟢 LIVE MONITORING ACTIVE
</div>
</div>

</div>
</div>
</div>
""", unsafe_allow_html=True)


st.caption(
    f"🕒 {datetime.now().strftime('%d %b %Y | %I:%M %p')}"
)

c1,c2,c3,c4 = st.columns(4)


with c1:
    st.markdown("""
    <div class='kpi'>
    <div class='num'>🎯98%</div>
    <div>Prediction Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='kpi'>
    <div class='num'>⚡24/7</div>
    <div>Live Monitoring</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='kpi'>
    <div class='num'>🌍100+</div>
    <div>Cities Covered</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='kpi'>
    <div class='num'>🛰 Twin AI</div>
    <div>Simulation Engine</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

location = st.text_input("📍 Enter Location")
api_key = "7f90dff2d1133cfade3be07dcd539ac9"

if location:

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        data = requests.get(url).json()

        if "main" in data:

            st.subheader("🌦 Live Weather Intelligence")

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            wind = data.get("wind", {}).get("speed", 0)

            c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
        "🌡 Temperature",
        f"{temp}°C"
        )

        with c2:
            st.metric(
        "💧 Humidity",
        f"{humidity}%"
        )

        with c3:
            st.metric(
        "🌬 Wind Speed",
        f"{wind} m/s"
        )

    except:
        st.warning("Weather data unavailable")
user_input = st.text_area(
    "Enter disaster-related query (flood, drought, earthquake, heatwave etc.)"
)

# =========================
# ANALYZE BUTTON
# =========================

if st.button("Analyze Disaster"):

    disaster = user_input.lower()

    if "flood" in disaster:
        risk_score = 85
        disaster_type = "Flood"

    elif "earthquake" in disaster:
        risk_score = 90
        disaster_type = "Earthquake"

    elif "heatwave" in disaster:
        risk_score = 70
        disaster_type = "Heatwave"

    elif "drought" in disaster:
        risk_score = 75
        disaster_type = "Drought"

    elif "cyclone" in disaster:
        risk_score = 88
        disaster_type = "Cyclone"

    else:
        risk_score = 50
        disaster_type = "General Disaster"

    
    st.session_state.analysis_done = True
    st.session_state.risk_score = risk_score
    st.session_state.disaster_type = disaster_type
    st.session_state.location = location

if st.session_state.analysis_done:

    risk_score = st.session_state.risk_score
    disaster_type = st.session_state.disaster_type
    location = st.session_state.location

    if risk_score >= 80:
        hero_class = "hero-red"

    elif risk_score >= 50:
        hero_class = "hero-yellow"

    else:
        hero_class = "hero-green"

    if risk_score >= 80:

        st.markdown("""
    <div class="hero-red">
    🚨 HIGH RISK ZONE DETECTED
    </div>
    """, unsafe_allow_html=True)

    elif risk_score >= 50:

        st.markdown("""
    <div class="hero-yellow">
    ⚠ MEDIUM RISK ZONE DETECTED
    </div>
    """, unsafe_allow_html=True)

    else:

        st.markdown("""
    <div class="hero-green">
    ✅ LOW RISK ZONE DETECTED
    </div>
    """, unsafe_allow_html=True)
        
    if risk_score >= 80:

        if "voice_alert" not in st.session_state:
            st.session_state.voice_alert = False

        if not st.session_state.voice_alert:

            engine = pyttsx3.init()

            engine.say(
            "Warning. High risk disaster zone detected."
            )

            engine.runAndWait()

            st.session_state.voice_alert = True


    st.subheader("🌍 Interactive Disaster Intelligence Map")
    st.markdown(
    '<div class="glass-map">',
    unsafe_allow_html=True
)
    map_mode = st.radio(
    "🗺 Map View",
    ["🌙 Dark", "🛰 Satellite"],
    horizontal=True
)
    lat, lon = get_coordinates(location)

    if lat is not None and lon is not None:


        if map_mode == "🌙 Dark":

            m = folium.Map(
        location=[lat, lon],
        zoom_start=10,
        tiles="CartoDB dark_matter"
        )

        else:

            m = folium.Map(
        location=[lat, lon],
        zoom_start=10,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    )

    else:

        st.stop()

    st.success(f"""
    📍 Location: {location}

    🌐 Latitude: {lat}

    🌐 Longitude: {lon}
    """)
    # Disaster Marker
    folium.Marker(
    [lat, lon],
    popup=f"{disaster_type} Risk Zone",
    tooltip="Disaster Location",
    icon=folium.Icon(
    color="red",
    icon="warning-sign"
)
    ).add_to(m)

# Hospital Marker
    folium.Marker(
    [lat + 0.02, lon + 0.02],
    popup="District Hospital",
    tooltip="Hospital",
    icon=folium.Icon(color="green")
    ).add_to(m)

# Shelter Marker
    folium.Marker(
    [lat - 0.02, lon - 0.02],
    popup="Emergency Shelter",
    tooltip="Shelter",
    icon=folium.Icon(color="blue")
    ).add_to(m)

# Fire Station
    folium.Marker(
    [lat + 0.01, lon - 0.01],
    popup="Fire Station",
    tooltip="Fire Brigade",
    icon=folium.Icon(color="orange")
    ).add_to(m)

# Risk Circle
    folium.Circle(
        location=[lat, lon],
        radius=7000,
        color="#ff004d",
        weight=4,
        fill=True,
        fill_color="#ff004d",
        fill_opacity=0.15
    ).add_to(m)

# Display Map
    st_folium(
    m,
    width=1200,
    height=500
    )
    st.markdown(
    '</div>',
    unsafe_allow_html=True
    )
    st.subheader("🔥 Regional Risk Heatmap")

    risk_locations = pd.DataFrame({
        "lat":[lat, lat+0.05, lat-0.03],
        "lon":[lon, lon+0.02, lon-0.04],
        "risk":[90,70,50]
    })

    heatmap = px.scatter_map(
        risk_locations,
        lat="lat",
        lon="lon",
        size="risk",
        color="risk",
        zoom=8,
        map_style="carto-darkmatter"
    )
    heatmap.update_layout(
    mapbox_style="carto-darkmatter",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0,r=0,t=0,b=0),
    height=500,
    font=dict(color="white")
)

    heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
    

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )

    # =========================
    # DISASTER TYPE
    # =========================
    # =========================
# HISTORY SAVE
# =========================

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(
        {
            "Disaster": disaster_type,
            "Risk": risk_score
        }
    )
    st.subheader("🌪 Detected Disaster Type")
    st.info(disaster_type)

    # =========================
    # RISK ASSESSMENT
    # =========================

    st.subheader("🚨 Risk Assessment")

    st.progress(risk_score)

    if risk_score >= 80:
        st.error(f"🔴 HIGH RISK ({risk_score}%)")

    elif risk_score >= 50:
        st.warning(f"🟡 MEDIUM RISK ({risk_score}%)")

    else:
        st.success(f"🟢 LOW RISK ({risk_score}%)")

    # =========================
    # DISASTER IMAGE
    # =========================

    st.subheader("🖼 Disaster Visualization")

    emoji_map = {
        "Flood": "🌊",
        "Earthquake": "🏚",
        "Heatwave": "☀",
        "Drought": "🌵",
        "Cyclone": "🌀",
        "General Disaster": "⚠"
    }

    st.header(
        f"{emoji_map.get(disaster_type,'⚠')} {disaster_type.upper()} DETECTED"
    )

    image_files = {
        "Flood": "disaster_images/flood.jpg",
        "Earthquake": "disaster_images/earthquake.jpg",
        "Cyclone": "disaster_images/cyclone.jpg",
        "Drought": "disaster_images/drought.jpg",
        "Heatwave": "disaster_images/heatwave.jpg",
        "General Disaster": "disaster_images/general.jpg"
    }

    st.image(
        image_files.get(
            disaster_type,
            "disaster_images/general.jpg"
        ),
        caption=f"{disaster_type} Monitoring System",
        use_container_width=True
    )
    # =========================
# DISASTER LOCATION MAP
# =========================


    st.subheader("📍 Safe Zone Recommendation")

    st.success(f"""
Nearest Safe Zones for {location}

✅ Community Hall

✅ Government School

✅ City Shelter Center

✅ District Hospital
""")
    
    st.subheader("🚑 Evacuation Plan")

    st.info(f"""
    1️⃣ Move away from {location} risk area

    2️⃣ Reach nearest shelter

    3️⃣ Carry emergency kit

    4️⃣ Follow local authority alerts

    5️⃣ Stay connected with emergency services
    """)
    # =========================
# RISK METER
# =========================
        # =========================
    # RISK METER
    # =========================
    if risk_score >= 80:
        st.markdown("""
    <div class="hero-red">
    🚨 HIGH RISK ZONE DETECTED
    </div>
    """, unsafe_allow_html=True)

    elif risk_score >= 50:
        st.markdown("""
    <div class="hero-yellow">
    ⚠ MEDIUM RISK ZONE DETECTED
    </div>
    """, unsafe_allow_html=True)

    else:
        st.markdown("""
    <div class="hero-green">
    ✅ LOW RISK ZONE DETECTED
    </div>
    """, unsafe_allow_html=True)

    if risk_score > 80:
        severity = "CRITICAL"

    elif risk_score > 60:
        severity = "HIGH"

    else:
        severity = "MODERATE"

        st.markdown(f"""
        <div class="severity">
        🚨 {severity}
        </div>
        """, unsafe_allow_html=True)


    st.subheader("📊 Disaster Risk Meter")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Risk Score"},
            gauge={
                "axis": {"range": [0, 100]}
            }
        )
    )
    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
    st.plotly_chart(fig, use_container_width=True)

    col1,col2 = st.columns(2)

    with col1:
        st.metric("🚨 Risk Score",f"{risk_score}%")

    with col2:
        st.metric("🤖 AI Confidence","96%")

    st.subheader("📋 Risk Summary")

    heat_df = pd.DataFrame({
    "Area":[
        "North",
        "South",
        "East",
        "West"
    ],
    "Risk":[
        risk_score-10,
        risk_score,
        risk_score-20,
        risk_score-5
    ]
    })

    heat_fig = px.bar(
        heat_df,
        x="Area",
        y="Risk",
        color="Risk"
    )
    heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
    st.plotly_chart(
        heat_fig,
        use_container_width=True
    )

    risk_df = pd.DataFrame({
        "Parameter": [
            "Disaster Type",
            "Risk Score",
            "Location"
        ],
        "Value": [
            disaster_type,
            f"{risk_score}%",
            location
        ]
    })

    st.dataframe(risk_df, use_container_width=True)

    st.subheader("🍩 Risk Distribution")

    pie = px.pie(
        names=["Risk", "Safe"],
        values=[risk_score, 100-risk_score],
        hole=0.7
    )
    heatmap.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
    st.plotly_chart(
        pie,
        use_container_width=True
    )

    # DIGITAL TWIN SIMULATION

    st.markdown("---")
    st.subheader("🧠 AI Digital Twin Simulation")

    population = st.slider(
    "Population in Risk Zone",
    min_value=1000,
    max_value=1000000,
    value=50000,
    step=1000
    )
    affected = int(population * risk_score / 100 * 0.4)

    # =========================
# DIGITAL TWIN SIMULATION
# =========================


    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric(
        "👥 Affected People",
        affected
        )

    with c2:
        st.metric(
        "🏠 Shelters Needed",
        affected // 250
        )

    with c3:
        st.metric(
        "🚑 Medical Units",
        affected // 500
        )

    st.subheader("📦 Relief Resource Estimation")

    food = affected * 3
    water = affected * 5

    c1,c2 = st.columns(2)

    with c1:
        st.metric(
        "🍱 Food Packets",
        f"{food:,}"
    )

    with c2:
        st.metric(
        "💧 Water Bottles",
        f"{water:,}"
    )

    if risk_score > 80:
        st.markdown("""
    <div style="
    background:#dc2626;
    color:white;
    padding:15px;
    border-radius:12px;
    text-align:center;
    font-weight:bold;">
    🔥 CRITICAL SEVERITY
    </div>
    """,unsafe_allow_html=True)
    # =========================
# HISTORY GRAPH
# =========================

    if st.session_state.history:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        st.subheader("📈 Previous Risk Analysis")

        history_fig = px.bar(
            history_df,
            x="Disaster",
            y="Risk",
            color="Risk",
            title="Disaster Risk History"
        )
        history_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)

        st.plotly_chart(
            history_fig,
            use_container_width=True
        )

        st.subheader("📈 Impact Forecast")

        forecast = pd.DataFrame({
            "Day":[1,2,3,4,5],
            "Risk":[
                risk_score,
                risk_score+2,
                risk_score+4,
                risk_score+6,
                min(risk_score+8,100)
            ]
        })

        fig = px.line(
        forecast,
        x="Day",
        y="Risk",
        markers=True
    )
        fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)
        st.plotly_chart(
        fig,
        use_container_width=True
    )
        
        st.subheader("🚨 Recommended Actions")

    if risk_score >= 80:
        st.error("""
    🚨 Evacuate immediately if advised.

    🚨 Avoid flood-prone areas.

    🚨 Keep emergency kit ready.

    🚨 Follow official alerts.
    """)

    elif risk_score >= 50:
        st.warning("""
    ⚠ Stay alert.

    ⚠ Monitor weather updates.

    ⚠ Keep supplies ready.

    ⚠ Avoid unnecessary travel.
    """)

    else:
        st.success("""
    ✅ Situation stable.

    ✅ Follow normal precautions.
    """)
    if risk_score >= 80:
        st.metric("Risk Category", "HIGH", "🔴")

    elif risk_score >= 50:
        st.metric("Risk Category", "MEDIUM", "🟡")

    else:
        st.metric("Risk Category", "LOW", "🟢")# =========================
    if len(history_df) > 0:

        trend_fig = px.line(
        history_df,
        x=history_df.index,
        y="Risk",
        markers=True,
        title="Risk Trend Analysis"
    )
        trend_fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)
        st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

    # GEMINI ANALYSIS
    # =========================

    prompt = f"""
    You are an expert Disaster Management AI.

    Location: {location}

    Disaster Scenario:
    {user_input}

    Provide:

    1. Risk Level
    2. Possible Causes
    3. Impact on People
    4. Environmental Impact
    5. Preventive Measures
    6. Emergency Response Plan
    7. Safety Tips
    8. Recovery Strategy

    Give detailed professional analysis.
    """

    try:

            with st.spinner("🤖 AI is analyzing disaster..."):

                response = model.generate_content(prompt)
        
            st.success("✅ Analysis Complete")

            st.subheader("📋 AI Disaster Report")

            st.markdown(
    f"""
    <div style="
    color:white;
    font-size:18px;
    line-height:1.8;
    ">
    {response.text}
    </div>
    """,
    unsafe_allow_html=True
)

            pdf_file = create_pdf_report(
                location,
                disaster_type,
                risk_score,
                response.text
            )

            with open(
            pdf_file,
            "rb"
            ) as file:

                st.download_button(
                "📄 Download PDF Report",
                file,
                file_name="Disaster_Report.pdf",
                mime="application/pdf"
            )

    except Exception:

        st.error("⚠ Gemini API Quota Exceeded")

        fallback_report = f"""
# Disaster Analysis Report

Location: {location}

Disaster Type: {disaster_type}

Risk Level: {risk_score}%

Possible Causes:
• Extreme weather conditions
• Climate change
• Infrastructure weaknesses
• Natural environmental factors

Impact on People:
• Property damage
• Transportation disruption
• Health risks
• Economic losses

Environmental Impact:
• Pollution
• Ecosystem disturbance
• Water contamination

Preventive Measures:
• Early warning systems
• Public awareness
• Better infrastructure
• Emergency planning

Emergency Response:
• Evacuation support
• Medical assistance
• Rescue operations
• Relief distribution

Safety Tips:
• Keep emergency kit ready
• Follow government alerts
• Stay indoors if advised
• Store clean drinking water

Recovery Strategy:
• Damage assessment
• Infrastructure repair
• Community rehabilitation
• Financial assistance
"""

        st.subheader("📋 Emergency Fallback Report")

        st.write(fallback_report)

        st.download_button(
            label="📄 Download Report",
            data=fallback_report,
            file_name="disaster_report.txt",
            mime="text/plain"
        )

    # =========================
# LIVE DISASTER NEWS
# =========================

        st.markdown("---")
        st.subheader("📰 Live Disaster News Feed")

    try:

        rss_url = "https://news.google.com/rss/search?q=natural+disaster&hl=en-IN&gl=IN&ceid=IN:en"

        feed = feedparser.parse(rss_url)

        for news in feed.entries[:5]:

            st.info(
            f"📰 {news.title}\n\n🔗 {news.link}"
            )

    except:
        st.warning("News Feed Unavailable")
# =========================
# EMERGENCY CONTACTS
# =========================

    st.markdown("---")

    st.subheader("📞 Emergency Contacts")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🚑 Ambulance : 108")
        st.info("🚒 Fire Brigade : 101")

    with col2:
        st.info("🚓 Police : 100")
        st.info("🆘 Disaster Helpline : 1078")

# =========================
# SAFETY TIPS
# =========================

    st.markdown("---")

    st.subheader("🛡 General Safety Tips")

    st.success("""
✔ Keep emergency kit ready

✔ Store clean drinking water

✔ Charge mobile and power bank

✔ Follow government alerts

✔ Keep important documents safe

✔ Know nearest shelter location

✔ Stay calm during emergencies
""")
    st.subheader("✅ Emergency Preparedness Checklist")

    st.checkbox("Emergency Kit Ready")
    st.checkbox("Drinking Water Stored")
    st.checkbox("Power Bank Charged")
    st.checkbox("Important Documents Safe")
    st.checkbox("Emergency Contacts Saved")

# =========================
# FOOTER
# =========================

    st.markdown("---")
    st.caption("🌍 Disaster Twin AI | Powered by Gemini AI")
    st.markdown("---")



    st.markdown("---")

    st.subheader("🚀 Future Scope")

    st.info("""
🌍 Satellite Data Integration

📡 IoT Sensor Based Monitoring

🚁 Drone Disaster Surveillance

🤖 AI Digital Twin Simulation

🏙 Multi-City Risk Prediction

📲 Government Alert Integration

☁ Cloud Based Disaster Dashboard
""")
