import pandas as pd
from plotly import express as px
from plotly import graph_objects as go

df = pd.read_csv("./scenarios-costs.csv")


def main():
    fig = px.bar(
        data_frame=df,
        x="Renewable Energy Usage Percentage",
        y="Cost",
        color="Cost Source",
        barmode="stack",
        title="Scenarios Cost Graph",
        color_discrete_map={
            "Fossil": "Grey",
            "Pollution": "LightGrey",
            "Wind": "Green",
            "Solar": "Yellow",
            "Storage": "DeepSkyBlue",
        },
    )
    fig.update_traces(marker_line_width=1.5, opacity=0.7)
    fig.show()


if __name__ == "__main__":
    main()
