import sys
import scrython
from scrython import *
import re

intro = """These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`{Class_name}().scryfallJson`)."""

for _class in scrython.__all__:

    match = list(filter(None, (token.strip() for token in re.findall(r'[^\n]*', eval(_class).__doc__))))

    with open('{}.md'.format(eval(_class).__name__), 'w') as f:
        f.write('# **class** `{}()`\n'.format(eval(_class).__name__))
        f.write(intro)
        for token in match:
            # Match section header
            if re.findall(r'[A-Z][a-z].*:', token) and ':' in re.findall(r':.*', token):
                f.write('\n\n## {}\n\n'.format(token.replace(':', '')))
                if 'Example' in token:
                    f.write()
                else:
                    f.write('| arg | description |\n|:---:|:---:|')

            # Match args description
            elif re.findall(r'[\w]+\s\(.+\):', token):
                if 'Defaults' in token:
                    f.write(token)
                else:
                    f.write('\n|{}'.format(token))
            else:
                f.write('\n|{}|'.format(token))
        # r'[\w]+\s\(.+\):' Matches anything that's a described parameter
        # r'[A-Z][a-z](.*)' Matches section titles
    break
