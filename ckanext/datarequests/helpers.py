# -*- coding: utf-8 -*-

# Copyright (c) 2015 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of CKAN Data Requests Extension.

# CKAN Data Requests Extension is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CKAN Data Requests Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with CKAN Data Requests Extension. If not, see <http://www.gnu.org/licenses/>.

import ckan.model as model
import ckan.plugins.toolkit as tk
from ckanext.datarequests import db

from ckan.common import c


def get_comments_number(datarequest_id):
    # DB should be intialized
    db.init_db(model)
    return db.Comment.get_comment_datarequests_number(datarequest_id=datarequest_id)


def get_comments_badge(datarequest_id):
    return tk.render_snippet('datarequests/snippets/badge.html',
                             {'comments_count': get_comments_number(datarequest_id)})


def get_open_datarequests_number():
    # DB should be initialized
    db.init_db(model)
    return db.DataRequest.get_open_datarequests_number()


def is_following_datarequest(datarequest_id):
    # DB should be intialized
    db.init_db(model)
    return len(db.DataRequestFollower.get(datarequest_id=datarequest_id, user_id=c.userobj.id)) > 0


def get_open_datarequests_badge(show_badge):
    '''The snippet is only returned when show_badge == True'''
    if show_badge:
        return tk.render_snippet('datarequests/snippets/badge.html',
                                 {'comments_count': get_open_datarequests_number()})
    else:
        return ''


def datarequest_url_for(action, **kwargs):
    '''Helper function to generate URLs for datarequest actions with proper fallback'''
    from ckanext.datarequests import constants
    import ckan.lib.helpers as h
    
    # Map actions to direct paths to avoid routing issues
    action_paths = {
        'index': '/' + constants.DATAREQUESTS_MAIN_PATH,
        'show': '/' + constants.DATAREQUESTS_MAIN_PATH + '/' + kwargs.get('id', ''),
        'comment': '/' + constants.DATAREQUESTS_MAIN_PATH + '/comment/' + kwargs.get('id', ''),
        'new': '/' + constants.DATAREQUESTS_MAIN_PATH + '/new',
        'update': '/' + constants.DATAREQUESTS_MAIN_PATH + '/edit/' + kwargs.get('id', ''),
        'delete': '/' + constants.DATAREQUESTS_MAIN_PATH + '/delete/' + kwargs.get('id', ''),
        'close': '/' + constants.DATAREQUESTS_MAIN_PATH + '/close/' + kwargs.get('id', ''),
        'follow': '/' + constants.DATAREQUESTS_MAIN_PATH + '/follow/' + kwargs.get('id', ''),
        'unfollow': '/' + constants.DATAREQUESTS_MAIN_PATH + '/unfollow/' + kwargs.get('id', ''),
        'delete_comment': '/' + constants.DATAREQUESTS_MAIN_PATH + '/comment/' + kwargs.get('datarequest_id', '') + '/delete/' + kwargs.get('comment_id', ''),
    }
    
    try:
        # Try Flask-style Blueprint routing first
        endpoint = 'datarequests.' + action
        return h.url_for(endpoint, **kwargs)
    except Exception:
        # Use direct path construction as fallback
        if action in action_paths:
            # Handle special parameters for some actions
            url = action_paths[action]
            
            # Add query parameters if any (like organization for new action)
            query_params = []
            for key, value in kwargs.items():
                if key not in ['id', 'datarequest_id', 'comment_id'] and value:
                    query_params.append(f"{key}={value}")
            
            if query_params:
                url += '?' + '&'.join(query_params)
                
            return url
        else:
            # Generic path construction for unknown actions
            path = '/' + constants.DATAREQUESTS_MAIN_PATH
            if 'id' in kwargs:
                path += '/' + action + '/' + kwargs['id']
            else:
                path += '/' + action
            return path
