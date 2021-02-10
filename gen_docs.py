import scrython
import re
import os

def format_args(string, f):
    f.write('\n## Args\n\n|arg|type|description|\n|:---:|:---:|:---:|\n')

    arg_list = re.findall(r'(\w*\s*\(\w+[,\s\w]{1,}\):[\w\s\'\\`,.]*[^\w\s\(])', string)

    for arg in arg_list:
        arg_name = re.findall(r'[^\s]*', arg)[0]

        description = re.findall(r'(?<=:\s)(.*)', arg)[0]

        type_and_optional = re.findall(r'(?<=\()\w+[,\s\w]+(?=\))', arg)[0]

        if len(type_and_optional) > 1:
            f.write('|{}|{}|{}|\n'.format(arg_name, type_and_optional, description))

        else:
            f.write('|{}|{}|{}|\n'.format(arg_name, type_and_optional, description))

def format_returns(string, f):
    f.write('\n## Returns\n{}\n'.format(string.strip()))

def format_raises(string, f):

    if 'N/A' in string:
        f.write('\n## Raises\nN/A\n')
        return

    f.write('\n## Raises\n\n|exception type|reason|\n|:---:|:---:|\n')

    exception_list = re.findall(r'\w+:[\w\s\\\']+[^\s\w:]', string)

    for exception in exception_list:
        exception_name = re.findall(r'[^:]*', exception)[0]

        exception_description = re.findall(r'(?<=:\s)([\w\s\.\'\\]*)', exception)[0]

        f.write('|{}|{}|\n'.format(exception_name, exception_description))

def format_examples(string, f):

    example_list = re.findall(r'>{3}[\s\w=.("+:,\-)]+', string)

    f.write('\n## Examples\n')
    f.write('```python\n{}\n```\n'.format('\n'.join(example_list)))

def format_functions(_class, function_list, f):

    f.write('\n## Methods\n')

    for function in function_list:
        function_docstring = getattr(eval(_class), function).__doc__

        f.write('\n---\n### `{}()`\n'.format(getattr(eval(_class), function).__name__))

        f.write('\n```\n{}\n```'.format(function_docstring))

def main(subpackage):
    for _class in subpackage.__all__:

        intro = """
These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`{}().scryfallJson`).
""".format(eval(_class).__name__)

        class_docstring = repr(re.sub(r'\n+', '', eval(_class).__doc__)) # removes newlines

        remove_extra_spaces = re.sub(' +', ' ', class_docstring)

        try:
            args = re.findall(r'(?<=Args:)(.*)(?=Returns:)', remove_extra_spaces)[0]

            returns = re.findall(r'(?<=Returns:)(.*)(?=Raises:)', remove_extra_spaces)[0]

            raises = re.findall(r'(?<=Raises:)(.*)(?=Examples:)', remove_extra_spaces)[0]

            examples = re.findall(r'(?<=Examples:)(.*)', remove_extra_spaces)[0]

            functions = [x for x in dir(eval(_class)) if not x.startswith('_')]

            if not os.path.exists('./docs/{}'.format(subpackage.__name__)):
                os.makedirs('./docs/{}'.format(subpackage.__name__))

            with open('./docs/{}/{}.md'.format(subpackage.__name__, _class), 'w') as f:
                f.write('# **class** `{}.{}()`\n'.format(subpackage.__name__, _class))
                f.write(intro)
                format_args(args, f)
                format_returns(returns, f)
                format_raises(raises, f)
                format_examples(examples, f)
                format_functions(_class, functions, f)

        except Exception as e:
            print(_class.upper())
            print(repr(eval(_class).__doc__))
            print('Args: ', re.findall(r'(?<=Args:)(.*)(?=Returns:)', remove_extra_spaces))
            print('Returns: ', re.findall(r'(?<=Returns:)(.*)(?=Raises:)', remove_extra_spaces))
            print('Raises: ', re.findall(r'(?<=Raises:)(.*)(?=Examples:)', remove_extra_spaces))
            print('Examples: ', re.findall(r'(?<=Examples:)(.*)', remove_extra_spaces))
            print(e)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~')

if __name__ == '__main__':
    from scrython.bulk_data import *
    main(scrython.bulk_data)
    del scrython.bulk_data

    from scrython.cards import *
    main(scrython.cards)
    del scrython.cards

    from scrython.catalog import *
    main(scrython.catalog)
    del scrython.catalog

    from scrython.rulings import *
    main(scrython.rulings)
    del scrython.rulings

    from scrython.sets import *
    main(scrython.sets)
    del scrython.sets

    from scrython.symbology import *
    main(scrython.symbology)
    del scrython.symbology