import json
import yaml
from typing import Text 
def read_txt_from_gcsfs(fs, file_path: Text):
    with fs.open(file_path, "rb") as pf: 
        prompt = str(pf.read())    
    return prompt

def read_df_from_gscfs(fs, file_path: Text): 
    import pandas as pd 
    function_by_format = dict(
        csv = pd.read_csv, 
        xlsx = pd.read_excel, 
    )
    func = function_by_format[file_path.split('.')[-1]]
    with fs.open(file_path) as f: 
        df = func(f)
    
    return df

def read_json(fdir) ->dict: 
    with open(fdir) as f: 
        output = json.load(f)
    return output
  
def read_json_to_proto(json_dir):
    from google.protobuf.json_format import ParseDict
    from tensorflow_metadata.proto.v0 import statistics_pb2
    ds_dict = {'datasets': []}
    ds_dict['datasets'].append(read_json(json_dir))
    stat_proto = statistics_pb2.DatasetFeatureStatisticsList()
    ParseDict(ds_dict, stat_proto)
    return stat_proto

def read_text(txt_path: str = '') -> str: 
    if not txt_path: 
        raise RuntimeError('Invalid text path')

    with open(txt_path, 'r') as f: 
        text = f.read()
    return text


def read_yaml(yaml_filepath: str ='') -> dict:
    if not yaml_filepath: 
        raise RuntimeError('Invalid yaml path')

    with open(yaml_filepath, 'r') as f:
        cfg = yaml.full_load(f)
    return cfg
