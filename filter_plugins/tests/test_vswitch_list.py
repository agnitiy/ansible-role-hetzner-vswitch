import unittest

from filter_plugins.vswitch_list import *


class VSwitchListTest(unittest.TestCase):

    def test_init(self):
        module = FilterModule()
        filters = module.filters()
        self.assertEqual(filters.get('hetzner_vswitch_vswitch_list'), vswitch_list)

    def test_vswitch_list(self):
        host_vars = {
            'x': {
                'hetzner_vswitch_host': [
                    {'name': 'vswitch1', 'state': 'absent'},
                    {'name': 'vswitch2'}
                ],
                'ansible_host': '111.111.111.111'
            },
            'y': {
                'hetzner_vswitch_host': [
                    {'name': 'vswitch1'}
                ],
                'ansible_host': '111.111.111.112'
            },
            'z': {
                'ansible_host': '111.111.111.113'
            }
        }
        hosts = ['x', 'y', 'z']
        expected_results = [
            {
                'name': 'vswitch1',
                'server': [
                    {'server_ip': '111.111.111.111', 'state': 'absent'},
                    {'server_ip': '111.111.111.112', 'state': 'present'}
                ]
             },
            {
                'name': 'vswitch2',
                'server': [
                    {'server_ip': '111.111.111.111', 'state': 'present'}
                ]
            }
        ]
        actual_results = vswitch_list(host_vars, hosts)

        self.assertEqual(expected_results, actual_results)

    def test_vswitch_list_ip_address(self):
        host_vars = {
            'x': {
                'hetzner_vswitch_host': [
                    {'name': 'vswitch1'},
                ],
                'ansible_default_ipv4': {'address', '111.111.111.111'}
            },
            'y': {
                'hetzner_vswitch_host': [
                    {'name': 'vswitch1'}
                ],
                'ansible_default_ipv4': {'address', '111.111.111.112'}
            }
        }
        hosts = ['x', 'y']
        expected_results = [
            {
                'name': 'vswitch1',
                'server': [
                    {'server_ip': '111.111.111.111', 'state': 'present'},
                    {'server_ip': '111.111.111.112', 'state': 'present'}
                ]
            }
        ]
