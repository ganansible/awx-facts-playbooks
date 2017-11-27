#!/usr/bin/env python

from ansible.module_utils.basic import * # noqa

DOCUMENTATION = '''
---
module: scan_subnets
short_description: Return the list of subnets that the host is connected
description:
    - Return the list of subnets that the host is connected
version_added: "2.3"
options:
requirements: [ ]
author: Koray Seremet
'''

EXAMPLES = '''
# Example fact output:
# host | success >> {
#    "ansible_facts": {
#        "subnets": [
#           "10.100.198.0",
#           "192.0",
#           "172.19.123",
#           "10.100.199.0",
#           "192.168",
#           "10.100.193.0",
#         ]
#       }
#     }
'''

def get_subnet_list():
    import os

    subnets = []
    r = filter(None, os.popen('ip route list scope link | cut -d" " -f1 | cut -d/ -f1').read().split('\n'))

    for route in r:
      subnet = ''
      for p in route.split('.'):
         if subnet:
           subnet = subnet + "." + p
         else:
           subnet = p
         subnets.append(subnet)

    return list(set(subnets))


def main():
    module = AnsibleModule(
        argument_spec = dict()
    )

    subnets = get_subnet_list()

    if subnets:
        results = dict(ansible_facts=dict(subnets=subnets))
    else:
        results = dict(skipped=True, msg="Failed to get subnets")
    module.exit_json(**results)

main()
