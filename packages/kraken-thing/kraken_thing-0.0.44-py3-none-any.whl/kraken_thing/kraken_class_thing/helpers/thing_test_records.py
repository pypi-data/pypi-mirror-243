



def get_test_record(record_type='thing', record_id='test01'):
    """Return a test record
    """
    record = {
        '@type': record_type,
        '@id': record_id,
        'name': 'name_' + str(record_id),
        'subjectOf': [
            {
            '@type': 'thing',
            '@id': str(record_id) + '_1',
            'name': 'subject_of_name_' + str(record_id) + '_1',
            },
            {
            '@type': 'thing',
            '@id': str(record_id) + '_2',
            'name': 'subject_of_name_' + str(record_id) + '_2',
            }
        ],
        'image': {
            '@type': 'imageObject',
            '@id': 'image_id_' + str(record_id) + '_3',
            'contentUrl': '/test.png?id=' + 'image_id_' + str(record_id) + '_3'
        }
    }

    return record


def get_test_records(quantity=20):
    """Return test records
    """
    records = []
    for i in range(quantity):
        record = get_test_record('thing', 'id_' + str(i))
        records.append(record)
    return records

        
        