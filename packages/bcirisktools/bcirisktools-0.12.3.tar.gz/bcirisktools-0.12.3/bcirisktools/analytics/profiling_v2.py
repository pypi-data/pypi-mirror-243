import pandas as pd


def find_optimal_number_of_intervals(
            df: pd.DataFrame,
            q: int,
            score_col: str = 'y_score',
            label_col: str = 'y_true',
            max_iter: int = None,
        ) -> pd.DataFrame:
    """
        Given a dataframe, this function returns the optimal number of intervals that have their bad_rate (mean y_true)
        monotonically increasing following a greedy algorithm. The steps are the following:

        1. Group the dataframe by the quantiles of the scores
        2. Calculate the bad rate of each quantile
        3. Calculate the difference of bad rates between two consecutive quantiles
        4. If the difference is negative, merge the two quantiles with the closest bad rates
        5. Repeat steps 3 and 4 until there are no more negative differences

        If there's no way to find an optimal numbers of intervals, the function will return a dataframe with only
        one quantile. You can also control this by setting the max_iter parameter.

        :param df: Dataframe with the bad rates
        :param q: Number of quantiles
        :param score_col: Name of the column with the scores
        :param label_col: Name of the column with the labels
        :param max_iter: Maximum number of iterations
        :return: Dataframe with the optimal number of quantiles
    """
    df = df.groupby(pd.qcut(df[score_col], q=q, duplicates='drop')).agg({label_col: ["mean", "count"]}).reset_index()
    df.columns = df.columns.droplevel(0)
    df.rename(columns={'': 'interval', 'mean': 'bad_rate'}, inplace=True)
    iteration = 0
    while True:
        # Get the difference of y_true between two consecutive quantiles
        df['diff'] = df['bad_rate'].diff()
        # Get the indexes of all the rows where the difference is negative
        indexes = set(df[df['diff'] < 0].index.to_list())
        dropped_indexes = set()
        if len(indexes) == 0 or (max_iter is not None and iteration >= max_iter):
            break
        df_temp = df.copy()
        iter_indexes = iter(indexes)
        while iter_indexes:
            try:
                index_to_process = next(iter_indexes)
            except StopIteration:
                break
            if index_to_process in dropped_indexes:
                continue
            # Choose the index of the previous or the next row which has the closest y_true value
            # to the original index
            nearest_index = _choose_nearest_bad_rate_index(
                df,
                index_to_process,
                index_to_process - 1,
                index_to_process + 1,
                dropped_indexes
            )
            # Sort indexes and update the bad rate and count of the row with the lowest index
            index_sorted = sorted([index_to_process, nearest_index])
            df_temp = _merge_rows_with_similar_bad_rates(df_temp, index_sorted, dropped_indexes)
        df = df_temp.reset_index(drop=True)
        iteration += 1
    df.drop(columns=['diff'], inplace=True)
    return df


def merge_intervals(df: pd.DataFrame, indexes: list[int], agg_function: str = 'mean') -> pd.DataFrame:
    """
    Given a dataframe and a list of indexes, this function merges the rows in the indexes, aggregating the bad rates
    with the agg_function and summing the counts. To use this function the df should be ordered by 'interval' column
    in ascending order and with the index of the df starting from 0 to len(df) - 1 (if not, you should reset the
    index first).

    :param df: Dataframe with the bad rates
    :param indexes: List with the two indexes we are going to merge
    :return: Dataframe with the rows merged
    """
    df.loc[indexes[0], 'bad_rate'] = _get_agg_consecutive_bad_rates(df, indexes, agg_function)
    df.loc[indexes[0], 'count'] = df.loc[indexes, 'count'].sum()
    df['interval'] = df['interval'].cat.rename_categories(
        {
            df.loc[indexes[0], 'interval']: pd.Interval(
                left=df.loc[indexes[0], 'interval'].left,
                right=df.loc[indexes[-1], 'interval'].right,
                closed='right'
            )
        }
    )
    df.drop(indexes[1:], inplace=True)
    return df

def _choose_nearest_bad_rate_index(
            df: pd.DataFrame,
            fixed_index: int,
            lower_index: int,
            upper_index: int,
            dropped_indexes: set[int],
            col: str = 'bad_rate'
        ) -> int:
    """
    Given a dataframe and an index, this function returns the index of the row with the closest bad rate
    :param df: Dataframe with the bad rates
    :param fixed_index: Index of the row we are analyzing (this index if fixed, won't be modified)
    :param lower_index: Lower index to scan the df recursively
    :param upper_index: Upper index to scan the df recursively
    :param dropped_indexes: Set of indexes that have been dropped
    :return: Index of the row with the closest bad rate
    """
    if lower_index == 0:
        return lower_index
    if upper_index == (len(df) - 1):
        return upper_index
    # Check the difference between the bad rates of the fixed row and the upper and lower to find the nearest bad rate
    if (abs(df.loc[lower_index, col] - df.loc[fixed_index, col]) <
        abs(df.loc[upper_index, col] - df.loc[fixed_index, col])):
        if lower_index in dropped_indexes:
            lower_index = _choose_nearest_bad_rate_index(df, fixed_index, lower_index - 1, upper_index, dropped_indexes)
        return lower_index
    else:
        if upper_index in dropped_indexes:
            upper_index = _choose_nearest_bad_rate_index(df, fixed_index, lower_index, upper_index + 1, dropped_indexes)
        return upper_index


def _get_agg_consecutive_bad_rates(df: pd.DataFrame, indexes: list[int], agg_function: str = 'mean') -> float:
    """
    Given a dataframe, this function returns some aggregation (min, mean, max) of the consecutive bad rates
    :param df: Dataframe with the bad rates
    :param indexes: List with the indexes that we are going to merge in the df
    :return: Average of the consecutive bad rates
    """
    if agg_function == 'mean':
        new_bad_rate = (df.loc[indexes, 'bad_rate'] * df.loc[indexes, 'count']).sum() / df.loc[indexes, 'count'].sum()
    elif agg_function in {'min', 'max'}:
        new_bad_rate = df.loc[indexes, 'bad_rate'].agg(agg_function)
    else:
        raise ValueError(f'agg_function should be one of the following: mean, min, max. Received: {agg_function}')
    return new_bad_rate


def _merge_rows_with_similar_bad_rates(
            df: pd.DataFrame,
            indexes_to_merge: list[int],
            dropped_indexes: set[int],
        ) -> pd.DataFrame:
    """
    Given a dataframe, this function merges the rows with similar bad rates
    :param df: Dataframe with the bad rates
    :param indexes_to_merge: List with the two indexes we are going to merge
    :param dropped_indexes: Set with the indexes already dropped
    :return: Dataframe with the rows merged
    """
    df = merge_intervals(df, indexes_to_merge)
    dropped_indexes.add(indexes_to_merge[1])
    return df
