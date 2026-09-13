# 🪨 Rock Mass Rating (RMR) Calculator

A professional **Rock Mass Rating Classification Tool** built with Streamlit for geotechnical engineers and geologists. This calculator implements the Bieniawski RMR system to assess and classify rock mass quality based on site investigation parameters.

## Features

✨ **Beautiful Modern UI** - Intuitive interface with custom styling and visual feedback
📊 **Comprehensive Analysis** - All 5 RMR parameters with detailed sub-parameters
🎯 **Real-time Classification** - Instant RMR calculation and rock mass classification
📋 **Detailed Reporting** - Downloadable reports and breakdown tables
📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
🔧 **Parameter Validation** - Smart input validation and helpful guides

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/munna44sagarpal-collab/final_proj.git
   cd final_proj
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. Open your browser to `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Select `streamlit_app.py` as the main file
5. Deploy!

## 📖 How to Use

### Step 1: Input Parameters (Tab 1)
Enter the following parameters:
- **R1 - Strength**: UCS or Point Load test results
- **R2 - RQD**: Rock Quality Designation percentage
- **R3 - Spacing**: Spacing of discontinuities in mm
- **R5 - Groundwater**: Select assessment method and enter values

### Step 2: Discontinuity Details (Tab 2)
Provide detailed information about rock discontinuities:
- **R4a - Length**: Length/persistence of discontinuity
- **R4b - Separation**: Separation between discontinuity walls
- **R4c - Roughness**: Surface roughness condition
- **R4d - Infilling**: Type and thickness of infilling material
- **R4e - Weathering**: Degree of weathering

### Step 3: View Results (Tab 3)
- Select structure type (Tunnels, Foundations, Slopes)
- Choose discontinuity orientation
- Review final RMR classification with detailed breakdown
- Download your report

## 📊 RMR Classifications

| Classification | Range | Condition | Support |
|---|---|---|---|
| **Class I** | 81-100 | Very Good Rock | High stability, minimal support |
| **Class II** | 61-80 | Good Rock | Generally stable, localized support |
| **Class III** | 41-60 | Fair Rock | Partially stable, systematic support |
| **Class IV** | 21-40 | Poor Rock | Unstable, substantial support |
| **Class V** | 0-20 | Very Poor Rock | Highly unstable, major support |

## 🏗️ Project Structure

```
final_proj/
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── .gitignore               # Git ignore rules
```

## 🔧 Technical Details

### Parameters Calculated

**Parameter 1 (R1)**: Strength of intact rock material
- UCS Range: 0 (< 1 MPa) to 15 (> 250 MPa)
- Point Load: 0 to 15

**Parameter 2 (R2)**: Drill core quality (RQD)
- Range: 5 (< 25%) to 20 (90-100%)

**Parameter 3 (R3)**: Spacing of discontinuities
- Range: 5 (< 60 mm) to 20 (> 2000 mm)

**Parameter 4 (R4)**: Condition of discontinuities
- Sub-ratings: Length (R4a), Separation (R4b), Roughness (R4c), Infilling (R4d), Weathering (R4e)
- Combined range: 0-26

**Parameter 5 (R5)**: Groundwater condition
- Range: 0 to 15

**Table B**: Adjustment for discontinuity orientation
- Varies by structure type (Tunnels, Foundations, Slopes)
- Range: -60 to 0

## 🎨 Customization

### Theme Colors
Edit `.streamlit/config.toml` to customize:
```toml
[theme]
primaryColor = "#2E86AB"
backgroundColor = "#F8F9FA"
textColor = "#1B1D1F"
```

### CSS Styling
Modify the custom CSS in `streamlit_app.py` for visual appearance changes.

## 📚 References

- **Bieniawski, Z. T.** (1989). Engineering Rock Mass Classifications. Wiley-Interscience
- **Bieniawski, Z. T.** (1993). Classification of Rock Masses for Engineering: The RMR System and Future Trends

## 📝 License

This project is open-source and available for educational and professional use.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests

## 📧 Contact

For questions or support, please open an issue on the GitHub repository.

---

**Built with ❤️ using [Streamlit](https://streamlit.io/)**
