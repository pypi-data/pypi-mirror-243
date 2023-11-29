from .msg import Msg
from .protobuf import master_pb2


# for resolver db 2.0
class DocumentRecord(Msg):
    def __init__(self, *args, **kwargs):
        instance = master_pb2.DocumentRecord()
        links = kwargs.pop('links', None)
        super(DocumentRecord, self).__init__(instance, args, kwargs)
        if links:
            link_record = instance.links
            for key in links.keys():
                if isinstance(links[key], bool):
                    setattr(link_record, key, links[key])
                elif isinstance(links[key], list):
                    if key == 'ARXIV':
                        instance.links.ARXIV.extend(links[key])
                    elif key == 'DOI':
                        instance.links.DOI.extend(links[key])
                elif isinstance(links[key], dict):
                    if key == 'DATA':
                        for sub_type_key in links[key].keys():
                            link_type = instance.links.DATA[sub_type_key]
                            link_type.url.extend(links[key][sub_type_key]['url'])
                            link_type.title.extend(links[key][sub_type_key]['title'])
                            link_type.count = links[key][sub_type_key]['count']
                    elif key == 'ESOURCE':
                        for sub_type_key in links[key].keys():
                            link_type = instance.links.ESOURCE[sub_type_key]
                            link_type.url.extend(links[key][sub_type_key]['url'])
                            link_type.title.extend(links[key][sub_type_key]['title'])
                    elif key == 'ASSOCIATED':
                        link_type = instance.links.ASSOCIATED
                        link_type.url.extend(links[key]['url'])
                        link_type.title.extend(links[key]['title'])
                    elif key == 'TOC':
                        link_type = instance.links.TOC
                        link_type.url.extend(links[key]['url'])
                    elif key == 'PRESENTATION':
                        link_type = instance.links.PRESENTATION
                        link_type.url.extend(links[key]['url'])
                    elif key == 'LIBRARYCATALOG':
                        link_type = instance.links.LIBRARYCATALOG
                        link_type.url.extend(links[key]['url'])
                    elif key == 'INSPIRE':
                        link_type = instance.links.INSPIRE
                        link_type.url.extend(links[key]['url'])


class DocumentRecords(Msg):
    def __init__(self, *args, **kwargs):
        """converts list of dicts to list of protobuf instances of message DocumentRecord"""
        if 'document_records' in kwargs:
            kwargs['document_records'] = [DocumentRecord(**x)._data for x in kwargs['document_records']]
        super(DocumentRecords, self).__init__(master_pb2.DocumentRecords(), args, kwargs)
