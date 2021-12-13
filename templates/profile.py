import pandas as pd
import numpy as np
from pathlib import Path
from pandas_profiling import ProfileReport
from yaml import safe_load

# Import parameters
with open('params.yml','r') as file:
    config = safe_load(file)

def run_script() -> None:
    ####### READ IN FILES #######
    base_dir = Path.cwd()

    # Script is invoked from root
    path_data_in = base_dir.joinpath('data', 'processed','clean_data.csv')

    path_out_processed = base_dir.joinpath('data', 'profile_reports')
    path_data_processed = path_out_processed.joinpath('profile_report.html')

    df = pd.read_csv(path_data_in)

    ####### WRANGLE DATA  #######
    profile = ProfileReport(df, title="Pandas Profiling Report", explorative=config.get('explorative', False))

    ####### SAVE DATA #######
    # DVC destroys output directories if cached
    path_out_processed.mkdir(parents=True, exist_ok=True)

    profile.to_file(path_data_processed)

    
# ============================================================= #
#                         EXECUTE                               #
# ============================================================= #

if __name__ == "__main__":
    run_script()