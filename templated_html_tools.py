import argparse
from functools import reduce
import json
import subprocess
import tempfile
import shlex
import shutil
import os


def collate_content(content):
    return reduce(
        lambda a, b: a | b,
        (json.load(open(i)) for i in (content or [])),
        dict()
    )


def dereference_template(template, content):
    html = template.format(**content)
    return html


def make_css_snippet(css_files):
    return "\n".join(
        [
            f"""<style class="{os.path.basename(i)}">
            {open(i).read()}
            </style>"""
            for i in (css_files or [])
        ]
    )


def apply_template(template, content, css_files):
    template = open(template).read()
    body = dereference_template(template, content)
    css = make_css_snippet(css_files)
    return f"""
    <html>
    <head>
    <title>Doc</title>
    {css}
    </head>
    <body>
    {body}
    </body>
    </html>
    """


def do_template(template, content_json_files, css_files, out_filename,
                resources_dir):
    content = collate_content(content_json_files)
    v = apply_template(template, content, css_files)
    if out_filename:
        if resources_dir:
            d = os.path.dirname(out_filename)
            shutil.copytree(
                resources_dir,
                os.path.join(
                    d,
                    os.path.basename(
                        resources_dir
                    )
                )
            )
        open(out_filename, "w").write(v)

    return v


def template_command(args):
    print(
        do_template(
            args.template,
            args.content,
            args.css,
            args.out,
            args.resources
        )
    )


def pdf_command(args):
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as fd:
        out_html = os.path.join(fd, "out.html")
        do_template(
            args.template,
            args.content,
            args.css,
            out_html,
            args.resources
        )
        s = shlex.split(
            f"""chromium --no-sandbox --headless --print-to-pdf='{args.out}' {out_html}"""
        )
        r = subprocess.run(s)
        print(r)
    
    # open("foo.html", "wt").write(v)
    # s = shlex.split(
    #     f"""chromium --headless --print-to-pdf='{args.out}' foo.html"""
    # )
    # r = subprocess.run(s)
    # print(r)
    # with tempfile.NamedTemporaryFile(
    #         mode="wt",
    #         dir=os.getcwd(),
    #         suffix=".html"
    # ) as ftemp:
    #     ftemp.write(v)
    #     ftemp.flush()
    #     # chromium --headless --print-to-pdf="another.pdf" test.html
    #     s = shlex.split(
    #         f"""chromium --no-sandbox --headless --print-to-pdf='{args.out}' {ftemp.name}"""
    #     )
    #     r = subprocess.run(s)
    #     print(r)


def main():
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help',
    )
    subparsers = parser.add_subparsers(help='subcommand help', required=True)
    parser_template = subparsers.add_parser(
        'template',
        help='Merge content with template'
    )
    parser_template.add_argument(
        "template",
        type=str,
        help="Template HTML body file path",
    )
    parser_template.add_argument(
        "--content",
        type=str,
        help="Template content JSON file path",
        action="append",
    )
    parser_template.add_argument(
        "--css",
        type=str,
        help="Style CSS file path",
        action="append",
    )
    parser_template.add_argument(
        "--out",
        "-o",
        type=str,
        help="Output file path",
        default=None,
    )
    parser_template.add_argument(
        "--resources",
        "-r",
        type=str,
        help="Folder containing resources to copy to output folder",
        default=None,
    )
    parser_template.set_defaults(func=template_command)

    parser_pdf = subparsers.add_parser(
        'pdf',
        help='Create PDF from HTML with template'
    )
    parser_pdf.add_argument(
        "template",
        type=str,
        help="Template HTML body file path",
    )
    parser_pdf.add_argument(
        "out",
        type=str,
        help="PDF output file path",
    )
    parser_pdf.add_argument(
        "--content",
        type=str,
        help="Template content JSON file path",
        action="append",
    )
    parser_pdf.add_argument(
        "--css",
        type=str,
        help="Style CSS file path",
        action="append",
    )
    parser_pdf.add_argument(
        "--resources",
        "-r",
        type=str,
        help="Folder containing resources to copy to output folder",
        default=None,
    )
    parser_pdf.set_defaults(func=pdf_command)

    args = parser.parse_args()
    print(args)
    if "func" in args:
        args.func(args)


if __name__ == "__main__":
    main()
