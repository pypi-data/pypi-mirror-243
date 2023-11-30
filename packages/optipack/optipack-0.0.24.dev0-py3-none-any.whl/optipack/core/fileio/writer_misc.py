import json
import yaml
from typing import Dict, List, Union, Text
import pandas as pd

def write_json(file_path: Text, content: Union[Dict, List], mode: Text = 'a+'): 
    with open(file_path, mode) as f: 
        f.write(json.dumps(content))
        
def write_json_to_gcsfs(fs, file_path: Text, content: Union[Dict, List], mode: Text = 'a+'): 
    with fs.open(file_path, mode) as f:
        f.write(json.dumps(content))

def write_df_to_gcsfs(fs, file_path: Text, df: pd.DataFrame, mode: Text = 'w'): 
    function_by_format = dict(
        csv = df.to_csv, 
        xlsx = df.to_excel, 
    )
    func = function_by_format[file_path.split('.')[-1]]
    with fs.open(file_path, mode) as f: 
        func(f)
        
def write_stat_html(fdir: str, content: Union[Dict, List], mode: Text = 'a+'):
    with open(fdir, 'a+') as f: 
        f.write(content.data)
        
def write_images(fdir, content): 
    with open(fdir, 'wb') as f: 
        for r in content: 
            f.write(r)

def write_yaml(yaml_filepath: str, content: Union[Dict, List]):
    if not yaml_filepath: 
        raise RuntimeError('Invalid yaml path')
    
    with open(yaml_filepath, 'a+') as f: 
        yaml.dump(content, f, default_flow_style=False, allow_unicode=True)

def write_text(file_path: str, content: List): 
    with open(file_path, 'a+') as f: 
        f.writelines(content)  
