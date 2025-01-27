import pandas as pd
from shapely.geometry import Point
from typing import Optional, Union, Dict, Any, List
import os
import json


class TaxisVisAnalyser:
    def __init__(
            self,
            file_input: Union[str, pd.DataFrame],
            spatial_data: Optional[Any] = None,
            datetime_columns: Optional[Dict[str, str]] = None,
            location_columns: Optional[Dict[str, str]] = None
    ) -> None:
        self.file_input: Union[str, pd.DataFrame] = file_input
        self.spatial_data: Optional[Any] = spatial_data
        self.df: Optional[pd.DataFrame] = None
        self.datetime_columns: Dict[str, str] = datetime_columns or {
            'pickup': 'tpep_pickup_datetime',
            'dropoff': 'tpep_dropoff_datetime'
        }
        self.location_columns: Dict[str, str] = location_columns or {
            'pickup': 'pickup',
            'dropoff': 'dropoff'
        }
        self.required_columns: List[str] = [
            self.datetime_columns['pickup'],
            self.datetime_columns['dropoff'],
            self.location_columns['pickup'],
            self.location_columns['dropoff'],
            'payment_type',
            'passenger_count',
            'fare_amount',
            'trip_distance',
            'tip_amount'
        ]
        self.load_data()
        self.validate_columns()
        self.extract_location_coordinates()
        self.preprocess_data()

    def load_data(self) -> None:
        if isinstance(self.file_input, str):
            if not os.path.isfile(self.file_input):
                raise FileNotFoundError(f"File not found: {self.file_input}")
            self.df = pd.read_csv(
                self.file_input,
                parse_dates=[self.datetime_columns['pickup'], self.datetime_columns['dropoff']],
                infer_datetime_format=True
            )
        elif isinstance(self.file_input, pd.DataFrame):
            self.df = self.file_input.copy()
            self.parse_datetime_columns()
        else:
            raise ValueError("file_input must be a file path (str) or a pandas DataFrame")

    def parse_datetime_columns(self) -> None:
        for key, col in self.datetime_columns.items():
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            else:
                raise ValueError(f"Missing datetime column: {col}")

    def validate_columns(self) -> None:
        if self.df is None:
            raise ValueError("DataFrame is not loaded.")
        missing_columns: List[str] = [col for col in self.required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def extract_location_coordinates(self) -> None:
        for point_type in ['pickup', 'dropoff']:
            geo_col: str = self.location_columns[point_type]
            lat_col: str = f"{point_type}_latitude"
            lon_col: str = f"{point_type}_longitude"

            if self.df[geo_col].dtype == object:
                self.df[lat_col], self.df[lon_col] = zip(*self.df[geo_col].apply(self.parse_geo_column))
            else:
                raise ValueError(f"The {geo_col} column must contain JSON strings or dictionaries.")

    @staticmethod
    def parse_geo_column(geo_data: Union[str, Dict[str, Any]]) -> (Optional[float], Optional[float]):
        try:
            if isinstance(geo_data, str):
                geo_json = json.loads(geo_data)
            elif isinstance(geo_data, dict):
                geo_json = geo_data
            else:
                return (None, None)

            latitude = geo_json.get('latitude') or geo_json.get('lat')
            longitude = geo_json.get('longitude') or geo_json.get('lon') or geo_json.get('lng')

            return (float(latitude) if latitude is not None else None,
                    float(longitude) if longitude is not None else None)
        except (json.JSONDecodeError, TypeError, ValueError):
            return (None, None)

    def preprocess_data(self) -> None:
        if self.df is not None:
            self.df['trip_duration'] = (
                                               self.df[self.datetime_columns['dropoff']] - self.df[
                                           self.datetime_columns['pickup']]
                                       ).dt.total_seconds() / 60
            self.df['pickup_hour'] = self.df[self.datetime_columns['pickup']].dt.hour
            self.df['pickup_date'] = self.df[self.datetime_columns['pickup']].dt.date
            self.create_point('pickup')
            self.create_point('dropoff')

    def create_point(self, point_type: str) -> None:
        lat_col: str = f"{point_type}_latitude"
        lon_col: str = f"{point_type}_longitude"
        point_col: str = f"{point_type}_point"

        if lat_col in self.df.columns and lon_col in self.df.columns:
            self.df[point_col] = self.df.apply(
                lambda row: Point(row[lon_col], row[lat_col]) if pd.notnull(row[lat_col]) and pd.notnull(
                    row[lon_col]) else None,
                axis=1
            )
        else:
            raise ValueError(f"Missing location columns for {point_type}: {lat_col}, {lon_col}")

    def identify_peak_hours(self, threshold: Optional[int] = None) -> pd.DataFrame:
        peak_hours: pd.DataFrame = self.df.groupby('pickup_hour').size().reset_index(name='trip_count')
        if threshold is not None:
            peak_hours = peak_hours[peak_hours['trip_count'] >= threshold]
        return peak_hours

    def analyse_passenger_count(self) -> pd.DataFrame:
        passenger_count: pd.DataFrame = self.df['passenger_count'].value_counts().reset_index()
        passenger_count.columns = ['passenger_count', 'count']
        return passenger_count

    def analyse_payment_type(self) -> pd.DataFrame:
        payment_type: pd.DataFrame = self.df['payment_type'].value_counts().reset_index()
        payment_type.columns = ['payment_type', 'count']
        return payment_type

    def analyse_distance_fare_scatter(self) -> pd.DataFrame:
        distance_fare: pd.DataFrame = self.df[['trip_distance', 'fare_amount']].dropna()
        return distance_fare

    def analyse_time_series_trips(self) -> pd.DataFrame:
        time_series_trips: pd.DataFrame = self.df.groupby('pickup_date').size().reset_index(name='trip_count')
        return time_series_trips

    def get_trip_durations(self) -> pd.Series:
        trip_durations: pd.Series = self.df['trip_duration'].dropna()
        return trip_durations

    def get_fare_amounts(self) -> pd.Series:
        fare_amounts: pd.Series = self.df['fare_amount'].dropna()
        return fare_amounts

    def get_tip_amounts(self) -> pd.Series:
        tip_amounts: pd.Series = self.df['tip_amount'].dropna()
        return tip_amounts
