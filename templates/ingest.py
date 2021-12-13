import pandas as pd
from pathlib import Path
# Script is invoked from repository root

def run_script() -> None:
    ####### READ IN FILES #######
    base_dir = Path.cwd()
    
    # Could be cloud hosted, local database, etc...
    # If just using a flat file, ingest stage is not needed
    path_data_in = base_dir.joinpath('data', 'external','external_data.csv')

    path_out_processed = base_dir.joinpath('data', 'raw')
    path_data_processed = path_out_processed.joinpath('raw_data.csv')

    ####### DO SOMETHING ########
    # Read in external data
    df = pd.read_csv(path_data_in)

    ####### SAVE DATA #######
    # DVC destroys output directories if cached
    path_out_processed.mkdir(parents=True, exist_ok=True)

    df.to_csv(path_data_processed)
    

# ============================================================= #
#                         EXECUTE                               #
# ============================================================= #

if __name__ == "__main__":
    run_script()