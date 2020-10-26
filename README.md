# Abuse.ch APIs Python Library

## Installation

    pip install git+https://github.com/colingrady/AbuseCh

## Examples of Usage

### MalwareBazaar API

```python
>>> from AbuseCh import MalwareBazaar
>>> mb = MalwareBazaar()
>>> res = mb.query_tag('Qakbot', limit=1)
>>> res['data'][0]
{'sha256_hash': '1c0ecf7736c78c764ac9b4f9eb7db709ae08ad65bab6bf1d0f8c8de4476abe35', 'sha3_384_hash': None, 'sha1_hash': None, 'md5_hash': '383142315baf079e673d311becc8cea1', 'first_seen': '2020-10-22 15:42:03', 'last_seen': None, 'file_name': 'Document10275.xlsb', 'file_size': 764378, 'file_type_mime': 'application/octet-stream', 'file_type': 'xlsb', 'reporter': 'lazyactivist192', 'anonymous': 0, 'signature': None, 'imphash': None, 'tlsh': None, 'ssdeep': None, 'tags': ['Qakbot', 'qbot', 'tr01', 'xlsb'], 'code_sign': [], 'intelligence': {'clamav': None, 'downloads': '0', 'uploads': '1', 'mail': None}}
```

### URLhaus API

```python
>>> from AbuseCh import URLhaus
>>> uh = URLhaus()
>>> res = uh.get_domains()
>>> res[:5]
['020dz.net', '0377hhd.com', '0931tangfc.com', '1008691.com', '180clubrealestate.com']
```
