#!/usr/bin/env python

import json
import argparse
from bs4 import BeautifulSoup
import re

def html_to_markdown(element):
    """
    Convert HTML elements into the matching markdown hypertext.
    """
    if element.name is None:
        return element.string
    elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(element.name[1])
        return '#' * level + ' ' + element.get_text().strip() + '\n\n'
    elif element.name == 'p':
        return element.get_text().strip() + '\n\n'
    elif element.name == 'a':
        return f"[{element.get_text()}]({element.get('href')})"
    elif element.name in ['strong', 'b']:
        return f"**{element.get_text()}**"
    elif element.name in ['em', 'i']:
        return f"*{element.get_text()}*"
    elif element.name == 'code':
        return f"`{element.get_text()}`"
    elif element.name in ['ul', 'ol']:
        items = []
        for li in element.find_all('li', recursive=False):
            prefix = '- ' if element.name == 'ul' else '1. '
            items.append(prefix + ' '.join(html_to_markdown(child) for child in li.children))
        return '\n'.join(items) + '\n\n'
    else:
        return ' '.join(html_to_markdown(child) for child in element.children)


def clean_text(text):
    # Remove the ¶ symbol
    text = re.sub(r'¶', '\n\n', text)
    return text.strip()


def html_to_ipynb(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    notebook = {
        "cells": [],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 4
    }

    cells = soup.find_all('div', class_='jp-Cell')

    # Check each cell type based on css class and parse appropriately.
    for cell in cells:
        if 'jp-CodeCell' in cell['class']:
            source = cell.find('div', class_='highlight').get_text()
            notebook['cells'].append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": clean_text(source).split('\n')
            })
        elif 'jp-MarkdownCell' in cell['class']:
            markdown_content = cell.find('div', class_='jp-RenderedMarkdown')
            source = ''.join(html_to_markdown(child) for child in markdown_content.children)
            notebook['cells'].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": clean_text(source).split('\n')
            })

    return json.dumps(notebook, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Convert HTML to Jupyter Notebook')
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('-o', '--output', help='Output ipynb file', default='output.ipynb')

    args = parser.parse_args()

    # Read the HTML file
    with open(args.input, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Convert to .ipynb format
    ipynb_content = html_to_ipynb(html_content)

    # Write to .ipynb file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(ipynb_content)
    
    print(f"Conversion complete. Notebook saved as {args.output}")

if __name__ == "__main__":
    main()