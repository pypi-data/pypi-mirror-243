import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
import urllib.request


def modify_interval(interval1, interval2):
    if interval2 > interval1:
        return pd.Interval(interval1.left, interval2.right, closed="right")
    else:
        return pd.Interval(interval2.left, interval1.right, closed="right")


def summary_intervals(df, model_label):
    df_q = df.copy()
    df[model_label].sum()
    rank_intervals = df_q.groupby(by=["decile_rank"]).agg(
        {model_label: ["count", "sum"]}
    )
    rank_intervals.columns = ["count", "sum"]
    rank_intervals["perc"] = rank_intervals["sum"] * 100 / rank_intervals["count"]
    rank_intervals = rank_intervals.rename(columns={"perc": "BadRate %"})
    rank_intervals = rank_intervals.reset_index()
    return rank_intervals


def concat_intervals(df_in, i, j, model_label):
    df_modify = df_in.copy()
    rank_intervals = summary_intervals(df_modify, model_label)
    rank_intervals = sortIntervals(rank_intervals)
    percentiles = rank_intervals["decile_rank"].unique()

    new_interval = modify_interval(percentiles[i], percentiles[j])
    df_modify["decile_rank"] = df_modify["decile_rank"].cat.remove_categories(
        [percentiles[i], percentiles[j]]
    )
    df_modify["decile_rank"] = df_modify["decile_rank"].cat.add_categories(
        [new_interval]
    )
    df_modify["decile_rank"] = df_modify["decile_rank"].fillna(new_interval)
    rank_intervals = summary_intervals(df_modify, model_label)
    return df_modify, rank_intervals


def heapify(series, n, i):
    largest = i
    l = 2 * i + 1 # noqa
    r = 2 * i + 2
    if l < n and series.iloc[i] < series.iloc[l]:
        largest = l
    if r < n and series.iloc[largest] < series.iloc[r]:
        largest = r
    if largest != i:
        (series.iloc[i], series.iloc[largest]) = (
            series.iloc[largest],
            series.iloc[i],
        )
        heapify(series, n, largest)


def heapSort(series_in):
    
    series = series_in.copy()
    n = len(series)
    for i in range(n // 2 - 1, -1, -1):
        heapify(series, n, i)
    for i in range(n - 1, 0, -1):
        (series[i], series[0]) = (series[0], series[i])
        heapify(series, i, 0)
    return series


def sortIntervals(df, interval_name="decile_rank"):
    series_out = heapSort(df[interval_name])
    return (
        df.merge(pd.DataFrame(series_out).reset_index(), on=interval_name, how="left")
        .sort_values("index")
        .drop(columns="index")
        .reset_index(drop=True)
    )


def next_state(df, i, target):
    # Generate the comparison between the previous and next values
    df_modify_forward, df_summary_forward = concat_intervals(df, i, i + 1, target)
    df_summary_forward = sortIntervals(df_summary_forward)
    br_f = df_summary_forward.loc[i + 1, "BadRate %"]  # next badrate

    if i != 0:
        df_modify_back, df_summary_back = concat_intervals(df, i, i - 1, target)
        df_summary_back = sortIntervals(df_summary_back)
        br_back = df_summary_back.loc[i, "BadRate %"]  # next badrate
    else:
        br_back = float("inf")

    # output
    if br_f < br_back:
        idx_sum = 0
        return df_modify_forward, df_summary_forward, idx_sum
    else:
        idx_sum = -1
        return df_modify_back, df_summary_back, idx_sum


def get_badrates(df, idx):
    br_i = df.iloc[idx]["BadRate %"]
    br_next = df.iloc[idx + 1]["BadRate %"] if idx + 1 <= df.shape[0] else -1
    br_previous = df.iloc[idx - 1]["BadRate %"] if idx != 0 else -1
    return br_i, br_next, br_previous


def plot_steps(df, x, y):
    image_url = "https://bitbucket.org/imezade/bcirisktools/raw/cddb3e4b99cf89c8792c2d5027b4525003532628/bcirisktools/bci_logo.png"
    urllib.request.urlretrieve(image_url, "bci_logo.png")
    bci_logo = Image.open("bci_logo.png")

    fig = px.bar(
        df.astype({x: str}),
        x=x,
        y=y,
        animation_frame="step",
        text_auto=True,
    )
    fig.update_layout(
        title=f"Evolution of the {y} in the iterations",
        height=400,
        template="simple_white",
    )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=-0.95,
                x=0.01,
                xanchor="left",
                yanchor="bottom",
            )
        ],
    )
    fig.layout["sliders"][0]["pad"] = dict(
        t=100.0,
    )
    fig.update(layout_yaxis_range=[0, df[y].max()])
    fig.add_layout_image(
        dict(
            source=bci_logo,
            xref="paper",
            yref="paper",
            x=1,
            y=1.05,
            sizex=0.2,
            sizey=0.2,
            xanchor="right",
            yanchor="bottom",
        )
    )
    # update layout properties
    fig.update_layout(
        autosize=True,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
    )

    return fig


def plot_badrate_pop(df_summary):
    bool_ko = df_summary["KO"] == True
    df_KO = df_summary[bool_ko]
    df_non_KO = df_summary[~bool_ko]
    
    image_url = "https://bitbucket.org/imezade/bcirisktools/raw/cddb3e4b99cf89c8792c2d5027b4525003532628/bcirisktools/bci_logo.png"
    urllib.request.urlretrieve(image_url, "bci_logo.png")
    bci_logo = Image.open("bci_logo.png")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=df_non_KO["decile_rank"].astype(str),
            y=df_non_KO["count"],
            name="Population",
            marker_color="#4C78A8",
        ),
    )
    fig.add_trace(
        go.Bar(
            x=df_KO["decile_rank"].astype(str),
            y=df_KO["count"],
            name="Population",
            marker_color="#E45756",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df_summary["decile_rank"].astype(str),
            y=df_summary["BadRate %"],
            name="BadRates",
            mode="lines+markers+text",
            textposition="top center",
            text=df_summary["BadRate %"].round(2).astype(str),
            marker_color="#F58518",
        ),
        secondary_y=True,
    )
    fig.update_yaxes(type="log")
    fig.update_layout(
        height=500,
        title_text="BadRate and Population",
        showlegend=False,
        template="simple_white",
    )
    fig.update_yaxes(title_text="<b>Population</b> Quantity (n)", secondary_y=False)
    fig.update_yaxes(title_text="<b>BadRate</b> Percentage (%)", secondary_y=True)
    # Add logo
    fig.add_layout_image(
        dict(
            source=bci_logo,
            xref="paper",
            yref="paper",
            x=1,
            y=1.05,
            sizex=0.2,
            sizey=0.2,
            xanchor="right",
            yanchor="bottom",
        )
    )
    # update layout properties
    fig.update_layout(
        autosize=True,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
    )

    return fig


def autoProfiling(clf, data, timestamp="period", model_target="target_value", set_p=10, diff_br=0, search_br=None, KO=20, max_iterations=150, quantils=20,):
    """Create score cuts to mantain the badrate along the time given
    a set of scores, performance variable and expected variables.

    Args:
        target (list): performance variable for a given population.
        scores (list): probability scores for a given population.
        expected_br (list): Expected badrates to be achieved.
        n_exploitation (int, optional): Number of exploitation rounds. 
        Defaults to 100.

    Returns:
        pandas.DataFrame, figure: Return a tuple where the [1] is the
        summary of the created profiles, while [2] is a figure with
        the profiles and badrate.
    """
    # time and target list
    tt_list = [timestamp, model_target]

    # Get predictions from the model
    y_pred = clf.predict_proba(data.drop(columns=tt_list))[::, -1]

    # get intervals for the data
    df_modify = data[tt_list]
    df_modify.loc[:, "scores"] = y_pred
    df_modify.loc[:, "decile_rank"] = pd.qcut(df_modify["scores"], q=quantils)

    # get the summaary for th
    steps = []  # list to save steps
    df_summary = summary_intervals(df_modify, model_target)
    steps.append(df_summary)

    # Set values for the while and index
    create_profiles = True
    idx = 0
    stagnant = 0
    iterations = 0
    while create_profiles:
        print(f"Processing profiles... loading index {idx}", end="\r")
        # calculate the porcentage and badrate for the reference and reference + 1
        p = df_summary.iloc[idx]["count"] * 100 / df_summary["count"].sum()
        # badrates with the new profiles
        br_i, br_next, br_previous = get_badrates(df_summary, idx)
        # we check if we must to add 1 to the idx or not
        if (br_i > br_previous and br_i < br_next) or (
            stagnant == 1 and br_i > br_previous
        ):
            idx += 1
            stagnant = 0  # reset the stagnant moving us 1 position ahead
            steps.append(df_summary)  # save the summary that we get in this step
        # finish the iteration
        if idx == df_summary.shape[0] - 1 or iterations == max_iterations:
            if iterations == max_iterations:
                print(
                    f"""It was not possible to reach an optimum of profiles: \n
                    Total Iterations: {max_iterations}"""
                )
            else:
                break

        # rules to concatenate the intervals
        if p < set_p and br_i >= br_next or stagnant == 1:
            df_modify, df_summary, idx_sum = next_state(df_modify, idx, model_target)
            idx = idx_sum + idx  # correct the reference
        elif p > set_p and (br_i >= br_next or br_i <= br_previous):
            if br_previous == -1:
                # force forward
                df_modify, df_summary = concat_intervals(
                    df_modify, idx, idx + 1, model_target
                )
                df_summary = sortIntervals(df_summary)
            else:
                # force back
                df_modify, df_summary = concat_intervals(
                    df_modify, idx, idx - 1, model_target
                )
                df_summary = sortIntervals(df_summary)
                # we set this kind of behaviour as stagnant using 1
                stagnant = 1
        elif p < set_p and br_i < br_previous:
            df_modify, df_summary = concat_intervals(
                df_modify, idx, idx + 1, model_target
            )
            df_summary = sortIntervals(df_summary)

        # add 1 to the number of iterations
        iterations += 1

    if not isinstance(search_br, list):
        # Add here the bad rate diff iterator
        idx = 0
        print("\n")
        while True:
            print(f"Looking differences...loading index {idx}", end="\r")
            if idx == df_summary.shape[0] - 1:
                break

            # Calculate the actual, next and previous badrate
            br_i, br_next, br_previous = get_badrates(df_summary, idx)
            # Calculate the difference between the badrates
            diff_bool = np.abs(br_next - br_i) > diff_br
            # we check if we must to add 1 to the idx or not
            # added a new diff to check if exists difference between
            # badrates
            if br_i > br_previous and br_i < br_next and diff_bool:
                idx += 1
                stagnant = 0  # reset the stagnant moving us 1 position ahead
                steps.append(df_summary)  # save the summary that we get in this step
            else:
                df_modify, df_summary = concat_intervals(
                    df_modify, idx, idx + 1, model_target
                )
                df_summary = sortIntervals(df_summary)
    else:
        # Check if we have numbers
        search_br = list(set(search_br))
        check_numbers = all([isinstance(i, (float, int)) for i in search_br])
        if not check_numbers:
            raise TypeError("Only integers or floats are allowed")

        # Optimize badrates
        idx = 0
        print("\n")
        while True:
            print("Reaching the best br 4 U", end="\r")
            if (
                idx == len(search_br)
                or df_summary.shape[0] == len(search_br)
                or idx == max_iterations
            ):
                break

            # Calculate the actual, next and previous badrate
            br_i, br_next, br_previous = get_badrates(df_summary, idx)
            # Calculate the difference between the badrates
            search_bool = br_i <= search_br[idx]
            # we check if we must to add 1 to the idx or not
            # added a new diff to check if exists difference between
            # badrates
            if br_i > br_previous and br_i < br_next and search_bool:
                idx += 1
                steps.append(df_summary)  # save the summary that we get in this step
            else:
                df_modify, df_summary = concat_intervals(
                    df_modify, idx, idx + 1, model_target
                )
                df_summary = sortIntervals(df_summary)

    # Concatenate KO profiles
    intervals_list = [-0.01]
    for row in df_summary.iloc[1:, :].iterrows():
        if KO > row[1]["BadRate %"]:
            intervals_list.append(row[1]["decile_rank"].left)
        else:
            intervals_list.append(row[1]["decile_rank"].left)
            break
    intervals_list.append(1)
    df_modify.loc[:, "decile_rank"] = pd.cut(df_modify["scores"], intervals_list)
    df_summary = summary_intervals(df_modify, "target_value")
    df_summary.loc[:, "KO"] = df_summary["decile_rank"].apply(lambda x: 1 in x)


    # return df_modify, df_summary

    # Plot
    fig = plot_badrate_pop(df_summary)

    # add figure to a output dict
    figs = dict()
    figs["profiles"] = fig

    # plot steps
    df_output_steps = pd.DataFrame()
    for it, step in enumerate(steps):
        step["step"] = it + 1
        step
        df_output_steps = pd.concat([df_output_steps, step], axis=0)

    # plot badrate steps
    figs["steps_badrate"] = plot_steps(df_output_steps, "decile_rank", "BadRate %")
    # plot population steps
    figs["steps_population"] = plot_steps(df_output_steps, "decile_rank", "count")

    return df_summary, intervals_list, figs


def refillProfiles(target, scores, expected_br, n_exploitation=100):
    """Create score cuts to mantain the badrate along the time given
    a set of scores, performance variable and expected variables.

    Args:
        target (list): performance variable for a given population.
        scores (list): probability scores for a given population.
        expected_br (list): Expected badrates to be achieved.
        n_exploitation (int, optional): Number of exploitation rounds. 
        Defaults to 100.

    Returns:
        pandas.DataFrame, figure: Return a tuple where the [1] is the
        summary of the created profiles, while [2] is a figure with
        the profiles and badrate.
    """
    # TODO: Optimize the code, use pandas's paralellism to improve the 
    # execution time
    expected_br.append(100)

    # Prepare the data to sort the data
    df_pred = pd.DataFrame(columns=["yhat", "target"])
    df_pred["yhat"] = scores
    df_pred["target"] = target
    df_pred = df_pred.sort_values(["yhat", "target"], ascending=True).reset_index(
        drop=True
    )

    # Generate variables to search the badrate
    df_temp = pd.DataFrame(columns=["yhat", "target"])
    br_idx, idx = 0, 0
    br_output = pd.DataFrame(columns=["decile_rank", "BadRate %", "count"])
    # Don't try this loop at home please, put a True is a really bad practice
    while True:
        # comprobate if the len
        if br_idx > len(expected_br) or idx == df_pred.shape[0]:
            break

        # Generate de dataframe to compare the badrate
        df_temp = pd.concat([df_temp, pd.DataFrame(df_pred.iloc[idx, :]).T], axis=0)
        crr_br = df_temp["target"].mean() * 100

        # If the current badrate is bigger than the expected badrate enter here
        if crr_br >= expected_br[br_idx] and crr_br < 100 and crr_br > 0:
            # Exploitation over N values
            # The idea here is explore more option, sometimes we have a 
            # fake high rate and, we need to see beyond.
            df_exploit = df_temp.copy()
            exploited = False
            for it_exploit in range(1, n_exploitation):
                if idx + it_exploit <= df_pred.shape[0]:
                    df_exploit = pd.concat(
                        [df_exploit, pd.DataFrame(df_pred.iloc[idx + it_exploit, :]).T],
                        axis=0,
                    )
                    crr_br_exploit = df_exploit["target"].mean() * 100
                    if (
                        crr_br_exploit < crr_br
                        and crr_br_exploit >= expected_br[br_idx]
                        and crr_br < 100
                        and crr_br > 0
                    ):
                        df_temp = df_exploit.copy()
                        idx = idx + it_exploit
                        exploited = True
                        break
                else:
                    break

            if exploited:
                continue

            # If we can't find a good fit, we choose the previous value
            # so we prepare this info
            df_temp_2 = df_temp.iloc[:-1, :]
            save_br = df_temp_2["target"].mean() * 100
            n_pop = df_temp_2["target"].count()
            br_idx += 1
            # If the badrate is more than zero, we save the value in the dict
            if save_br > 0:
                df = pd.DataFrame(
                    {
                        "decile_rank": df_temp["yhat"].max(),
                        "BadRate %": crr_br,
                        "count": n_pop,
                    },
                    index=[0],
                )
                br_output = pd.concat([br_output, df], axis=0)
            # Else, choose
            else:
                n_pop = df_temp["target"].count()
                df = pd.DataFrame(
                    {
                        "decile_rank": df_temp["yhat"].max(),
                        "BadRate %": crr_br,
                        "count": n_pop,
                    },
                    index=[0],
                )
                br_output = pd.concat([br_output, df], axis=0)
            df_temp = pd.DataFrame(columns=["yhat", "target"])
        # loop
        idx += 1

    br_output["KO"] = False
    # Add the KO profile to the output
    n_pop = df_temp["target"].count()
    df = pd.DataFrame(
        {
            "decile_rank": df_temp["yhat"].max(),
            "BadRate %": crr_br,
            "count": n_pop,
            "KO": True,
        },
        index=[0],
    )
    br_output = pd.concat([br_output, df], axis=0)

    return br_output.reset_index(drop=True), plot_badrate_pop(br_output)
