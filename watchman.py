from finder import find_new_files
from mailer import send_mail_with_images
import time
import email, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
import os

sync_delay = 5
folder_path = "<path/to/stored/images>"

while True:
        try:
            new_files, deleted_files = find_new_files(folder_path)
            print("new files:", new_files, flush=True)
            print("deleted files:", deleted_files, flush=True)
            send_mail_with_images(folder_path, new_files)
            time.sleep(sync_delay)
        except Exception as e:
            print(e, flush=True)
