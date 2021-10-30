from flask import make_response, render_template
import pdfkit
import os

def pdf_template(**kwargs):
    rendered = render_template(kwargs["template"], **kwargs)

    #LOCAL
    #pdf = pdfkit.from_string(rendered, "./static/pdfs/{}.pdf".format(kwargs["output"]))
    #pdf = pdfkit.from_string(rendered, False)

    #HEROKU

    config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
    #pdf = pdfkit.from_string(rendered, "/app/static/pdfs/{}.pdf".format(kwargs["output"]), configuration=config)
    
    #pdf = pdfkit.from_string("rendered", "/app/tmp/{}.pdf".format(kwargs["output"]), configuration=config)
    
    #pdf = pdfkit.from_string("Holaaaa", "/app/tmp/output.pdf", configuration=config )

    # file = open("/app/tmp/filename.txt", "w")
    # file.write("Primera línea" + os.linesep)
    # file.write("Segunda línea")
    # file.close()
    # return file

    pdf = None

    pdf = pdfkit.from_string(rendered, False, configuration=config)
    
    return pdf
