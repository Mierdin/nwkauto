from jinja2 import Environment, FileSystemLoader
import yaml
from bracket_expansion import *

ENV = Environment(loader=FileSystemLoader('./templates/'))


# To keep the python portion as simple as possible, I am passing all
# of our variable data in under a big dictionary. So we have to refer
# to them with the config.key notation.
# In the next section, Ansible allows us to refer to variables directly.

def gen(filename):

    print('-------------------')
    print('')
    with open('vars/' + filename + '.yml') as _:
        varfile = yaml.load(_)
        template = ENV.get_template(filename + ".j2")
        print(template.render(config=varfile))

gen('1-basicloop')

gen('2-iterdict')

gen('3-conditional')

gen('4-advobjects')

gen('5-childtemplates')

gen('6-inlinevars')

ENV.filters['bracket_expansion'] = bracket_expansion
template2 = ENV.get_template('7-customfilter.j2')
print template2.render(iface_pattern='GigabitEthernet0/0/[0-5]', vlan_name=100)
