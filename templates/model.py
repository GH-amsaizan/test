import pandas as pd
import numpy as np
from pathlib import Path
from time import sleep
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.inspection import permutation_importance
from mlflow import log_metric, log_param, start_run
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

    ####### MODEL DATA  #######
    print('Building model...')
    features = df.loc[:, df.columns != 'strength']
    target = df.loc[:, df.columns == 'strength']
    X_train, X_test, y_train, y_test = train_test_split(features, target, random_state=0)

    alphas = params.get('train').keys()
    for tune in alphas:
        # New Run for each value of alpha
        # We are training the model across a Grid of hyper-parameters defined in params.yaml
        with start_run():
            alpha = params.get('train').get(tune).get('alpha')
            log_param('alpha', alpha)
            model = Ridge(alpha=alpha).fit(X_train, y_train)
            results = permutation_importance(model, X_test, y_test, n_repeats=300, random_state=42)
            score = model.score(X_test, y_test)
            log_metric('score', score)
            # Make dataframe out of raw importance values by feature. A distribution of values is returned.
            df_results = pd.DataFrame(results.get('importances'))


    ####### SAVE IMPORTANCE RESULTS #######
    path_out_dir.mkdir(parents=True, exist_ok=True)
    df_results.to_csv(path_out_results)

# ============================================================= #
#                         EXECUTE                               #
# ============================================================= #

if __name__ == "__main__":
    run_script()