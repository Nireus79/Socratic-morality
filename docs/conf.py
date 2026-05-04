"""Sphinx configuration for socratic-morality."""
project = 'Socratic Morality'
copyright = '2026, Anthropic'
author = 'Anthropic'
release = '1.0.0-alpha'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_member_order = 'bysource'
