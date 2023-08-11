import sqlite3
from collections import Counter
from os.path import join

import pandas as pd
from tqdm import tqdm


def assess(sqlite_output_filepath, table_name):
    con = sqlite3.connect(sqlite_output_filepath)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    for row in cur:
        yield row


dir = "data/nerel"
table_name = "contents"

samples_filepath = join(dir, "sample-train-0.csv")
df = pd.read_csv(samples_filepath, sep='\t')
df.insert(len(df.columns), "relations_pretty_type", None)
df.insert(len(df.columns), "relations_pretty_value", None)
df.insert(len(df.columns), "relation_type", None)
df.insert(len(df.columns), "entity_values", None)

rel_types_count = Counter()

acc_results = {}

for row_id, response in tqdm(assess(sqlite_output_filepath=join(dir, "answers.sqlite3"), table_name=table_name)):

    answer = response.split('.')[0].lower()

    row = df[df["id"] == row_id].iloc[0]
    text_a = row["text_a"]
    query = text_a[text_a.index(':') + 1:].split()
    s_ind = row["s_ind"]
    t_ind = row["t_ind"]

    rel_type = None
    for i, w in enumerate(query):
        if i > 5 and w.upper() == w and query[i-1] == "type" and query[i-2] == "of":
            rel_type = w
            break

    inds = [int(x) for x in row["entities"].split(',')]
    values = [query[i].replace(",", "") for i in inds]
    types = row["entity_types"].split(',')
    type_src = types[inds.index(s_ind)]
    type_tgt = types[inds.index(t_ind)]
    val_src = query[s_ind]
    val_tgt = query[t_ind]

    answer_sent = "pos" if "yes" in answer else "neg"

    # Writing value
    pretty_type = f"({type_src}->{type_tgt};{answer_sent})"
    pretty_value = f"({val_src}->{val_tgt};{answer_sent})"
    row_index = df.index[df["id"] == row_id].tolist()[0]
    df.at[row_index, "relations_pretty_type"] = pretty_type
    df.at[row_index, "relations_pretty_value"] = pretty_value
    df.at[row_index, "relation_type"] = rel_type
    df.at[row_index, "entity_values"] = ",".join(values)

    rel_types_count[rel_type] += 1
    if rel_type not in acc_results:
        acc_results[rel_type] = [0, 0]
    acc_results[rel_type][0 if answer_sent == "pos" else 1] += 1


def calc_acc(v):
    t, f = v
    return round(float(t)/float(t+f), 2)


print(rel_types_count)
for r_type, r_value in sorted(list(acc_results.items()), key=lambda item: calc_acc(item[1]), reverse=True):
    result = calc_acc(r_value)
    count = rel_types_count[r_type]
    print(f"{r_type} (ACC): {result} ({count})")
df.to_csv(join(dir, "responses-train-0.csv"))
