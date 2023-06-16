import hashlib
import re

from airium import Airium

LINK_REGEX = '\\[(.+)\\]\\((.+)\\)'
MAX_REPLACEMENTS = 12

# Requirements:
# - Words generally listed in order of more common to less common frequency in usage
# - Words are not repeated

a = Airium()
words = []
parts = set()
corpus = []


def write_table(table_data_fn, l1_header_fn, l2_header_fn, l3_header_fn):
    with a.table():
        with a.thead(style='visibility: collapse;'):
            with a.tr():
                with a.th(klass='palabra'):
                    a('Palabra')
                with a.th(klass='part'):
                    a('Part of Speech')
                with a.th(klass='definitions'):
                    a('Definitions')
        with a.tbody():
            for data in table_data_fn:
                hash_id = hashlib.md5(bytes(data, 'utf-8')).hexdigest()[0:12]
                data = re.split(r'\t+', data)
                word = data[0]
                words.append(word)  # TODO a better way to do this
                query_word = word.split('/')[0] if '/' in word else word
                query_word = query_word.removesuffix('(s)') if query_word.endswith('(s)') else query_word
                part = data[1]
                parts.add(part)
                defn = data[2]
                with a.tr():
                    tsv_data = ''
                    with a.td():
                        # TODO: Rewrite all manual to a(id= etc)
                        spanish = '<a id=' + hash_id \
                          + ' href="https://www.linguee.com/english-spanish/search?source=auto&query=' \
                          + query_word + '"' \
                          + ' target="_blank" rel="noopener noreferrer"' + '>' \
                          + word + '</a>'
                        a(spanish)
                        tsv_data += spanish + '\t'
                    with a.td():
                        part_of_speech = '<a href="https://www.wordreference.com/es/en/translation.asp?spen='  \
                          + query_word + '"' \
                          + ' target="_blank" rel="noopener noreferrer"' + '>' \
                          + part + '</a>'
                        a(part_of_speech)
                        tsv_data += part_of_speech + '<br>'
                    with a.td():
                        definition = '<a href="https://www.spanishdict.com/translate/' \
                          + query_word + '"' \
                          + ' target="_blank" rel="noopener noreferrer"' + '>' \
                          + defn + '</a>'
                        a(definition)
                        tsv_data += definition + '\t'
                    headers = 'h1:_' + l1_header_fn
                    if l2_header_fn:
                        headers += ' ' + 'h2:_' + l2_header_fn
                    if l3_header_fn:
                        headers += ' ' + 'h3:_' + l3_header_fn
                    tsv_data += headers
                    corpus.append(tsv_data)


def format_header(h: str):
    return h.replace(' ', '_').lower()


a('<!DOCTYPE html>')
with a.html():
    with a.head():
        a.meta(charset='utf-8')
        a.link(rel='preconnect', href='https://fonts.googleapis.com')
        a.link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin="")
        a.link(href='https://fonts.googleapis.com/css2?family=Noto+Sans&family=Noto+Serif&display=swap',
               rel='stylesheet')
        a.link(rel='stylesheet', href='style.css')
    with a.body():

        # Create the table of contents
        with a.h2():
            a('Table of Contents')
            a.hr()
        with a.dl():
            with open('vocab.txt', 'r', encoding='utf-8') as file:
                while line := file.readline():
                    line = line.strip()
                    if line.startswith('###'):
                        pass  # Basically skip over level 3 headings
                    elif line.startswith('##'):
                        header = line[2:].strip()
                        with a.dd():
                            with a.a(href=('#' + format_header(header))):
                                a(header)
                    elif line.startswith('#'):
                        header = line[1:].strip()
                        with a.dt():
                            with a.a(href=('#' + format_header(header))):
                                a(header)

        # Create the dictionary
        with open('vocab.txt', 'r', encoding='utf-8') as file:
            l1_header = None
            l2_header = None
            l3_header = None
            table_data = []
            while line := file.readline():
                line = line.strip()
                if line.startswith('#') or line.startswith('>'):  # Then we have a title or comment
                    if table_data:  # If there is a table to write, then write it
                        write_table(table_data, l1_header, l2_header, l3_header)
                        table_data = []
                    if line.startswith('>'):
                        comment = line[1:].strip()
                        result = re.search(LINK_REGEX, comment)
                        replacements = 0
                        while result and replacements < MAX_REPLACEMENTS:  # Avoid infinite loop
                            name = result.group(1)
                            url = result.group(2)
                            match = comment[result.start():result.end()]
                            link = "<a href='" + url + "' style='text-decoration:underline'>" + name + "</a>"
                            comment = comment.replace(match, link)
                            result = re.search(LINK_REGEX, comment)
                            replacements += 1
                        with a.p():
                            a(comment)
                    elif line.startswith('###'):
                        header = line[3:].strip()
                        l3_header = format_header(header)  # Save header info
                        with a.h4():
                            a(header)
                    elif line.startswith('##'):
                        header = line[2:].strip()
                        formatted_header = format_header(header)
                        l2_header = formatted_header
                        l3_header = None  # Reset l3 sub headers
                        with a.h3(id=formatted_header):
                            a(header)
                    else:
                        header = line[1:].strip()
                        formatted_header = format_header(header)
                        l1_header = formatted_header
                        l2_header = None  # Reset l2 and l3 sub headers
                        l3_header = None
                        with a.h2(id=formatted_header):
                            a(header)
                            a.hr()
                elif line:
                    table_data.append(line)
            if table_data:  # Write the final table data
                write_table(table_data, l1_header, l2_header, l3_header)

html = str(a)  # casting to string extracts the value

# Write the html file
with open('./public/index.html', 'w', encoding='utf-8') as file:
    file.write(html)

with open('./private/corpus.txt', 'w', encoding='utf-8') as file:
    for entry in corpus:
        file.write(f"{entry}\n")

# Some metadata for reference
seen = set()
dupes = []
for w in words:
    if w in seen:
        dupes.append(w)
    else:
        seen.add(w)
print(dupes)
print(len(seen))
print(parts)
