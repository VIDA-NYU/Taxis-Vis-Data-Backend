import json
import os
from typing import Optional, Union, Dict, Any, List, Tuple
import pandas as pd
from shapely.geometry import Point
from functools import wraps


def parse_geo_column(geo_data: Union[str, Dict[str, Any]]) -> Tuple[Optional[float], Optional[float]]:
    try:
        if isinstance(geo_data, str):
            geo_json = json.loads(geo_data)
        elif isinstance(geo_data, dict):
            geo_json = geo_data
        else:
            return (None, None)

        latitude = geo_json.get('latitude') or geo_json.get('lat')
        longitude = geo_json.get('longitude') or geo_json.get('lon') or geo_json.get('lng')

        return (
            float(latitude) if latitude is not None else None,
            float(longitude) if longitude is not None else None
        )
    except (json.JSONDecodeError, TypeError, ValueError):
        return (None, None)


def parse_time_column(time_data: Union[str, pd.Series], format: str = None) -> pd.Series:
    try:
        if format:
            return pd.to_datetime(time_data, format=format, errors='coerce')
        else:
            return pd.to_datetime(time_data, errors='coerce')
    except Exception as e:
        raise ValueError(f"Error parsing time column: {e}")

def is_json_column(df: pd.DataFrame, column: str) -> bool:
    return df[column].dtype == object


def load_dataframe(file_input: Union[str, pd.DataFrame, Any], datetime_columns: List[str]) -> pd.DataFrame:
    if isinstance(file_input, str):
        if not os.path.isfile(file_input):
            raise FileNotFoundError(f"File not found: {file_input}")
        df = pd.read_csv(
            file_input,
        )
    elif isinstance(file_input, pd.DataFrame):
        df = file_input.copy()
        df[datetime_columns] = df[datetime_columns].apply(pd.to_datetime, errors='coerce')
    else:
        try:
            print(f"File Input: {file_input}")
            df = pd.read_csv(file_input)
            print(f"Df Head: {df.head()}")
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty.")
        except pd.errors.ParserError:
            raise ValueError("CSV file is malformed.")
        except Exception as e:
            raise ValueError("file_input must be a file path (str), a pandas DataFrame, or a file-like object")

    print(f"Data Shape: {df.shape}")
    print(f"Data Columns: {df.columns}")
    print("_" * 50)
    return df
