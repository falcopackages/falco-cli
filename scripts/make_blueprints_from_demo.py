from pathlib import Path

root_dir = Path(__file__).parent.parent
products_app_dir = root_dir / "demo" / "products"
falco_crud_blueprints_dir = root_dir / "src" / "falco_blueprints" / "crud"

python_blueprints = ("views.py", "forms.py")
python_variables_mapping = {
    "products:": "{{app_label}}:",
    "products": "{{model_name|lower}}s",
    "product": "{{model_name|lower}}",
    "Product": "{{model_name}}",
    "Products": "{{model_name}}s",
    'fields = ("id", "name", "description", "price", "sku", "created_at")': """fields = (
        {% for item in model_fields %}
            {% if not forloop.first %}, {% endif %}"{{ item }}"
        {% endfor %}
        )""",
}


def copy_python_files():
    for blueprint in python_blueprints:
        content = (products_app_dir / blueprint).read_text()
        for key, value in python_variables_mapping.items():
            content = content.replace(key, value)
        dest = falco_crud_blueprints_dir / f"{blueprint}.bp"
        dest.write_text(content)


def copuy_html_files():
    pass


def main():
    copy_python_files()


if __name__ == "__main__":
    main()
