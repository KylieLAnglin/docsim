# %%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from openpyxl import load_workbook

from docsim.library import start


# %%
results = pd.read_csv(start.CLEAN_FILEPATH + "results_stop_stem_wgt_lsa.csv").set_index(
    ["study", "id"]
)
results["study"] = [i[0] for i in results.index]
results["study_sim"] = np.where(
    results.study == "fall2017",
    results.sim_fall2017,
    np.where(
        results.study == "fall2018",
        results.sim_fall2018,
        np.where(
            results.study == "spring2018",
            results.sim_spring2018,
            np.where(
                results.study == "spring2019",
                results.sim_spring2019,
                np.where(
                    results.study == "fall2019TAP", results.sim_fall2019TAP, np.nan
                ),
            ),
        ),
    ),
)

results2 = pd.read_csv(start.CLEAN_FILEPATH + "results_lsa.csv").set_index(
    ["study", "id"]
)

# %% Giant Histogram

studies = ["fall2017", "fall2018", "spring2018", "spring2019"]

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

sns.distplot(
    results.loc[studies]["script_sim"],
    hist=True,
    kde=False,
    bins=int(180 / 5),
    hist_kws={"edgecolor": "black"},
    kde_kws={"linewidth": 4},
)

ax.set_xlabel("Adherence Scores")
ax.set_ylabel("Number of Transcripts")
plt.title("Treatment Adherence in TeachSIM", fontsize=30)


# %% By Study
study_labels = {
    "fall2017": "Feedback 1",
    "fall2018": "Feedback 2",
    "spring2018": "Behavior 1",
    "spring2019": "Behavior 2",
    "fall2019TAP": "Behavior 3",
}

study_colors = {
    "fall2017": "navy",
    "fall2018": "lightblue",
    "spring2018": "darkgreen",
    "spring2019": "seagreen",
    "fall2019TAP": "sandybrown",
}

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))


for study in studies:
    subset = results.loc[study]

    # Draw the density plot
    sns.distplot(
        subset["script_sim"],
        hist=False,
        kde=True,
        kde_kws={"linewidth": 3},
        label=study_labels[study],
        color=study_colors[study],
    )

sns.color_palette("colorblind")


# Add lines for high and low-fidelity
# ax.axvline(x=0.10, color="black")
# ax.axvline(x=0.70, color="black")


# Plot formatting
plt.legend(prop={"size": 16}, title="Study")
plt.title("Adherence in TeachSIM, Disaggregated by Study", fontsize=30)
plt.xlabel("Adherence", fontsize=20)
plt.ylabel("Count", fontsize=20)


# %% Adherence in Feedback

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
bins = np.linspace(0, 0.75, num=30)


for study in ["fall2017", "fall2018"]:
    subset = results.loc[study]

    # Draw the density plot
    sns.histplot(
        subset["script_sim"],
        stat="count",
        bins=bins,
        kde=True,
        label=study_labels[study],
        color=study_colors[study],
    )


# Add lines for high and low-fidelity
# ax.axvline(x=0.10, color="black")
# ax.axvline(x=0.70, color="black")


# Plot formatting
plt.legend(prop={"size": 16}, title="Study")
plt.title("Adherence in TeachSIM, Disaggregated by Study", fontsize=30)
plt.xlabel("Adherence", fontsize=20)
plt.ylabel("Count", fontsize=20)

# %% Adherence in Behavior

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
bins = np.linspace(0, 0.75, num=30)


for study in ["spring2018", "spring2019"]:
    subset = results.loc[study]

    # Draw the density plot
    sns.histplot(
        subset["script_sim"],
        stat="count",
        bins=bins,
        kde=True,
        label=study_labels[study],
        color=study_colors[study],
    )


# Add lines for high and low-fidelity
# ax.axvline(x=0.10, color="black")
# ax.axvline(x=0.70, color="black")


# Plot formatting
plt.legend(prop={"size": 16}, title="Study")
plt.title("Adherence in TeachSIM, Disaggregated by Study", fontsize=30)
plt.xlabel("Adherence", fontsize=20)
plt.ylabel("Count", fontsize=20)

# %% Coaches in Feedback 2
study = ["spring2019"]

fig = plt.figure(figsize=(10, 10))
ax = plt.axes()

# ax.set_title('Figure 2: Fidelity Scores for Feedback Study 2 by Coach',
#             fontsize=15)

coach_code = {
    "Casedy": "C",
    "Sarah": "A",
    "Alex": "D",
    "Arielle": "B",
    "Emily": "E",
    "Bryan": "F",
}
results["coach_code"] = results["coach"].map(coach_code)


sns.boxplot(
    x="coach_code",
    y="script_sim",
    data=results.loc[study][results.coach != "Alex"],
    color="white",
)
sns.swarmplot(
    x="coach_code",
    y="script_sim",
    data=results.loc[study][results.coach != "Alex"],
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

for coach in ["A", "B", "C", "D", "E", "F"]:
    print(results.loc[study][results.coach_code == coach].script_sim.median())

# %%
for study in studies:
    print(results.loc[study].script_sim.mean().round(2))
    print("[", results.loc[study].script_sim.std().round(2), "]")

# %%
