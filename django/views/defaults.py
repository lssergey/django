import warnings

from django import http
from django.template import (Context, RequestContext,
                             loader, Template, TemplateDoesNotExist)
from django.views.decorators.csrf import requires_csrf_token


# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def page_not_found(request, template_name='404.html'):
    """
    Default 404 handler.

    Templates: :template:`404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        template = Template(
            '<h1>Not Found</h1>'
            '<p>The requested URL {{ request_path }} was not found on this server.</p>')
    return http.HttpResponseNotFound(template.render(RequestContext(request, {'request_path': request.path})))


@requires_csrf_token
def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: :template:`500.html`
    Context: None
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>')
    return http.HttpResponseServerError(template.render(Context({})))


# This can be called when CsrfViewMiddleware.process_view has not run,
# therefore need @requires_csrf_token in case the template needs
# {% csrf_token %}.
@requires_csrf_token
def permission_denied(request, template_name='403.html'):
    """
    Permission denied (403) handler.

    Templates: :template:`403.html`
    Context: None

    If the template does not exist, an Http403 response containing the text
    "403 Forbidden" (as per RFC 2616) will be returned.
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return http.HttpResponseForbidden('<h1>403 Forbidden</h1>')
    return http.HttpResponseForbidden(template.render(RequestContext(request)))


def shortcut(request, content_type_id, object_id):
    warnings.warn(
        "django.views.defaults.shortcut will be removed in Django 1.8. "
        "Import it from django.contrib.contenttypes.views instead.",
        PendingDeprecationWarning, stacklevel=2)
    from django.contrib.contenttypes.views import shortcut as real_shortcut
    return real_shortcut(request, content_type_id, object_id)
