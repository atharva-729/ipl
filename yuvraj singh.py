import pandas as pd
import os
import glob

search_path = os.path.join("auction roi/", '*.csv')
csv_files = glob.glob(search_path)

for file_path in csv_files:
    df = pd.read_csv(file_path, low_memory=False)

    df = df.replace("Yudhvir Singh", "Yuvraj Singh", regex=True)

    df.to_csv(file_path, index=False)

