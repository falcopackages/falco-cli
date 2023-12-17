from django.forms import  ModelForm

from .models import {{model_name_cap}}

class {{model_name_cap}}Form(ModelForm):
    class Meta:
        model = {{model_name_cap}}
        fields = (
        {% for item in fields_names %}
            {% if not forloop.first %}, {% endif %}"{{ item }}"
        {% endfor %}
        )
