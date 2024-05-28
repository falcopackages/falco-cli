import falco

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Falco"
copyright = "Copyright &copy; 2023, Tobi DEGNON"
author = "Tobi DEGNON"
version = falco.falco_version
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks",
    "myst_parser",
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
    "sphinx_design",
    "jupyter_sphinx",
    "sphinx_tabs.tabs",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "cappa.ext.docutils",
    "sphinx_github_changelog",
    "sphinxcontrib.mermaid",
    "sphinx_docsearch",
]
todo_include_todos = True
extlinks = {
    "pull": ("https://github.com/tobi-de/falco/pull/%s", "pull request #%s"),
    "issue": ("https://github.com/tobi-de/falco/issues/%s", "issue #%s"),
    "repo": ("https://github.com/tobi-de/falco", "github repository"),
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
    "source_user": "tobi-de",
    "source_repo": "falco",
}
html_theme_options = {
    "mastodon_url": "https://fosstodon.org/@tobide",
    "github_url": "https://github.com/tobi-de/falco",
    "twitter_url": "https://twitter.com/tobidegnon",
    "discussion_url": "https://github.com/tobi-de/falco/discussions",
    "accent_color": "sky",
    "globaltoc_expand_depth": 1,
}
html_logo = "images/logo_with_text.svg"
html_favicon = "../assets/falco-logo.svg"
html_css_files = [
    "custom.css",
]

html_js_files = [
    (
        "https://plausible.service.dotfm.me/js/script.js",
        {"defer": "", "data-domain": "falco.oluwatobi.dev"},
    ),
    "add-og-title-to-home.js",
]

# Jupyter sphinx configs
jupyter_sphinx_thebelab_config = {
    "requestKernel": True,
}
jupyter_sphinx_require_url = ""

# -- DocSearch configs -----------------------------------------------------
docsearch_app_id = "CJEHOB5X2Y"
docsearch_api_key = "e467f62765922e10749dec55f81a0a76"
docsearch_index_name = "falco"
