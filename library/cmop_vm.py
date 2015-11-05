#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) 2015, zhi chuanxiu(yumaojun03@gmail.com)

This file is part of Ansible

Ansible is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Ansible is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ansible. If not, see <http://www.gnu.org/licenses/>.
"""


from ansible.module_utils.basic import *

import requests
import json


class Main(object):
    """
    this is the main module
    """

    def __init__(self):
        global module
        module = AnsibleModule(
            argument_spec=dict(
                accessKey        = dict(required=True),
                vpcCode          = dict(required=True),
                subnetCode       = dict(required=True),
                instanceTypeCode = dict(required=True),
                imageCode        = dict(required=True),
                numbers          = dict(required=True),
                ),
            supports_check_mode=True
        )
        self.accessKey           = module.params['accessKey']
        self.vpcCode             = module.params['vpcCode']
        self.subnetCode          = module.params['subnetCode']
        self.instanceTypeCode    = module.params['instanceTypeCode']
        self.imageCode           = module.params['imageCode']
        self.numbers             = module.params['numbers']
        self.vm_ids              = []
        self.vm_ips              = []


    def create_vm(self):
        """
        create a vm
        """
        creat_uri = "http://10.10.12.31:8080/cmop-api/v1/instance?accessKey={0}&vpcCode={1}&subnetCode={2}&instanceTypeCode={3}&imageCode={4}".format(
                     self.accessKey,
                     self.vpcCode,
                     self.subnetCode,
                     self.instanceTypeCode,
                     self.imageCode)
       
        for i in range(int(self.numbers)): 
            r = requests.post(creat_uri, timeout=300)
            if not r:
                module.fail_json(change=False, msg="not date received")
            data = r.json()
            if data.get('code') == "0":
                self.vm_ids.append(data.get("message"))
        else:
            module.fail_json(change=False, msg="response code isn't 0")



    def get_vm_ip(self, *vm_ids):
        """
        get vm id
        """
        vminfo_uri = "http://10.10.12.31:8080/cmop-api/v1/instance/{0}/{1}".format(vm_id, self.accessKey)

        for vm_id in vm_ids:
            r = requests.get(vminfo_uri, timeout=300)
            if not r:
                module.fail_json(change=False, msg="not date received")
            data = r.json()
            if data.get('code') == "0":
                self.vm_ips.append(data.get("entity").get("ipaddress"))
            else:
                module.fail_json(change=False, msg="response code isn't 0")
        module.exit_json(change=True, result=self.vm_ips)

        
    def __call__(self):
        """
        execute the module.
        """
        vm_id = self.create_vm()
        self.get_vm_ip(self.vm_ids)


if __name__ == "__main__":
    main = Main()
    main()

