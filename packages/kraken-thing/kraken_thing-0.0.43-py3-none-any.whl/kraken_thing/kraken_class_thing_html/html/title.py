

def title(text, level = 'H1'):
    content = '''
        <{level}>{text}</{level}>
        '''.format(
            text = text,
            level = level
        )
    return content