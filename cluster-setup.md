# Cluster Setup and Design
The hardware components are relatively easy to set up, but now we want to start using our set of nodes in a cluster manner.  This isn't in a cluster, as you see the HPC clusters that are focused on hardware; rather, as a set of software clusters that make logical use of the system to solve problems.  Using this approach, this material will use some docker images to process jobs.  In particular, this projects sets up a simple swarm and runs jobs through the swarm.

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

This configuration sets up a swarm using the basic swarm commands

**Set up the manager**

```bash
docker swarm init --advertise-addr 192.168.1.161
```

This now comes back with a message:
docker swarm join --token SWMTKN-1-35g6opjhj037e6w7bglesod29wphvauncz7l5i9mf31l36eu7k-9vg0fs6zyakfycfggnjoc9dga 192.168.1.161:2377

so log into rb-2 and issue this command.

Check the configuration using:

```bash
docker info
```

## Using Docker Swarm

TBD