## Network Automation with Ansible and Python

This repository houses all of the material from my talk on Network Automation at Interop Vegas 2015.

For an overview of my talk, see my [blog post](http://keepingitclassless.net/2015/01/network-automation-interop-vegas-2015/). I will try to get more material posted to that page once I actually give the talk (such as recordings). However, this repository houses not only my slides, but also all of the configuration artifacts and source code used in the talk.

There are four distinct parts to this talk, and I have separated these parts into their own directories within this repository. Please look in those directories for more details on each section, but the high-level description is as follows:
- **_1-yaml_** - This directory houses several YAML files that contain examples of how we might be using YAML in the more advanced sections later. It also contains a Python script to parse these YAML files and output the data to the screen.
- **_2-jinja2_** - Here, you can find an assortment of YAML files, and Jinja2 templates. The Jinja2 templates are rendered using data from the YAML files, by a Python script that is found in the root of this directory.
- **_3-ansible_** - In this demo, I outline the basics of Ansible, first by walking through a sample playbook, then implementing an Ansible role on a Linux machine to make it into a router. Then I pull out all the stops by spinning up a 3-router topology using Vagrant and Juniper vSRX, and use Ansible to these these routers from a blank config, to a fully-operational BGP configuration.
- **_4-python_** - In this section, I explore some of the Python tools that have been made available for network automation tasks.

Again, please look into each of these directories for more detail on how to make these demonstrations useful to you

Enjoy!