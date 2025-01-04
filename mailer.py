import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from datetime import datetime
from configuration import default_mail_config, default_misc_config
import os


log_file = None
log_file_path = default_misc_config.path_log_file


def log(content):
    global log_file
    global log_file_path
    if log_file is None:
        try:
            with open(log_file_path, "a+") as log_file:
                # os.chmod(log_file_path, 0o666)
                print(content, flush=True)
                log_file.write("[{}] {} \n".format(datetime.now(), content))
        except Exception as e:
            print("Cannot open log, Reason:\n" + str(e))
            return


def create_default_message():
    mc = default_mail_config

    msg = MIMEMultipart()
    msg["Subject"] = mc.default_subject
    msg["From"] = mc.send_from
    msg["To"] = mc.send_to
    body = MIMEText("From Your Automated Friend")
    msg.attach(body)

    return msg, mc


def talk_to_mail_server(msg, mc):
    # parameter: message, mail config
    service = smtplib.SMTP(mc.smtp_server, mc.smtp_port)
    service.ehlo()
    service.starttls()
    service.ehlo()
    try:
        service.login(mc.login_account, mc.login_password)
    except Exception as e:
        log("Can't Authenticate, Reason:\n" + str(e))
    log("Connected to the mail server, starting SEND.")
    service.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

    result = service.quit()
    log("Mail sent: {}".format(result))


def send_mail_with_images(folder_path, list_of_image_paths):

    if len(list_of_image_paths) <= 0:
        log("No new images found.")
        return

    msg, mc = create_default_message()

    number_of_images = len(list_of_image_paths)
    for index, path_to_image in enumerate(list_of_image_paths):
        path_to_image = os.path.join(folder_path, path_to_image)
        log("\tattaching: {}/{}".format(index + 1, number_of_images))
        with open(path_to_image, "rb") as f:
            binary_image = f.read()
        image = MIMEImage(binary_image, name=os.path.basename(path_to_image))
        msg.attach(image)

    talk_to_mail_server(msg, mc)


def send_mail_with_a_video(path_to_video):
    msg, mc = create_default_message()

    # Attach video file
    log("Reading file into memory: {}".format(path_to_video))
    try:
        with open(path_to_video, "rb") as attachment:
            attachment_content = attachment.read()
    except Exception as e:
        print("Cannot open file: {}, Reason:\n" + str(e))
        return
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment_content)
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition", "attachment; filename= {}".format(path_to_video)
    )
    msg.attach(part)
    talk_to_mail_server(msg, mc)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: python3 script.py <path to a video file>")
        sys.exit(1)
    send_mail_with_a_video(sys.argv[1])
