from lxml import etree
import os, sys
from unidecode import unidecode


# @func: fast_iter
# @param context : iterparsed (chunk of xml) data
# @param func : handler
# @desc: Read xml chunk. After read, clear and delete chunk to release memory.
#		Also, replace html encoding to similar ascii code

def fast_iter(context, func, *args, **kwargs):
    collaborations = ['www', 'phdthesis', 'inproceedings', 'incollection', 'proceedings', 'book',
                      'mastersthesis', 'article']
    # xml categories
    author_array = []
    title = ''
    book_title = ''
    key = ''
    year = ''
    ee = ''
    url = ''

    # read chunk line by line
    # we focus author and title, key, year, url
    for event, elem in context:

        if elem.tag == 'author':
            author_array.append(unidecode(elem.text))

        if elem.tag == 'title':
            if elem.text:
                title = unidecode(elem.text)

        key = elem.get('key')
        year = elem.get('year')
        ee = elem.get('ee')
        url = elem.get('url')

        if key is None:
            key = ''
        if book_title is None:
            book_title = ''
        if year is None:
            year = ''
        if ee is None:
            ee = ''
        if url is None:
            url = ''

        if elem.tag in collaborations:
            if len(author_array) is not 0 and title is not '':
                # rejected paper has no author or title
                # it should be check

                for a in author_array:
                    string = a + ',' + title + ',' + key + ',' + book_title + ',' + year + ',' + url + ',' + ee
                    # print(string)
                    func(string, *args, **kwargs)

                # write into csv file

                title = ''
                del author_array[:]

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


# clear chunks

# @func: process_element
# @param elem : parsed data of chunk
# @param fout : file name to write
# @desc: It is handler to write content. just write content to file
def process_element(elem, fout):
    print("writing ... " + elem)
    print(elem, file=fout)


if __name__ == "__main__":
    fout = open('parsed_data.csv', 'w')
    context = etree.iterparse('./dblp.xml', load_dtd=True, html=True)
    # To use iterparse, we don't need to read all of xml.
    fast_iter(context, process_element, fout)

