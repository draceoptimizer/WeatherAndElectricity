# Cluster Setup and Design

The hardware components are relatively easy to set up, but now we want to start using our set of nodes in a cluster manner.  This isn't in a cluster, as you see the HPC clusters that are focused on hardware; rather, as a set of software clusters that make logical use of the system to solve problems.  Using this approach, this material will use some docker images to process jobs.  In particular, this projects sets up a simple swarm for microservices and runs jobs through docker for longer running jobs.

The use case for this model is:

> The user has a workstation for interactive work and can use cloud services for high intensity work, but the preprocessing and postprocessing is low intensity so can be done with relatively small systems.  Additionally it is fun to work with hardware, so a small raspberry pi configuration is both fun and supports the data cleaning and postprocessing requirements.

The topics covered are:

* Installing Docker
* Setting up a swarm - Microservices and very basic cluster information
* Adding NFS to the management node - For common data management and reliability

## Install Docker CE on each node

Using the official instructions, [Docker Instructions](https://docs.docker.com/install/linux/docker-ce/debian/)we issue the following command on each computer in the cluster:

```bash
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
```

**Verify the correct key**
```bash
sudo apt-key fingerprint 0EBFCD88
```
**WARNING:  Raspian does not yet support installing from repository.**

The installation must use the convenience script:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker your-user
```

This installs the docker cli and containerd capabilities to use for the swarm.

## Set up the swarm

This configuration sets up a swarm using the basic swarm commands.  This provides some basic clustering capabilities and information management for the servers.

### Set up the manager

```bash
docker swarm init --advertise-addr 192.168.1.161
```

This now comes back with a message:
docker swarm join --token SWMTKN-1-35g6opjhj037e6w7bglesod29wphvauncz7l5i9mf31l36eu7k-9vg0fs6zyakfycfggnjoc9dga 192.168.1.161:2377

If you are adding a node later, then issue this command on the management node to get the swarm token:

```bash
docker swarm join-token worker
```

At this point, since the manager will be doing additional tasks it is best to drain the node

```bash
docker node update --availability drain
```

Now tasks won't be assigned to the manager node.

### Set up the compute nodes

Log into rb-2, rb-3, ... and issue the previous command.

Check the configuration using:

```bash
docker info
```

Check the nodes in the swarm:

```bash
docker node ls
```

## Add NFS to the management node

In this use case, the management node doesn't do processing; therefore, it can service permanent storage.  This configuration uses NFS to serve file to the work nodes.  This sets a convenient place for common storage so applications can be run on any node.  _(NOTE:  NFS can be a little slow, but it is acceptable since our servers aren't the fastest in the world.)_

### Starting NFS on the management node

The management node is rb-1, so let set it up for nfs.

* Make sure it is drained:  issue the command

>```bash
>docker node ls
>```

>Then check to make sure the management server is in _drain_ state.

* Add the nfs server to the management node

```bash
sudo apt-get install nfs-kernel-server
```

Set up the server and check

```bash
sudo /etc/init.d/nfs-kernel-server restart
systemctl status nfs-server.service
```

* Mount the files systems on the usb drives

Manually enter a command similar to:

```bash
mkdir /work/usb/usb2
sudo mount -t <file system type> /dev/sdb2 /work_usb/usb2
```

Then update the /etc/fstab similar to the following:

```bash
UUID=37FF-31CA  /work_usb/usb1  exfat   defaults,auto,umask=000,rw      0       0
UUID=58AE37E5AE37BA78   /work_usb/usb2  ntfs-3g defaults,auto,umask=000,rw      0       0
```

If you need ntfs, then you need to 

```bash
sudo apt-get install ntfs-3g
```

_It is best to reboot now so you can make sure your usb drives are mounted._

* Edit /etc/exports

Issue the command:

```bash
sudo vi /etc/exports
```

Then insert lines similar to

```bash
/work_usb/usb1  192.168.1.0/24(rw,sync)
/work_usb/usb2  192.168.1.0/24(rw,sync)
```

We can work on the security later, but this basically gives read/write to anyone on the local network.

* Make sure the server doesn't start too soon

Within raspi-config, set the Boot Options to wait for Network Connection.  This makes sure the nfs file system is correctly served.

### Start NFS on the compute nodes

This is relatively easy. 

```bash
sudo apt-get install nfs-common
```

Using _raspi-config_, set the boot options to wait for the network connnection.

Create some mount directories similar to :

```bash
sudo mkdir /mnt/nfs1
```

You will need to do this for each file system you will mount.

Update the /etc/fstab file to include lines similar to :

```bash
192.168.1.161:/work_usb/usb1    /mnt/nfs1       nfs     defaults        0       2
192.168.1.161:/work_usb/usb2    /mnt/nfs2       nfs     defaults        0       2
```

To manually mount the file systems:

```bash
mount -a
```

Check that the files are in the right place.

Reboot the system and check again.

## Using Docker Swarm

At this point the shared file systems are working, so lets look at how we use the Docker Swarm.