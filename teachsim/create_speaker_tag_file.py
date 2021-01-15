# %%
import os
import fnmatch

import pandas as pd
from openpyxl import load_workbook

from docsim.library import start

# %%
path = start.RAW_FILEPATH + "fall_2019_TAP/coaching/"

files = [file for file in os.listdir(path) if fnmatch.fnmatch(file, "*docx")]

files.sort()

tag_file = pd.DataFrame({"doc": files})

tag_file.to_excel(path + "fall2019_speaker_tags.xlsx", index=False)
# %%
