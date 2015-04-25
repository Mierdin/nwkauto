# Credit for this exercise goes to Jeremy Schulman - he has
# been fighting the good fight for the automation community
# for a long time. See video: https://vimeo.com/119996709

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
