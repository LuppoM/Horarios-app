import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # para que Sphinx encuentre tu código

# Idioma
language = 'es'

# Extensiones recomendadas
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # para docstrings estilo Google/NumPy
    'sphinx.ext.viewcode',
]

# Tema bonito
html_theme = 'sphinx_rtd_theme'
