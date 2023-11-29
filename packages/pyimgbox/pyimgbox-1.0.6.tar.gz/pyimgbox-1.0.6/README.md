Python 3.6+ library for uploading images to [https://imgbox.com/](imgbox.com).

[imgbox-cli](https://codeberg.org/plotski/imgbox-cli) is a command line tool that uses pyimgbox.

### Installation

pyimgbox is on [PyPI](https://pypi.org/project/pyimgbox/).

```sh
$ pip install pyimgbox
```

### Usage

```python
async with pyimgbox.Gallery(title="Hello, World!") as gallery:
    async for submission in gallery.add(files):
        pprint.pprint(submission)
```

See [examples.py](examples.py) for more examples.
