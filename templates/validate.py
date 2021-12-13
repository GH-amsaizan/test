import pandas as pd
from pathlib import Path
from yaml import safe_load


def run_script() -> None:
    ####### READ IN FILES #######
    base_dir = Path.cwd()
    
    with open("params.yaml", 'r') as fd:
        params = safe_load(fd)
    
    # Script is invoked from root
    path_analysis_in = base_dir.joinpath('data', 'processed', 'clean_data.csv')
    
    path_out_dir = base_dir.joinpath('data', 'results')
    path_out_results = path_out_dir.joinpath('analysis_results.csv')
    
    df = pd.read_csv(path_analysis_in, index_col=0)

    ####### VALIDATE DATA  #######
    print('Validating data...')
    # Validate here
    df_results = df.copy()

    ####### SAVE IMPORTANCE RESULTS #######
    path_out_dir.mkdir(parents=True, exist_ok=True)
    df_results.to_csv(path_out_results)

# ============================================================= #
#                         EXECUTE                               #
# ============================================================= #

if __name__ == "__main__":
    run_script()