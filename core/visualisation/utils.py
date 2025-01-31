from typing import Any, Dict, Union, Tuple

import pandas as pd

from core.data_analysis.taxis_vis_analyser import TaxisVisAnalyser


def load_and_analyse(
        csv_file: Any,
        analysis_function: Any,
        return_data: bool = False,
        **kwargs
) -> Union[Any, Tuple[Any, pd.DataFrame]]:
    analyser = TaxisVisAnalyser(file_input=csv_file)
    result = analysis_function(analyser, **kwargs)
    if return_data:
        return result, analyser.df
    return result
