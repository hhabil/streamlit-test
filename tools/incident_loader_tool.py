import json
import os

import pandas as pd
from langchain_core.tools import tool


@tool
def incident_info_loader_tool(paxID: int):
    """Returns a result json"""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, "../mock_data/trainingdata_for_nbre.csv")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path,index_col="pax_id")
    if paxID in df.index:
        result_dict = df.loc[paxID].to_dict()

        result_json = json.dumps(result_dict)
        return result_json

    else:
        return None
