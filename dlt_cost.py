# -*- coding: utf-8 -*-
"""DLT cost.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GBd6DOLBdIBuPAdM-XROrwvlB4YXrMFN
"""

#BOTH THE COST TOGETHER


import pandas as pd
import csv

# Step 1: Load and clean initial file ('bhooki_check.csv')
df = pd.read_csv('parse_sona.csv', delimiter='\t', header=None, quotechar='"', skipinitialspace=True, dtype=str)
df[0] = df[0].str.replace("word.", "", regex=False)  # Remove "word." from first column

# Preserve trailing zeros
def preserve_trailing_zeros(value):
    parts = value.split('.')
    if len(parts) == 2 and parts[1].endswith('0'):
        return value
    else:
        return value

df[0] = df[0].apply(preserve_trailing_zeros)
df.to_csv('parse_joota1.csv', index=False, sep='\t', header=False, quoting=csv.QUOTE_NONE)

# Step 2: Modify the 4th column in 'parse_joota1.csv' and save to 'joota_dep2.csv'
df = pd.read_csv('parse_joota1.csv', sep=",", header=None, dtype=str)
def add_suffix(row):
    suffix = str(row[0]).split('.')[0] + "."
    return suffix + str(row[2])

df[3] = df.apply(lambda row: add_suffix(row) if pd.notnull(row[0]) else row[3], axis=1)
df.to_csv('joota_dep2.csv', sep=',', index=False, header=False)

# Step 3: Calculate distances in 'joota_dep2.csv' and save to 'bhooki_dep3.csv'
df = pd.read_csv('joota_dep2.csv', header=None, names=['index', 'word', 'pos', 'value', 'connect'], dtype=str)
df['distance'] = 0
for i, row in df.iterrows():
    for j, target_row in df.iterrows():
        if row['value'] == target_row['index'] and row['index'] != target_row['index']:
            distance_value = abs(i - j) - 1
            df.at[j, 'distance'] += distance_value

df.to_csv('bhooki_dep3.csv', index=False, header=False, float_format='%.2f')

# Step 4: Load final data for storage cost calculation
data = pd.read_csv('bhooki_dep3.csv', names=['Word_ID', 'with', 'word_eng', 'word', 'pos', 'dep', 'rel'], dtype=str)

# Storage cost calculation function
def calculate_storage_cost(df):
    storage_cost = []
    current_cost = 0
    current_sentence = None

    increment_deprels = {'k1', 'r6', 'pof', 'k1s', 'k7t', 'k5', 'k7p', 'pof', 'r6-k2', 'k2', 'k2p', 'k3', 'k4', 'k7', 'vmod', 'pof_cn', 'rt'}
    reset_deprels = {'main', 'lwg_vaux', 'nmod_relc'}

    for index, row in df.iterrows():
        word_id = row['with']
        dep_rel = str(row['rel'])
        pos = str(row['pos'])

        word_id_parts = word_id.split('.')
        if len(word_id_parts) >= 2:
            sentence_id = word_id_parts[1]
        else:
            print(f"Warning: Skipping row with invalid word_id format: {word_id}")
            storage_cost.append(current_cost)
            continue

        if sentence_id != current_sentence:
            current_sentence = sentence_id
            current_cost = 0

        if dep_rel == 'main' and pos == 'CC':
            storage_cost.append(current_cost)
            continue
        elif dep_rel == 'nmod_relc' and pos == 'VM':
            current_cost = 0
        elif dep_rel in increment_deprels:
            current_cost += 1
        elif dep_rel in reset_deprels:
            current_cost = 0
        elif dep_rel == 'lwg_vaux' and pos == 'VAUX':
            if index == len(df) - 1 or (index + 1 < len(df) and df.iloc[index + 1]['with'].split('.')[1] != sentence_id):
                current_cost = 0
            else:
                next_dep_rel = str(df.iloc[index + 1]['rel'])
                if next_dep_rel in increment_deprels:
                    current_cost -= 1
                else:
                    current_cost = 0
        elif dep_rel == 'ccof':
            if pos == 'VM':
                if index == len(df) - 1 or (index + 1 < len(df) and df.iloc[index + 1]['with'].split('.')[1] != sentence_id):
                    current_cost = 0
                else:
                    current_cost -= 1
            elif pos == 'NN':
                current_cost += 1
        elif pos == 'CC':
            pass
        elif dep_rel == 'lwg_vaux' and pos == 'VM':
            current_cost = 0

        storage_cost.append(current_cost)

    df['Storage_Cost'] = storage_cost
    return df

# Apply the storage cost calculation
result_df = calculate_storage_cost(data)

# Save the final output
output_path = 'final_output.csv'
result_df.to_csv(output_path, index=False)
print("Processing complete. Results saved to", output_path)