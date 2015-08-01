# Backup plan
- ssh mierdin@mierdin.ddns.net -p 8080

# Pre-Workshop Checklist

Set repo to public

Start with a fresh restart (make sure chrome doesn't autostart)

Disable all services/apps that might produce a notification

Open slides (making a quick PDF export and opening this would be ideal)

Ensure that nwkauto, nwkauto-blank, and ansible-junos-stdlib are NOT in dropbox, but are directly next to each other somewhere on the filesystem.

Set up three screens in order:
- iTerm
- ST2 with Bare Repo
- ST2 with Full Repo

Set up TMUX panes in an iTerm tab for sections 1 and 2

---------------------------
|           |             |
|           |             |
|           |     VIM     |
|           |             |
|  iPython  |-------------|
|           |             |
|           |             |
|           |     VIM     |
|           |             |
---------------------------

cd into the nwkauto-blank repo on all three windows, start ipython on left side

Make sure terminal text size is large enough

Need to devise a list of commands to run to double-check that the environment is good to go for the workshop
Also make sure that your vagrant machines are destroyed
- trustybox
- vsrx01
- vsrx02
- vsrx03

# Intro

Go to Intro Slide

    Basic Bio/Introduction/Background

Go to Disclaimer slide

    I do have a day job, and this is not that.

    Not endorsing or promoting any one platform - automation is possible in many forms

Go to overview slide, talk through it briefly

Ask audience for some network automation anecdotes

Network Automation Concepts

Go to "Workshop Tips" slide

    I'd rather leave a chunk of information off at the end than
    have you not follow the stuff I do manage to get through
 
# 1 - YAML

<< SHOW OF HANDS WHO HAS EXPERIENCE WITH YAML >>

Why YAML - it's simple, well known, and does the job

Great tool for representing data, no more (just want the data)

Similar-ish to XML or JSON but more useful to human beings than those two

<!-- Make sure to cd to the 1-yaml dir in all windows/panes prior to launching ipython, etc -->

First exercise is a list:

<!-- 1-list.yml -->
    ---
    - Juniper
    - Cisco
    - Brocade
    - VMware

Just an arbitrary list. No particular order, doesn't have to be unique.

I'll keep the Python light - for illustrative purposes only. Focus on YAML.
We need to write a small function to import the YAML data

<!-- interpreter -->

    import yaml
    from pprint import pprint

    def ly(filename):
        with open(filename) as _:
            return yaml.load(_)

Now we have a function we can use to quickly load the YAML files we write

Let's load the YAML file we wrote.

<!-- interpreter -->

  w  body = ly('1-list.yml')
    print(type(body))
    print(len(body))
    print(body)

This is the representation of the data in Python

Items in list don't even have to be same type!!
YAML mimics the flexibility of Python
Notice that strings (usually) don't have to be enclosed in quotes.

<!-- 2-mixedtypeslist.yml -->

    ---
    - Plants
    - 12345
    - False
    - ['Hello', 'Workld', '!']

Let's run our function again

<!-- interpreter -->

    body = ly('2-mixedtypeslist.yml')
    print(type(body))
    print(len(body))
    print(body)

Small loop to show individual types

<!-- interpreter -->

    for item in body:
        print(type(item))

Dictionaries. Explain key/value pairs (hashes, hash maps, etc)

We can write dict of vendor to website mappings

<!-- 3-dictionary.yml -->

    ---
    Juniper: http://www.juniper.net/us/en/
    Cisco: http://www.cisco.com/
    Brocade: http://www.brocade.com/index.page
    VMware: http://www.vmware.com/

Same as before, we can print type and length

<!-- interpreter -->

    body = ly('3-dictionary.yml')
    print(type(body))
    print(len(body))

pprint is good for dictionaries

<!-- interpreter -->

    pprint(body)

We can call up a specific member of this dictionary by key

<!-- interpreter -->

    print(body['Juniper'])

Dictionaries can be mixed types

Also notice # for comment. Not part of data.

<!-- 4-mixedtypesdict.yml -->

    ---
    Juniper: Also a plant
    Cisco: 6500 # They're still around, trust me.
    Brocade: True
    VMware: ['esxi', 'vcenter', 'nsx']

<!-- interpreter -->

    body = ly('4-mixedtypesdict.yml')
    pprint(body)

If we specify values, iterates like a list

<!-- interpreter -->

    for v in body.values():
        print(type(v))

Nesting is possible with lists and dictionaries

Here is a list OF dictionaries

<!-- 5-nesting.yml (already created) -->

    ---
    - name: Juniper
      products: ['vMX', 'vSRX', 'Contrail']
    - name: Cisco
      products: ['Nexus 7K', 'Catalyst 3750', 'ACI']
    - name: Brocade
      products: ['BVC', 'Vyatta 5400 vRouter', 'VDX 6740']
    - name: VMware
      products: ['vCenter', 'NSX', 'Virtual SAN']

<!-- interpreter -->

Pretty print definitely comes in handy here.

    body = ly('5-nesting.yml')
    pprint(body)

As you can see, the root object is still a list

<!-- interpreter -->

    print(type(body))

However, we can loop through this list and see that there are dictionaries
nested inside. This is a list of dictionaries.

<!-- interpreter -->

    for vendor in body:
        print(type(vendor))

Let's augment this loop a little bit to print the vendor name, and
the first product in the list

<!-- interpreter -->

    for vendor in body:
        print('First %s product is %s' % (vendor['name'], vendor['products'][0]))

You may have noticed YAML can store lists one of two ways
I tend to use the one that looks better (explicit is better than implicit)

<!-- 6-nesting2.yml (already created) -->

    ---
    - name: Juniper
      products:
      - vMX
      - vSRX
      - Contrail
    - name: Cisco
      products:
      - Nexus 7K
      - Catalyst 3750
      - ACI
    - name: Brocade
      products:
      - BVC
      - Vyatta 5400 vRouter
      - VDX 6740
    - name: VMware
      products: ['vCenter', 'NSX', 'Virtual SAN']

I'll run the same thing I ran in the last example on this new file. Same results.

<!-- interpreter -->

    body = ly('6-nesting2.yml')

    for vendor in body:
        print('First %s product is %s' % (vendor['name'], vendor['products'][0]))

We'll use Ansible in a bit - it does module arguments a little differently.

Either all on one line, or chunked up like this:

<!-- 7-sampleargs.yml (already created) -->

    login_to_router: 
        user=root
        passwd=Juniper
        port=22
        host=10.12.0.1

Python renders this as a single dictionary, all args just one big string

<!-- interpreter -->

    body = ly('7-sampleargs.yml')
    print(body)

This implies that your Python is responsible for parsing this out.
Fortunately, Ansible does this for us.


# 2 - Jinja2

<< SHOW OF HANDS WHO HAS EXPERIENCE WITH YAML OR AT LEAST DJANGO TEMPLATES >>

Why templates?

    Makes your configs more consistent - eliminates future challenges
    This IS infra-as-code. Enforced configuration
    Some eng orgs don't even touch devices - must go through template engine
    
    Jeremy Schulman wrote [PP article](http://packetpushers.net/python-jinja2-tutorial/), here are some other benefits:
    - HARMLESS to play with
    - Numerous applications
    - Instant Gratification
    - Helps develop basic coding skills


Why Jinja2?

    Jinja2's logic is very similar to Python.
    If you're going to learn some basic code concepts, it may as well be Python

    Jinja2 inserts dynamic data into static data

<!-- Don't forget to cd to ../2-jinja2 -->

The YAML section started with a simple list, so let's do that here.

<!-- vars/1-basicloop.yml -->

    ---
    - Juniper
    - Cisco
    - Brocade
    - VMware

<!-- templates/1-basicloop.j2 -->

    {# We can put in comments like so #}

    Here are four random networking vendors:
    {% for vendor in config -%}
        {{ vendor }}
    {% endfor %}

Note that this is just some text with tags in it

Note comments go in hash sign brackets

Logic statements go in percentage sign brackets

Hyphens keep it all clean

Double bracket means a dyanamic value is inserted, like a variable.

Like before, I need to write a quick Python function to import our data

note the config dictionary. Ansible will break this up for us

<!-- interpreter -->

    from jinja2 import Environment, FileSystemLoader
    import yaml
    from bracket_expansion import *

    ENV = Environment(loader=FileSystemLoader('./templates/'))

    def gen(filename):

        print('-------------------')
        print('')
        with open('vars/' + filename + '.yml') as _:
            varfile = yaml.load(_)
            template = ENV.get_template(filename + ".j2")
            print(template.render(config=varfile))


Now, I can render a template with a YAML data file with a simple function call

(since they're the same name, sans file extension)

<!-- interpreter -->

    gen('1-basicloop')

Okay that was easy enough.
Let's do the same thing, but with a dictionary this time.

<!-- vars/2-iterdict.yml -->

    ---
    Juniper: http://www.juniper.net/us/en/
    Cisco: http://www.cisco.com/
    Brocade: http://www.brocade.com/index.page
    VMware: http://www.vmware.com/

Using an iterator, we can get key and value on each loop pass

<!-- templates/2-iterdict.j2 -->

    {% for vendor, website in config.items() -%}
    You can find more information about {{ vendor }} at {{ website }}
    {% endfor %}

<!-- interpreter -->

    gen('2-iterdict')

Let's use a conditional (if statement)

Our basic list data will do for this example

<!-- vars/3-conditional.yml -->

    ---
    - Juniper
    - Cisco
    - Brocade
    - VMware

I've noticed that Jinja2 is not OCD-compliant re: nesting
(XML is forgiving)

<!-- templates/3-conditional.j2 -->

    {% for vendor in config -%}
    {% if vendor == 'Cisco' -%}
    Big Teal
    {% else -%}
    {{ vendor }}
    {% endif -%}
    {% endfor %}

Cisco has been replaced with Big Teal

<!-- interpreter -->

    gen('3-conditional')

Okay....time to go for hard mode.
Let's represent a VLAN DB for three switches in YAML

<!-- vars/4-advobjects.yml -->

    ---
    - switch_hostname: sw01
      vlans:
        10: Management
        20: vMotion
        30: Server Network 1
        40: Server Network 2
    - switch_hostname: sw02
      vlans:
        10: Management
        20: vMotion
        30: Server Network 1
        40: Server Network 2
    - switch_hostname: sw03
      vlans:
        210: Marketing
        220: Sales
        230: Finance

Remember like the YAML section, there is one object represented here - a list.
Describe the data structures represented above

So, we need two nested loops. One for the outer list, and one inside that for the inner dictionary.
I'm going to write this to output like a Cisco Nexus VLAN configuration.

<!-- templates/4-advobjects.j2 -->

    {% for switch in config -%}
    hostname {{ switch.switch_hostname }}
        {# "dictsort" automatically creates an iterator for us #}
        {% for id, name in switch.vlans|dictsort -%}
            vlan {{ id }}
            name {{ name }}
        {% endfor %}
    {% endfor %}

<!-- interpreter -->

    gen('4-advobjects')

You can re-use templates from other templates.
Let's repeat our last data structure for this exercise.

<!-- vars/5-childtemplates.yml -->

    ---
    - switch_hostname: sw01
      vlans:
        10: Management
        20: vMotion
        30: Server Network 1
        40: Server Network 2
    - switch_hostname: sw02
      vlans:
        10: Management
        20: vMotion
        30: Server Network 1
        40: Server Network 2
    - switch_hostname: sw03
      vlans:
        210: Marketing
        220: Sales
        230: Finance

The way we'll do this in Ansible is the include statement.

<!-- templates/5-childtemplates.j2 -->

    {% include "4-advobjects.j2" %}

    There were {{ config|length }} switches in this configuration.

Bc of import, it renders against our YAML data

The text below the import will augment the included template

<!-- interpreter -->

    gen('5-childtemplates')



You can set values in the template itself using set statements

Lets create a basic YAML file with a single key/value pair

<!-- vars/6-inlinevars.yml -->

    ---
    message: Hello World!

We use the set statement to declare or change values in Jinja2

<!-- templates/6-inlinevars.j2 -->

    {% set TESTVAR = config['message'] %}
    {{ TESTVAR }}
    {% set TESTVAR = '!dlroW olleH' %}
    {{ TESTVAR }}

Next, we're going to use a custom filter to render some interface names. 

More on bracket expansion later. For now, it's just some cool function

One potential problem in writing YAML files is representing interface names

We could create a YAML file containing IF names, but this is better:

<!-- templates/7-customfilter.j2 -->

    {# Credit to Jeremy Schulman - https://vimeo.com/120012280 #}
    {% for iface_name in iface_pattern | bracket_expansion %}
    interface {{ iface_name }}
        speed ludicrous
        switchport mode access
        switchport access vlan {{ vlan_name }}
    {% endfor %}

Adding a few things via Python since we don't have a YAML file

<!-- interpreter -->

    ENV.filters['bracket_expansion'] = bracket_expansion
    template2 = ENV.get_template('7-customfilter.j2')
    print template2.render(iface_pattern='GigabitEthernet0/0/[0-5]', vlan_name=100)

# 3a - Ansible (Linux)

<!-- Might want to use Sublime Text at this point -->

<!-- cd to ../3-ansible/linux -->

Let's spin up a basic virtual machine (Ubuntu 14.04)

    vagrant up

Ansible is pretty awesome, no need for persistent connection, idempotent, uses YAML as a workflow language

Getting the ephemeral state of a network using tools like Ansible is much better than logging in box-by-box
These tools gather it all quickly, and show it to you in one place.

Ease us into use of Ansible, on "home turf": Linux

Look at vagrant ssh-config and update hosts file based on SSH port

Also add SSH key to VM

    ssh-copy-id vagrant@127.0.0.1 -i ~/.ssh/id_rsa -p 2222

If you have an SSH key warning, delete the offending known_hosts line with:

    sed -i.bak -e '<line#>d' ~/.ssh/known_hosts

Step through the sample playbook, run this after each play you write

    ansible-playbook -i hosts sampleplaybook.yml

<!-- linux/sampleplaybook.yml -->

    ---
    - name: Show OS type
      hosts: lab
      gather_facts: yes

      tasks:
      - name: Show operating system
        debug: msg="{{ansible_os_family}}"
        # Feel free to use something else from the setup module

You can run the setup module independently to see all available facts for this host

    ansible -m setup lab -i hosts

Add additional plays to the playbook (keep running it once after each play)

<!-- linux/sampleplaybook.yml (continued) -->

    - name: Install something
      hosts: lab
      sudo: yes

      tasks:

      - name: Install cowsay
        apt: name=cowsay state=present update_cache=yes
        # Idempotence for the win!

        # Test it out! Run cowsay in the trustybox! (vagrant ssh)

    - name: Display Remote Output
      hosts: lab
      # No sudo! Separate plays allows us to run least-privilege

      tasks:

      - name: Record Uptime
        shell: /usr/bin/uptime
        register: result
        
      - name: Display Uptime
        debug: msg="{{result.stdout}}"


Rule of thumb - new play if you need to modify sudo or hosts, etc.
Also consider order. You might use the same play header again later in your playbook.

We can make our playbooks even easier by using roles
What if we could do this:

<!-- linux/config_router_roles.yml -->

    ---
    - name: Configure Trustybox
      hosts: lab
      sudo: yes
      roles:
        - router

Run script to autodownload some roles for us to look at:

    ./refreshroles.sh

Walk through the anatomy of the router role

Run the playbook

    ansible-playbook -i hosts config_router_roles.yml

Check to see our template was placed correctly

<!-- after vagrant ssh -->
    cat /etc/sysctl.conf

Check that our notifier worked

<!-- after vagrant ssh -->
    sysctl net.ipv4.ip_forward
    sysctl net.ipv6.conf.all.forwarding

Routing enabled, but we need a protocol stack - Quagga.

Installing Quagga pulls packages from internet, hopefully it works

Show Quagga role files

Add quagga role to playbook

Run playbook again, with quagga role added
Note idempotence of router role

    ansible-playbook -i hosts config_router_roles.yml

Verify Quagga is running:

<!-- after vagrant ssh -->
    /etc/init.d/quagga status
    ps -ef | grep quagga

We can also telnet directly to ospfd

<!-- after vagrant ssh -->
    telnet 127.0.0.1 2604
    <!-- password is Quagga -->
    show ip ospf database

More network-centric Ansible roles for Linux in the Git repo than what I showed
<!-- Poke around at these if there is time -->

Shut down our trustybox

    vagrant halt

# 3b - Ansible (JunOS)

<!-- make sure you cd ../junos -->

Spin up our three routers while you talk

    vagrant up 

vagrant junos images GREAT work by Juniper; they run at 2G RAM, so an 8G machine is pushing it

Instructions for installing vagrant plugin and box are in repo. I've done this

Requires Junos Ansible modules - my initdemo.sh takes care of this for us

I'll be using a modified version of Juniper's public Ansible playbooks

Talk through the network topology (show slide)
The goal is to get the loopback on vsrx03 advertised to vsrx01 via BGP ***WITHOUT LOGGING INTO A ROUTER MANUALLY***

vSRXs start totally blank, but with my repo, you can run full BGP in one command. BOOM

Run init script and source junos ansible libs

    ./lab_init.sh && source ../../../ansible-junos-stdlib/env-setup

Show hosts file

Let's start constructing our playbook. Fact gathering

<!-- junos/junos.yml -->

    ---
    - name: "Gather Facts"
      hosts: vsrx
      connection: local # Note local
      gather_facts: no # note no fact gathering, have to go in registers

      tasks:

        - name: gathering info from device
          junos_get_facts: 
            user=root
            passwd=Juniper
            port={{ ncssh_port }}
            host={{ ip_addr }}
          register: junos

        - name: version
          debug: msg={{ junos.facts.version }}

        - name: serial-number
          debug: msg={{ junos.facts.serialnumber }}

Run playbook, noting facts

    ansible-playbook -i hosts junos.yml

Add play for creating build directories

Note the set_fact for per-device key/value pairs

<!-- (append) junos/junos.yml -->

    - name: Creating build directories for each host
      hosts: vsrx
      connection: local
      gather_facts: no

      # You can use multiple identical play headers, if it helps it look better

      tasks:
        - set_fact: 
            build_dir: "{{ build_dir }}/{{ inventory_hostname }}/tmp"
        - name: remove host build temp directory
          file: path={{ build_dir }} state=absent
        - name: create host build temp directory
          file: path={{ build_dir }} state=directory

Run again

    ansible-playbook -i hosts junos.yml

Show the local directories have been created

    ll build

Look at host_vars. Data model for networking (only IF names are junos-specific)
Idempotence of Ansible means deviations are squashed easily

We'll use roles to build our JunOS configs (show router_baseconf)

Writing a play to leverage this role is quite similar to our linux example

<!-- (append) junos/junos.yml -->

    - name: Generate templates for each device by roles
      hosts: vsrx
      connection: local
      gather_facts: no

      # These roles just build our configs, not deploy them

      roles:
        - router_baseconf

Re-run the playbook to generate our configs

    ansible-playbook -i hosts junos.yml

Compare the host_vars and role templates with the configs in the build directory

The junos_install_config module will load-merge our configuration
This is safer than overwrite

<!-- (append) junos/junos.yml -->

    - name: Merge the Base Configuration
      hosts: vsrx
      connection: local
      gather_facts: no

      tasks:
        - name: load-merge config file
          junos_install_config: 
            user=root
            passwd=Juniper
            port={{ ncssh_port }}
            host={{ ip_addr }}
            file={{ build_dir }}/router_baseconf.conf
            logfile={{ log_dir }}/{{ inventory_hostname }}.log

Run playbook again

    ansible-playbook -i hosts junos.yml

I'm going to run a quick test script - more on this later

    python ../../4-python/post-ansibletest.py < port# >

This allows us to verify things worked without logging into a box

On to the main attraction - BGP 
 - Show junos/finished/bgp_config_final (desired end state for vSRX03)
 - Show router_bgp role files

Need to add the role statement to our playbook so we have the configs built

<!-- (append) junos/junos.yml -->

      roles:
        - router_baseconf
        - router_bgp # <-- ADD THIS

Run our playbook to build the BGP configs

    ansible-playbook -i hosts junos.yml

Show the new BGP config files in the build dir

Now we deploy the BGP configs

<!-- (append) junos/junos.yml -->

    - name: Merge the BGP Configuration
      hosts: vsrx
      connection: local
      gather_facts: no

      tasks:
        - name: load-merge config file
          junos_install_config: 
            user=root
            passwd=Juniper
            port={{ ncssh_port }}
            host={{ ip_addr }}
            file={{ build_dir }}/router_bgp.xml
            logfile={{ log_dir }}/{{ inventory_hostname }}.log

Run once more!

    ansible-playbook -i hosts junos.yml

Time to test once more to make sure our mission has been accomplished!

    python ../../4-python/post-ansibletest.py < port# >

I'll explain that script, and more, in the next section!

# 4 - Python

<!-- don't forget to cd ../../4-python -->

Remember bracket_expansion from Jinja2?
Let's do that in the Python shell now

<!-- interpreter -->

    # Part of stdlib (comes with Python)
    import itertools

    # 3rd party lib (install via pip)
    from bracket_expansion import *

    # I called it iface_list because it will result in a list of interfaces
    # but the object actually is a generator
    iface_list = bracket_expansion('GigabitEthernet1/1/[0-9]')

    # See?
    iface_list

    # Generators don't even have a length (How could they?)
    len(iface_list)  # This will raise an exception

    # Iterating over this generator expands the numbers in the brackets
    # VERY useful for creating a list of network interfaces
    for iface in iface_list:
        print iface

    # Generators are one-time-use (calculates on the fly)
    # So if we try to run it again, we get nothing
    for iface in iface_list:
        print iface

    # We have to recreate it if we want to iterate over it again
    iface_list = bracket_expansion('GigabitEthernet1/1/[0-9]')

    # Converts to list (so we can re-use - stores in memory)
    my_list = list(iface_list)

    # Stored in memory, not on-the-fly, so has a length.
    len(my_list)

    # Time to look at chaining

    # Let's create two generators
    iface_list1 = bracket_expansion('GigabitEthernet1/1/[0-24]')
    iface_list2 = bracket_expansion('GigabitEthernet1/2/[0-24]')

    # If we wanted to, we could put these in a list
    iface_test = [iface_list1, iface_list2]

    # But that list contains two separate iterables, so we'd
    # have to use nested loops (non-optimal)
    for iface in iface_test:
        print iface

    # Itertools "chain" method lets us merge these two iterables together
    # Even generators! (Which IMO is really cool)
    iface_chain = itertools.chain(iface_list1, iface_list2)

    # We can now iterate over the chain as if we had created one big generator
    for iface in iface_chain:
        print iface

    # By the way, multiple brackets works too!
    iface_list1 = bracket_expansion('GigabitEthernet1/[0-3]/[0-24]')
    for iface in iface_list1:
        print iface

Let's see if we can use the Python interpreter to verify success of Ansible exercise

Talk through below commands

<!-- python interpreter -->

    >>> from jnpr.junos import Device
    >>> from jnpr.junos.op.routes import RouteTable
    >>> dev = Device(host='127.0.0.1', user='root', password='Juniper', port=<port>)
    >>> dev.open()
    >>> routes = RouteTable(dev).get('123.123.123.1/24')
    >>> print routes

<!-- DONT CLOSE IPYTHON -->

Show the post-ansibletest.py script and explain how it works

Also some fact gathering (this is how Junos Ansible module works)

<!-- python interpreter -->

    >>> from pprint import pprint  # makes output prettier
    >>> pprint(dev.facts)

Walk through pyez_advanced
Once ports are set correctly, run it.

<!-- shell -->

    python pyez_advanced.py

Talk about TDD and how it can be applied to networking
(Everyone wants to automate config, validation is just as if not more important)
Useful to take baseline comparisons before and after a change

Run unitttest to validate our network is as it should be

We can use the Tables/Views concepts we just learned to give us useful data

<!-- shell -->

    python -m unittest pyez_unittest

# Conclusion

Lots of other things to explore
- Jason Edelman session with Cisco NXAPI
- Increasing number of Ansible modules for networking

Advance to Parting thoughts slide

Your automation project will not find success without buy-in.

Make automation-friendly infra decisions

Open up a GH issue for any questions after the workshop, I'll try to watch the repo
If I don't answer, tweet me @Mierdin 