import pandas as pd
from shapely.geometry import Point
from typing import Optional, Union, Dict, Any, List
from .utils import (
    parse_geo_column,
    is_json_column,
    load_dataframe, parse_time_column
)


class TaxisVisAnalyser:
    def __init__(
            self,
            file_input: Union[str, pd.DataFrame],
            config: Dict[str, Any]
    ) -> None:
        self.file_input: Union[str, pd.DataFrame, Any] = file_input
        self.df: Optional[pd.DataFrame] = None
        self.config: Dict[str, Any] = config
        self.datetime_columns: List[str] = list(config.get('datetime_columns', {}).values())
        self.location_columns: Dict[str, str] = config.get('location_columns', {})
        self.required_columns: Dict[str, Optional[str]] = config.get('required_columns', {})
        self.load_data()
        self.validate_columns()
        self.extract_location_coordinates()
        self.preprocess_data()

    def load_data(self) -> None:
        self.df = load_dataframe(self.file_input, self.datetime_columns)

    def validate_columns(self) -> None:
        missing_columns: List[str] = []
        for logical_field, dataset_col in self.required_columns.items():
            if dataset_col and dataset_col not in self.df.columns:
                missing_columns.append(dataset_col)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def extract_location_coordinates(self) -> None:
        for point_type in ['pickup', 'dropoff']:
            geo_col: Optional[str] = self.location_columns.get(point_type)
            if not geo_col:
                continue
            lat_col: str = f"{point_type}_latitude"
            lon_col: str = f"{point_type}_longitude"

            if is_json_column(self.df, geo_col):
                self.df[[lat_col, lon_col]] = self.df[geo_col].apply(
                    lambda x: pd.Series(parse_geo_column(x))
                )
            else:
                raise ValueError(f"The '{geo_col}' column must contain JSON strings or dictionaries.")

    def preprocess_data(self) -> None:
        if self.df is not None:
            pickup_col = self.config.get('datetime_columns', {}).get('pickup')
            dropoff_col = self.config.get('datetime_columns', {}).get('dropoff')

            if pickup_col and dropoff_col:
                # Use parse_time_column to ensure proper parsing
                self.df[pickup_col] = parse_time_column(self.df[pickup_col])
                self.df[dropoff_col] = parse_time_column(self.df[dropoff_col])

                if pickup_col in self.df.columns and dropoff_col in self.df.columns:
                    self.df['trip_duration'] = (
                                                       self.df[dropoff_col] - self.df[pickup_col]
                                               ).dt.total_seconds() / 60  # Duration in minutes
                    self.df['pickup_hour'] = self.df[pickup_col].dt.hour
                    self.df['pickup_date'] = self.df[pickup_col].dt.date
                else:
                    self.df['trip_duration'] = None
                    self.df['pickup_hour'] = None
                    self.df['pickup_date'] = None

            for point_type in ['pickup', 'dropoff']:
                lat_col = f"{point_type}_latitude"
                lon_col = f"{point_type}_longitude"
                point_col = f"{point_type}_point"
                if lat_col in self.df.columns and lon_col in self.df.columns:
                    self.df[point_col] = self.df.apply(
                        lambda row: Point(row[lon_col], row[lat_col])
                        if pd.notnull(row[lat_col]) and pd.notnull(row[lon_col])
                        else None,
                        axis=1
                    )
                else:
                    self.df[point_col] = None

    def identify_peak_hours(self, threshold: Optional[int] = None) -> pd.DataFrame:
        if 'pickup_hour' not in self.df.columns or self.df['pickup_hour'].isnull().all():
            raise ValueError("Cannot identify peak hours as 'pickup_hour' data is missing.")
        peak_hours: pd.DataFrame = self.df.groupby('pickup_hour').size().reset_index(name='trip_count')
        if threshold is not None:
            peak_hours = peak_hours[peak_hours['trip_count'] >= threshold]
        return peak_hours

    def analyse_passenger_count(self) -> pd.DataFrame:
        passenger_count_col = self.required_columns.get('passenger_count')
        passenger_count: pd.DataFrame = self.df[passenger_count_col].value_counts().reset_index()
        passenger_count.columns = ['passenger_count', 'count']
        return passenger_count

    def analyse_payment_type(self) -> pd.DataFrame:
        payment_type_col = self.required_columns.get('payment_type')
        payment_type: pd.DataFrame = self.df[payment_type_col].value_counts().reset_index()
        payment_type.columns = ['payment_type', 'count']
        return payment_type

    def analyse_distance_fare_scatter(self) -> pd.DataFrame:
        trip_distance_col = self.required_columns.get('trip_distance')
        fare_amount_col = self.required_columns.get('fare_amount')
        distance_fare: pd.DataFrame = self.df[[trip_distance_col, fare_amount_col]].dropna()
        distance_fare.columns = ['trip_distance', 'fare_amount']
        return distance_fare

    def analyse_time_series_trips(self) -> pd.DataFrame:
        pickup_date_col = 'pickup_date'
        if pickup_date_col not in self.df.columns or self.df[pickup_date_col].isnull().all():
            raise ValueError("Cannot analyze time series trips as 'pickup_date' column is missing.")
        time_series_trips: pd.DataFrame = self.df.groupby(pickup_date_col).size().reset_index(name='trip_count')
        return time_series_trips

    def get_trip_durations(self) -> pd.Series:
        if 'trip_duration' not in self.df.columns or self.df['trip_duration'].isnull().all():
            raise ValueError("Cannot get trip durations as 'trip_duration' data is missing.")
        trip_durations: pd.Series = self.df['trip_duration'].dropna()
        return trip_durations

    def get_fare_amounts(self) -> pd.Series:
        fare_amount_col = self.required_columns.get('fare_amount')
        fare_amounts: pd.Series = self.df[fare_amount_col].dropna()
        return fare_amounts

    def get_tip_amounts(self) -> pd.Series:
        tip_col = self.required_columns.get('tip_amount')
        tip_amounts: pd.Series = self.df[tip_col].dropna()
        return tip_amounts
