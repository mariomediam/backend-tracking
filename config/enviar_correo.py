from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from os import environ
from dotenv import load_dotenv
load_dotenv()
import email.mime.application



# def enviarCorreo(destinatario, cuerpo, ruta_attach):    
#     print("destinatario " +  destinatario)
#     mensaje["To"]=destinatario
#     texto=mensaje
#     mensaje.attach(MIMEText(cuerpo, "html"))
#     #mensaje.attach(MIMEText(open("./static/pdfs/16fff8.pdf").read()))
#     #filename = './static/pdfs/16fff8.pdf' #path to file
#     filename = ruta_attach
#     fo=open(filename,'rb')
#     attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
#     fo.close()
#     attach.add_header('Content-Disposition','attachment',filename=filename)
#     mensaje.attach(attach)
#     try:
#         servidorSMTP = smtplib.SMTP("smtp.gmail.com", 587)
#         servidorSMTP.starttls()
#         servidorSMTP.login(user=mensaje.get("From"), password=password)
#         servidorSMTP.sendmail(
#             from_addr=mensaje.get("From"),
#             to_addrs=mensaje.get("To"),
#             msg=mensaje.as_string()
#         )
#         servidorSMTP.quit()
#     except Exception as e:
#         print(e)

def enviarCorreo(destinatario, cuerpo, file_attch):  

    mensaje = MIMEMultipart()

    mensaje["From"] = environ.get("EMAIL")
    mensaje["Subject"]="Registro de compra"
    password = environ.get("EMAIL_PASSWORD")  
    
    print("destinatario " +  destinatario)
    mensaje["To"]=destinatario
    texto=mensaje
    mensaje.attach(MIMEText(cuerpo, "html"))
    # filename = ruta_attach
    # fo=open(filename,'rb')
    # attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
    # fo.close()
    # attach.add_header('Content-Disposition','attachment',filename=filename)
    # mensaje.attach(attach)
    
    attach = email.mime.application.MIMEApplication(file_attch,_subtype="pdf")
    attach.add_header('Content-Disposition','attachment',filename="RegistroPedido.pdf")
    mensaje.attach(attach)
    try:

        servidorSMTP = smtplib.SMTP("smtp.gmail.com", 587)
        servidorSMTP.starttls()
        servidorSMTP.login(user=mensaje.get("From"), password=password)
        servidorSMTP.sendmail(
            from_addr=mensaje.get("From"),
            to_addrs=mensaje.get("To"),
            msg=mensaje.as_string()
        )
        servidorSMTP.quit()

        del attach
    except Exception as e:
        print(e)

