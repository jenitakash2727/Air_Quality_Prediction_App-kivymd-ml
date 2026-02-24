🌍 Air Quality Monitor Dashboard 🌫️

A modern data analysis dashboard built with Python, Pandas, and KivyMD that monitors and analyzes air quality data for cities. The application provides AQI insights, pollutant statistics, hourly trends, and structured data visualization through an interactive Material Design interface.

🚀 Features

AQI Status Monitoring – Calculates and displays average AQI with health category

Pollutant Analysis – PM2.5, PM10, NO2, SO2, CO, O3 statistics

Hourly Trend Analysis – Displays pollution patterns across 24 hours

Peak Event Detection – Identifies highest pollution events

Raw Data Viewer – Paginated data table view

Material Design UI – Clean, responsive KivyMD interface

Automatic Data Handling – Loads CSV dataset or generates sample data

📊 Dashboard Sections
1️⃣ Summary Tab

Average AQI calculation

Health status classification (Good, Moderate, Unhealthy, etc.)

Pollutant-wise average and maximum values

Dataset statistics (record count, date range, city name)

2️⃣ Raw Data Tab

Structured paginated table

Displays date, PM2.5, PM10, NO2, SO2, AQI

Scrollable and optimized layout

3️⃣ Trends Tab

Hourly pollution pattern analysis

Peak pollution event detection

Time-based aggregation using Pandas

🧠 Data Processing Pipeline

Data Loading (CSV or Sample Data)

Datetime Conversion

Missing Value Handling (Fill with 0)

GroupBy Aggregation (Hourly Trends)

Statistical Summary Calculation

AQI & Pollutant Health Classification

📦 Requirements
Python Dependencies
kivymd>=1.1.1
kivy>=2.1.0
pandas>=1.5.0
numpy>=1.23.0
System Requirements

Python 3.8+

512MB RAM minimum

50MB storage space

▶️ Installation
git clone <your-repo-url>
cd air-quality-dashboard
pip install kivymd pandas numpy
python main.py
📁 Dataset Format (CSV Example)
City,Datetime,PM2.5,PM10,NO2,SO2,CO,O3,AQI
Ahmedabad,2015-01-01 00:00,45,78,30,12,0.8,40,110
Ahmedabad,2015-01-01 01:00,52,80,32,14,0.9,42,120
...
🌡 AQI Classification Levels
AQI Range	Status
0–50	Good
51–100	Moderate
101–150	Unhealthy (Sensitive)
151–200	Unhealthy
201–300	Very Unhealthy
300+	Hazardous
📈 Technical Highlights

Built using Pandas for data analysis

Implemented hourly aggregation using groupby

Developed health classification logic using threshold mapping

Designed multi-tab interactive dashboard using KivyMD

Applied data validation and error handling

📱 Future Enhancements

📊 Data visualization charts (Matplotlib integration)

🌍 Multi-city comparison

📡 Live AQI API integration

📥 Export results (CSV/PDF)

📲 Android APK deployment
