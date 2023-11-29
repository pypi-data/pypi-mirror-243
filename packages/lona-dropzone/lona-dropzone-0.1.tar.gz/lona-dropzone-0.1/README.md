# lona-dropzone

![license MIT](https://img.shields.io/pypi/l/lona-dropzone.svg)
![Python Version](https://img.shields.io/pypi/pyversions/lona-dropzone.svg)
![Latest Version](https://img.shields.io/pypi/v/lona-dropzone.svg)

[Dropzone.js](https://www.dropzone.dev/) bindings for [Lona](https://lona-web.org)


## Installation

lona-dropzone can be installed using pip

```
pip install lona lona-dropzone
```


## Usage

lona-dropzone uses Lonas [Bucket](https://lona-web.org/1.x/api-reference/buckets.html) API.
`lona_dropzone.Dropzone` accepts all arguments of a Lona Bucket to create a new Bucket on the fly.
You can also use a previously created Bucket using the keyword `bucket`.

```python
from lona.html import HTML, H1
from lona import View

from lona_dropzone import Dropzone


class DropzoneView(View):
    def handle_request(self, request):
        self.dropzone = Dropzone(
            request=request,
            on_add=self.on_add,
            on_delete=self.on_delete,
        )

        return HTML(
            H1('Dropzone'),
            self.dropzone,
        )

    def on_add(self, file_names):
        print(f'{file_names} added to {self.dropzone.bucket.get_path()}')

    def on_delete(self, file_names):
        print(f'{file_names} deleted from {self.dropzone.bucket.get_path()}')
```
