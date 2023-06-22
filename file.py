import pandas as pd

data = []
with open('en-abbreviations.txt', 'r') as file:
    for line in file:
        try:
            abbreviation, word = line.strip().split('\t')
            data.append([abbreviation, word])
        except ValueError:
            print(f"Ignoring line: {line.strip()}")

df = pd.DataFrame(data, columns=['Abbreviation', 'Word'])
# print(df)
df.to_csv('abbr.csv')