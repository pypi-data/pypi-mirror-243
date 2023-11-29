from uuid import uuid1

from lona.static_files import StyleSheet, Script, SORT_ORDER
from lona.html import Div, Form
from lona import Bucket


class DropzoneComponent:
    STATIC_FILES = [

        # stylesheets
        StyleSheet(
            name='basic.css',
            path='static/lona-dropzone/dist/basic.css',
            url='/lona-dropzone/dist/basic.css',
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        StyleSheet(
            name='basic.css.map',
            path='static/lona-dropzone/dist/basic.css.map',
            url='/lona-dropzone/dist/basic.css.map',
            sort_order=SORT_ORDER.FRAMEWORK,
            link=False,
        ),

        StyleSheet(
            name='dropzone.css',
            path='static/lona-dropzone/dist/dropzone.css',
            url='/lona-dropzone/dist/dropzone.css',
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        StyleSheet(
            name='dropzone.css.map',
            path='static/lona-dropzone/dist/dropzone.css.map',
            url='/lona-dropzone/dist/dropzone.css.map',
            sort_order=SORT_ORDER.FRAMEWORK,
            link=False,
        ),

        StyleSheet(
            name='widgets.css',
            path='static/lona-dropzone/widgets.css',
            url='/lona-dropzone/widgets.css',
            sort_order=SORT_ORDER.LIBRARY,
        ),

        # scripts
        Script(
            name='dropzone-min.js',
            path='static/lona-dropzone/dist/dropzone-min.js',
            url='/lona-dropzone/dist/dropzone-min.js',
            sort_order=SORT_ORDER.FRAMEWORK,
        ),
        Script(
            name='dropzone-min.js.map',
            path='static/lona-dropzone/dist/dropzone-min.js.map',
            url='/lona-dropzone/dist/dropzone-min.js.map',
            sort_order=SORT_ORDER.FRAMEWORK,
            link=False,
        ),

        Script(
            name='widgets.js',
            path='static/lona-dropzone/widgets.js',
            url='/lona-dropzone/widgets.js',
            sort_order=SORT_ORDER.LIBRARY,
        ),
    ]


class Dropzone(DropzoneComponent, Div):
    CLASS_LIST = ['lona-dropzone']
    WIDGET = 'LonaDropzoneWidget'

    def __init__(
            self,
            request,
            max_files=None,
            max_size=None,
            index=True,
            on_add=None,
            on_delete=None,
            bucket=None,
            *args,
            **kwargs,
    ):

        super().__init__(*args, **kwargs)

        self.dropzone_id = f'dropzone_{str(uuid1())}'

        if bucket:
            self.bucket = bucket

        else:
            self.bucket = Bucket(
                request=request,
                max_files=max_files,
                max_size=max_size,
                index=index,
                on_add=on_add,
                on_delete=on_delete,
            )

        self.form = Form(
            _id=self.dropzone_id,
            _class='dropzone',
            action=self.bucket.get_add_url(),
        )

        self.nodes = [
            self.form,
        ]

        self.widget_data = {
            'dropzoneId': self.dropzone_id,
            'deleteUrl': self.bucket.get_delete_url(),
        }
