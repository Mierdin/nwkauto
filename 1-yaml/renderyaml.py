#!/usr/bin/env python

# There's a lot more to YAML than what I'll cover here. I will be
# covering only that which is strictly needed for the rest of this
# workshop, and use with network automation tools.

# This Python is really simple, and is only used for illustrating
# how the YAML might be rendered in software. The focus is on the YAML
# syntax itself

# Read the spec here:
# http://www.yaml.org/spec/1.2/spec.html

import yaml
from pprint import pprint


def ly(filename):
    with open(filename) as _:
        return yaml.load(_)

print('##################################')

# Print list

body = ly('1-list.yml')
print(type(body))
print(len(body))
print(body)

print('##################################')

# Mixed Types List

body = ly('2-mixedtypeslist.yml')
print(type(body))
print(len(body))
print(body)

# Small loop to show individual types
for item in body:
    print(type(item))


print('##################################')

# Basic Dictionary

body = ly('3-dictionary.yml')
print(type(body))
print(len(body))

# pprint makes this easier to look at
pprint(body)

# We can call up a specific member of this dictionary by key
print(body['Juniper'])


print('##################################')

# Dictionary with mixed types

# YAML mimics the flexibility of Python
# Notice that strings (usually) don't have to be enclosed in quotes.

# Also notice the hash symbol to indicate a comment
# (it is not part of our data)

body = ly('4-mixedtypesdict.yml')

pprint(body)

for v in body.values():
    print(type(v))

print('##################################')

# Dictionary with mixed types

# YAML mimics the flexibility of Python
# Notice that strings (usually) don't have to be enclosed in quotes

body = ly('5-nesting.yml')

pprint(body)

# There's only one object on this page, and it's a list
print(type(body))

# We can loop through this list and see that there are dictionaries
# nested inside. This is a list of dictionaries.
for vendor in body:
    print(type(vendor))

# Let's augment this loop a little bit to print the vendor name, and the
# first product in the list
for vendor in body:
    print('First %s product is %s' % (vendor['name'], vendor['products'][0]))

print('##################################')

# Dictionary with mixed types (different list format)

# You may have noticed that the previous example seemed to use different
# formats for storing lists. YAML allows us to use either format, and I
# typically choose the right one for the circumstance (what looks better)

# I'll run the same thing I ran in the last example - same results.

body = ly('6-nesting2.yml')

for vendor in body:
    print('First %s product is %s' % (vendor['name'], vendor['products'][0]))


print('##################################')

# Ansible module argument style

# We'll see later on in the workshop that Ansible uses an interesting format
# for passing arguments to a module. These all get placed into a single string
# whether it's all on one line, or split up like you see here.

body = ly('7-sampleargs.yml')

print(body)
