# Template-html-tools

Tools for manipulating HTML templates and creating PDFs.

# Dependencies

- Chromium browser (for PDF creation)
- 

# Usage

Produce a PDF file from an HTML template, content JSON file, and CSS styling.
```
python3 templated_html_tools.py PDF --content test/test_content.json --css test/test_style.css --resources test/resources test/test_template.html out.pdf
```

# Docker

A public docker image exists <a href="https://quay.io/repository/kelsey_anderson/html2pdf">here</a>. 

```
$ docker pull quay.io/kelsey_anderson/html2pdf:0.1
$ docker run quay.io/kelsey_anderson/html2pdf:0.1 --help
usage: HTML template tools [-h] {template,pdf} ...

Tools for manipulating HTML templates and creating PDFs

positional arguments:
  {template,pdf}  subcommand help
    template      Merge content with template
    pdf           Create PDF from HTML with template

options:
  -h, --help      show this help message and exit
```



