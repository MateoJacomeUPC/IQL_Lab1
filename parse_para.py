import os


def parse_para(filename):
    content = ""
    with open(filename, "r") as f:
        content = f.read()

    paragraphs = ""
    start_idx = content.find("<para>")
    while start_idx != -1:
        end_idx = content.find("</para>")
        if start_idx > end_idx:
            return

        para = content[start_idx+6:end_idx]
        paragraphs += para + " "
        content = content[end_idx+7:]

        start_idx = content.find("<para>")

    return paragraphs
