# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['micromed_io']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'mne>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['mmio_tcp_emulator = micromed_io.emulate_trc_tcpip:run']}

setup_kwargs = {
    'name': 'micromed-io',
    'version': '0.3.0',
    'description': 'A library to handle Micromed data',
    'long_description': '# Micromed library\n\nLibrary to handle Micromed data. It also provides some useful scripts.\n\n## Install\n\n``` bash\npip install micromed-io\n```\n\n## Convert a Micromed (*.trc*) file to MNE (*.fif*) format\n\n``` python\nfrom micromed_io.to_mne import create_mne_from_micromed_recording\nmne_raw = create_mne_from_micromed_recording("path/to/file.TRC")\n```\n\n## Emulate Micromed TCP from *.trc* file\n\n### CLI tool\n\nUse the following command:\n\n``` bash\nmmio_tcp_emulator --file=../data/sample.TRC --address=localhost --port=5123\nmmio_tcp_emulator --help\n```\n\n### From python script\n\nDownload `emulate_trc_tcpip.py` from the [gihub repo](https://github.com/etiennedemontalivet/micromed-io) in *scripts/*\n\n``` bash\npython emulate_trc_tcpip.py --file=../data/sample.TRC --address=localhost --port=5123\n```\n\nMore details:\n``` bash\npython emulate_trc_tcpip.py --help\n```\n\n## Read and parse Micromed TCP live data\n\nDownload `read_tcp_data.py` from the [gihub repo](https://github.com/etiennedemontalivet/micromed-io) in *scripts/*\n``` bash\npython read_tcp_data.py --address=localhost --port=5123\n```\n\n> **Note**: Micromed TCP behaves as a client. If you want to try the emulate/read TCP script, launch the reader first that acts as server, then the emulator. \n\n## Read Micromed TCP in a sliding window buffer\n\nIf you plan to use the Micromed data as input of a decoder, you probably want epochs of format `(n_channels, n_samples)`. Then the ``MicromedBuffer`` class is for you. The script ``read_tcp_to_epoch.py`` show you how to use it (see the ``PROCESS HERE`` comment). It uses a **buffer** that mimics the **sliding window** and triggers each time it is filled.\n\n``` python\nfrom micromed_io.buffer import MicromedBuffer\nmicromed_buffer = MicromedBuffer(epoch_duration=5, epoch_overlap=2.5)\n\n```\n\n## Read TRC file\n\n``` python\nfrom micromed_io.trc import MicromedTRC\nmmtrc = MicromedTRC("sample.TRC")\n```\nThen you have access to the *trc* data:\n``` python\nmmtrc.get_header()\nmmtrc.get_markers()\nmmtrc.get_data()\nmmtrc.get_notes()\n```\n> **Note:** ``get_data()`` might take times because it loads the brain data\n\n## TODO\n\n- [x] Include serial markers parsing\n- [ ] Parse all info from Micromed header\n- [ ] Emulate serial markers + notes\n- [ ] Add tests \n\nPlease feel free to reach me if you want to contribute.\n',
    'author': 'Etienne de MONTALIVET',
    'author_email': 'etienne.demontalivet@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
