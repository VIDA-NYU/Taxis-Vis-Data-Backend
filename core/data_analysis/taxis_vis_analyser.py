import pandas as pd
from shapely.geometry import Point
from typing import Optional, Union, List


class TaxisVisAnalyser:
    def __init__(self, file_input: Union[str, pd.DataFrame]) -> None:
        self.file_input: Union[str, pd.DataFrame] = file_input
        self.df: Optional[pd.DataFrame] = None
        self.load_data()
        self.extract_location_coordinates()
        self.preprocess_data()

    def load_data(self) -> None:
        if isinstance(self.file_input, str):
            self.df = pd.read_csv(self.file_input)
        elif isinstance(self.file_input, pd.DataFrame):
            self.df = self.file_input.copy()
        else:
            try:
                self.df = pd.read_csv(self.file_input)  # assume file_input object.
            except Exception as e:
                raise ValueError(f"Invalid input: {e}")

        if self.df.empty:
            raise ValueError("Dataset is empty.")

    def extract_location_coordinates(self) -> None:
        for point_type in ['pickup', 'dropoff']:
            geo_col = point_type
            lat_col = f"{point_type}_latitude"
            lon_col = f"{point_type}_longitude"

            if geo_col in self.df.columns:
                self.df[[lat_col, lon_col]] = self.df[geo_col].apply(lambda x: pd.Series(self.parse_geo_column(x)))
            else:
                raise ValueError(f"Missing required column: {geo_col}")

    def preprocess_data(self) -> None:
        pickup_col = "pickup_datetime"
        dropoff_col = "dropoff_datetime"

        if pickup_col not in self.df.columns or dropoff_col not in self.df.columns:
            raise ValueError("Missing datetime columns for pickup or dropoff.")

        self.df[pickup_col] = pd.to_datetime(self.df[pickup_col], errors="coerce")
        self.df[dropoff_col] = pd.to_datetime(self.df[dropoff_col], errors="coerce")

        self.df['trip_duration'] = (self.df[dropoff_col] - self.df[pickup_col]).dt.total_seconds() / 60
        self.df['pickup_hour'] = self.df[pickup_col].dt.hour
        self.df['pickup_date'] = self.df[pickup_col].dt.date

        for point_type in ['pickup', 'dropoff']:
            lat_col = f"{point_type}_latitude"
            lon_col = f"{point_type}_longitude"
            point_col = f"{point_type}_point"

            if lat_col in self.df.columns and lon_col in self.df.columns:
                self.df[point_col] = self.df.apply(
                    lambda row: Point(row[lon_col], row[lat_col])
                    if pd.notnull(row[lat_col]) and pd.notnull(row[lon_col]) else None,
                    axis=1
                )
            else:
                self.df[point_col] = None

    def get_trip_durations(self) -> pd.Series:
        if 'trip_duration' not in self.df.columns or self.df['trip_duration'].isnull().all():
            raise ValueError("Trip duration data is missing.")
        return self.df['trip_duration'].dropna()

    def identify_peak_hours(self, threshold) -> pd.DataFrame:
        if 'pickup_hour' not in self.df.columns or self.df['pickup_hour'].isnull().all():
            raise ValueError("Cannot identify peak hours as 'pickup_hour' data is missing.")
        peak_hours: pd.DataFrame = self.df.groupby('pickup_hour').size().reset_index(name='trip_count')
        if threshold is not None:
            peak_hours = peak_hours[peak_hours['trip_count'] >= threshold]
        return peak_hours

    def analyse_passenger_count(self) -> pd.DataFrame:
        if 'passenger_count' not in self.df.columns:
            raise ValueError("Passenger count data is missing.")
        passenger_count: pd.DataFrame = self.df["passenger_count"].value_counts().reset_index()
        passenger_count.columns = ['passenger_count', 'count']
        return passenger_count

    def analyse_payment_type(self) -> pd.DataFrame:
        if 'payment_type' not in self.df.columns:
            raise ValueError("Payment type data is missing.")
        payment_type: pd.DataFrame = self.df['payment_type'].value_counts().reset_index()
        payment_type.columns = ['payment_type', 'count']
        return payment_type

    def analyse_distance_fare_scatter(self) -> pd.DataFrame:
        if 'trip_distance' not in self.df.columns or 'fare_amount' not in self.df.columns:
            raise ValueError("Distance and fare amount data is missing.")
        return self.df[['trip_distance', 'fare_amount']].dropna()

    def analyse_time_series_trips(self) -> pd.DataFrame:
        if 'pickup_date' not in self.df.columns or self.df['pickup_date'].isnull().all():
            raise ValueError("Pickup date data is missing.")
        return self.df.groupby('pickup_date').size().reset_index(name='trip_count')

    def get_fare_amounts(self) -> pd.Series:
        if 'fare_amount' not in self.df.columns:
            raise ValueError("Fare amount data is missing.")
        return self.df['fare_amount'].dropna()

    def get_tip_amounts(self) -> pd.Series:
        if 'tip_amount' not in self.df.columns:
            raise ValueError("Tip amount data is missing.")
        return self.df['tip_amount'].dropna()

    @staticmethod
    def parse_geo_column(geo_data):
        if isinstance(geo_data, dict):
            lat = geo_data.get('latitude') or geo_data.get('lat')
            lon = geo_data.get('longitude') or geo_data.get('lon') or geo_data.get('lng')
            return float(lat) if lat else None, float(lon) if lon else None
        return None, None
