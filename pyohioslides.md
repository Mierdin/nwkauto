## Practical Network Automation with Ansible and Python

###Matt Oswalt
###@Mierdin
###keepingitclassless.net

---

# Disclaimers

<!--
Just a disclaimer on what I'll be covering....in short,
I do have a day job, and this is not that.
-->

Nothing in this presentation should be viewed to reflect any opinion or infrastructure detail of any employer, past or present, or any other organization. What I present is mine and mine alone.

Details provided should not be perceived to reflect the actual design or configuration of any specific real-world technology or infrastructure deployment, unless otherwise explicitly stated.

---

# Workshop Outline

- Brief Intro to Network Automation concepts
- Basic Data Modeling with YAML
- Creating templates with Jinja2
- Provisioning Network Services with Ansible
- Network Automation with Python Tools

---

# Workshop Tips

- ALL material online (including detailed walkthrough)
- Take light notes if you have to, but stay engaged
- Stop me for questions or clarifications at any time

---

# Networks are Inherently Distributed

<!--

Network infrastructure was a distributed system before distributed systems were cool

As a result, we've had to get really good at the data plane and control plane, but I feel like we've really dropped the ball wrt management plane. That brings me to....

-->

---

# Tightly Coupled Data and Syntax 

<!--

Show HTML, ask audience about biggest improvement since writing static pages....dynamic pages! Separating syntax from data. 

Right now we have the equivalent of statically written pages. Even the examples where someone generates a switch config from an excel spreadsheet - this is like Github Pages.....but even that doesn't work everywhere.

-->

---

```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
  <title>Title of document</title>
</head>

<body>
  some content 
</body>

</html>
```

---

```
vlan 40
  name Server1
vlan 50
  name Server2
interface Vlan40
  description "Server_1"
  no shutdown
  no ip redirects
  ip address 192.168.0.2/24
interface Vlan50
  description "Server_2"
  no shutdown
  no ip redirects
  ip address 192.168.1.2/24
interface GigabitEthernet1/0/1
 switchport access vlan 60
 switchport mode access
 channel-group 60 mode on
```

---

# WHY?

- Networking should just work.
- Current, complicated stack will take effort
- Better methodology = better uptime, agility, security

---

# Principles of Network Automation

- Culture (Need buy-in, remember benefits)
- Transactions (Device-level and System-level)
- Simple, well-understood abstractions at the right level
- Source Control (Git)

<!-- With respect to "benefits", keep the results listed on the last slide in mind. -->

---

![inline](images/topology.png)

---

# Other Ansible Modules

- Ansible Modules for Ansible, Cumulus
- Also F5, A10, Netscaler, OVS, SNMP

---

# Netmiko

- Python library for simplifying SSH management for network devices
- LOTS of Cisco support, Arista, HP, Juniper, Brocade, Huawei, etc.
- https://github.com/ktbyers/netmiko

---

# Parting Thoughts

- Use these tools in a CI Pipeline (Git + Jenkins)
- Start SIMPLE, work up from there
- Communication and buy-in is KEY!

---

# Resources

- EVERYTHING is here: https://github.com/Mierdin/nwkauto
- Much more YAML, Jinja2, Ansible, Python to explore

![inline](images/qrcode.png)