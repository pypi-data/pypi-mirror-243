project_name = "korexo_profile"

project = f"{project_name} documentation"
copyright = "2021-2022 DEW"
author = "DEW Water Science (Kent Inverarity)"

from pkg_resources import get_distribution

release = get_distribution(project_name).version
version = '.'.join(release.split('.')[:2])


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "nbsphinx",
]

templates_path = ["_templates"]

source_suffix = ".rst"
master_doc = "index"
language = None

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = None

import sphinx_rtd_theme

html_theme = "sphinx_rtd_theme"
extensions.append("sphinx_rtd_theme")

html_theme_options = {
    'globaltoc_collapse': False,
    'globaltoc_includehidden': False,
    'navigation_depth': 4,
}

html_context = {
    'display_github': False,
    'github_user': 'dew-waterscience',
    'github_repo': 'korexo_profile',
    'github_version': f'v{release}/' 
}

html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
}
intersphinx_cache_limit = 1

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

