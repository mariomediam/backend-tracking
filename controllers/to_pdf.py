from flask import make_response, render_template
import pdfkit

def pdf_template(**kwargs):
    rendered = render_template(kwargs["template"], **kwargs)
    pdf = pdfkit.from_string(rendered, "./static/pdfs/{}.pdf".format(kwargs["output"]))

