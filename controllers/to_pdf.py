from flask import make_response, render_template
import pdfkit

def pdf_template(**kwargs):
    rendered = render_template(kwargs["template"], **kwargs)
    config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
    pdf = pdfkit.from_string(rendered, "./static/pdfs/{}.pdf".format(kwargs["output"]), configuration=config)

