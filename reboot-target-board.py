#!/usr/bin/env python3

"""
Copyright: Nobuhiro Iwamatsu <iwamatsu@nigauri.org>

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""

import sys
import time
import yaml
import xmlrpc.client

if __name__ == "__main__":

    username = sys.argv[1]
    token= sys.argv[2]
    lava_server = sys.argv[3]
    http_scheme = sys.argv[4]
    target_board = sys.argv[5]

    server = xmlrpc.client.ServerProxy("%s://%s:%s@%s/RPC2" %
            (http_scheme, username, token, lava_server), allow_none=True)

    board_status_data = server.scheduler.get_device_status(target_board)
    status = board_status_data['status']
    if status == 'offline':
        print ("%s is offline. reboot...." % target_board)
        server.scheduler.put_into_maintenance_mode(target_board, "debug")
        time.sleep(3)
        server.scheduler.put_into_online_mode(target_board, "debug", False)
