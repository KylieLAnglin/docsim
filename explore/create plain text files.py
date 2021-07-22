# %%
import pandas as pd

df = pd.read_csv("/Users/kylie/Dropbox/Active/docsim/data/clean/text_transcripts.csv")
transcripts = list(df.clean_text)
file_names = [filename[:-5] for filename in df.filename]
# %%
OUTPUT = "/Users/kylie/Dropbox/Active/docsim/data/plain text transcripts/"


for n in list(range(len(transcripts))):
    print(n)
    f = open(OUTPUT + file_names[n] + ".txt", "w+")
    f.write(transcripts[n])


# %%
