import streamlit as st

# RMR CALCULATION FUNCTIONS

# PARAMETER 1: Strength of intact rock material 
def rating_from_strength(test_type, value):
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
            # For this low range, UCS is preferred instead of point load index
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
        else:  # < 1 MPa
            rating = 0
    else:
        rating = None

    return rating


# PARAMETER 2: Drill core quality RQD 
def rating_from_rqd(rqd1):
    if 90 <= rqd1 <= 100:
        rating = 20
    elif 75 <= rqd1 < 90:
        rating = 17
    elif 50 <= rqd1 < 75:
        rating = 13
    elif 25 <= rqd1 < 50:
        rating = 8
    else:  # < 25%
        rating = 5
    return rating


# PARAMETER 3: Spacing of discontinuities 
def rating_from_spacing(spacing1):
    if spacing1 > 2000:
        rating = 20
    elif 600 <= spacing1 <= 2000:
        rating = 15
    elif 200 <= spacing1 < 600:
        rating = 10
    elif 60 <= spacing1 < 200:
        rating = 8
    else:  # < 60 mm
        rating = 5
    return rating


# PARAMETER 4: Condition of discontinuities 
def rating_from_length(length1):
    if length1 < 1:
        rating = 6
    elif 1 <= length1 < 3:
        rating = 4
    elif 3 <= length1 < 10:
        rating = 2
    elif 10 <= length1 <= 20:
        rating = 1
    else:
        rating = 0
    return rating


def rating_from_separation(separation1):
    if separation1 == 0:
        rating = 6
    elif separation1 < 0.1:
        rating = 5
    elif 0.1 <= separation1 <= 1:
        rating = 4
    elif 1 < separation1 <= 5:
        rating = 1
    else:
        rating = 0
    return rating


def rating_from_roughness(roughness):
    roughness = roughness.strip().lower()
    if roughness == "very rough":
        rating = 6
    elif roughness == "rough":
        rating = 5
    elif roughness == "slightly rough":
        rating = 3
    elif roughness == "smooth":
        rating = 1
    elif roughness == "slickensided":
        rating = 0
    else:
        rating = 0
    return rating


def rating_from_infilling(infill_type, thickness=None):
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
    weathering = weathering.strip().lower()
    if weathering == "unweathered":
        rating = 6
    elif weathering == "slightly weathered":
        rating = 5
    elif weathering == "moderately weathered":
        rating = 3
    elif weathering == "highly weathered":
        rating = 1
    elif weathering == "decomposed":
        rating = 0
    else:
        rating = 0
    return rating


# PARAMETER 5: Groundwater 
def rating_from_inflow(inflow):
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
    condition = condition.strip().lower()
    if condition == "completely dry":
        rating = 15
    elif condition == "damp":
        rating = 10
    elif condition == "wet":
        rating = 7
    elif condition == "dripping":
        rating = 4
    elif condition == "flowing":
        rating = 0
    else:
        rating = 0
    return rating


# TABLE B: Rating adjustment for discontinuity orientation
def get_orientation_adjustment(structure_type, orientation):
    structure_type = structure_type.strip().lower()
    orientation = orientation.strip().lower()

    if structure_type == "tunnels":
        if orientation == "very favourable":
            rating = 0
        elif orientation == "favourable":
            rating = -2
        elif orientation == "fair":
            rating = -5
        elif orientation == "unfavourable":
            rating = -10
        elif orientation == "very unfavourable":
            rating = -12
        else:
            rating = None

    elif structure_type == "foundations":
        if orientation == "very favourable":
            rating = 0
        elif orientation == "favourable":
            rating = -2
        elif orientation == "fair":
            rating = -7
        elif orientation == "unfavourable":
            rating = -15
        elif orientation == "very unfavourable":
            rating = -25
        else:
            rating = None

    elif structure_type == "slopes":
        if orientation == "very favourable":
            rating = 0
        elif orientation == "favourable":
            rating = -5
        elif orientation == "fair":
            rating = -25
        elif orientation == "unfavourable":
            rating = -50
        elif orientation == "very unfavourable":
            rating = -60
        else:
            rating = None

    else:
        rating = None

    return rating


# LOOKUP TABLES: map HTML short-codes -> full text the
# rating functions above expect

ROUGHNESS_MAP = {
    "Very Rough": "very rough",
    "Rough": "rough",
    "Slightly Rough": "slightly rough",
    "Smooth": "smooth",
    "Slickensided": "slickensided",
}

WEATHERING_MAP = {
    "Unweathered": "unweathered",
    "Slightly Weathered": "slightly weathered",
    "Moderately Weathered": "moderately weathered",
    "Highly Weathered": "highly weathered",
    "Decomposed": "decomposed",
}

ORIENTATION_MAP = {
    "Very Favourable": "very favourable",
    "Favourable": "favourable",
    "Fair": "fair",
    "Unfavourable": "unfavourable",
    "Very Unfavourable": "very unfavourable",
}

INFILL_MAP = {
    "None": "none",
    "Soft Filling": "soft",
    "Hard Filling": "hard",
}

GENERAL_CONDITION_MAP = {
    "Completely Dry": "completely dry",
    "Damp": "damp",
    "Wet": "wet",
    "Dripping": "dripping",
    "Flowing": "flowing",
}


# STREAMLIT APP

st.set_page_config(page_title="RMR Calculator", layout="wide")

st.title("Rock Mass Rating (RMR) Calculator")
st.markdown("Calculate the RMR classification for rock masses based on Bieniawski's RMR system.")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Input Parameters", "Discontinuity Details", "Results"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parameter 1: Strength of Intact Rock Material")
        type_test = st.selectbox("Test Type", ["UCS", "Point Load"], key="type_test")
        
        if type_test == "UCS":
            strength_value = st.number_input("UCS Value (MPa)", min_value=0.0, value=50.0, key="ucs_value")
            r1 = rating_from_strength('ucs', strength_value)
        else:  # Point Load
            strength_value = st.number_input("Point Load Index (MPa)", min_value=0.0, value=5.0, key="point_load_value")
            r1 = rating_from_strength('point_load', strength_value)
            if r1 is None:
                r1 = 0
        
        st.info(f"**Rating R1: {r1}**")
    
    with col2:
        st.subheader("Parameter 2: Drill Core Quality (RQD)")
        rqd1 = st.number_input("RQD (%)", min_value=0.0, max_value=100.0, value=75.0, key="rqd")
        r2 = rating_from_rqd(rqd1)
        st.info(f"**Rating R2: {r2}**")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Parameter 3: Spacing of Discontinuities")
        spacing1 = st.number_input("Spacing (mm)", min_value=0.0, value=500.0, key="spacing")
        r3 = rating_from_spacing(spacing1)
        st.info(f"**Rating R3: {r3}**")
    
    with col4:
        st.subheader("Parameter 5: Groundwater")
        gw_choice = st.radio("Groundwater Assessment Method", 
                            ["Inflow Rate", "Pore Water Pressure Ratio", "General Conditions"],
                            key="gw_choice")
        
        if gw_choice == "Inflow Rate":
            inflow = st.number_input("Inflow (L/min)", min_value=0.0, value=0.0, key="inflow_value")
            r5 = rating_from_inflow(inflow)
        elif gw_choice == "Pore Water Pressure Ratio":
            ratio = st.number_input("Pw/σ1 Ratio", min_value=0.0, max_value=1.0, value=0.0, key="ratio_value")
            r5 = rating_from_pw_sigma1(ratio)
        else:  # General Conditions
            condition_code = st.selectbox("Condition", list(GENERAL_CONDITION_MAP.keys()), key="general_condition_value")
            condition_text = GENERAL_CONDITION_MAP.get(condition_code, '')
            r5 = rating_from_condition(condition_text)
        
        st.info(f"**Rating R5: {r5}**")

with tab2:
    st.subheader("Parameter 4: Condition of Discontinuities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Length of Discontinuity**")
        length1 = st.number_input("Length (m)", min_value=0.0, value=5.0, key="length")
        r4a = rating_from_length(length1)
        st.metric("R4a", r4a)
    
    with col2:
        st.write("**Separation**")
        separation1 = st.number_input("Separation (mm)", min_value=0.0, value=0.5, key="separation")
        r4b = rating_from_separation(separation1)
        st.metric("R4b", r4b)
    
    with col3:
        st.write("**Roughness**")
        roughness_code = st.selectbox("Roughness", list(ROUGHNESS_MAP.keys()), key="roughness")
        roughness_text = ROUGHNESS_MAP.get(roughness_code, '')
        r4c = rating_from_roughness(roughness_text)
        st.metric("R4c", r4c)
    
    col4, col5 = st.columns(2)
    
    with col4:
        st.write("**Infilling Type**")
        infill_code = st.selectbox("Infilling Type", list(INFILL_MAP.keys()), key="infilling_type")
        infill_text = INFILL_MAP.get(infill_code, 'none')
        
        if infill_text == 'soft':
            thickness = st.number_input("Soft Infill Thickness (mm)", min_value=0.0, value=2.0, key="soft_thickness")
            r4d = rating_from_infilling('soft', thickness)
        elif infill_text == 'hard':
            thickness = st.number_input("Hard Infill Thickness (mm)", min_value=0.0, value=2.0, key="hard_thickness")
            r4d = rating_from_infilling('hard', thickness)
        else:
            r4d = rating_from_infilling('none')
        
        st.metric("R4d", r4d)
    
    with col5:
        st.write("**Weathering**")
        weathering_code = st.selectbox("Weathering", list(WEATHERING_MAP.keys()), key="weathering")
        weathering_text = WEATHERING_MAP.get(weathering_code, '')
        r4e = rating_from_weathering(weathering_text)
        st.metric("R4e", r4e)
    
    r4 = r4a + r4b + r4c + r4d + r4e
    st.divider()
    st.markdown(f"### Total R4 (Condition): **{r4}**")

with tab3:
    st.subheader("Table B: Rating Adjustment for Discontinuity Orientation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        structure_type = st.selectbox("Structure Type", ["Tunnels", "Foundations", "Slopes"], key="structure_type")
    
    with col2:
        orientation_code = st.selectbox("Orientation", list(ORIENTATION_MAP.keys()), key="orientation")
    
    orientation_text = ORIENTATION_MAP.get(orientation_code, '')
    adjustment = get_orientation_adjustment(structure_type, orientation_text)
    if adjustment is None:
        adjustment = 0
    
    st.info(f"**Orientation Adjustment: {adjustment}**")
    
    st.divider()
    
    # Calculate final RMR
    basic_rmr = r1 + r2 + r3 + r4 + r5
    final_rmr = basic_rmr + adjustment
    
    # Display results
    st.subheader("RMR Calculation Summary")
    
    result_col1, result_col2 = st.columns(2)
    
    with result_col1:
        st.metric("R1 (Strength)", r1)
        st.metric("R2 (RQD)", r2)
        st.metric("R3 (Spacing)", r3)
        st.metric("R4 (Condition)", r4)
        st.metric("R5 (Groundwater)", r5)
    
    with result_col2:
        st.metric("Basic RMR", basic_rmr)
        st.metric("Orientation Adjustment", adjustment)
        st.metric("Final RMR", final_rmr, delta=adjustment)
    
    st.divider()
    
    # RMR Classification
    st.subheader("RMR Classification")
    
    if final_rmr >= 81:
        classification = "Class I: Very Good Rock"
        color = "🟢"
    elif final_rmr >= 61:
        classification = "Class II: Good Rock"
        color = "🟢"
    elif final_rmr >= 41:
        classification = "Class III: Fair Rock"
        color = "🟡"
    elif final_rmr >= 21:
        classification = "Class IV: Poor Rock"
        color = "🟠"
    else:
        classification = "Class V: Very Poor Rock"
        color = "🔴"
    
    st.markdown(f"### {color} {classification}")
    
    # Display detailed breakdown
    with st.expander("View Detailed Breakdown"):
        breakdown_data = {
            "Parameter": ["Strength (R1)", "RQD (R2)", "Spacing (R3)", "Condition (R4)", "Groundwater (R5)", "Subtotal", "Orientation Adjustment", "Final RMR"],
            "Rating": [r1, r2, r3, r4, r5, basic_rmr, adjustment, final_rmr]
        }
        
        import pandas as pd
        df = pd.DataFrame(breakdown_data)
        st.dataframe(df, use_container_width=True)
