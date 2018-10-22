import pdfkit
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def df_to_html(df):
    html = df.round(4).style.background_gradient(cmap='RdBu').set_table_styles([{'selector': 'th', 'props': [('font-size', '7pt')]}]).set_properties(**{'width': '260px'}, **{'font-size': '7pt'}, **{'text-align': 'right'}).render()
    return html


def html_to_pdf(html, footer, pdfname):
    path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    options = {
            'dpi': 365,
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.3in',
            'margin-bottom': '0.25in',
            'margin-left': '0.3in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'footer-left': footer,
            'footer-font-size': '5',
            # 'footer-right': '[page] of [topage]',
            'no-outline': None,
        }
    pdfkit.from_string(html, pdfname, configuration=config, options=options)


def df_to_pdf(df, footer, pdf_name):
    html_to_pdf(df_to_html(df), footer, pdf_name)


def get_dates_from_week_back(num_of_week):
    today = date.today()
    end_date = today - timedelta(days=(today.weekday() - 4) % 7)
    start_date = end_date - timedelta(days=7*num_of_week-3)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def get_dates_from_month_back(num_of_month):
    d = date.today()
    end_date = date(d.year, d.month, 1) - timedelta(days=1)
    start_date = date(d.year, d.month, 1) - relativedelta(months=num_of_month)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def get_dates_from_period_back(num_of_periods, period):
    if period == 'M':
        return get_dates_from_month_back(num_of_periods)
    elif period == 'W':
        return get_dates_from_week_back(num_of_periods)
    else:
        return None


def year_month_format(date_list):
    return date_list.map(lambda d: d.strftime('%b-%Y'))


def year_week_format(num_of_weeks):
    return [str(d) + ' Week' for d in list(range((-1)*num_of_weeks, 0))]
