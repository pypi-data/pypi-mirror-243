# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temporian',
 'temporian.beam',
 'temporian.beam.io',
 'temporian.beam.io.test',
 'temporian.beam.operators',
 'temporian.beam.operators.test',
 'temporian.beam.operators.window',
 'temporian.beam.operators.window.test',
 'temporian.beam.test',
 'temporian.core',
 'temporian.core.data',
 'temporian.core.data.test',
 'temporian.core.operators',
 'temporian.core.operators.binary',
 'temporian.core.operators.calendar',
 'temporian.core.operators.calendar.test',
 'temporian.core.operators.scalar',
 'temporian.core.operators.test',
 'temporian.core.operators.window',
 'temporian.core.operators.window.test',
 'temporian.core.test',
 'temporian.implementation',
 'temporian.implementation.numpy',
 'temporian.implementation.numpy.data',
 'temporian.implementation.numpy.data.test',
 'temporian.implementation.numpy.operators',
 'temporian.implementation.numpy.operators.binary',
 'temporian.implementation.numpy.operators.calendar',
 'temporian.implementation.numpy.operators.scalar',
 'temporian.implementation.numpy.operators.window',
 'temporian.implementation.numpy.test',
 'temporian.implementation.numpy_cc',
 'temporian.implementation.numpy_cc.operators',
 'temporian.io',
 'temporian.io.test',
 'temporian.proto',
 'temporian.test',
 'temporian.utils',
 'temporian.utils.test']

package_data = \
{'': ['*'],
 'temporian.implementation.numpy.data.test': ['test_data/*'],
 'temporian.test': ['test_data/*', 'test_data/io/*', 'test_data/prototype/*']}

install_requires = \
['absl-py>=1.3.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pandas>=1.5.2',
 'protobuf>=3.20.3']

extras_require = \
{'all': ['apache-beam>=2.48.0,<3.0.0', 'tensorflow>=2.12.0,<3.0.0'],
 'beam': ['apache-beam>=2.48.0,<3.0.0'],
 'tensorflow': ['tensorflow>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'temporian',
    'version': '0.1.6',
    'description': 'Temporian is a Python package for feature engineering of temporal data, focusing on preventing common modeling errors and providing a simple and powerful API, a first-class iterative development experience, and efficient and well-tested implementations of common and not-so-common temporal data preprocessing functions.',
    'long_description': '<img src="https://github.com/google/temporian/raw/main/docs/src/assets/banner.png" width="100%" alt="Temporian logo">\n\n[![pypi](https://img.shields.io/pypi/v/temporian?color=blue)](https://pypi.org/project/temporian/)\n[![docs](https://readthedocs.org/projects/temporian/badge/?version=stable)](https://temporian.readthedocs.io/en/stable/?badge=stable)\n![tests](https://github.com/google/temporian/actions/workflows/test.yaml/badge.svg)\n![formatting](https://github.com/google/temporian/actions/workflows/formatting.yaml/badge.svg)\n![publish](https://github.com/google/temporian/actions/workflows/publish.yaml/badge.svg)\n\n**Temporian** is a library for **safe**, **simple** and **efficient** preprocessing and feature engineering of temporal data in Python. Temporian supports multivariate time-series, multivariate time-sequences, event logs, and cross-source event streams.\n\nTemporian is to [temporal data](https://temporian.readthedocs.io/en/stable/user_guide/#what-is-temporal-data) what Pandas is to tabular data.\n\n## Key features\n\n- **Supports most types of temporal data** 📈: Handles both uniformly sampled and\n  non-uniformly sampled data, both single-variate and multivariate data, both flat\n  and multi-index data, and both mono-source and multi-source non-synchronized\n  events.\n\n- **Optimized for Temporal data** 🔥: Temporian\'s core computation is\n  implemented in C++ and optimized for temporal data. Temporian can be more than\n  1,000x faster than off-the-shelf data processing libraries when operating on\n  temporal data.\n\n- **Easy to integrate into an existing ML ecosystem**: Temporian does not perform any ML model training - instead it integrates seamlessly with any ML library, such as PyTorch, Scikit-Learn, Jax, TensorFlow, XGBoost, or Yggdrasil Decision Forests.\n\n- **Prevents unwanted future leakage** 😰: Unless explicitly specified with\n  `tp.leak`, feature computation cannot depend on future data, thereby preventing\n  unwanted, hard-to-debug, and potentially costly future leakage.\n\n<!--\n- **Iterative and interactive development** 📊: Users can easily analyze\n  temporal data and visualize results in real-time with iterative tools like\n  notebooks. When prototyping, users can iteratively preprocess, analyze, and\n  visualize temporal data in real-time with notebooks. In production, users\n  can easily reuse, apply, and scale these implementations to larger datasets.\n\n- **Flexible runtime** ☁️: Temporian programs can run seamlessly in-process in\n  Python, on large datasets using [Apache Beam](https://beam.apache.org/).\n-->\n\n## QuickStart\n\n### Installation\n\nInstall Temporian from [PyPI](https://pypi.org/project/temporian/) with `pip`:\n\n```shell\npip install temporian -U\n```\n\n### Minimal example\n\nConsider sale records that contain contain the `timestamp`, `store`, and `revenue` of individual sales.\n\n```shell\n$ cat sales.csv\ntimestamp,store,revenue\n2023-12-04 21:21:05,STORE_31,5071\n2023-11-08 17:14:38,STORE_4,1571\n2023-11-29 21:44:46,STORE_49,6101\n2023-12-20 18:17:14,STORE_18,4499\n2023-12-15 10:55:09,STORE_2,6666\n...\n```\n\nOur goal is to compute the sum of revenue for each store at 11 pm every weekday (excluding weekends).\n\nFirst, we load the data and list the workdays.\n\n```python\nimport temporian as tp\n\n# Load sale transactions\nsales = tp.from_csv("sales.csv")\n\n# Index sales per store\nsales_per_store = sales.add_index("store")\n\n# List work days\ndays = sales_per_store.tick_calendar(hour=22)\nwork_days = (days.calendar_day_of_week() <= 5).filter()\n\nwork_days.plot(max_num_plots=1)\n```\n\n![](https://github.com/google/temporian/raw/main/docs/src/assets/frontpage_workdays.png)\n\nThen, we sum the daily revenue for each workday and each store.\n\n```python\n# Aggregate revenue per store and per work day\ndaily_revenue = sales_per_store["revenue"].moving_sum(tp.duration.days(1), sampling=work_days).rename("daily_revenue")\n\n# Plot the results\ndaily_revenue.plot(max_num_plots=3)\n```\n\n![](https://github.com/google/temporian/raw/main/docs/src/assets/frontpage_aggregated_revenue.png)\n\nFinally, we can export the result as a Pandas DataFrame for further processing or for consumption by other libraries.\n\n```python\ntp.to_pandas(daily_revenue)\n```\n\n![](https://github.com/google/temporian/raw/main/docs/src/assets/frontpage_pandas.png)\n\nCheck the [Getting Started tutorial](https://temporian.readthedocs.io/en/stable/tutorials/getting_started/) to find out more!\n\n## Next steps\n\nNew users should refer to the [Getting Started](https://temporian.readthedocs.io/en/stable/getting_started/) guide, which provides a\nquick overview of the key concepts and operations of Temporian.\n\nAfter that, visit the [User Guide](https://temporian.readthedocs.io/en/stable/user_guide/) for a deep dive into\nthe major concepts, operators, conventions, and practices of Temporian. For a\nhands-on learning experience, work through the [Tutorials](https://temporian.readthedocs.io/en/stable/tutorials/) or refer to the [API\nreference](https://temporian.readthedocs.io/en/stable/reference/).\n\n## Documentation\n\nThe documentation 📚 is available at [temporian.readthedocs.io](https://temporian.readthedocs.io/en/stable/). The [Getting Started guide](https://temporian.readthedocs.io/en/stable/getting_started/) is the best way to start.\n\n## Contributing\n\nContributions to Temporian are welcome! Check out the [contributing guide](CONTRIBUTING.md) to get started.\n\n## Credits\n\nTemporian is developed in collaboration between Google and [Tryolabs](https://tryolabs.com/).\n',
    'author': 'Mathieu Guillame-Bert, Braulio Ríos, Guillermo Etchebarne, Ian Spektor, Richard Stotz',
    'author_email': 'gbm@google.com',
    'maintainer': 'Mathieu Guillame-Bert',
    'maintainer_email': 'gbm@google.com',
    'url': 'https://github.com/google/temporian',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}
from config.build import *
build(setup_kwargs)

setup(**setup_kwargs)
