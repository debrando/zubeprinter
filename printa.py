import json
import html
from yattag import Doc, indent

BOOTSTRAP = '''
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
'''

with open('example.json') as infile:
    alldata = json.load(infile)

def extract(src, *fields):
    return {k: '' if v is None else v for k, v in src.items() if k in fields}

printus = []
for card in alldata['cards']:
    data = extract(card, 'number', 'points', 'priority', 'title', 'labels')
    data['labels'] = sorted(l['name'] for l in data['labels'])
    printus.append(data)

def renderone(card):
    if not card:
        return
    with tag('div', klass="card", style="width: 18rem;"):
        with tag('div', klass="card-body"):
            with tag('h5', klass="card-title"):
                text('#%(number)s' % card)
            with tag('h6', klass="card-subtitle mb-2 text-muted"):
                text('pr: %(priority)s po: %(points)s' % card)
            with tag('h6', klass="card-subtitle mb-2 text-muted"):
                text(', '.join(card['labels']))
            with tag('p', klass="card-text"):
                text(card['title'])


doc, tag, text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
with tag('html', lang="en"):
    with tag('head'):
        doc.asis('<meta charset="utf-8">')
        doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
        for bline in BOOTSTRAP.splitlines():
            if bline.strip():
                doc.asis(bline.strip())
        with tag('title'):
            text('Zube Sprint Cards')
    with tag('body'):
        with tag('div', klass='container'):
            while printus:
                with tag('div', klass='row'):
                    for _ in range(3):
                        renderone(printus.pop(0) if printus else None)

with open('example.html', 'w') as outfile:
    outfile.write(indent(doc.getvalue(), indentation='  '))