# HTML to Jupyter Notebook Converter

This Python script converts HTML exports of Jupyter notebooks back into `.ipynb` files.

Made by Andrew Smith

## Features

- Converts HTML exports to Jupyter Notebook (.ipynb) format
- Preserves code and markdown cell structure
- Converts HTML elements in markdown cells to Markdown syntax:
- Command-line interface

## Requirements

- Python 3.6+
- BeautifulSoup4 library

Install the required library using pip:

```
pip install beautifulsoup4
```

## Usage

Run the script from the command line:

```
python3 convert-nb.py input.html [-o output.ipynb]
```

Arguments:

- `input.html`: Path to the input HTML file (required)
- `-o output.ipynb` or `--output output.ipynb`: Path to the output .ipynb file (optional, defaults to 'output.ipynb')

Example:

```
python3 convert-nb.py my_notebook.html -o converted_notebook.ipynb
```

## Limitations

- Conversion of complex features like LaTex or images may not be perfect
- Cell outputs are not preserved; you'll need to run the notebook to regenerate outputs
