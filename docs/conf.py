from importlib.metadata import version as get_version

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import django

import os, sys
os.environ["DJANGO_SETTINGS_MODULE"] = "demo.demo.settings"
sys.path.insert(0, os.path.abspath('..'))
from django.conf import settings
settings.configure(INSTALLED_APPS = ["falco"])
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Falco"
copyright = "Copyright &copy; 2023, Tobi DEGNON"
author = "Tobi DEGNON"
version = get_version("falco-app")
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks",
    "myst_parser",
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
    "sphinx_design",
    "sphinx_tabs.tabs",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",
    # "sphinx_docsearch",
    "sphinx_exec_code",
]
todo_include_todos = True
extlinks = {
    "pull": ("https://github.com/falcopackages/falco-app/pull/%s", "pull request #%s"),
    "issue": ("https://github.com/falcopackages/falco-app/issues/%s", "issue #%s"),
    "repo": ("https://github.com/falcopackages/falco-app", "github repository"),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"
html_static_path = ["_static"]
html_baseurl = "https://falco.oluwatobi.dev"
html_title = "Falco"

# -- Shibuya theme options ---------------------------------------------------
html_context = {
    "source_type": "github",
    "source_user": "falcopackages",
    "source_repo": "falco-app",
}
html_theme_options = {
    "mastodon_url": "https://fosstodon.org/@tobide",
    "github_url": "https://github.com/falcopackages/falco-app",
    "twitter_url": "https://twitter.com/tobidegnon",
    "discussion_url": "https://github.com/falcopackages/falco-app/discussions",
    "accent_color": "blue",
    "globaltoc_expand_depth": 1,
}
html_logo = "https://raw.githubusercontent.com/falcopackages/website/refs/heads/main/_static/logo_with_text.svg"
html_favicon = "https://raw.githubusercohtml_logontent.com/falcopackages/website/refs/heads/main/_static/falco-logo.svg"

# html_sidebars = {
#     "**": [
#         "sidebars/localtoc.html",
#         "sidebars/repo-stats.html",
#         "sidebars/edit-this-page.html",
#         "sidebars/consulting.html",
#         # "sidebars/buy-me-a-coffee.html",
#     ]
# }

# html_js_files = [
#     (
#         "https://plausible.service.dotfm.me/js/script.js",
#         {"defer": "", "data-domain": "falco.oluwatobi.dev"},
#     ),
#     "add-og-title-to-home.js",
#     (
#         "https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js",
#         {
#             "data-name": "BMC-Widget",
#             "data-cfasync": "false",
#             "data-id": "oluwa.tobi",
#             "data-description": "Support me on Buy me a coffee!",
#             "data-message": "",
#             "data-color": "#5F7FFF",
#             "data-position": "Right",
#             "data-x_margin": "18",
#             "data-y_margin": "18",
#         },
#     ),
# ]
#
# # Jupyter sphinx configs
# jupyter_sphinx_thebelab_config = {
#     "requestKernel": True,
# }
# jupyter_sphinx_require_url = ""

# -- DocSearch configs -----------------------------------------------------
# docsearch_app_id = "CJEHOB5X2Y"
# docsearch_api_key = "e467f62765922e10749dec55f81a0a76"
# docsearch_index_name = "falco"
