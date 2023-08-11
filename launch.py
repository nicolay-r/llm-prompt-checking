import sqlite3

import pandas as pd
from tqdm import tqdm

from llm.setup_v1 import ChatBotRev


def launch(sample_filepath, sqlite_output_filepath, chatbot, table_name="contents"):

    con = sqlite3.connect(sqlite_output_filepath)
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(id TEXT, response TEXT)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS i_id ON {table_name}(id)")

    df = pd.read_csv(sample_filepath, sep='\t')
    it = tqdm(df.iterrows(), desc=sample_filepath, total=len(df))

    for i, r in it:
        d = r.to_dict()

        uid = d["id"]

        r = cur.execute(f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE id='{uid}');")
        ans = r.fetchone()[0]
        if ans == 1:
            continue

        it.refresh()
        response = chatbot.ask(d["text_a"])

        cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (str(uid), response))
        con.commit()


# launch(sample_filepath="data/nerel/sample-train-0.csv",
#        sqlite_output_filepath="data/nerel/answers.sqlite3",
#        chatbot=ChatBotRev(),
#        table_name="contents")

launch(sample_filepath="data/nerel-bio/sample-train-0.csv",
       sqlite_output_filepath="data/nerel-bio/answers.sqlite3",
       chatbot=ChatBotRev(),
       table_name="train")
