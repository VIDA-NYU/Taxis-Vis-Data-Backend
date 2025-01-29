import pandas as pd
from typing import Any, Optional, Union, List
import os


def read_csv_file(
        csv_file: Union[str, Any],
        datetime_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    datetime_cols = datetime_columns or []
    try:
        if isinstance(csv_file, str):
            if not os.path.isfile(csv_file):
                raise FileNotFoundError(f"File not found: {csv_file}")
            df = pd.read_csv(csv_file, parse_dates=datetime_cols)
        else:
            df = pd.read_csv(csv_file, parse_dates=datetime_cols)  # Assuming file-like object

        if df.empty:
            raise ValueError("CSV file is empty.")

        return df
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty.")
    except pd.errors.ParserError:
        raise ValueError("CSV file is malformed.")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the CSV file: {str(e)}")


def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> None:
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
