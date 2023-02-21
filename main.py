import re

from airium import Airium

# Requirements:
# - Words generally listed in order of more common to less common frequency in usage
# - Words are not repeated

a = Airium()
words = []


def write_table(table_data_fn):
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
                data = re.split(r'\t+', data)
                word = data[0]
                words.append(word)  # TODO a better way to do this
                query_word = word.split('/')[0] if '/' in word else word
                part = data[1]
                defn = data[2]
                with a.tr():
                    with a.td():
                        a('<a href="https://www.linguee.com/english-spanish/search?source=auto&query='
                          + query_word + '"'
                          + ' target="_blank" rel="noopener noreferrer"' + '>'
                          + word + '</a>')
                    with a.td():
                        a('<a href="https://www.wordreference.com/es/en/translation.asp?spen='
                          + query_word + '"'
                          + ' target="_blank" rel="noopener noreferrer"' + '>'
                          + part + '</a>')
                    with a.td():
                        a('<a href="https://www.spanishdict.com/translate/'
                          + query_word + '"'
                          + ' target="_blank" rel="noopener noreferrer"' + '>'
                          + defn + '</a>')


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
        with open('vocab.txt', 'r', encoding='utf-8') as file:
            table_data = []
            while line := file.readline():
                line = line.strip()
                if line.startswith('#'):  # Then we have a title
                    if table_data:  # If there is a table to write, then write it
                        write_table(table_data)
                        table_data = []
                    if line.startswith('###'):
                        with a.h4():
                            a(line[3:].strip())
                    elif line.startswith('##'):
                        with a.h3():
                            a(line[2:].strip())
                    else:
                        with a.h2():
                            a(line[1:].strip())
                            a.hr()
                elif line:
                    table_data.append(line)
            if table_data:  # Write the final table data
                write_table(table_data)

html = str(a)  # casting to string extracts the value

with open('./public/index.html', 'w', encoding='utf-8') as file:
    file.write(html)

seen = set()
dupes = []
for w in words:
    if w in seen:
        dupes.append(w)
    else:
        seen.add(w)
print(dupes)
