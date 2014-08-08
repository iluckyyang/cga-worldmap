#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

from django.conf import settings
from geonode.search.util import iso_fmt

from datetime import datetime

def add_bbox_query(q, bbox):
    '''modify the queryset q to limit to the provided bbox

    bbox - 4 tuple of floats representing x0,x1,y0,y1
    returns the modified query
    '''
    bbox = map(str, bbox) # 2.6 compat - float to decimal conversion
    q = q.filter(bbox_x0__gte=bbox[0])
    q = q.filter(bbox_x1__lte=bbox[1])
    q = q.filter(bbox_y0__gte=bbox[2])
    return q.filter(bbox_y1__lte=bbox[3])

def filter_by_period(model, q, start, end, user=None):
    '''modify the query to filter the given model for dates between start and end
    start, end - iso str ('-5000-01-01T12:00:00Z')
    '''

    parse = lambda v: datetime.strptime(v, iso_fmt)
    if not user:
        if start:
            q = q.filter(date__gte = parse(start))
        if end:
            q = q.filter(date__lte = parse(end))
    else:
        # @todo handle map and/or users - either directly if implemented or ...
        # this will effectively short-circuit the query at this point
        q = q.none()
    return q

def filter_by_extent(model, q, extent, user=None):
    '''modify the query to filter the given model for the provided extent and optional user
    extent: tuple of float coordinates representing x0,x1,y0,y1
    '''
    if not user:
        q = add_bbox_query(q, extent)
    else:
        # @todo handle map and/or users - either directly if implemented or ...
        # this will effectively short-circuit the query at this point
        q = q.none()
    return q

using_geodjango = False