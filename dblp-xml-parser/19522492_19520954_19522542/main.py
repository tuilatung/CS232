"""Problem at https://stackoverflow.com/questions/49818428/parsing-dblp-xml-file"""


from lxml import etree
from unidecode import unidecode

CATEGORIES = {'article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www'}
DATA_ITEMS = ['title', 'booktitle', 'year', 'journal', 'ee', 'url']
TABLE_KEYS = ['dblpkey', 'tag', 'title', 'mdate', 'booktitle', 'year', 'journal', 'ee', 'url']


def save_result(paper, authors, file_out):
    arranged_fields = []
    for field in TABLE_KEYS:
        if field in paper and paper[field] is not None:
            arranged_fields.append(unidecode(paper[field]))
        else:
            arranged_fields.append('')
    for author in authors:
        print(author + ',' + ','.join(arranged_fields), file=file_out)


def clear_element(element):
    element.clear()
    while element.getprevious() is not None:
        del element.getparent()[0]


def extract_paper_elements(context):
    for event, element in context:
        if element.tag in CATEGORIES:
            yield element
            clear_element(element)


def fast_iter(context, output_file):
    for element in extract_paper_elements(context):
        authors = []
        for author in element.findall('author'):
            if author is not None and author.text is not None:
                authors.append(unidecode(author.text))
            paper = {
                'tag': element.tag,
                'mdate': element.get('mdate'),
                'dblpkey': element.get('key')
            }
            try:
                for data_item in DATA_ITEMS:
                    items_concatenated = ""
                    for data in element.findall(data_item):
                        items_concatenated += data.text + ";"
                    if items_concatenated != "":
                        paper[data_item] = items_concatenated[0:-1]
                save_result(paper, authors, output_file)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    fo = open('parsed_data.csv', mode='w')
    fo.write('author' + ',' + ','.join(TABLE_KEYS) + '\n')
    context = etree.iterparse('./dblp.xml', dtd_validation=True, events=('start', 'end'))
    fast_iter(context, fo)
    fo.close()
