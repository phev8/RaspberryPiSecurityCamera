# RaspberryPiSecurityCamera
Take pictures and stream them to dropbox account from the raspberry pi

This repository contians the source and design files for a hobby project to create a security camera with the Raspberry Pi mini computer, which stream the taken picture to your Dropbox account. So you will be able to check the taken pictures easily on the way.
(If you have a server or other options to store the pictures, it could work better, but this is for people who want to minimise the resources.)

### Warning
This project is just for playing around or maybe watch your pet moving around in your flat. This solution doesn't provide a fully featured security camera that's why it doesn't want to compete with any commercial one.

## Workflow
1. You have to register an app at Dropbox developer site.
2. Copy your app secret and key into the dropbox_auth.py and run the script
3. Launch the main_camera.py script
4. Optional: create a shell script to launch application on system start.
