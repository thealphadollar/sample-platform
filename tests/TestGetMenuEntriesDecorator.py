import unittest

from decorators import get_menu_entries
from mod_auth.models import User, Role


class TestGetMenuEntriesDecorator(unittest.TestCase):
    def test_get_menu_entries_for_user_with_route_that_is_public(self):
        user = User('foo')
        title = 'bar'
        icon = 'baz'
        route = 'foo/bar'
        expected = {
            'title': title,
            'icon': icon,
            'route': route
        }

        actual = get_menu_entries(user, title, icon, route=route)

        self.assertDictEqual(expected, actual)

    def test_get_menu_entries_for_user_with_route_that_is_restricted(self):
        user = User('foo')
        title = 'bar'
        icon = 'baz'
        route = 'foo/bar'
        expected = {
            'title': title,
            'icon': icon,
            'route': route
        }

        actual = get_menu_entries(user, title, icon, [Role.user], route)

        self.assertDictEqual(expected, actual)

    def test_get_menu_entries_for_user_with_route_that_is_restricted_and_unacessible(self):
        user = User('foo')
        title = 'bar'
        icon = 'baz'
        route = 'foo/bar'
        expected = {}

        actual = get_menu_entries(user, title, icon, [Role.admin], route)

        self.assertDictEqual(expected, actual)

    def test_get_menu_entries_for_user_with_no_access_to_any_sub_entry(self):
        expected = {}
        user = User('foo')

        actual = get_menu_entries(user, 'bar', 'baz', [Role.admin], all_entries=[
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]},
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]},
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]}
        ])

        self.assertDictEqual(expected, actual)

    def test_get_menu_entries_for_user_with_access_to_some_sub_entries(self):
        user = User('foo')
        title = 'bar'
        icon = 'baz'
        expected = {
            'title': title,
            'icon': icon,
            'entries': [
                {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.user]},
                {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': []}
            ]
        }

        actual = get_menu_entries(user, title, icon, [Role.user], all_entries=[
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]},
            expected['entries'][0],
            expected['entries'][1]
        ])

        self.assertDictEqual(expected, actual)

    def test_get_menu_entries_for_no_user_and_not_public_should_return_empty(self):
        self.assertDictEqual({}, get_menu_entries(None, 'foo', 'bar', [Role.admin]))

    def test_get_menu_entries_for_no_user_that_is_public_should_return_the_entry(self):
        title = 'bar'
        icon = 'baz'
        route = 'foo/bar'
        expected = {
            'title': title,
            'icon': icon,
            'route': route
        }

        actual = get_menu_entries(None, title, icon, route=route)

        self.assertDictEqual(expected, actual)
        
    def test_get_menu_entries_for_no_user_with_private_sub_entries(self):
        expected = {}

        actual = get_menu_entries(None, 'bar', 'baz', all_entries=[
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]},
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]},
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]}
        ])

        self.assertDictEqual(expected, actual)

    def test_get_menu_entries_for_no_user_with_access_to_some_sub_entries(self):
        title = 'bar'
        icon = 'baz'
        expected = {
            'title': title,
            'icon': icon,
            'entries': [
                {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': []}
            ]
        }

        actual = get_menu_entries(None, title, icon, all_entries=[
            {'title': 'foo', 'icon': 'bar', 'route': 'baz', 'access': [Role.admin]},
            expected['entries'][0]
        ])

        self.assertDictEqual(expected, actual)
