import re

from airium import Airium

# Requirements:
# - Words generally listed in order of more common to less common frequency in usage
# - Words are not repeated


style = """body {
  font-family: "Libre Baskerville", serif;
  font-size: 24px;
  position: relative;
  margin-top: 0px;
  margin-bottom: 7%;
  margin-right: 7%;
  margin-left: 7%;
  background-color: #ffffff;
  color: #000000;
}

h2 {
  margin-block-start: 2em;
  margin-block-end: 1em;
}
h3 {
  margin-block-start: 0.5em;
  margin-block-end: 0.5em;
}

hr {
  margin-block-start: 0.2em;
  border-top: 2px solid black;
  border-bottom: 1px solid white;
  border-right: 1px solid white;
  border-left: 1px solid white;
}

table {
  left: -2px;
  position: relative;
}

th {
  font-family: Noto Sans;
  text-align: left;
}

th.palabra {
  width: 30%;
}

th.part {
  width: 10%;
}

th.definitions {
  width: 60%;
}

td {
  vertical-align: top;
  break-inside:avoid;
}

a:link {
  text-decoration: none;
  color: inherit;
}

a:visited {
  text-decoration: none;
  color: inherit;
}

a:hover {
  text-decoration: none;
  color: inherit;
}

a:active {
  text-decoration: none;
  color: inherit;
}
@page {
  margin: 1in;
}

@media print {
  body {
    font-size: 12px;
    margin: 0;
  }
}"""

a = Airium()


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
                part = data[1]
                defn = data[2]
                with a.tr():
                    with a.td():
                        a('<a href="https://www.linguee.com/english-spanish/search?source=auto&query='
                          + word + '"'
                          + ' target="_blank" rel="noopener noreferrer"' + '>'
                          + word + '</a>')
                    with a.td():
                        a('<a href="https://www.wordreference.com/es/en/translation.asp?spen='
                          + word + '"'
                          + ' target="_blank" rel="noopener noreferrer"' + '>'
                          + part + '</a>')
                    with a.td():
                        a('<a href="https://www.spanishdict.com/translate/'
                          + word + '"'
                          + ' target="_blank" rel="noopener noreferrer"' + '>'
                          + defn + '</a>')


a('<!DOCTYPE html>')
with a.html():
    with a.head():
        a.meta(charset='utf-8')
        a.link(rel='preconnect', href='https://fonts.googleapis.com')
        a.link(rel='preconnect', href='https://fonts.gstatic.com', crossorigin="")
        a.link(href='https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=EB+Garamond&display=swap',
               rel='stylesheet')
        with a.style():
            a('      '.join(style.splitlines(True)))
    with a.body():
        with open('vocab.txt', 'r', encoding='utf-8') as file:
            table_data = []
            while line := file.readline():
                line = line.strip()
                if line.startswith('#'):  # Then we have a title
                    if table_data:  # If there is a table to write, then write it
                        write_table(table_data)
                        table_data = []
                    if line.startswith('##'):
                        with a.h3():
                            a(line[2:])
                    else:
                        with a.h2():
                            a(line[1:])
                            a.hr()
                elif line:
                    table_data.append(line)
            if table_data:  # Write the final table data
                write_table(table_data)

html = str(a)  # casting to string extracts the value

with open('./public/index.html', 'w', encoding='utf-8') as file:
    file.write(html)
