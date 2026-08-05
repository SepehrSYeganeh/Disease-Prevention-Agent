import pandas as pd
from src.tools.arrhythmia_classifier import ecg_classifier

test_df = pd.read_csv("../data/mit-bih-arrhythmia-dataset/mitbih_test.csv")
row = 0
X = test_df.iloc[row, :186].to_numpy()
y = test_df.iloc[row, 186]

print(f"predicted: {ecg_classifier(X)}")
print(f"actual: {y}")

