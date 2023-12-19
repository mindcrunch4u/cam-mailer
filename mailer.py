import email, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from datetime import datetime
import base64
import os

class MailConfiguration:
    def __init__(self):
        self.send_from="<from>"
        self.send_to="<to1>,<to2>"
        self.login_account = self.send_from
        self.login_password = "<password>"
        self.smtp_server = "<server>"
        self.smtp_port = 587 # STRTTLS

        self.default_subject = "Automated Message"


log_file=None
log_file_path="<path/to/log/file>"
def log(content):
    global log_file
    global log_file_path
    if log_file == None:
        log_file = open(log_file_path, "a+")
    os.chmod(log_file_path, 0o666)
    print(content, flush=True)
    log_file.write("[{}] {} \n".format(datetime.now(), content))
    log_file.flush()


def send_mail_with_images(folder_path, list_of_image_paths):
        mc = MailConfiguration()

        if len(list_of_image_paths) <= 0:
            log("No new images found.")
            return

        msg = MIMEMultipart()
        msg["Subject"] = mc.default_subject
        msg["From"] = mc.send_from
        msg["To"] = mc.send_to

        body = MIMEText("From Your Automated Friend")
        msg.attach(body)

        number_of_images = len(list_of_image_paths)
        for index, path_to_image in enumerate(list_of_image_paths):
                path_to_image = os.path.join(folder_path, path_to_image)
                log("\tattaching: {}/{}".format(
                        index + 1, number_of_images
                ))
                with open(path_to_image, 'rb') as f:
                        binary_image = f.read()
                image = MIMEImage(binary_image, name=os.path.basename(path_to_image))
                msg.attach(image)

        service = smtplib.SMTP(mc.smtp_server, mc.smtp_port)
        service.ehlo()
        service.starttls()
        service.ehlo()
        try:
                service.login(mc.login_account, mc.login_password)
        except:
                log("Can't Authenticate")
        log("Connected to the mail server, starting SEND.")
        service.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

        result = service.quit()
        log("Mail sent: {}".format(result))

def send_mail_with_a_video(path_to_video):
        mc = MailConfiguration()

        msg = MIMEMultipart()
        msg["Subject"] = mc.default_subject
        msg["From"] = mc.send_from
        msg["To"] = mc.send_to

        body = MIMEText("From Your Automated Friend")
        msg.attach(body)

        # Attach video file
        log("Reading file into memory: {}".format(path_to_video))
        attachment = open(path_to_video, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= {}".format(path_to_video))
        msg.attach(part)

        service = smtplib.SMTP(mc.smtp_server, mc.smtp_port)
        service.ehlo()
        service.starttls()
        service.ehlo()
        try:
                service.login(mc.login_account, mc.login_password)
        except:
                log("Can't Authenticate")
        log("Connected to the mail server, starting SEND.")
        service.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

        result = service.quit()
        log("Mail sent: {}".format(result))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("usage: python3 script.py <path to a video file>")
        sys.exit(1)
    send_mail_with_a_video(sys.argv[1])

