import datetime

all_to_get_data_on = [
    {'resource': 'GSAD_2222', 'raw_data':
        {
            'F5MSCX001889': [
                {'location_id': '6022', 'device_id': 'F5MSCX001889', 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 4, 22, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 4, 22, 20, 7)},
                {'location_id': '6022', 'device_id': 'F5MSCX001889', 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 10, 23, 10, 8),
                 'ended_at': datetime.datetime(2016, 2, 10, 23, 20, 8)}],
            'F5MSCX001736': [
                {'location_id': '6022', 'device_id': 'F5MSCX001736', 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 2, 23, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 2, 23, 20, 7)},
                {'location_id': '6022', 'device_id': 'F5MSCX001736', 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 4, 23, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 4, 23, 20, 7)},
                {'location_id': '6022', 'device_id': 'F5MSCX001736', 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 4, 21, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 4, 21, 20, 7)},
                {'location_id': '6022', 'device_id': 'F5MSCX001736', 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 6, 22, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 6, 22, 20, 7)}],
            'F5MSCX001896': [
                {'location_id': '6022', 'device_id': 'F5MSCX001896',
                 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 5, 21, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 5, 21, 20, 7)},
                {'location_id': '6022', 'device_id': 'F5MSCX001896',
                 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 6, 20, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 6, 20, 20, 7)},
                {'location_id': '6022', 'device_id': 'F5MSCX001896',
                 'resource_id': 'GSAD_2222',
                 'started_at': datetime.datetime(2016, 2, 8, 21, 10, 7),
                 'ended_at': datetime.datetime(2016, 2, 8, 21, 20, 7)}]}}]

resulting_dictionaries = [
    {
        'F5MSCX001736': {'Play Count': 4, 'Content': 'GSAD_2222', 'Location': '6022', 'Display': 'F5MSCX001736'},
        'F5MSCX001889': {'Play Count': 2, 'Content': 'GSAD_2222', 'Location': '6022', 'Display': 'F5MSCX001889'},
        'F5MSCX001896': {'Play Count': 3, 'Content': 'GSAD_2222', 'Location': '6022', 'Display': 'F5MSCX001896'}},

    {
        'F5MSCX001736': {'Play Count': 4, 'Content': 'GSAD_5447', 'Location': '6023', 'Display': 'F5MSCX001736'},
        'F5MSCX001896': {'Play Count': 9, 'Content': 'GSAD_5447', 'Location': '6023', 'Display': 'F5MSCX001896'},
        'F5MSCX001889': {'Play Count': 3, 'Content': 'GSAD_5447', 'Location': '6023', 'Display': 'F5MSCX001889'}}
]

merged = {'F5MSCX001896': {'Location': '6023', 'Content': 'GSAD_5447', 'Display': 'F5MSCX001896', 'Play Count': 9},
          'F5MSCX001889': {'Location': '6023', 'Content': 'GSAD_5447', 'Display': 'F5MSCX001889', 'Play Count': 3},
          'F5MSCX001736': {'Location': '6023', 'Content': 'GSAD_5447', 'Display': 'F5MSCX001736', 'Play Count': 4}}

a = [
    {
        'resource': 'GSAD_2222',
        'raw_data': {'F5MSCX001889': [
            {'device_id': 'F5MSCX001889', 'location_id': '6022', 'ended_at': datetime.datetime(2016, 2, 4, 22, 20, 7),
             'started_at': datetime.datetime(2016, 2, 4, 22, 10, 7), 'resource_id': 'GSAD_2222'},
            {'device_id': 'F5MSCX001889', 'location_id': '6022', 'ended_at': datetime.datetime(2016, 2, 10, 23, 20, 8),
             'started_at': datetime.datetime(2016, 2, 10, 23, 10, 8), 'resource_id': 'GSAD_2222'}],
            'F5MSCX001896': [
                {'device_id': 'F5MSCX001896', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 5, 21, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 5, 21, 10, 7), 'resource_id': 'GSAD_2222'},
                {'device_id': 'F5MSCX001896', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 6, 20, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 6, 20, 10, 7), 'resource_id': 'GSAD_2222'},
                {'device_id': 'F5MSCX001896', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 8, 21, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 8, 21, 10, 7), 'resource_id': 'GSAD_2222'}],
            'F5MSCX001736': [
                {'device_id': 'F5MSCX001736', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 2, 23, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 2, 23, 10, 7), 'resource_id': 'GSAD_2222'},
                {'device_id': 'F5MSCX001736', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 4, 23, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 4, 23, 10, 7), 'resource_id': 'GSAD_2222'},
                {'device_id': 'F5MSCX001736', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 4, 21, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 4, 21, 10, 7), 'resource_id': 'GSAD_2222'},
                {'device_id': 'F5MSCX001736', 'location_id': '6022',
                 'ended_at': datetime.datetime(2016, 2, 6, 22, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 6, 22, 10, 7), 'resource_id': 'GSAD_2222'}]}},
    {
        'resource': 'GSAD_5447',
        'raw_data': {'F5MSCX001896': [
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 1, 21, 20, 7),
             'started_at': datetime.datetime(2016, 2, 1, 21, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 2, 21, 20, 7),
             'started_at': datetime.datetime(2016, 2, 2, 21, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 3, 22, 20, 7),
             'started_at': datetime.datetime(2016, 2, 3, 22, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 5, 22, 20, 7),
             'started_at': datetime.datetime(2016, 2, 5, 22, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 7, 20, 20, 7),
             'started_at': datetime.datetime(2016, 2, 7, 20, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 8, 23, 20, 7),
             'started_at': datetime.datetime(2016, 2, 8, 23, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 8, 22, 20, 7),
             'started_at': datetime.datetime(2016, 2, 8, 22, 10, 7), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 10, 22, 20, 8),
             'started_at': datetime.datetime(2016, 2, 10, 22, 10, 8), 'resource_id': 'GSAD_5447'},
            {'device_id': 'F5MSCX001896', 'location_id': '6023', 'ended_at': datetime.datetime(2016, 2, 10, 21, 20, 8),
             'started_at': datetime.datetime(2016, 2, 10, 21, 10, 8), 'resource_id': 'GSAD_5447'}],
            'F5MSCX001889': [
                {'device_id': 'F5MSCX001889', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 1, 20, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 1, 20, 10, 7), 'resource_id': 'GSAD_5447'},
                {'device_id': 'F5MSCX001889', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 7, 23, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 7, 23, 10, 7), 'resource_id': 'GSAD_5447'},
                {'device_id': 'F5MSCX001889', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 9, 22, 20, 8),
                 'started_at': datetime.datetime(2016, 2, 9, 22, 10, 8), 'resource_id': 'GSAD_5447'}],
            'F5MSCX001736': [
                {'device_id': 'F5MSCX001736', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 1, 23, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 1, 23, 10, 7), 'resource_id': 'GSAD_5447'},
                {'device_id': 'F5MSCX001736', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 1, 22, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 1, 22, 10, 7), 'resource_id': 'GSAD_5447'},
                {'device_id': 'F5MSCX001736', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 4, 20, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 4, 20, 10, 7), 'resource_id': 'GSAD_5447'},
                {'device_id': 'F5MSCX001736', 'location_id': '6023',
                 'ended_at': datetime.datetime(2016, 2, 5, 23, 20, 7),
                 'started_at': datetime.datetime(2016, 2, 5, 23, 10, 7), 'resource_id': 'GSAD_5447'}]}}]
