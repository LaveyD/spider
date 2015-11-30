#__author__ = 'FUMA2'

list_first_item = lambda x:x[0] if x else None


def clean_link(link_text):
    return link_text.strip('\t\n\r ')
