import falco

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Falco"
copyright = "2023, Tobi DEGNON"
author = "Tobi DEGNON"
version = falco.falco_version
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_tabs.tabs",
    "sphinx_copybutton",
    "sphinx_togglebutton",
    "sphinx_autorun",
]

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
}
html_logo = "images/logo.svg"
