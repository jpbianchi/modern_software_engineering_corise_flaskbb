# -*- coding: utf-8 -*-
"""
    flaskbb.fixtures.groups
    ~~~~~~~~~~~~~~~~~~~~~~~

    The fixtures module for our groups.

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from collections import OrderedDict


fixture = OrderedDict((
    ('Administrator', {
            'id': 1,
        'description': 'The Administrator Group',
        'admin': True,
        'super_mod': False,
        'mod': False,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': True,
        'deletetopic': True,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': True,
        'mod_banuser': True,
        'viewhidden': True,
        'makehidden': True,
    }),
    ('Super Moderator', {
            'id': 2,
        'description': 'The Super Moderator Group',
        'admin': False,
        'super_mod': True,
        'mod': False,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': True,
        'deletetopic': True,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': True,
        'mod_banuser': True,
        'viewhidden': True,
        'makehidden': True,
    }),
    ('Moderator', {
            'id': 3,
        'description': 'The Moderator Group',
        'admin': False,
        'super_mod': False,
        'mod': True,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': True,
        'deletetopic': True,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': True,
        'mod_banuser': True,
        'viewhidden': True,
        'makehidden': False,
    }),
    ('Member', {
            'id': 4,
        'description': 'The Member Group',
        'admin': False,
        'super_mod': False,
        'mod': False,
        'banned': False,
        'guest': False,
        'editpost': True,
        'deletepost': False,
        'deletetopic': False,
        'posttopic': True,
        'postreply': True,
        'mod_edituser': False,
        'mod_banuser': False,
        'viewhidden': False,
        'makehidden': False,
    }),
    ('Banned', {
            'id': 5,
        'description': 'The Banned Group',
        'admin': False,
        'super_mod': False,
        'mod': False,
        'banned': True,
        'guest': False,
        'editpost': False,
        'deletepost': False,
        'deletetopic': False,
        'posttopic': False,
        'postreply': False,
        'mod_edituser': False,
        'mod_banuser': False,
        'viewhidden': False,
        'makehidden': False,
    }),
    ('Guest', {
            'id': 6,
        'description': 'The Guest Group',
        'admin': False,
        'super_mod': False,
        'mod': False,
        'banned': False,
        'guest': True,
        'editpost': False,
        'deletepost': False,
        'deletetopic': False,
        'posttopic': False,
        'postreply': False,
        'mod_edituser': False,
        'mod_banuser': False,
        'viewhidden': False,
        'makehidden': False
    })
))

def default_group_ids():
    ids = []
    for key, value in fixture.items():
        ids.append(getattr(value,'id'))
    return set(ids)