# coding: utf-8
{% if cookiecutter.django_api != "🥷 django_ninja" %}
import json
{% endif %}
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

{% if cookiecutter.django_api == "🥷 django_ninja" %}
from ninja import Router

from .schemas import List{{cookiecutter.model}}Schema, {{cookiecutter.model_singular}}Schema, {{cookiecutter.model_singular}}SchemaIn
{% else %}
from django.views.decorators.http import require_http_methods

from ..commons.django_views_utils import ajax_login_required
{% endif %}

from .service import {{cookiecutter.model_lower}}_svc

{% if cookiecutter.django_api == "🥷 django_ninja" %}

router = Router()
{% endif %}


{% if cookiecutter.django_api == "🥷 django_ninja" %}
@router.post("/{{cookiecutter.model_lower}}/add", response={% raw %}{201{% endraw %}: {{cookiecutter.model_singular}}Schema{% raw %}}{% endraw %})
@csrf_exempt
def add_{{cookiecutter.model_singular_lower}}(request, {{cookiecutter.model_singular_lower}}: {{cookiecutter.model_singular}}SchemaIn):
    new_{{cookiecutter.model_singular_lower}} = {{cookiecutter.model_lower}}_svc.add_{{cookiecutter.model_singular_lower}}({{cookiecutter.model_singular_lower}}.description)
{% else %}
@csrf_exempt
@ajax_login_required
def add_{{cookiecutter.model_singular_lower}}(request):
    body = json.loads(request.body)
    description = body.get("description")

    if not description:
        raise ValueError("body.{{cookiecutter.model_singular_lower}}.description: field required (value_error.missing)")
    if type(description) not in [str, int]:
        raise ValueError("body.{{cookiecutter.model_singular_lower}}.description: str type expected (type_error.str)")

    description = str(description)
    if len(description) <= 2:
        raise ValueError(
            "body.{{cookiecutter.model_singular_lower}}.description: It must be at least 3 characteres long. (value_error)"
        )

    new_{{cookiecutter.model_singular_lower}} = {{cookiecutter.model_lower}}_svc.add_{{cookiecutter.model_singular_lower}}(description)
{% endif %}
    return JsonResponse(new_{{cookiecutter.model_singular_lower}}, status=201)


{% if cookiecutter.django_api == "🥷 django_ninja" %}
@router.get("/{{cookiecutter.model_lower}}/list", response=List{{cookiecutter.model}}Schema)
{% else %}
@require_http_methods(["GET"])
@ajax_login_required
{% endif %}
def list_{{cookiecutter.model_lower}}(request):
    {{cookiecutter.model_lower}} = {{cookiecutter.model_lower}}_svc.list_{{cookiecutter.model_lower}}()
    return JsonResponse({"{{cookiecutter.model_lower}}": {{cookiecutter.model_lower}}})
