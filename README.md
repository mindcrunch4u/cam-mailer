# Things to do before running the script
Before executing `watchman.py`

## motion.conf
Edit "target" in motion.conf
and copy it to /etc/motion/motion.conf

Edit /etc/default/motion
so that it only contains:
`start_motion_daemon=yes`

Find out your video device:
```
apt install v4l-utils
v4l2-ctl --list-device
```

## motion-mailer.service
Edit "ExecStart" and "User" in motion-mailer.service
change the path to the script if yours is different
change the user if don't want to use `root`

## configuration.py
Edit this file to configure your mailing service

## permissions
If you started motion as non-root, then:
```
mkdir /var/log/motion
chown -R motion:motion /var/log/motion
mkdir /var/run/motion/
chown -R motion:motion /var/run/motion
mkdir /var/lib/motion
chown -R motion:motion /var/lib/motion
```
You might also want to manage the permission for the `image` folder,
since both `motion` and `motion-mailer` use this folder.
