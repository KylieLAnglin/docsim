# %%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from openpyxl import load_workbook

from docsim.library import start


# %%
rep_results = pd.read_csv(start.CLEAN_FILEPATH + "study_sims.csv").set_index(
    ["study", "id"]
)

# %%
rep_results["study"] = [i[0] for i in rep_results.index]
rep_results["study_sim"] = np.where(
    rep_results.study == "fall2017",
    rep_results.rep4_study4,
    np.where(
        rep_results.study == "fall2018",
        rep_results.rep4_study5,
        np.where(
            rep_results.study == "spring2018",
            rep_results.rep4_study1,
            np.where(
                rep_results.study == "spring2019",
                rep_results.rep4_study2,
                np.where(
                    rep_results.study == "fall2019TAP", rep_results.rep4_study3, np.nan
                ),
            ),
        ),
    ),
)


sns.set_style("white")

# %% Fidelity Results

script_results = pd.read_csv(start.CLEAN_FILEPATH + "script_sims.csv").set_index(
    ["study", "id"]
)


study1_values = script_results.loc["spring2018"].script_sim3
study2_values = script_results.loc["spring2019"].script_sim3
study3_values = script_results.loc["fall2019TAP"].script_sim3
study4_values = script_results.loc["fall2017"].script_sim3
study5_values = script_results.loc["fall2018"].script_sim3


# %% Figure 1 Fidelity Score Distributions

fig = plt.figure(figsize=(10, 10))
ax = plt.axes()

# ax.set_title('Figure 1: Fidelity Score Distributions', fontsize=15)

bins = np.linspace(0, 0.5, num=10)

sns.distplot(
    study1_values,
    hist=False,
    rug=False,
    color="0.01",
    kde_kws={"linestyle": "solid"},
    label="Behavior Study 1",
)

sns.distplot(
    study2_values,
    hist=False,
    rug=False,
    color="black",
    kde_kws={"linestyle": "dashed"},
    label="Behavior Study 2",
)

sns.distplot(
    study3_values,
    hist=False,
    rug=False,
    color="black",
    kde_kws={"linestyle": "dotted"},
    label="Behavior Study 3",
)

sns.distplot(
    study4_values,
    hist=False,
    rug=False,
    color="lightgray",
    kde_kws={"linestyle": "solid"},
    label="Feedback Study 1",
)

sns.distplot(
    study5_values,
    hist=False,
    rug=False,
    color="lightgray",
    kde_kws={"linestyle": "dashed"},
    label="Feedback Study 2",
)

ax.legend(loc="upper right")
ax.set_xlabel("Adherence Scores")
ax.set_ylabel("Kernel Density")
# notes = "Notes: Fidelity scores are estimated by calculating the " \
#     "similarity between each transcript and an ideal script. " \
#     "A higher score indicates higher fidelity to the script."
# fig.text(.1, .05, notes, ha='left', wrap=True)

fig.savefig(
    start.TABLE_FILEPATH + "Figure 1 Fidelity Score Distributions",
    bbox="tight",
    pad_inches=0.05,
)


for study in [
    study1_values,
    study2_values,
    study3_values,
    study4_values,
    study5_values,
]:
    print(study.std())

# %% Figure 2
fig = plt.figure(figsize=(10, 10))
ax = plt.axes()

# ax.set_title('Figure 2: Fidelity Scores for Feedback Study 2 by Coach',
#             fontsize=15)

coach_code = {
    "Sarah": "A",
    "Arielle": "B",
    "Casedy": "C",
    "Alex": "D",
}
script_results["coach_code"] = script_results["coach"].map(coach_code)
script_results = script_results.sort_values(by="coach_code")

sns.boxplot(
    x="coach_code",
    y="script_sim3",
    data=script_results.loc["fall2018"],
    color="white",
)
sns.swarmplot(
    x="coach_code",
    y="script_sim3",
    data=script_results.loc["fall2018"],
    color="black",
)

ax.set_xlabel("Coach")
ax.set_ylabel("Adherence Scores")

# notes = "Notes: Fidelity scores are estimated by calculating" \
#     " the similarity between" \
#     " each transcript and an ideal script. " \
#     "A higher score indicates \n " \
#     "higher fidelity to the script." \
#     "Boxes indicate the 50th percentile and interquartile range. " \
#     "Whiskers extend to all scores within 1.5 \n times the" \
#     " interquartile range. "
# fig.text(.1, .025, notes, ha='left', wrap=True)


fig.savefig(
    start.TABLE_FILEPATH + "Figure 2 Fidelity Scores for Feedback Study 2 by Coach"
)
plt.show()

for coach in ["A", "B", "C", "D"]:
    print(
        script_results[
            (script_results.coach_code == coach)
            & (script_results.semester == "fall")
            & (script_results.year == 2018)
        ].script_sim3.median()
    )

# %% Figure 3: Panel of Histograms

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(10, 10))
ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax3 = axs[0, 2]
ax4 = axs[1, 0]
ax5 = axs[1, 1]

bins = np.linspace(0, 0.75, num=30)

# fig.suptitle('Figure 3: Fidelity Scores  with Unusual Transcripts Highlighted',
#            fontsize=15)
ax1.hist(study1_values, bins, color="darkgray", alpha=0.75)
ax1.set_xlabel("Behavior Study 1")

ax2.hist(study2_values, bins, color="darkgray", alpha=0.75)
ax2.set_xlabel("Behavior Study 2")


ax3.hist(study3_values, bins, color="darkgray", alpha=0.75)
ax3.set_xlabel("Behavior Study 3")
ax3.hist(study3_values.where(study3_values < 0.15), bins, color="black")

ax4.hist(study4_values, bins, color="darkgray", alpha=1)
ax4.set_xlabel("Feedback Study 1")
ax4.hist(
    study4_values.where((study4_values > 0.33)),
    bins,
    color="black",
)

ax5.hist(study5_values, bins, color="darkgray", alpha=1)
ax5.set_xlabel("Feedback Study 2")
ax5.hist(
    study5_values.where((study5_values < 0.23) | (study5_values > 0.5)),
    bins,
    color="black",
)

for ax in [ax1, ax2, ax3, ax4, ax5]:
    ax.set_ylim(0, 20)

fig.delaxes(axs[1, 2])

fig.text(0.5, 0.04, "Adherence Scores", ha="center")
fig.text(0.04, 0.5, "Number of Transcripts", va="center", rotation="vertical")

# notes = "Notes: Fidelity scores are estimated by calculating the " \
#     "similarity between each transcript and an ideal script. " \
#     "A higher score  \nindicates higher fidelity to the script. " \
#     "Potentially abnormal transcripts (based on visual examination) " \
#     "are highlighted in black. \nThese are the transcripts we have" \
#     " flagged for manual observation."
# fig.text(.1, .025, notes, ha='left')

plt.savefig(start.TABLE_FILEPATH + "Figure 3: Fidelity Panels", dpi=200)

# %% plot
# fall 2017


# study = results.loc[["fall2017", "fall2018"]]
# sns.scatterplot(study.script_sim, study.study_sim, marker="", hue=study.study)
# plt.xlabel("Adherence Score")
# plt.ylabel("Replicability Score")


# for i, txt in enumerate(study.loc["fall2017"].index):
#     plt.annotate(
#         txt,
#         (study.loc["fall2017"].script_sim[i], study.loc["fall2017"].study_sim[i]),
#         color="blue",
#     )

# for i, txt in enumerate(study.loc["fall2018"].index):
#     plt.annotate(
#         txt,
#         (study.loc["fall2018"].script_sim[i], study.loc["fall2018"].study_sim[i]),
#         color="darkorange",
#     )


# %%
