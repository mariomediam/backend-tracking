from flask import make_response, render_template
import pdfkit

def pdf_template(**kwargs):
    rendered = render_template(kwargs["template"], **kwargs)
    config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
    #pdf = pdfkit.from_string(rendered, "/app/static/pdfs/{}.pdf".format(kwargs["output"]), configuration=config)
    #pdf = pdfkit.from_string("rendered", "/app/tmp/{}.pdf".format(kwargs["output"]), configuration=config)
    #pdf = pdfkit.from_string(rendered, "./static/pdfs/{}.pdf".format(kwargs["output"]))
    pdf = pdfkit.from_string("Holaaaa", "/app/tmp/output.pdf", configuration=config)
    #pdfkit.from_string('Hello!', 'out.pdf')
    

