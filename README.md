
# About

The main script `watchman.py` starts an infinite loop which manages changes in the image folder, and it sends new images to the mail server after `sync_delay`.

# Quick Start

## Configure Motion

Edit the "target" entry in `extra/motion.conf`, this specifies the destination folder to save video recordings. Afterwards, copy the `extra/motion.conf` to `/etc/motion/motion.conf`.

If you are not sure about which video device you are using, try `v4l2-ctl`:
```
apt install v4l-utils
v4l2-ctl --list-device
```

Edit `/etc/default/motion` so that it only contains:
```
start_motion_daemon=yes
```

## Add the Mailer Service

Edit `extra/motion-mailer.service`:
- Update `ExecStart` to match the path of the source code.
- Update `User` if you don't want to use `root`.

Copy the `extra/motion-mailer.service` to `/etc/systemd/system/`.

## Edit `configuration.py`

Edit this file to configure your mailing service

- `default_mail_config.send_from=`: This is your email account, for example: bob@test.com
- `default_mail_config.send_to=`: This is your receipients, if there are multiple receipients, use a comma (`,`) to separate them.

An example:

```
default_mail_config = MailConfiguration()
default_mail_config.send_from= "sender@posteo.de"
default_mail_config.send_to= "receiver@posteo.de"
default_mail_config.login_password = "password_of_sender"
default_mail_config.smtp_server = "posteo.de"
default_mail_config.smtp_port = 587
```

## Manage Permissions

If you intend to start `motion` as non-root, then to avoid permission issues:

```
mkdir /var/log/motion
chown -R motion:motion /var/log/motion
mkdir /var/run/motion/
chown -R motion:motion /var/run/motion
mkdir /var/lib/motion
chown -R motion:motion /var/lib/motion
```

Since both `motion` and `motion-mailer` use a shared `images` folder, you have to also manage the permission for this folder (configured in `configuration.py` by `path_image_folder`). 

## Start All Services

1. Start `motion`: `systemctl restart motion`
2. Start the mailer: `systemctl restart motion-mailer`

