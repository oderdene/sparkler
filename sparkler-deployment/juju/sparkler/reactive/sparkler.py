# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import when, when_not, set_state
from charmhelpers.core.hookenv import status_set, log
from charmhelpers.core import hookenv, unitdata
import jujuresources
from charmhelpers.core.host import adduser, chownr, mkdir
import urllib


hook_data = unitdata.HookData()
db = unitdata.kv()
hooks = hookenv.Hooks()

resources = {
    'sparkler-0.1': 'sparkler-0.1'
}

@when_not('sparkler.installed')
def install_sparkler():
    resource_key="sparkler-0.1"
    resource = resources[resource_key]
    mkdir('/opt/sparkler/')
    urllib.request.urlretrieve("https://dl.dropboxusercontent.com/u/8503756/sparkler-app-0.1-SNAPSHOT.jar", "/opt/sparkler/sparkler-app-0.1-SNAPSHOT.jar")
    #jujuresources.install(1resource,
    #                      destination="/opt/sparkler",
    #                      skip_top_level=False)
    set_state('sparkler.installed')

@when_not('java.ready')
def no_java():
    status_set('waiting', 'Waiting for Java to become available')

@when_not('solr-interface.connected')
@when_not('solr-interface.available')
def no_solr():
    status_set('waiting', 'Waiting for Solr to become available')

@when('solr-interface.available')
@when('java.ready')
def configure_sparkler(j, s):
    set_state('sparkler.configured')



@when('sparkler.configured')
def run_sparkler():
    status_set('active', 'Sparkler is configured awaiting action')
