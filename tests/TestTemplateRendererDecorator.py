import unittest

from mock import mock

from decorators import template_renderer


class TestTemplateRendererDecorator(unittest.TestCase):
    def test_template_renderer_with_template_and_status_returns_a_rendered_template_and_status(self):
        status = 1337
        template = 'foo.bar.html'
        initial_context = {'foo': 'bar', 'baz': 'foobar'}
        expected_template = "<h1>Foo bar baz</h1>"
        full_context = dict(initial_context)
        full_context['applicationName'] = 'CCExtractor CI platform'
        full_context['applicationVersion'] = 'Unknown'
        full_context['currentYear'] = "YYYY"
        full_context['build_commit'] = "Unknown"
        full_context['user'] = None
        full_context['menu'] = {}
        full_context['active_route'] = "route.foo.bar"

        # TODO: swithc to http://pythonhosted.org/Flask-Testing/ to complete this test
        with mock.patch('flask.request') as mock_request:
            with mock.patch('flask.g') as mock_g:
                with mock.patch('flask.render_template') as mock_render:
                    mock_g.version.return_value = 'Unknown'

                    @template_renderer(template, status)
                    def wrapped():
                        return initial_context

                    rendered_template, status_code = wrapped()

                    mock_render.assert_called_once_with(template, **full_context)

                    self.assertEqual(expected_template, rendered_template)
                    self.assertEqual(status, status_code)
