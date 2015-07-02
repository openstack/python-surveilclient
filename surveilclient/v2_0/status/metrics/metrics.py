# Copyright 2014-2015 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json

from surveilclient.common import surveil_manager


class MetricsManager(surveil_manager.SurveilManager):
    base_url = '/status/hosts'

    def get(self, host_name, metric_name=None, service_description=None):
        """Get a list of last metrics."""

        resp, body = self.http_client.json_request(
            self._create_url(host_name, service_description, metric_name),
            'GET'
        )

        return body

    def list(self, host_name, metric_name, service_description=None,
             live_query=None, start_time=None, end_time=None):
        """Get a list of metrics name."""

        if live_query is None:
            live_query = {}
        else:
            live_query = json.loads(live_query)

        if start_time and end_time:
            live_query['time_interval'] = {
                "start_time": start_time,
                "end_time": end_time
            }

        resp, body = self.http_client.json_request(
            self._create_url(host_name, service_description, metric_name),
            'POST', body=live_query)

        return body

    def _create_url(self, host_name, service_description=None,
                    metric_name=None):
        url = self.base_url + '/' + host_name

        if service_description:
            url += '/services/' + service_description

        url += '/metrics'

        if metric_name:
            url += '/' + metric_name

        return url
