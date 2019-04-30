# Raspberrypi Setup

This note contains the steps I used for configuring the raspberry pi computers for the network for this work.  It is general, but was done for this work.

## Computer Used

This project used Raspberrypi 3 B+ computers.

## Additional Parts

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

## Initial Configuration

The initial configuration is just following the screens, so everything is very easy.  For the custom configuration, I set the following changs _(details follow)_.

* Set a hostname
* Install vim
* Turn off the wifi (since I only want to use wires for my little servers)
* Turn on ssh
* Set a static ip address (since I don't have a local named server, kinda overkill for this system)
* Add a custom user for the servers
* Delete the pi user
* Update pip3 (since I only use python 3)

These will be defined in the following paragraphs.  For many of these items, we will just use the **raspi-config**  command to perform the actions.  For all of these actions, you will need to work from the command shell.

### Set a hostname

Start the command shell, then enter **sudo raspi-config**.  Scroll down to _2 Network Options_ and hit enter.  Then choose _N1 Hostname_.  I changed the default from _raspberrpi_ to _rb-<int>_ so it would be a smaller name.  Reboot the computer and it is updated.

### Install vim

```bash
sudo apt-get install vim
```

### Turn off the wifi

Since I am using a small local switch, I want to turn off the wifi.  This is done by inserting the following lines into /boot/config.txt.

```bash
#
#  Turn off wifi
#
dtoverlay=pi3-disable-wifi
```

### Turn on ssh

Start raspi-config, scroll down to _Interfacing Options_, scroll down to _O2 ssh_.  Select this option then using tab, select to enable ssh.  Easy enough.

### Set a static ip address

Raspian is very nice, because you only need to edit the /etc/dhcpcd.conf file.  You will need two bits of informaiton:

* An address to use.  You can check your router to make sure you aren't using one that is assigned.
* The address of the router (normally 192.168.1.1 for a local router)

Then change /etc/dhcpcd.conf to the following

```bash
    interface eth0
    static ip_address=192.168.1.xxx
    static routers=192.168.1.1
    static domain_name_servers=192.168.1.1
```

**At this point is is good to reboot so your routing is correct.**  I normally use the command 

```bash
sudo reboot -h now
```

Check your configuration using 

```bash
ip a
```

###  Add a custom user

As with all good security, you probably want to add a custom user and delete the pi account.  Adding a user is as simple as 

```
sudo adduser xxxxxxxxx
```

With the user name of choice.  Now since you will eventually delete the pi user, it is best to add your new user to all of the groups that pi is a member.  You need to edit /etc/group as sudo and where you see pi as the user, just add your new user name. Just make a comma seperated list in each instance.

At this point use raspi-config to make users login so you can test your new user.  Now reboot.

When you log back in as the new user, make sure you can sudo from the account.

### Delete the pi account

As simple as -

```bash
sudo userdel -r pi
```

You have now removed the default user configuration completely from your raspberry pi 3 b+.

### Set to boot to the cli

At this point everything is ready for a server mode, so I don't need the GUI.  I use raspi-config to boot to the cli using our new user.

### Update pip

Since I primarily use python 3, I like to update pip.

```bash
sudo python3 -m pip install --upgrade pip
```

After this finishes, it won't work for normal users until you rehash.

```bash
sudo -s
```

_(This puts you in the shell as root.)_

Next, issue the following command.

```bash
hash -d pip
exit
```

Now reboot the system and everything is ready for general use.

## Advanced Configuration

Once the system is set up and configured, it is ready for advanced configuration.  For the advanced configuration, we have the following additions:

* Set up passwordless ssh between the servers (and my workstation)
* Set up common host files
* Install basic Docker images on the work servers

### Passwordless ssh

On the small cluster, we don't want to require passwords when moving between servers.  For this I need to install passwordless ssh between the computers.  _(NOTE:  I currently require a password for sudo since that is a learned safety capability.)_

On my main workstation, I have already used ssh-keygen to generate a key.  Thus I now use ssh-copy-id to copy the id to the remote computers.  This is simply 

```bash
ssh-copy-id  user@remote_server
```

Then answer the simple questions and away you go.  You do need to do the remote_server for every server in the cluster, but that isn't a very big issues.

### Common host files

The host file need to contain the following line:

```bash
192.168.1.xxx  rb-y
```

For each server rb-y.

## Conclusion

At this point the hardware has been set up and ready for use.  Rather than try to set up and maintain all of the software exactly as desired, further work will make use of Docker images for some of the applications that are necessary for our processing.