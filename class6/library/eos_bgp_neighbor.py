#!/usr/bin/python
#
# Copyright (c) 2015, Arista Networks, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
#   Neither the name of Arista Networks nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ARISTA NETWORKS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
DOCUMENTATION = """
---
module: eos_bgp_neighbor
short_description: Manage BGP neighbor statements in EOS
description:
  - This eos_bgp_neighbor module provides stateful management of the
    neighbor statements for the BGP routing process for Arista EOS nodes
version_added: 1.1.0
category: BGP
author: Arista EOS+
requirements:
  - Arista EOS 4.13.7M or later with command API enable
  - Python Client for eAPI 0.3.1 or later
notes:
  - All configuraiton is idempontent unless otherwise specified
  - Supports eos metaparameters for using the eAPI transport
  - Supports tateful resource configuration
options:
  name:
    description:
      - The name of the BGP neighbor to manage.  This value can be either
        an IPv4 address or string (in the case of managing a peer group)
    required: true
    default: null
    choices: []
    aliases: []
    version_added: 1.1.0
  peer_group:
    description:
      - The name of the peer-group value to associate with the neighbor.  This
        argument is only valid if the neighbor is an IPv4 address
    default: null
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  remote_as:
    description:
      - Configures the BGP neighbors remote-as value.  Valid AS values are
        in the range of 1 to 65535.
    default: null
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  send_community:
    description:
      - Configures the BGP neighbors send-community value.  If enabled then
        the BGP send-community value  is enable.  If disabled, then the
        BGP send-community value is disabled.
    default: false
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  next_hop_self:
    description:
      - Configures the BGP neighbors next-hop-self value.  If enabled then
        the BGP next-hop-self value is enabled.  If disabled, then the BGP
        next-hop-self community value is disabled.
    default: false
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  route_map_in:
    description:
      - Configures the BGP neigbhors route-map in value.  The value specifies
        the name of the route-map.
    default: null
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  route_map_out:
    description:
      - Configures the BGP neigbhors route-map out value.  The value specifies
        the name of the route-map.
    default: null
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  description:
    description:
      - Configures the BGP neighbors description value.  The value specifies
        an arbitrary description to add to the neighbor statement in the
        nodes running-configuration.
    default: null
    required: false
    choices: []
    aliases: []
    version_added: 1.1.0
  enable:
    description:
      - Configures the administrative state for the BGP neighbor
        process. If enable is True then the BGP neighbor process is
        administartively enabled and if enable is False then
        the BGP neighbor process is administratively disabled.
    default: true
    required: false
    choices: ['True', 'False']
    aliases: []
    version_added: 1.1.0
"""

EXAMPLES = """

- name: add neighbor 172.16.10.1 to BGP
  eos_bgp_neighbor: name=172.16.10.1 enable=yes remote_as=65000

- name: remove neighbor 172.16.10.1 to BGP
  eos_bgp_neighbor name=172.16.10.1 enable=yes remote_as=65000 state=absent
"""
#<<EOS_COMMON_MODULE_START>>

import syslog
import collections

from ansible.module_utils.basic import *

try:
    import pyeapi
    PYEAPI_AVAILABLE = True
except ImportError:
    PYEAPI_AVAILABLE = False

DEFAULT_SYSLOG_PRIORITY = syslog.LOG_NOTICE
DEFAULT_CONNECTION = 'localhost'
TRANSPORTS = ['socket', 'http', 'https', 'http_local']

class EosAnsibleModule(AnsibleModule):

    meta_args = {
        'config': dict(),
        'username': dict(),
        'password': dict(),
        'host': dict(),
        'connection': dict(default=DEFAULT_CONNECTION),
        'transport': dict(choices=TRANSPORTS),
        'port': dict(),
        'debug': dict(type='bool', default='false'),
        'logging': dict(type='bool', default='true')
    }

    stateful_args = {
        'state': dict(default='present', choices=['present', 'absent']),
    }

    def __init__(self, stateful=True, *args, **kwargs):

        kwargs['argument_spec'].update(self.meta_args)

        self._stateful = stateful
        if stateful:
            kwargs['argument_spec'].update(self.stateful_args)

        super(EosAnsibleModule, self).__init__(*args, **kwargs)

        self.result = dict(changed=False, changes=dict())

        self._debug = kwargs.get('debug') or self.boolean(self.params['debug'])
        self._logging = kwargs.get('logging') or self.params['logging']

        self.log('DEBUG flag is %s' % self._debug)

        self.debug('pyeapi_version', self.check_pyeapi())
        self.debug('stateful', self._stateful)
        self.debug('params', self.params)

        self._attributes = self.map_argument_spec()
        self.validate()

        self._node = self.connect()
        self._instance = None

        self.desired_state = self.params['state'] if self._stateful else None
        self.exit_after_flush = kwargs.get('exit_after_flush')

    @property
    def instance(self):
        if self._instance:
            return self._instance

        func = self.func('instance')
        if not func:
            self.fail('Module does not support "instance"')

        try:
            self._instance = func(self)
        except Exception as exc:
            self.fail('instance[error]: %s' % exc.message)

        self.log("called instance: %s" % self._instance)
        return self._instance

    @property
    def attributes(self):
        return self._attributes

    @property
    def node(self):
        if self._node:
            return self._node
        self._node = self.connect()
        return self._node

    def check_pyeapi(self):
        if not PYEAPI_AVAILABLE:
            self.fail('Unable to import pyeapi, is it installed?')
        return pyeapi.__version__

    def map_argument_spec(self):
        """map_argument_spec maps only the module argument spec to attrs

        This method will map the argumentspec minus the meta_args to attrs
        and return the attrs.  This returns a dict object that includes only
        the original argspec plus the stateful_args (if self._stateful=True)

        Returns:
            dict: Returns a dict object that includes the original
                argument_spec plus stateful_args with values minus meta_args

        """
        keys = set(self.params).difference(self.meta_args)
        attrs = dict()
        attrs = dict([(k, self.params[k]) for k in self.params if k in keys])
        if 'CHECKMODE' in attrs:
            del attrs['CHECKMODE']
        return attrs

    def validate(self):
        for key, value in self.attributes.iteritems():
            func = self.func('validate_%s' % key)
            if func:
                self.attributes[key] = func(value)

    def create(self):
        if not self.check_mode:
            func = self.func('create')
            if not func:
                self.fail('Module must define "create" function')
            return self.invoke(func, self)

    def remove(self):
        if not self.check_mode:
            func = self.func('remove')
            if not func:
                self.fail('Module most define "remove" function')
            return self.invoke(func, self)

    def flush(self, exit_after_flush=False):
        self.exit_after_flush = exit_after_flush

        if self.desired_state == 'present' or not self._stateful:
            if self.instance.get('state') == 'absent':
                changed = self.create()
                self.result['changed'] = changed or True
                self.refresh()

            changeset = self.attributes.viewitems() - self.instance.viewitems()

            if self._debug:
                self.debug('desired_state', self.attributes)
                self.debug('current_state', self.instance)

            changes = self.update(changeset)
            if changes:
                self.result['changes'] = changes
                self.result['changed'] = True

            self._attributes.update(changes)

            flush = self.func('flush')
            if flush:
                self.invoke(flush, self)

        elif self.desired_state == 'absent' and self._stateful:
            if self.instance.get('state') == 'present':
                changed = self.remove()
                self.result['changed'] = changed or True

        elif self._stateful:
            if self.desired_state != self.instance.get('state'):
                changed = self.invoke(self.instance.get('state'))
                self.result['changed'] = changed or True

        self.refresh()
        self.result['instance'] = self.instance

        if self.exit_after_flush:
            self.exit()

    def update(self, changeset):
        changes = dict()
        for key, value in changeset:
            if value is not None:
                changes[key] = value
                func = self.func('set_%s' % key)
                if func and not self.check_mode:
                    try:
                        self.invoke(func, self)
                    except Exception as exc:
                        self.fail(exc.message)
        return changes

    def connect(self):
        if self.params['config']:
            pyeapi.load_config(self.params['config'])

        config = dict()

        if self.params['connection']:
            config = pyeapi.config_for(self.params['connection'])
            if not config:
                msg = 'Connection name "%s" not found' % self.params['connection']
                self.fail(msg)

        if self.params['username']:
            config['username'] = self.params['username']

        if self.params['password']:
            config['password'] = self.params['password']

        if self.params['transport']:
            config['transport'] = self.params['transport']

        if self.params['port']:
            config['port'] = self.params['port']

        if self.params['host']:
            config['host'] = self.params['host']

        if 'transport' not in config:
            self.fail('Connection must define a transport')

        connection = pyeapi.client.make_connection(**config)
        node = pyeapi.client.Node(connection, **config)

        try:
            resp = node.enable('show version')
            self.debug('eos_version', resp[0]['result']['version'])
            self.debug('eos_model', resp[0]['result']['modelName'])
        except (pyeapi.eapilib.ConnectionError, pyeapi.eapilib.CommandError):
            self.fail('unable to connect to %s' % node)
        else:
            self.log('Connected to node %s' % node)
            self.debug('node', str(node))

        return node

    def config(self, commands):
        self.result['changed'] = True
        if not self.check_mode:
            self.node.config(commands)

    def api(self, module):
        return self.node.api(module)

    def func(self, name):
        return globals().get(name)

    def invoke(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            self.fail(exc.message)

    def invoke_function(self, name, *args, **kwargs):
        func = self.func(name)
        if func:
            return self.invoke(func, *args, **kwargs)

    def fail(self, msg):
        self.invoke_function('on_fail', self)
        self.log('ERROR: %s' % msg, syslog.LOG_ERR)
        self.fail_json(msg=msg)

    def exit(self):
        self.invoke_function('on_exit', self)
        self.log('Module completed successfully')
        self.exit_json(**self.result)

    def refresh(self):
        self._instance = None

    def debug(self, key, value):
        if self._debug:
            if 'debug' not in self.result:
                self.result['debug'] = dict()
            self.result['debug'][key] = value

    def log(self, message, priority=None):
        if self._logging:
            syslog.openlog('ansible-eos')
            priority = priority or DEFAULT_SYSLOG_PRIORITY
            syslog.syslog(priority, str(message))

    @classmethod
    def add_state(cls, name):
        cls.stateful_args['state']['choices'].append(name)

#<<EOS_COMMON_MODULE_END>>

def instance(module):
    """Returns the BGP network instance
    """
    name = module.attributes['name']
    result = module.node.api('bgp').get()

    _instance = dict(name=name, state='absent')
    config = result['neighbors'].get(name)

    if config:
        _instance['state'] = 'present'
        _instance['peer_group'] = config['peer_group']
        _instance['description'] = config['description']
        _instance['next_hop_self'] = config['next_hop_self']
        _instance['remote_as'] = config['remote_as']
        _instance['route_map_in'] = config['route_map_in']
        _instance['route_map_out'] = config['route_map_out']
        _instance['send_community'] = config['send_community']
        _instance['enable'] = not config['shutdown']

    return _instance


def create(module):
    """Create an instance of BGP neighbor on the node
    """
    name = module.attributes['name']
    module.log('Invoked create for eos_bgp_neighbor[{}]'.format(name))
    module.node.api('bgp').neighbors.create(name)

def remove(module):
    """Removes an instance of BGP neighbor from the node
    """
    name = module.attributes['name']
    module.log('Invoked delete for eos_bgp_neighbor[{}]'.format(name))
    module.node.api('bgp').neighbors.delete(name)

def set_peer_group(module):
    """configures the BGP peer-group value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['peer_group']
    module.log('Invoked set_peer_group for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_peer_group(name, value)

def set_remote_as(module):
    """Configures the BGP remote-as value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['remote_as']
    module.log('Invoked set_remote_as for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_remote_as(name, value)

def set_send_community(module):
    """Configures the BGP send-community value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['send_community']
    module.log('Invoked set_send_community for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_send_community(name, value)

def set_next_hop_self(module):
    """Configures the BGP next-hop-self value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['next_hop_self']
    module.log('Invoked set_next_hop_self for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_next_hop_self(name, value)

def set_route_map_in(module):
    """Configures the BGP route-map in value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['route_map_in']
    module.log('Invoked set_route_map_in for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_route_map_in(name, value)

def set_route_map_out(module):
    """Configures the BGP route-map out value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['route_map_out']
    module.log('Invoked set_route_map_out for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_route_map_out(name, value)

def set_description(module):
    """Configures the BGP description value for this neighbor
    """
    name = module.attributes['name']
    value = module.attributes['description']
    module.log('Invoked set_description for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_description(name, value)

def set_enable(module):
    """Configures the BGP shutdown value for this neighbor
    """
    name = module.attributes['name']
    value = not module.attributes['enable']
    module.log('Invoked set_shutdown for eos_bgp_neighbor[{}] '
               'with value {}'.format(name, value))
    module.node.api('bgp').neighbors.set_shutdown(name, value)


def main():
    """The main module routine called when the module is run by Ansible
    """

    argument_spec = dict(
        name=dict(required=True),
        peer_group=dict(),
        remote_as=dict(),
        send_community=dict(type='bool'),
        next_hop_self=dict(type='bool'),
        route_map_in=dict(),
        route_map_out=dict(),
        description=dict(),
        enable=dict(type='bool', default=False)
    )

    module = EosAnsibleModule(argument_spec=argument_spec,
                              supports_check_mode=True)

    module.flush(True)


main()