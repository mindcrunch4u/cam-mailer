class MailConfiguration:
    def __init__(self):
        self.send_from = "<from>"
        self.send_to = "<to1>,<to2>"
        self.login_account = self.send_from
        self.login_password = "<password>"
        self.smtp_server = "<server>"
        self.smtp_port = 587  # STRTTLS
        self.default_subject = "Automated Message"


class MiscsConfiguration:
    def __init__(self):
        self.path_log_file = "<path/to/log.txt>"
        self.path_image_folder = "<path/to/stored/images/>"


# edit default_mail_config to change the behaviour of the mailer
default_mail_config = MailConfiguration()
default_mail_config.send_from = "..."  # your email account, for example: bob@test.com
default_mail_config.send_to = "..."  # your receipients, if there are multiple receipients, use "," to separate them.
default_mail_config.login_password = "..."
default_mail_config.smtp_server = "..."
default_mail_config.smtp_port = 587

# edit default_misc_config to change other behaviours
default_misc_config = MiscsConfiguration()
default_misc_config.path_log_file = "./images/log.txt"
default_misc_config.path_image_folder = "./images/"
default_misc_config.image_extension = ".jpg"
