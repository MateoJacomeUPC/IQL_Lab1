import os

def parse_all(xml_dir):
    all_files = os.listdir(xml_dir)
    all_info = {}
    for f in all_files:
        xml_file = os.path.join(xml_dir, f)
        if not os.path.isfile(xml_file):
            continue
        if xml_file[-4:] != ".xml":
            continue
        if xml_file.find("index.xml") != -1:
            continue

        print(xml_file)
        info = parse_para(xml_file)
        if info["lang"] in all_info:
            # Do we discard it, replace it
            # or append it?
            print("duplicate of %s" % (info["lang"]))
            continue

        all_info[info["lang"]] = info

    return all_info


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



