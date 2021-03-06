import pandas as pd

# people from: https://raw.githubusercontent.com/chadwickbureau/register/master/data/people.csv
# sc from:
from pybaseball import statcast
sc = statcast(start_dt='2012-01-01', end_dt='2020-01-01')
sc.to_parquet("statcast_dump.parquet", engine="fastparquet")
# full statcast.csv.gzip file available upon request.

people = pd.read_csv("people.csv")
# sc = pd.read_parquet("statcast_dump.parquet", engine="fastparquet")
people["batter_name"] = people.name_first + " " + people.name_last
merged = pd.merge(
    sc,
    people.loc[:, ["key_mlbam", "batter_name"]],
    how="left",
    left_on="batter",
    right_on="key_mlbam",
)
cols2keep = [
    "player_name",
    "batter_name",
    "pitch_type",
    "game_date",
    "release_speed",
    "events",
    "launch_speed",
    "woba_value",
    "bb_type",
    "balls",
    "strikes",
    "outs_when_up",
    "at_bat_number",
    "type",
    "plate_x",
    "plate_z",
    "stand",
]
sc = merged.loc[:, cols2keep]
sc.to_parquet("statcast.parquet", engine="pyarrow")

sc["date"] = pd.to_datetime(merged["game_date"])
recent = sc.loc[sc.date > "2018-01-01", :]
recent.drop(columns=["date"], inplace=True)
recent.to_parquet("statcast2018.parquet", engine="pyarrow")
