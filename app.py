from flask import Flask, render_template, request

app = Flask(__name__)
# RMR CALCULATION FUNCTIONS

#  PARAMETER 1: Strength of intact rock material 
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


#  PARAMETER 3: Spacing of discontinuities 
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


#  PARAMETER 4: Condition of discontinuities 
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


#  PARAMETER 5: Groundwater 
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


#  TABLE B: Rating adjustment for discontinuity orientation
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
    "vr": "very rough",
    "r": "rough",
    "sr": "slightly rough",
    "s": "smooth",
    "ss": "slickensided",
}

WEATHERING_MAP = {
    "w": "unweathered",
    "sw": "slightly weathered",
    "mw": "moderately weathered",
    "hw": "highly weathered",
    "d": "decomposed",
}

ORIENTATION_MAP = {
    "vf": "very favourable",
    "fav": "favourable",
    "fair": "fair",
    "uf": "unfavourable",
    "vuf": "very unfavourable",
}

INFILL_MAP = {
    "none": "none",
    "soft_filling": "soft",
    "hard_filling": "hard",
}

GENERAL_CONDITION_MAP = {
    "completely_dry": "completely dry",
    "damp": "damp",
    "wet": "wet",
    "dripping": "dripping",
    "flowing": "flowing",
}


def to_float(value, default=0.0):
    """Safely convert a form value to float, defaulting if missing/blank."""
    if value is None or str(value).strip() == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default

# FLASK ROUTE

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        # ---- Parameter 1: Strength ----
        type_test = request.form.get('type_test', '')
        if type_test == 'ucs':
            strength_value = to_float(request.form.get('ucs_value'))
            r1 = rating_from_strength('ucs', strength_value)
        elif type_test == 'point_load':
            strength_value = to_float(request.form.get('point_load_value'))
            r1 = rating_from_strength('point_load', strength_value)
            if r1 is None:
                # Low range -> UCS preferred, but no UCS value was given via this path
                r1 = 0
        else:
            r1 = 0

        #  Parameter 2: RQD
        rqd1 = to_float(request.form.get('rqd'))
        r2 = rating_from_rqd(rqd1)

        #  Parameter 3: Spacing 
        spacing1 = to_float(request.form.get('spacing'))
        r3 = rating_from_spacing(spacing1)

        # Parameter 4: Condition of discontinuities 
        length1 = to_float(request.form.get('length'))
        r4a = rating_from_length(length1)

        separation1 = to_float(request.form.get('separation'))
        r4b = rating_from_separation(separation1)

        roughness_code = request.form.get('roughness', '')
        roughness_text = ROUGHNESS_MAP.get(roughness_code, '')
        r4c = rating_from_roughness(roughness_text)

        infill_code = request.form.get('infilling_type', 'none')
        infill_text = INFILL_MAP.get(infill_code, 'none')

        if infill_text == 'soft':
            thickness = to_float(request.form.get('soft_thickness'))
            r4d = rating_from_infilling('soft', thickness)
        elif infill_text == 'hard':
            thickness = to_float(request.form.get('hard_thickness'))
            r4d = rating_from_infilling('hard', thickness)
        else:
            r4d = rating_from_infilling('none')

        weathering_code = request.form.get('weathering', '')
        weathering_text = WEATHERING_MAP.get(weathering_code, '')
        r4e = rating_from_weathering(weathering_text)

        r4 = r4a + r4b + r4c + r4d + r4e

        # Parameter 5: Groundwater
        gw_choice = request.form.get('gw_choice', '')

        if gw_choice == 'inflow':
            inflow = to_float(request.form.get('inflow_value'))
            r5 = rating_from_inflow(inflow)
        elif gw_choice == 'pw/sigma1':
            ratio = to_float(request.form.get('ratio_value'))
            r5 = rating_from_pw_sigma1(ratio)
        elif gw_choice == 'general_conditions':
            condition_code = request.form.get('general_condition_value', '')
            condition_text = GENERAL_CONDITION_MAP.get(condition_code, '')
            r5 = rating_from_condition(condition_text)
        else:
            r5 = 0

        # Basic RMR 
        basic_rmr = r1 + r2 + r3 + r4 + r5

        # Table B: Orientation adjustment
        structure_type = request.form.get('structure_type', '')
        orientation_code = request.form.get('orientation', '')
        orientation_text = ORIENTATION_MAP.get(orientation_code, '')

        adjustment = get_orientation_adjustment(structure_type, orientation_text)
        if adjustment is None:
            adjustment = 0

        final_rmr = basic_rmr + adjustment

        result = {
            'r1': r1,
            'r2': r2,
            'r3': r3,
            'r4': r4,
            'r5': r5,
            'basic_rmr': basic_rmr,
            'adjustment': adjustment,
            'final_rmr': final_rmr,
        }

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
