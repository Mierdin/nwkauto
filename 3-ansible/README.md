# Ansible - Linux

This part should be fairly straightforward. Just cd into "linux/" and type "vagrant up"

# Ansible - Junos

The JunOS portion assumes you've already configured Vagrant with the appropriate JunOS plugin. For a walkthrough of using the Vagrant vSRX work by Juniper, check out [this blog post](keepingitclassless.net/2015/03/go-go-gadget-networking-lab/).

It also assumes that you have installed the [Junos Ansible plugin](https://github.com/Juniper/ansible-junos-stdlib) appropriately for your machine.

In summary, here are the steps after cloning this repo, to getting a full JunOS lab ready for your Ansible playbooks:

- cd to "junos/"
- type "vagrant plugin install --plugin-version 0.2.0 vagrant-junos"
- type "vagrant up"
- type "./lab_init.sh"
- Install [Ansible plugin for Junos](https://github.com/Juniper/ansible-junos-stdlib) and run "ansible-playbook -i hosts junos.yml"
