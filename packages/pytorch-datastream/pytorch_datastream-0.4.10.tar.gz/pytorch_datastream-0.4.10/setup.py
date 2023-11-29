# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datastream', 'datastream.samplers', 'datastream.tools']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17.0,<2.0.0', 'pandas>=1.0.5,<2.0.0', 'pydantic', 'torch>=1.4.0']

setup_kwargs = {
    'name': 'pytorch-datastream',
    'version': '0.4.10',
    'description': 'Simple dataset to dataloader library for pytorch',
    'long_description': "==================\nPytorch Datastream\n==================\n\n.. image:: https://badge.fury.io/py/pytorch-datastream.svg\n       :target: https://badge.fury.io/py/pytorch-datastream\n\n.. image:: https://img.shields.io/pypi/pyversions/pytorch-datastream.svg\n       :target: https://pypi.python.org/pypi/pytorch-datastream\n\n.. image:: https://readthedocs.org/projects/pytorch-datastream/badge/?version=latest\n       :target: https://pytorch-datastream.readthedocs.io/en/latest/?badge=latest\n\n.. image:: https://img.shields.io/pypi/l/pytorch-datastream.svg\n       :target: https://pypi.python.org/pypi/pytorch-datastream\n\n\n\nThis is a simple library for creating readable dataset pipelines and\nreusing best practices for issues such as imbalanced datasets. There are\njust two components to keep track of: ``Dataset`` and ``Datastream``.\n\n``Dataset`` is a simple mapping between an index and an example. It provides \npipelining of functions in a readable syntax originally adapted from\ntensorflow 2's ``tf.data.Dataset``.\n\n``Datastream`` combines a ``Dataset`` and a sampler into a stream of examples.\nIt provides a simple solution to oversampling / stratification, weighted\nsampling, and finally converting to a ``torch.utils.data.DataLoader``.\n\nInstall\n=======\n\n.. code-block::\n\n    poetry add pytorch-datastream\n\nOr, for the old-timers:\n\n.. code-block::\n\n    pip install pytorch-datastream\n\nUsage\n=====\n\nThe list below is meant to showcase functions that are useful in most standard\nand non-standard cases. It is not meant to be an exhaustive list. See the \n`documentation <https://pytorch-datastream.readthedocs.io/en/latest/>`_ for \na more extensive list on API and usage.\n\n.. code-block:: python\n\n    Dataset.from_subscriptable\n    Dataset.from_dataframe\n    Dataset\n        .map\n        .subset\n        .split\n        .cache\n        .with_columns\n\n    Datastream.merge\n    Datastream.zip\n    Datastream\n        .map\n        .data_loader\n        .zip_index\n        .update_weights_\n        .update_example_weight_\n        .weight\n        .state_dict\n        .load_state_dict\n\nMerge / stratify / oversample datastreams\n-----------------------------------------\nThe fruit datastreams given below repeatedly yields the string of its fruit\ntype.\n\n.. code-block:: python\n\n    >>> datastream = Datastream.merge([\n    ...     (apple_datastream, 2),\n    ...     (pear_datastream, 1),\n    ...     (banana_datastream, 1),\n    ... ])\n    >>> next(iter(datastream.data_loader(batch_size=8)))\n    ['apple', 'apple', 'pear', 'banana', 'apple', 'apple', 'pear', 'banana']\n\nZip independently sampled datastreams\n-------------------------------------\nThe fruit datastreams given below repeatedly yields the string of its fruit\ntype.\n\n.. code-block:: python\n\n    >>> datastream = Datastream.zip([\n    ...     apple_datastream,\n    ...     Datastream.merge([pear_datastream, banana_datastream]),\n    ... ])\n    >>> next(iter(datastream.data_loader(batch_size=4)))\n    [('apple', 'pear'), ('apple', 'banana'), ('apple', 'pear'), ('apple', 'banana')]\n\nMore usage examples\n-------------------\nSee the `documentation <https://pytorch-datastream.readthedocs.io/en/latest/>`_\nfor more usage examples.\n\nInstall from source\n===================\n\n.. pip install -e .\n",
    'author': 'NextML',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nextml-code/pytorch-datastream',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
