import pandas as pd
import numpy as np
from pathlib import Path

def run_script() -> None:
    ####### READ IN FILES #######
    base_dir = Path.cwd()

    # Script is invoked from root
    path_data_in = base_dir.joinpath('data', 'raw','raw_data.csv')

    path_out_processed = base_dir.joinpath('data', 'processed')
    path_data_processed = path_out_processed.joinpath('clean_data.csv')

    df = pd.read_csv(path_data_in)

    ####### WRANGLE DATA  #######
    total_rows = df.shape[0]
    print(f'Raw data shape: {df.shape}')
    df = df.dropna(axis=0, how='any')
    df['filler'] = 0
    print(f'Clean data shape: {df.shape}')
    print(f'Percent Missingness: {(1 - df.shape[0] / total_rows) * 100}')

    ####### SAVE DATA #######
    # DVC destroys output directories if cached
    path_out_processed.mkdir(parents=True, exist_ok=True)

    df.to_csv(path_data_processed)
    

# ============================================================= #
#                         EXECUTE                               #
# ============================================================= #

if __name__ == "__main__":
    run_script()