import os


def parse_para(filename):
    content = ""
    with open(filename, "r") as f:
        content = f.read()

    lang_idx = content.find("xml:lang=\"")
    sep = "\""
    if lang_idx == -1:
        lang_idx = content.find("xml:lang='")
        sep = "'"
    content = content[lang_idx+10:]
    end_idx = content.find(sep)
    lang = content[:end_idx]

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

    return { "para" : paragraphs, "lang" : lang }



