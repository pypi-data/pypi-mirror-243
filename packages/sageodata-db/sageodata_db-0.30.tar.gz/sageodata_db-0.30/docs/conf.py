project_name = "sageodata_db"

project = f"{project_name} documentation"
copyright = "2019-20 DEW"
author = "Kent Inverarity"

from pkg_resources import get_distribution

release = get_distribution(project_name).version
version = ".".join(release.split(".")[:2])

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
]

templates_path = ["_templates"]

source_suffix = ".rst"
master_doc = "index"

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = None

html_theme = "sphinx_rtd_theme"

html_theme_options = {
}

html_context = {
    "github_user": "dew-waterscience",
    "github_repo": project_name,
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]


html_sidebars = {
    # "**": ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]
    # "**": ["search-field", "sidebar-nav-bs",]
    "**": [
        "search-field",
        "navbar-nav",
        "parent_links",
    ]
}


intersphinx_mapping = {
    "python": ("http://docs.python.org/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "cx_Oracle": ("https://cx-oracle.readthedocs.io/en/latest/", None),
    "sa_gwdata": ("https://python-sa-gwdata.readthedocs.io/en/latest/", None),
    # "sageodata_db": (
    #     "file:///P:/projects_gw/State/Groundwater_Toolbox/Python/wheels/docs/sageodata_db/latest_source",
    #     "sageodata_db.objects.inv",
    # ),
    "dew_gwdata": (
        "file:///P:/projects_gw/State/Groundwater_Toolbox/Python/wheels/docs/dew_gwdata/latest_source",
        "dew_gwdata.objects.inv",
    ),
    "wrap_technote": (
        "file:///P:/projects_gw/State/Groundwater_Toolbox/Python/wheels/docs/wrap_technote/latest_source",
        "wrap_technote.objects.inv",
    ),
    "waterkennect": (
        "file:///P:/projects_gw/State/Groundwater_Toolbox/Python/wheels/docs/waterkennect/latest_source",
        "waterkennect.objects.inv",
    ),
}
intersphinx_cache_limit = 1

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


def setup(app):
    app.add_css_file("custom.css")

