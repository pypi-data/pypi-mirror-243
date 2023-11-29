class LonaDropzoneWidget {
    constructor(lonaWindow, rootNode, widgetData) {
        this.lonaWindow = lonaWindow;
        this.rootNode = rootNode;

        this.dropzone = new Dropzone(`#${widgetData.data.dropzoneId}`, {
            addRemoveLinks: true,
            removedfile: file => {
                const xhr = new XMLHttpRequest();
                const formData = new FormData();

                formData.append('name', file.name);

                xhr.onloadend = () => {
                    if(xhr.status == 200) {
                        file.previewElement.remove();
                    }
                };

                xhr.open('POST', widgetData.data.deleteUrl, true);
                xhr.send(formData);
            },
        });
    }
}


Lona.register_widget_class('LonaDropzoneWidget', LonaDropzoneWidget);
