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

A public docker image exists <a href="">here</a>. 

```
docker run image PDF --content test/test_content.json --css test/test_style.css --resources test/resources test/test_template.html out.pdf
```



