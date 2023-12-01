# Configuration file for the Sphinx documentation builder.
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html
# -- Setup root --------------------------------------------------------------
import os
import time

from ...dvttestkit import confluence_handler


def get_version():
    with open('version.txt', 'r') as f:
        current_version = f.read().strip()
    return current_version


project = 'dvtTestKit'
author = 'Dan Edens'
release = get_version()

master_doc = 'DvtKit_index'
todo_include_todos = False
# pygments_style = 'classic'
source_suffix = {'.rst': 'restructuredtext'}
exclude_patterns = ['build/*']
html_theme = "classic"
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.coverage',
        'sphinxcontrib.confluencebuilder',
        'sphinx.ext.napoleon',
        'sphinx.ext.viewcode',
        ]

confluence_default_alignment = 'center'
# confluence_header_file = 'assets/header.tpl'
# confluence_footer_file = 'assets/footer.tpl'
# confluence_disable_ssl_validation = False
confluence_publish_debug = True

confluence_publish_onlynew = True


# confluence_publish_denylist = [
#     'index',
#     'foo/bar',
# ]

def generate_sphinx_config(theme='alabaster', pdf=False):
    """
    Generates a Sphinx configuration dictionary with the given theme.

    Args:
        theme (str): The name of the theme to use for HTML and HTML Help pages.
            Defaults to 'alabaster'.
        pdf (bool): Whether to generate settings for PDF output. Defaults to False.

    Returns:
        A dictionary containing the Sphinx configuration.
    """
    config = {
            'htmlhelp_basename':    'DVT Test Kit',
            'html_theme':           theme,
            'html_static_path':     [],
            'html_show_sourcelink': False,
            'html_show_sphinx':     False,
            'html_show_copyright':  False
            }

    if pdf:
        config['latex_engine'] = 'xelatex'
        config['latex_elements'] = {
                'papersize':    'letterpaper',
                'pointsize':    '10pt',
                'classoptions': ',oneside',
                'babel':        '\\usepackage[english]{babel}',
                'fontpkg':      '\\usepackage{fontspec}',
                'fncychap':     '\\usepackage[Bjornstrup]{fncychap}',
                'preamble':     '\\usepackage{unicode-math}\n\\setmathfont{XITS Math}\n\\setmainfont{XITS}\n'
                }

    return config


def publish_dvttestkit_to_confluence(pages):
    for file_name, page_id in pages:
        # print(file_name, page_id)
        confluence_handler.update_confluence_page(
                conf_file_path=file_name,
                page_id=page_id
                )


if __name__ == '__main__':
    docs_dir = os.path.abspath('docs')
    confluence_command = os.path.join(docs_dir, 'make confluence')

    # Run the "make confluence" command
    os.system(confluence_command)

    time.sleep(5)
    pages = []
    for each in (confluence_handler.get_child_page_ids("2751201315")):
        # print(confluence_handler.get_confluence_page_title(each))
        pages.append(
                (confluence_handler.get_confluence_page_title(each), each))
    print(f"pre-publish_dvttestkit: {pages}")
    publish_dvttestkit_to_confluence(pages)
