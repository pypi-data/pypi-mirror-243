# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tracelogger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tracelogger',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Tracelogger\n\nTag your functions with the `@tracelogger` decorator to be logged line-by-line.\n\nOptionally provide a function as the `printer` argument that takes the local variable dictionary and returns a string. This allows the customisation of which variables and how you want to print at each line. See the example with the provided `names_printer` function that only prints a selected set of variables.\n\nThe second `width` parameter determines the maximum character number for each line of code defaulting to `80`.\n\n```\nfrom tracelogger import tracelogger, names_printer\n\n\n@tracelogger(width=30)\ndef second_test_function(x):\n    y = x**2\n    return y\n\n\n@tracelogger(printer=lambda locals_: names_printer(locals_=locals_, names=['k', 'b']), width=30)\ndef first_test_function(a, b):\n    c = a + b\n    for k in range(5):\n        if k % 2 == 0:\n            b += k\n        else:\n            c += k\n            second_test_function(c)\n    return a, b, c\n\na, b, c = first_test_function(a=10, b=20)\n```\n\nThis will print the following:\n\n```\nEntering function: first_test_function\n    c = a + b                            locals: b=20\n    for k in range(5):                   locals: b=20\n        if k % 2 == 0:                   locals: b=20, k=0\n            b += k                       locals: b=20, k=0\n    for k in range(5):                   locals: b=20, k=0\n        if k % 2 == 0:                   locals: b=20, k=1\n            c += k                       locals: b=20, k=1\n            second_test_function(c)      locals: b=20, k=1\n\nEntering function: second_test_function\n    y = x**2                             locals: x=31\n    return y                             locals: x=31, y=961\n    return y                             locals: x=31, y=961\nReturning from: second_test_function() to: first_test_function()\n\n    for k in range(5):                   locals: b=20, k=1\n        if k % 2 == 0:                   locals: b=20, k=2\n            b += k                       locals: b=20, k=2\n    for k in range(5):                   locals: b=22, k=2\n        if k % 2 == 0:                   locals: b=22, k=3\n            c += k                       locals: b=22, k=3\n            second_test_function(c)      locals: b=22, k=3\n\nEntering function: second_test_function\n    y = x**2                             locals: x=34\n    return y                             locals: x=34, y=1156\n    return y                             locals: x=34, y=1156\nReturning from: second_test_function() to: first_test_function()\n\n    for k in range(5):                   locals: b=22, k=3\n        if k % 2 == 0:                   locals: b=22, k=4\n            b += k                       locals: b=22, k=4\n    for k in range(5):                   locals: b=26, k=4\n    return a, b, c                       locals: b=26, k=4\n    return a, b, c                       locals: b=26, k=4\nReturning from: first_test_function() to: None\n```\n\nJoin the [Code Quality for Data Science (CQ4DS) Discord channel](https://discord.com/invite/8uUZNMCad2) for feedback.\n\nI used the following StackOverflow threads as sources, many thanks to their authors:\n\n[https://stackoverflow.com/questions/32163436/python-decorator-for-printing-every-line-executed-by-a-function](https://stackoverflow.com/questions/32163436/python-decorator-for-printing-every-line-executed-by-a-function)\n\n[https://stackoverflow.com/questions/22362940/inspect-code-of-next-line-in-python](https://stackoverflow.com/questions/22362940/inspect-code-of-next-line-in-python)\n",
    'author': 'Laszlo Sragner',
    'author_email': 'sragner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
