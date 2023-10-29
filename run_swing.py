import numpy as np
from itertools import combinations
import polars as pl
from tqdm import tqdm
import pathlib

# https://www.kaggle.com/datasets/olxdatascience/olx-jobs-interactions?select=README.txt
path = pathlib.Path("path")




def calc_swing(data, alpha=1.):
    items = data.select("item").unique().to_numpy().squeeze()

    swing = dict()
    for i in tqdm(items):
        i_data = data.filter(pl.col("item") == i)
        ui = i_data.select("user").unique().to_numpy().squeeze()
        if ui.shape == ():
            continue
        for u,v in combinations(ui, 2): # should be permutations?
            iu = data.filter(pl.col("user") == u).select("item").unique("item").to_numpy().squeeze()
            iv = data.filter(pl.col("user") == v).select("item").unique("item").to_numpy().squeeze()
            
            if iu.shape == () or iv.shape == ():
                continue
            
            wu = 1 / np.sqrt(iu.shape[0])
            wi = 1 / np.sqrt(iv.shape[0])
            iu_and_iv = np.intersect1d(iu, iv)
            k = iu_and_iv.shape[0]
            if k < 2:
                # only the seed product in common
                continue
            
            for j in iu_and_iv:
                swing_i = swing.get(i, dict())
                swing_i[j] = swing_i.get(j, 0) + (wu * wi) / (alpha + k) # sum here?
                swing[i] = swing_i
            #print(u,v)
    return swing

if __name__ == "__main__":
    session_length = 30 * 60  # 30 minutes in seconds
    d = (pl.read_csv(path / "interactions.csv")
        .filter((pl.col("timestamp") < 1581638400) & (pl.col("event") == "click"))
        .filter((pl.col("item") < 1000))
        .sort("timestamp")
    )


    d_train = d.filter(pl.col("timestamp") < 1581552000)
    d_test = d.filter(pl.col("timestamp") >= 1581552000)
    
    swing = calc_swing(d_train, alpha=1.)
    
    k = 10
    u = d_test.unique(subset=["user", "item"]).group_by("user").agg(pl.col("item")).filter(pl.col("item").list.lengths() > k)
    
    for u_ in tqdm(u.rows()):
        true_clicked = u_[1][:k+1]
        seed_item = true_clicked[0]
        recs = swing.get(seed_item)
        
        print("True clicked:", true_clicked)
        print("Seed item:", seed_item)
        print("Recs:", recs)
        
        break