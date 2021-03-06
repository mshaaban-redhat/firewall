#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2020 Palo Alto Networks, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: panos_application_group
short_description: Create application groups on PAN-OS devices.
description:
    - Create application groups on PAN-OS devices.
author: "Michael Richardson (@mrichardson03)"
version_added: '2.1.0'
requirements:
    - pan-python can be obtained from PyPI U(https://pypi.python.org/pypi/pan-python)
    - pandevice can be obtained from PyPI U(https://pypi.python.org/pypi/pandevice)
notes:
    - Panorama is supported.
    - Check mode is supported.
extends_documentation_fragment:
    - paloaltonetworks.panos.fragments.transitional_provider
    - paloaltonetworks.panos.fragments.vsys
    - paloaltonetworks.panos.fragments.device_group
    - paloaltonetworks.panos.fragments.state
options:
    name:
        description:
            - Name of the object.
        type: str
        required: true
    value:
        description:
            - List of applications to add to the group
        type: list
        elements: str
    tag:
        description:
            - Administrative tags
        type: list
        elements: str
'''

EXAMPLES = '''
- name: Create application group
  panos_application_group:
    provider: '{{ provider }}'
    name: 'Software Updates'
    value:
        - ms-update
        - apple-update
        - adobe-update
        - google-update
        - ms-product-activation
'''

RETURN = '''
# Default return values
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.paloaltonetworks.panos.plugins.module_utils.panos import get_connection

try:
    from panos.objects import ApplicationGroup
    from panos.errors import PanDeviceError
except ImportError:
    try:
        from pandevice.objects import ApplicationGroup
        from pandevice.errors import PanDeviceError
    except ImportError:
        pass


def main():
    helper = get_connection(
        vsys=True,
        device_group=True,
        with_classic_provider_spec=True,
        with_state=True,
        argument_spec=dict(
            name=dict(type='str', required=True),
            value=dict(type='list', elements='str'),
            tag=dict(type='list', elements='str'),
        )
    )

    required_if = [
        ["state", "present", ["value"]]
    ]

    module = AnsibleModule(
        argument_spec=helper.argument_spec,
        required_one_of=helper.required_one_of,
        required_if=required_if,
        supports_check_mode=True
    )

    parent = helper.get_pandevice_parent(module)

    spec = {
        'name': module.params['name'],
        'value': module.params['value'],
        'tag': module.params['tag'],
    }

    try:
        listing = ApplicationGroup.refreshall(parent, add=False)
    except PanDeviceError as e:
        module.fail_json(msg='Failed refresh: {0}'.format(e))

    obj = ApplicationGroup(**spec)
    parent.add(obj)

    changed, diff = helper.apply_state(obj, listing, module)
    module.exit_json(changed=changed, diff=diff)


if __name__ == '__main__':
    main()
