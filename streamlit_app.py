import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="RMR Calculator",
    page_icon="🪨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Custom color scheme */
    :root {
        --primary: #2E86AB;
        --secondary: #A23B72;
        --success: #06A77D;
        --warning: #F18F01;
        --danger: #C1121F;
        --light: #F8F9FA;
        --dark: #1B1D1F;
    }
    
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .header-container h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .header-container p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Section card styling */
    .section-card {
        background: white;
        border: 2px solid #E8E8E8;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .section-card:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
        border-color: #2E86AB;
    }
    
    /* Result panel styling */
    .result-panel {
        background: linear-gradient(135deg, #06A77D 0%, #087E7F 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        box-shadow: 0 6px 20px rgba(6,167,125,0.3);
    }
    
    .result-panel h2 {
        margin-top: 0;
        font-size: 1.8rem;
    }
    
    /* Classification badge styling */
    .classification-badge {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
    
    .badge-class-i {
        background-color: #06A77D;
        color: white;
    }
    
    .badge-class-ii {
        background-color: #2E86AB;
        color: white;
    }
    
    .badge-class-iii {
        background-color: #F18F01;
        color: white;
    }
    
    .badge-class-iv {
        background-color: #E76F51;
        color: white;
    }
    
    .badge-class-v {
        background-color: #C1121F;
        color: white;
    }
    
    /* Metric boxes */
    .metric-box {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    
    .metric-box h4 {
        margin: 0 0 0.5rem 0;
        color: #2E86AB;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-box .value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1B1D1F;
        margin: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E86AB 0%, #1B5E8A 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(46,134,171,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 6px 16px rgba(46,134,171,0.4);
        transform: translateY(-2px);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #F8F9FA;
        border-radius: 8px;
    }
    
    /* Table styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    
    .dataframe th {
        background: #2E86AB;
        color: white;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
    }
    
    .dataframe td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #E8E8E8;
    }
    
    .dataframe tr:hover {
        background-color: #F8F9FA;
    }
</style>
""", unsafe_allow_html=True)

# RMR CALCULATION FUNCTIONS

def rating_from_strength(test_type, value):
    """Calculate rating based on rock strength test"""
    test_type = test_type.strip().lower()
    
    if test_type == "point_load":
        if value > 10:
            rating = 15
        elif 4 <= value <= 10:
            rating = 12
        elif 2 <= value < 4:
            rating = 7
        elif 1 <= value < 2:
            rating = 4
        else:
            rating = None
    elif test_type == "ucs":
        if value > 250:
            rating = 15
        elif 100 <= value <= 250:
            rating = 12
        elif 50 <= value < 100:
            rating = 7
        elif 25 <= value < 50:
            rating = 4
        elif 5 <= value < 25:
            rating = 2
        elif 1 <= value < 5:
            rating = 1
        else:
            rating = 0
    else:
        rating = None
    
    return rating


def rating_from_rqd(rqd):
    """Calculate rating from RQD (Rock Quality Designation)"""
    if 90 <= rqd <= 100:
        rating = 20
    elif 75 <= rqd < 90:
        rating = 17
    elif 50 <= rqd < 75:
        rating = 13
    elif 25 <= rqd < 50:
        rating = 8
    else:
        rating = 5
    return rating


def rating_from_spacing(spacing):
    """Calculate rating from spacing of discontinuities"""
    if spacing > 2000:
        rating = 20
    elif 600 <= spacing <= 2000:
        rating = 15
    elif 200 <= spacing < 600:
        rating = 10
    elif 60 <= spacing < 200:
        rating = 8
    else:
        rating = 5
    return rating


def rating_from_length(length):
    """Calculate rating from length of discontinuity"""
    if length < 1:
        rating = 6
    elif 1 <= length < 3:
        rating = 4
    elif 3 <= length < 10:
        rating = 2
    elif 10 <= length <= 20:
        rating = 1
    else:
        rating = 0
    return rating


def rating_from_separation(separation):
    """Calculate rating from separation of discontinuities"""
    if separation == 0:
        rating = 6
    elif separation < 0.1:
        rating = 5
    elif 0.1 <= separation <= 1:
        rating = 4
    elif 1 < separation <= 5:
        rating = 1
    else:
        rating = 0
    return rating


def rating_from_roughness(roughness):
    """Calculate rating from roughness of discontinuities"""
    roughness = roughness.strip().lower()
    ratings = {
        "very rough": 6,
        "rough": 5,
        "slightly rough": 3,
        "smooth": 1,
        "slickensided": 0
    }
    return ratings.get(roughness, 0)


def rating_from_infilling(infill_type, thickness=None):
    """Calculate rating from infilling type and thickness"""
    infill_type = infill_type.strip().lower()
    
    if infill_type == "none":
        rating = 6
    elif infill_type == "hard":
        if thickness is not None and thickness < 5:
            rating = 4
        elif thickness is not None and thickness > 5:
            rating = 2
        else:
            rating = 0
    elif infill_type == "soft":
        if thickness is not None and thickness < 5:
            rating = 2
        elif thickness is not None and thickness > 5:
            rating = 0
        else:
            rating = 0
    else:
        rating = 0
    
    return rating


def rating_from_weathering(weathering):
    """Calculate rating from weathering condition"""
    weathering = weathering.strip().lower()
    ratings = {
        "unweathered": 6,
        "slightly weathered": 5,
        "moderately weathered": 3,
        "highly weathered": 1,
        "decomposed": 0
    }
    return ratings.get(weathering, 0)


def rating_from_inflow(inflow):
    """Calculate rating from groundwater inflow"""
    if inflow == 0:
        rating = 15
    elif inflow < 10:
        rating = 10
    elif 10 <= inflow <= 25:
        rating = 7
    elif 25 < inflow <= 125:
        rating = 4
    else:
        rating = 0
    return rating


def rating_from_pw_sigma1(ratio):
    """Calculate rating from pore water pressure ratio"""
    if ratio == 0:
        rating = 15
    elif 0 < ratio <= 0.1:
        rating = 10
    elif 0.1 < ratio <= 0.2:
        rating = 7
    elif 0.2 < ratio <= 0.5:
        rating = 4
    else:
        rating = 0
    return rating


def rating_from_condition(condition):
    """Calculate rating from general groundwater condition"""
    condition = condition.strip().lower()
    ratings = {
        "completely dry": 15,
        "damp": 10,
        "wet": 7,
        "dripping": 4,
        "flowing": 0
    }
    return ratings.get(condition, 0)


def get_orientation_adjustment(structure_type, orientation):
    """Get adjustment rating based on discontinuity orientation"""
    structure_type = structure_type.strip().lower()
    orientation = orientation.strip().lower()
    
    adjustments = {
        "tunnels": {
            "very favourable": 0,
            "favourable": -2,
            "fair": -5,
            "unfavourable": -10,
            "very unfavourable": -12
        },
        "foundations": {
            "very favourable": 0,
            "favourable": -2,
            "fair": -7,
            "unfavourable": -15,
            "very unfavourable": -25
        },
        "slopes": {
            "very favourable": 0,
            "favourable": -5,
            "fair": -25,
            "unfavourable": -50,
            "very unfavourable": -60
        }
    }
    
    return adjustments.get(structure_type, {}).get(orientation, 0)


def get_classification(rmr_value):
    """Get RMR classification based on RMR value"""
    if rmr_value >= 81:
        return "Class I: Very Good Rock", "🟢", "badge-class-i"
    elif rmr_value >= 61:
        return "Class II: Good Rock", "🟢", "badge-class-ii"
    elif rmr_value >= 41:
        return "Class III: Fair Rock", "🟡", "badge-class-iii"
    elif rmr_value >= 21:
        return "Class IV: Poor Rock", "🟠", "badge-class-iv"
    else:
        return "Class V: Very Poor Rock", "🔴", "badge-class-v"


# STREAMLIT APP

# Header
st.markdown("""
<div class="header-container">
    <h1>🪨 Rock Mass Rating Calculator</h1>
    <p>Professional RMR Classification System | Based on Bieniawski's Method</p>
</div>
""", unsafe_allow_html=True)

st.markdown("**Calculate the RMR classification for rock masses to assess engineering properties and stability.**")

# Initialize session state
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# Create tabs for organization
tab1, tab2, tab3 = st.tabs(["📊 Input Parameters", "🔍 Discontinuity Details", "📈 Results"])

# ============ TAB 1: Input Parameters ============
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Parameter 1: Rock Strength")
        type_test = st.radio(
            "Select test type",
            ["UCS (Uniaxial Compressive Strength)", "Point Load Index"],
            key="type_test"
        )
        
        if "UCS" in type_test:
            strength_value = st.number_input(
                "UCS Value (MPa)",
                min_value=0.0,
                value=100.0,
                step=10.0,
                key="ucs_value"
            )
            r1 = rating_from_strength('ucs', strength_value)
        else:
            strength_value = st.number_input(
                "Point Load Index (MPa)",
                min_value=0.0,
                value=5.0,
                step=0.5,
                key="point_load_value"
            )
            r1 = rating_from_strength('point_load', strength_value)
            if r1 is None:
                r1 = 0
        
        st.markdown(f"<div class='metric-box'><h4>Rating R1 (Strength)</h4><p class='value'>{r1}</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Parameter 2: Rock Quality Designation")
        rqd_value = st.slider(
            "RQD (%)",
            min_value=0,
            max_value=100,
            value=75,
            step=5,
            key="rqd"
        )
        r2 = rating_from_rqd(rqd_value)
        st.markdown(f"<div class='metric-box'><h4>Rating R2 (RQD)</h4><p class='value'>{r2}</p></div>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### Parameter 3: Spacing of Discontinuities")
        spacing_value = st.number_input(
            "Spacing (mm)",
            min_value=0.0,
            value=500.0,
            step=50.0,
            key="spacing"
        )
        r3 = rating_from_spacing(spacing_value)
        st.markdown(f"<div class='metric-box'><h4>Rating R3 (Spacing)</h4><p class='value'>{r3}</p></div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("### Parameter 5: Groundwater Assessment")
        gw_choice = st.radio(
            "Groundwater assessment method",
            ["Inflow Rate", "Pore Water Pressure Ratio", "General Conditions"],
            key="gw_choice"
        )
        
        if gw_choice == "Inflow Rate":
            inflow_value = st.number_input(
                "Inflow (L/min)",
                min_value=0.0,
                value=0.0,
                step=5.0,
                key="inflow_value"
            )
            r5 = rating_from_inflow(inflow_value)
        elif gw_choice == "Pore Water Pressure Ratio":
            ratio_value = st.slider(
                "Pw/σ1 Ratio",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.05,
                key="ratio_value"
            )
            r5 = rating_from_pw_sigma1(ratio_value)
        else:
            condition_value = st.selectbox(
                "General condition",
                ["Completely Dry", "Damp", "Wet", "Dripping", "Flowing"],
                key="general_condition_value"
            )
            r5 = rating_from_condition(condition_value)
        
        st.markdown(f"<div class='metric-box'><h4>Rating R5 (Groundwater)</h4><p class='value'>{r5}</p></div>", unsafe_allow_html=True)

# ============ TAB 2: Discontinuity Details ============
with tab2:
    st.markdown("### Parameter 4: Condition of Discontinuities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Length of Discontinuity (m)**")
        length_value = st.number_input(
            "Length (m)",
            min_value=0.0,
            value=5.0,
            step=0.5,
            key="length",
            label_visibility="collapsed"
        )
        r4a = rating_from_length(length_value)
        st.markdown(f"<div class='metric-box'><h4>R4a</h4><p class='value'>{r4a}</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Separation (mm)**")
        separation_value = st.number_input(
            "Separation (mm)",
            min_value=0.0,
            value=0.5,
            step=0.1,
            key="separation",
            label_visibility="collapsed"
        )
        r4b = rating_from_separation(separation_value)
        st.markdown(f"<div class='metric-box'><h4>R4b</h4><p class='value'>{r4b}</p></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("**Roughness**")
        roughness_value = st.selectbox(
            "Roughness",
            ["Very Rough", "Rough", "Slightly Rough", "Smooth", "Slickensided"],
            key="roughness",
            label_visibility="collapsed"
        )
        r4c = rating_from_roughness(roughness_value)
        st.markdown(f"<div class='metric-box'><h4>R4c</h4><p class='value'>{r4c}</p></div>", unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("**Infilling Type**")
        infill_value = st.selectbox(
            "Infilling type",
            ["None", "Soft Filling", "Hard Filling"],
            key="infilling_type",
            label_visibility="collapsed"
        )
        
        thickness = None
        if "Soft" in infill_value:
            thickness = st.number_input(
                "Soft infill thickness (mm)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                key="soft_thickness"
            )
            r4d = rating_from_infilling('soft', thickness)
        elif "Hard" in infill_value:
            thickness = st.number_input(
                "Hard infill thickness (mm)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                key="hard_thickness"
            )
            r4d = rating_from_infilling('hard', thickness)
        else:
            r4d = rating_from_infilling('none')
        
        st.markdown(f"<div class='metric-box'><h4>R4d</h4><p class='value'>{r4d}</p></div>", unsafe_allow_html=True)
    
    with col5:
        st.markdown("**Weathering**")
        weathering_value = st.selectbox(
            "Weathering",
            ["Unweathered", "Slightly Weathered", "Moderately Weathered", "Highly Weathered", "Decomposed"],
            key="weathering",
            label_visibility="collapsed"
        )
        r4e = rating_from_weathering(weathering_value)
        st.markdown(f"<div class='metric-box'><h4>R4e</h4><p class='value'>{r4e}</p></div>", unsafe_allow_html=True)
    
    r4 = r4a + r4b + r4c + r4d + r4e
    st.markdown(f"<div class='metric-box' style='border-left-color: #A23B72; background: #FFF5F8;'><h4>Total R4 (Condition)</h4><p class='value' style='color: #A23B72;'>{r4}</p></div>", unsafe_allow_html=True)

# ============ TAB 3: Results ============
with tab3:
    st.markdown("### Orientation Adjustment (Table B)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        structure_type = st.selectbox(
            "Structure type",
            ["Tunnels", "Foundations", "Slopes"],
            key="structure_type",
            label_visibility="collapsed"
        )
    
    with col2:
        orientation_value = st.selectbox(
            "Discontinuity orientation",
            ["Very Favourable", "Favourable", "Fair", "Unfavourable", "Very Unfavourable"],
            key="orientation",
            label_visibility="collapsed"
        )
    
    adjustment = get_orientation_adjustment(structure_type, orientation_value)
    
    st.markdown(f"<div class='metric-box' style='border-left-color: #E76F51;'><h4>Orientation Adjustment</h4><p class='value' style='color: #E76F51;'>{adjustment}</p></div>", unsafe_allow_html=True)
    
    st.divider()
    
    # Calculate final RMR
    basic_rmr = r1 + r2 + r3 + r4 + r5
    final_rmr = basic_rmr + adjustment
    
    # Get classification
    classification, emoji, badge_class = get_classification(final_rmr)
    
    # Display results
    st.markdown("### 📊 RMR Calculation Summary")
    
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.markdown(f"<div class='metric-box'><h4>R1 (Strength)</h4><p class='value'>{r1}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'><h4>R2 (RQD)</h4><p class='value'>{r2}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'><h4>R3 (Spacing)</h4><p class='value'>{r3}</p></div>", unsafe_allow_html=True)
    
    with result_col2:
        st.markdown(f"<div class='metric-box'><h4>R4 (Condition)</h4><p class='value'>{r4}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'><h4>R5 (Groundwater)</h4><p class='value'>{r5}</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box' style='border-left-color: #E76F51;'><h4>Adjustment</h4><p class='value' style='color: #E76F51;'>{adjustment}</p></div>", unsafe_allow_html=True)
    
    with result_col3:
        st.markdown(f"""
        <div class='metric-box' style='border-left-color: #2E86AB; background: #F0F7FF;'>
            <h4>Basic RMR</h4>
            <p class='value' style='color: #2E86AB;'>{basic_rmr}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Final classification
    st.markdown("### 🎯 Final RMR Classification")
    
    final_rmr_col1, final_rmr_col2 = st.columns([1, 1])
    
    with final_rmr_col1:
        st.markdown(f"""
        <div class='result-panel'>
            <h2 style='margin-top: 0;'>Final RMR Score</h2>
            <div style='font-size: 3.5rem; font-weight: 700; color: white; text-align: center; margin: 1rem 0;'>
                {final_rmr:.1f}
            </div>
            <div class='classification-badge {badge_class}' style='width: 100%; text-align: center; font-size: 1.2rem;'>
                {emoji} {classification}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with final_rmr_col2:
        # Interpretation guide
        st.markdown("#### RMR Classification Guide")
        classification_guide = {
            "Class I (81-100)": "Very Good Rock - High stability, minimal support needed",
            "Class II (61-80)": "Good Rock - Generally stable, localized support needed",
            "Class III (41-60)": "Fair Rock - Partially stable, systematic support recommended",
            "Class IV (21-40)": "Poor Rock - Unstable, substantial support required",
            "Class V (0-20)": "Very Poor Rock - Highly unstable, major support needed"
        }
        
        for classification_level, description in classification_guide.items():
            color_map = {
                "Class I": "#06A77D",
                "Class II": "#2E86AB",
                "Class III": "#F18F01",
                "Class IV": "#E76F51",
                "Class V": "#C1121F"
            }
            color = next((c for k, c in color_map.items() if k in classification_level), "#666")
            st.markdown(f"**<span style='color: {color};'>{classification_level}</span>** - {description}", unsafe_allow_html=True)
    
    st.divider()
    
    # Detailed breakdown table
    with st.expander("📋 View Detailed Breakdown Table"):
        breakdown_data = {
            "Parameter": [
                "R1 - Strength",
                "R2 - RQD",
                "R3 - Spacing",
                "R4a - Length",
                "R4b - Separation",
                "R4c - Roughness",
                "R4d - Infilling",
                "R4e - Weathering",
                "R4 - Total Condition",
                "R5 - Groundwater",
                "Basic RMR",
                "Orientation Adjustment",
                "Final RMR"
            ],
            "Value": [
                r1, r2, r3, r4a, r4b, r4c, r4d, r4e, r4, r5, basic_rmr, adjustment, final_rmr
            ]
        }
        
        df = pd.DataFrame(breakdown_data)
        
        # Style the dataframe
        def highlight_rows(row):
            if row["Parameter"] == "Basic RMR":
                return ["background-color: #E8F4F8"] * len(row)
            elif row["Parameter"] == "Final RMR":
                return ["background-color: #D4EDDA"] * len(row)
            elif "Total" in row["Parameter"]:
                return ["background-color: #FFF3CD"] * len(row)
            return [""] * len(row)
        
        st.dataframe(
            df.style.apply(highlight_rows, axis=1),
            use_container_width=True,
            hide_index=True
        )
    
    # Download results
    st.markdown("---")
    
    # Create a summary report
    report = f"""
    ROCK MASS RATING (RMR) CALCULATION REPORT
    ==========================================
    
    INPUTS:
    -------
    Strength Test: {type_test}
    Strength Value: {strength_value:.2f} MPa
    RQD: {rqd_value}%
    Spacing: {spacing_value:.2f} mm
    Length: {length_value:.2f} m
    Separation: {separation_value:.2f} mm
    Roughness: {roughness_value}
    Infilling: {infill_value}
    Weathering: {weathering_value}
    Groundwater Method: {gw_choice}
    Structure Type: {structure_type}
    Orientation: {orientation_value}
    
    RESULTS:
    --------
    R1 (Strength): {r1}
    R2 (RQD): {r2}
    R3 (Spacing): {r3}
    R4a (Length): {r4a}
    R4b (Separation): {r4b}
    R4c (Roughness): {r4c}
    R4d (Infilling): {r4d}
    R4e (Weathering): {r4e}
    R4 (Total Condition): {r4}
    R5 (Groundwater): {r5}
    
    Basic RMR: {basic_rmr}
    Orientation Adjustment: {adjustment}
    
    FINAL RMR: {final_rmr:.1f}
    CLASSIFICATION: {classification}
    
    Generated with Rock Mass Rating Calculator
    """
    
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="rmr_report.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 2rem;'>
    <p><strong>Rock Mass Rating (RMR) Calculator</strong></p>
    <p>Based on Bieniawski's Classification System</p>
    <p>For professional geological and geotechnical engineering applications</p>
</div>
""", unsafe_allow_html=True)
