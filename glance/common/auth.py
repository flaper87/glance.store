# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from glance.common import exception


LOG = logging.getLogger(__name__)


def get_endpoint(service_catalog, service_type='image', endpoint_region=None,
                 endpoint_type='publicURL'):
    """
    Select an endpoint from the service catalog

    We search the full service catalog for services
    matching both type and region. If the client
    supplied no region then any 'image' endpoint
    is considered a match. There must be one -- and
    only one -- successful match in the catalog,
    otherwise we will raise an exception.
    """
    endpoint = None
    for service in service_catalog:
        s_type = None
        try:
            s_type = service['type']
        except KeyError:
            msg = _('Encountered service with no "type": %s') % s_type
            LOG.warn(msg)
            continue

        if s_type == service_type:
            for ep in service['endpoints']:
                if endpoint_region is None or endpoint_region == ep['region']:
                    if endpoint is not None:
                        # This is a second match, abort
                        raise exception.RegionAmbiguity(region=endpoint_region)
                    endpoint = ep
    if endpoint and endpoint.get(endpoint_type):
        return endpoint[endpoint_type]
    else:
        raise exception.NoServiceEndpoint()
