# Raspberrypi Setup

This note contains the steps I used for configuring the raspberry pi computers for the network for this work.  It is general, but was done for this work.

##  Computer Used
This project used Raspberrypi 3 B+ computers.

##  Additional Parts

### Power Connector - New
You need to power the computers.  For this the standard connection is a usb-mini.  I tried some older usb-mini connections around
my house, but they didn't work.  I ended up buying three different ones.  The one I like best is 
_"Raspberry Pi 3 Model B/B+ Plus Power Supply 5V 3A with Switch UL Certified Compatible w/ 2.5A 2A 1.5A 1A Fast Rapid Charge AC Adapter w/ 1.5m Extra Long On Off Power Switch Micro USB Cable"_.

It seems sturdy and it has an on/off switch.  This is nice for powering off the computer a few times.  From reading the comments around the net, you probably need to buy a new cable.

### Micro SD Card - New
I ended up buying 128 Sandisk cards.  Just follow the instructions at [SD Formatting](https://www.raspberrypi.org/documentation/installation/sdxc_formatting.md)

You have to create the 32 GB part FAT32 first, then the installation automatically expands to use the entire SD card.  You get a nice sized file system right out of the box.

### Reused Parts
I reused:  monitor, mouse, keyboard, ethernet cables.  I will be using these as small servers, so I don't need these except for setup.

##  Initial Configuration

The initial configuration is just following the screens, so everything is very easy.  For the custom configuration, I set the following changes _(details follow)_.

*  Set a hostname
*  Turn off the wifi (since I only want to use wires for my little servers)
*  Turn on ssh
*  Set a fixed ip address (since I don't have a local named server, kinda overkill for this system)
*  Add a custom user for the servers
*  Delete the pi user
*  Update pip3 (since I only use python 3)
*  Set up passwordless ssh between the servers (and my workstation)

These will be defined in the following paragraphs.  For many of these items, we will just use the **raspi-config**  command to perform the actions.  For all of these actions, you will need to work from the command shell.

### Set a hostname

Start the command shell, then enter **sudo raspi-config**.  Scroll down to _2 Network Options_ and hit enter.  Then choose _N1 Hostname_.  I changed the default from _raspberrpi_ to _rb-<int>_ so it would be a smaller name.  Reboot the computer and it is updated.

### Turn off the wifi



### Turn on ssh
