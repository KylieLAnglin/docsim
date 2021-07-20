# %%
from os import link
import pandas as pd

# %%

linking_file = pd.read_csv(start.RAW_FILEPATH + "linking_files.csv", header=0)


fall2017tags = pd.read_csv(
    "/Users/kylie/Dropbox/Active/docsim/data/transcripts/fall2017_speaker_tags.csv"
).rename(columns={"doc": "filename"})[["filename", "coach"]]

fall2018tags = pd.read_csv(
    "/Users/kylie/Dropbox/Active/docsim/data/transcripts/fall2018_speaker_tags.csv"
).rename(columns={"doc": "filename"})[["filename", "coach"]]
fall2019TAPtags = pd.read_csv(
    "/Users/kylie/Dropbox/Active/docsim/data/transcripts/fall2019TAP_speaker_tags.csv"
).rename(columns={"doc": "filename"})[["filename", "coach"]]
spring2018tags = pd.read_csv(
    "/Users/kylie/Dropbox/Active/docsim/data/transcripts/spring2018_speaker_tags.csv"
).rename(columns={"doc": "filename"})[["filename", "coach"]]
spring2019tags = pd.read_csv(
    "/Users/kylie/Dropbox/Active/docsim/data/transcripts/Spring2019_speaker_tags.csv"
).rename(columns={"doc": "filename"})[["filename", "coach"]]

tags = pd.concat(
    [fall2017tags, fall2018tags, spring2018tags, spring2019tags, fall2019TAPtags]
).rename(columns={"coach": "speaker"})


new_linking_file = linking_file.merge(tags, how="outer", on=["filename"])

new_linking_file.to_csv(start.RAW_FILEPATH + "linking_files.csv", index=False)