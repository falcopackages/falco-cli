from functools import wraps

from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string


def for_htmx(
    *,
    if_hx_target: str | None = None,
    use_template: str | None = None,
    use_partial: str | list[str] | None = None,
    use_partial_from_params: bool = False,
):
    """
    Adapted from https://github.com/spookylukey/django-htmx-patterns/blob/master/code/htmx_patterns/utils.py
    If the request is from htmx, then render a partial page, using either:
    - the template specified in `use_template` param
    - the partial/partials specified in `use_partial` param
    - the partial/partials specified in GET/POST parameter "use_partial", if `use_partial_from_params=True` is passed

    If the optional `if_hx_target` parameter is supplied, the
    hx-target header must match the supplied value as well in order
    for this decorator to be applied.
    """
    if len([p for p in [use_partial, use_template, use_partial_from_params] if p]) != 1:
        msg = "You must pass exactly one of 'use_template', 'use_partial' or 'use_partial_from_params=True'"
        raise ValueError(msg)

    def decorator(view):
        @wraps(view)
        def _view(request: HttpRequest, *args, **kwargs):
            resp = view(request, *args, **kwargs)

            if not request.htmx:
                return resp

            apply_decorator = if_hx_target is None or request.headers.get("Hx-Target", None) == if_hx_target
            if not apply_decorator:
                return resp

            partials_to_use = use_partial
            if not hasattr(resp, "render"):
                if not resp.content and any(
                    h in resp.headers
                    for h in (
                        "Hx-Trigger",
                        "Hx-Trigger-After-Swap",
                        "Hx-Trigger-After-Settle",
                        "Hx-Redirect",
                    )
                ):
                    # This is a special case response, it doesn't need modifying:
                    return resp

                msg = "Cannot modify a response that isn't a TemplateResponse"
                raise ValueError(msg)
            if resp.is_rendered:
                msg = "Cannot modify a response that has already been rendered"
                raise ValueError(msg)

            if use_partial_from_params:
                use_partial_from_params_val = _get_param_from_request(request, "use_partial")
                if use_partial_from_params_val is not None:
                    partials_to_use = use_partial_from_params_val

            if use_template is not None:
                resp.template_name = use_template
            elif partials_to_use is not None:
                if not isinstance(partials_to_use, list):
                    partials_to_use = [partials_to_use]

                rendered_partials = [
                    render_to_string(
                        f"{resp.template_name}#{b}",
                        context=resp.context_data,
                        request=request,
                    )
                    for b in partials_to_use
                ]
                # Create new simple HttpResponse as replacement
                resp = HttpResponse(
                    content="".join(rendered_partials),
                    status=resp.status_code,
                    headers=resp.headers,
                )

            return resp

        return _view

    return decorator


def _get_param_from_request(request, param):
    """
    Checks GET then POST params for specified param
    """
    if param in request.GET:
        return request.GET.getlist(param)
    if request.method == "POST" and param in request.POST:
        return request.POST.getlist(param)
    return None
