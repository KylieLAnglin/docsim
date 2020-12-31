# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# The purpose of this notebook is to create a series of demo charts for Kylie's interview at the University of Connecticut.
# %% [markdown]
# # First chart -- random data points with random growth
#
# This chart is intended to be a bipartite graph with initial points drawn from a normal distribution of mean 70 then adding a growth factor drawn from a normal distribution of mean 5. Deviations to be set as we see fit. Then, graph the points on a time scale and connect from one time _t_ to the other _t1_.

# %%
import altair as alt
import numpy as np
import pandas as pd


# %%
initial_draws = np.random.normal(loc=70, scale=5, size=60)


# %%
growth_factors = np.random.normal(loc=10, scale=3, size=60)


# %%
df = pd.DataFrame(initial_draws, columns=["value"])
df["t"] = 1
df["ind"] = df.index
df2 = pd.DataFrame((initial_draws + growth_factors), columns=["value"])
df2["t"] = 2
df2["ind"] = df2.index


# %%
df_com = pd.concat([df, df2])


# %%
df_com


# %%
alt.Chart(df_com).mark_line().encode(
    x="t:O",
    y="value",
    color="ind:O",
).properties(width=400, height=600)


# %%
df_com_2 = df_com.copy()
df_com_2.loc[df_com_2["t"] == 1, "t"] = " T₀"
df_com_2.loc[df_com_2["t"] == 2, "t"] = "T₁"


# %%
points = (
    alt.Chart(df_com_2)
    .mark_line(color="Black")
    .encode(
        alt.X(
            "t:O",
            scale=alt.Scale(
                zero=False,
            ),
            axis=alt.Axis(title="", labelAngle=0),
            sort=["T₀", "D", "T₂"],
        ),
        alt.Y(
            "mean(value)",
            scale=alt.Scale(zero=False, domain=(50, 100)),
            axis=alt.Axis(title="Y", titleAngle=0),
        ),
        order=alt.Order(
            "t",
        ),
    )
    .properties(width=400, height=400)
)

connect = (
    alt.Chart(df_com_2)
    .mark_point(color="Black", size=1000, filled=True)
    .encode(
        alt.X(
            "t:O",
            scale=alt.Scale(
                zero=False,
            ),
            axis=alt.Axis(title="", labelAngle=0),
            sort=["T₀", "D", "T₂"],
        ),
        alt.Y(
            "mean(value)",
            scale=alt.Scale(zero=False, domain=(50, 100)),
            axis=alt.Axis(title="Y", titleAngle=0),
        ),
        order=alt.Order(
            "t",
        ),
    )
    .properties(width=400, height=400)
)

line = alt.Chart(pd.DataFrame({"t": ["D"]})).mark_rule().encode(x="t:O")

points + connect + line


# %%
