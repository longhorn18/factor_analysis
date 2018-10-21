import pandas as pd
import utils as utils
import logging


def monthly_transform(df, start_month, end_month, model):
    df = df[(df.DataMonth >= start_month) & (df.DataMonth <= end_month) & (df.Model == model)]
    factor_list = df.Factor.unique()
    date_list = pd.to_datetime(df.DataMonth.unique().astype(str))
    df_out = pd.DataFrame(columns=factor_list, index=[d.strftime('%b-%y') for d in date_list.sort_values()])
    for factor in factor_list:
        df1 = df[df.Factor == factor]
        df1 = df1.sort_values(by='DataMonth', ascending=True)
        df_out[factor] = df1.loc[:, 'Return'].values
    print(df_out.T.head())
    return df_out.T


def daily_transform(df, start_date, end_date, model):
    df = df[(df.DataDate >= start_date) & (df.DataDate <= end_date) & (df.Model == model)]
    factor_list = df.Factor.unique()
    date_list = pd.to_datetime(df.DataDate.unique().astype(str))
    df_out = pd.DataFrame(columns=factor_list, index=[d.strftime('%b-%d') for d in date_list.sort_values()])
    for factor in factor_list:
        df1 = df[df.Factor == factor]
        df1 = df1.sort_values(by='DataDate', ascending=True)
        df_out[factor] = df1.loc[:, 'DlyReturn'].values
    return df_out.T


def get_df_by_dates(df, start_date, end_date, model):
    return df[(df.DataDate >= start_date) & (df.DataDate <= end_date) & (df.Model == model)]


def total_return_from_returns(returns):
    """Retuns the return between the first and last value of the DataFrame.
    Parameters
    ----------
    returns : pandas.Series or pandas.DataFrame
    Returns
    -------
    total_return : float or pandas.Series
        Depending on the input passed returns a float or a pandas.Series.
    """
    return (returns + 1).prod() - 1


def factor_by_year(df, fac_col, return_col, date_col, func):
    df_cp = df.copy()
    df_cp['Year'] = df[date_col].dt.year
    df_out = df_cp[[fac_col, return_col, 'Year']].pivot_table(index=fac_col, columns=['Year'], aggfunc=func)
    df_out.columns = df_out.columns.droplevel(0)
    return df_out


def factor_by_year_month(df, fac_col, return_col, date_col, func):
    df_cp = df.copy()
    df_dates = pd.to_datetime(df.loc[:, date_col])
    df_cp.loc[:, 'YearMonth'] = df_dates.map(lambda dt: dt.replace(day=1))
    df_out = df_cp[[fac_col, return_col, 'YearMonth']].pivot_table(index='Factor', columns=['YearMonth'], aggfunc=func)
    df_out.columns = df_out.columns.droplevel(0)
    return df_out


def factor_by_year_week(df, fac_col, return_col, date_col, func):
    df_cp = df.copy()
    df_cp['YearWeek'] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%U')
    df_out = df_cp[[fac_col, return_col, 'YearWeek']].pivot_table(index='Factor', columns=['YearWeek'], aggfunc=func)
    df_out.columns = df_out.columns.droplevel(0)
    return df_out


def factor_last_x_months(df, fac_col, return_col, date_col, func, model, num_of_months):
    (start_date, end_date) = utils.get_dates_from_month_back(num_of_months)
    logging.info('From ' + start_date + 'to ' + end_date)
    df = get_df_by_dates(df, start_date, end_date, model)
    df = factor_by_year_month(df, fac_col, return_col, date_col, func)
    df.columns = utils.year_month_format(df.columns)
    return df


def factor_last_x_weeks(df, fac_col, return_col, date_col, func, model, num_of_weeks):
    (start_date, end_date) = utils.get_dates_from_week_back(num_of_weeks)
    logging.info('From ' + start_date + ' to ' + end_date)
    df = get_df_by_dates(df, start_date, end_date, model)
    df = factor_by_year_week(df, fac_col, return_col, date_col, total_return_from_returns)
    df.columns = utils.year_week_format(num_of_weeks)
    return df


def factor_last_x_periods(df, fac_col, return_col, date_col, func, model, num_of_periods, period):
    if period == 'M':
        return factor_last_x_months(df, fac_col, return_col, date_col, func, model, num_of_periods)
    elif period == 'W':
        return factor_last_x_weeks(df, fac_col, return_col, date_col, func, model, num_of_periods)
