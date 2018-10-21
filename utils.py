import pdfkit


def df_to_html(df):
    html = df.round(4).style.background_gradient(cmap='RdBu').set_table_styles([{'selector': 'th', 'props': [('font-size', '7pt')]}]).set_properties(**{'width': '260px'}, **{'font-size': '7pt'}, **{'text-align': 'right'}).render()
    return html


def html_to_pdf(html, pdfname):
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
            'no-outline': None,
        }
    pdfkit.from_string(html, pdfname, configuration=config, options=options)


def df_to_pdf(df, pdf_name):
    html_to_pdf(df_to_html(df), pdf_name)


