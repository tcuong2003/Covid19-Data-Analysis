import json
from pathlib import Path

nb_path = Path('notebooks/1_data_understanding.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))
changed = False

for cell in nb.get('cells', []):
    # Convert import markdown cell to code cell
    if cell.get('cell_type') == 'markdown' and any('import pandas as pd' in s for s in cell.get('source', [])):
        cell['cell_type'] = 'code'
        cell['metadata']['language'] = 'python'
        changed = True

    # Update data-load paths
    if cell.get('cell_type') == 'code' and any('/mnt/data/time_series_covid19_confirmed_global.csv' in s for s in cell.get('source', [])):
        cell['source'] = [
            "# Update paths to local repository data folder",
            "confirmed = pd.read_csv('../data/1_raw/time_series_covid19_confirmed_global.csv')",
            "deaths = pd.read_csv('../data/1_raw/time_series_covid19_deaths_global.csv')",
            "recovered = pd.read_csv('../data/1_raw/time_series_covid19_recovered_global.csv')",
            ""
        ]
        changed = True

if changed:
    nb_path.write_text(json.dumps(nb, ensure_ascii=False, indent=4), encoding='utf-8')
    print('Notebook updated')
else:
    print('No changes applied')
