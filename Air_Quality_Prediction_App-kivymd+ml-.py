import pandas as pd
import numpy as np
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class AirQualityApp(MDApp):
    def __init__(self):
        super().__init__()
        self.data = None
        self.load_data()

    def load_data(self):

        try:

            self.data = pd.read_csv('city_hour.csv')


            self.data['Datetime'] = pd.to_datetime(self.data['Datetime'])


            self.data = self.data.fillna(0)

        except Exception as e:
            print(f"Error loading data: {e}")
            self.create_sample_data()

    def create_sample_data(self):

        dates = pd.date_range('2015-01-01', periods=100, freq='h')  # use 'h' instead of 'H'
        self.data = pd.DataFrame({
            'City': ['Ahmedabad'] * 100,
            'Datetime': dates,
            'PM2.5': np.random.uniform(0, 300, 100),
            'PM10': np.random.uniform(0, 500, 100),
            'NO': np.random.uniform(0, 50, 100),
            'NO2': np.random.uniform(0, 100, 100),
            'NOx': np.random.uniform(0, 200, 100),
            'CO': np.random.uniform(0, 5, 100),
            'SO2': np.random.uniform(0, 50, 100),
            'O3': np.random.uniform(0, 100, 100),
            'AQI': np.random.uniform(0, 500, 100)
        })

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        main_layout = MDFloatLayout()


        toolbar = MDTopAppBar(
            title="Air Quality Monitor - Ahmedabad",
            elevation=10,
            pos_hint={"top": 1}
        )
        main_layout.add_widget(toolbar)


        tabs = TabbedPanel(
            pos_hint={"top": 0.9, "center_x": 0.5},
            size_hint=(0.95, 0.85),
            do_default_tab=False
        )


        summary_tab = TabbedPanelItem(text='Summary')
        summary_layout = self.create_summary_tab()
        summary_tab.add_widget(summary_layout)
        tabs.add_widget(summary_tab)


        data_tab = TabbedPanelItem(text='Raw Data')
        data_layout = self.create_data_table_tab()
        data_tab.add_widget(data_layout)
        tabs.add_widget(data_tab)


        trends_tab = TabbedPanelItem(text='Trends')
        trends_layout = self.create_trends_tab()
        trends_tab.add_widget(trends_layout)
        tabs.add_widget(trends_tab)

        main_layout.add_widget(tabs)
        return main_layout

    def create_summary_tab(self):

        layout = ScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=20,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))


        aqi_card = MDCard(
            orientation='vertical',
            padding=15,
            size_hint=(1, None),
            height=120,
            elevation=5
        )

        if 'AQI' in self.data.columns and not self.data['AQI'].isna().all():
            avg_aqi = self.data['AQI'].mean()
            aqi_status = self.get_aqi_status(avg_aqi)
            aqi_color = self.get_aqi_color(avg_aqi)
        else:
            avg_aqi = "N/A"
            aqi_status = "No Data"
            aqi_color = (0.5, 0.5, 0.5, 1)


        if isinstance(avg_aqi, (int, float)):
            aqi_text = f"Average AQI: {avg_aqi:.1f}"
        else:
            aqi_text = f"Average AQI: {avg_aqi}"

        aqi_card.add_widget(MDLabel(
            text=aqi_text,
            theme_text_color="Primary",
            size_hint_y=None,
            height=40
        ))
        aqi_card.add_widget(MDLabel(
            text=f"Status: {aqi_status}",
            theme_text_color="Custom",
            size_hint_y=None,
            height=40,
            text_color=aqi_color
        ))
        content.add_widget(aqi_card)


        pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
        for pollutant in pollutants:
            if pollutant in self.data.columns:
                card = self.create_pollutant_card(pollutant)
                content.add_widget(card)


        stats_card = MDCard(
            orientation='vertical',
            padding=15,
            size_hint=(1, None),
            height=150,
            elevation=5
        )
        stats_card.add_widget(MDLabel(
            text="Dataset Statistics",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40
        ))

        stats_text = f"""
• Total Records: {len(self.data)}
• Date Range: {self.data['Datetime'].min().strftime('%Y-%m-%d')} to {self.data['Datetime'].max().strftime('%Y-%m-%d')}
• City: {self.data['City'].iloc[0] if 'City' in self.data.columns else 'N/A'}
"""
        stats_card.add_widget(MDLabel(
            text=stats_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=80
        ))
        content.add_widget(stats_card)

        layout.add_widget(content)
        return layout

    def create_pollutant_card(self, pollutant):

        card = MDCard(
            orientation='horizontal',
            padding=15,
            size_hint=(1, None),
            height=80,
            elevation=3
        )

        values = self.data[pollutant]
        avg_value = values.mean()
        max_value = values.max()


        left_layout = MDBoxLayout(orientation='vertical', size_hint_x=0.7)
        left_layout.add_widget(MDLabel(
            text=pollutant,
            theme_text_color="Primary",
            size_hint_y=None,
            height=30
        ))
        left_layout.add_widget(MDLabel(
            text=f"Avg: {avg_value:.2f} | Max: {max_value:.2f}",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        ))


        right_layout = MDBoxLayout(orientation='vertical', size_hint_x=0.3)
        status, color = self.get_pollutant_status(pollutant, avg_value)
        right_layout.add_widget(MDLabel(
            text=status,
            theme_text_color="Custom",
            text_color=color,
            size_hint_y=None,
            height=40
        ))

        card.add_widget(left_layout)
        card.add_widget(right_layout)
        return card

    def create_data_table_tab(self):

        layout = MDBoxLayout(orientation='vertical')


        columns = [
            ("Date", dp(30)),
            ("PM2.5", dp(20)),
            ("PM10", dp(20)),
            ("NO2", dp(20)),
            ("SO2", dp(20)),
            ("AQI", dp(20))
        ]


        table_data = []
        sample_data = self.data.head(50)

        for _, row in sample_data.iterrows():
            table_data.append(
                (
                    row['Datetime'].strftime('%m/%d %H:%M'),
                    f"{row.get('PM2.5', 0):.1f}",
                    f"{row.get('PM10', 0):.1f}",
                    f"{row.get('NO2', 0):.1f}",
                    f"{row.get('SO2', 0):.1f}",
                    f"{row.get('AQI', 0):.1f}" if 'AQI' in row else "N/A"
                )
            )

        self.data_table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=10,
            column_data=columns,
            row_data=table_data
        )

        layout.add_widget(self.data_table)
        return layout

    def create_trends_tab(self):
        """Create the trends analysis tab"""
        layout = ScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=20,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))


        daily_card = MDCard(
            orientation='vertical',
            padding=15,
            size_hint=(1, None),
            height=200,
            elevation=5
        )

        daily_card.add_widget(MDLabel(
            text="Daily Pattern Analysis",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40
        ))

        # Calculate hourly averages
        if 'Datetime' in self.data.columns:
            self.data['Hour'] = self.data['Datetime'].dt.hour
            hourly_avg = self.data.groupby('Hour').mean(numeric_only=True)

            trend_text = "Hourly Averages:\n"
            for hour in range(24):
                if hour in hourly_avg.index and 'PM2.5' in hourly_avg.columns:
                    pm25 = hourly_avg.loc[hour, 'PM2.5']
                    trend_text += f"{hour:02d}:00 - PM2.5: {pm25:.1f}\n"
        else:
            trend_text = "No datetime data available for trend analysis"

        daily_card.add_widget(MDLabel(
            text=trend_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=140
        ))
        content.add_widget(daily_card)


        peak_card = MDCard(
            orientation='vertical',
            padding=15,
            size_hint=(1, None),
            height=150,
            elevation=5
        )

        peak_card.add_widget(MDLabel(
            text="Peak Pollution Events",
            theme_text_color="Primary",
            size_hint_y=None,
            height=40
        ))

        if 'PM2.5' in self.data.columns:
            max_pm25_idx = self.data['PM2.5'].idxmax()
            max_pm25 = self.data.loc[max_pm25_idx, 'PM2.5']
            max_date = self.data.loc[max_pm25_idx, 'Datetime']

            peak_text = f"Highest PM2.5: {max_pm25:.1f}\n"
            peak_text += f"Date: {max_date.strftime('%Y-%m-%d %H:%M')}"
        else:
            peak_text = "No PM2.5 data available"

        peak_card.add_widget(MDLabel(
            text=peak_text,
            theme_text_color="Secondary",
            size_hint_y=None,
            height=80
        ))
        content.add_widget(peak_card)

        layout.add_widget(content)
        return layout

    def get_aqi_status(self, aqi):
        """Get AQI status based on value"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    def get_aqi_color(self, aqi):

        if aqi <= 50:
            return (0, 0.5, 0, 1)
        elif aqi <= 100:
            return (1, 1, 0, 1)
        elif aqi <= 150:
            return (1, 0.65, 0, 1)
        elif aqi <= 200:
            return (1, 0, 0, 1)
        elif aqi <= 300:
            return (0.5, 0, 0.5, 1)
        else:
            return (0.5, 0, 0, 1)

    def get_pollutant_status(self, pollutant, value):

        thresholds = {
            'PM2.5': (12, 35, 55, 150),
            'PM10': (50, 100, 250, 420),
            'NO2': (40, 80, 180, 400),
            'SO2': (40, 80, 380, 800),
            'CO': (1, 2, 10, 17),
            'O3': (100, 168, 208, 748)
        }

        if pollutant not in thresholds:
            return "N/A", (0.5, 0.5, 0.5, 1)

        low, moderate, high, severe = thresholds[pollutant]

        if value <= low:
            return "Good", (0, 0.5, 0, 1)
        elif value <= moderate:
            return "Moderate", (1, 1, 0, 1)
        elif value <= high:
            return "Poor", (1, 0.65, 0, 1)
        elif value <= severe:
            return "Very Poor", (1, 0, 0, 1)
        else:
            return "Severe", (0.5, 0, 0.5, 1)

if __name__ == '__main__':
    Window.size = (1200, 800)
    AirQualityApp().run()
