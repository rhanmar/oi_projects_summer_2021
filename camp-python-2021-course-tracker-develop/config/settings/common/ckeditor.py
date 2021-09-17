# Rich text editor which enables writing content directly inside of web pages.
# https://github.com/django-ckeditor/django-ckeditor

from ckeditor.configs import DEFAULT_CONFIG

from .paths import BASE_DIR

CKEDITOR_UPLOAD_PATH = BASE_DIR / "media/ckeditor/uploads"
CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_CONFIGS = {
    "default": DEFAULT_CONFIG,
    "text_only": {
        "toolbar_Full": [
            [
                "Styles",
                "Bold",
                "Italic",
                "Underline",
                "Strike",
                "SpellChecker"
            ],
            ["TextColor"],
            ["Smiley", "SpecialChar"],
            ["Source"],
            ["Maximize"],
        ],
    },
    "tasks_text": {
        "skin": "moono",
        "toolbar_Basic": [
            ["Source", "-", "Bold", "Italic"]
        ],
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "-",
                    "Save",
                    "NewPage",
                    "Preview",
                    "Print",
                    "-",
                    "Templates"
                ]
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo"
                ]
            },
            {
                "name": "editing",
                "items": [
                    "Find",
                    "Replace",
                    "-",
                    "SelectAll"
                ]
            },
            {
                "name": "forms",
                "items": [
                    "Form",
                    "Checkbox",
                    "Radio",
                    "TextField",
                    "Textarea",
                    "Select",
                    "Button",
                    "ImageButton",
                    "HiddenField"
                ]
            },
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat"
                ]
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language"
                ]
            },
            {"name": "links",
             "items": [
                 "Link",
                 "Unlink",
                 "Anchor"
             ]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe"
                ]
            },
            {
                "name": "styles",
                "items": [
                    "Styles",
                    "Format",
                    "Font",
                    "FontSize"
                ]
            },
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
            {"name": "about", "items": ["About"]},
            {
                "name": "yourcustomtools", "items": [
                # put the name of your editor.ui.addButton here
                "Preview",
                "Maximize",

            ]
            },
        ],
        "toolbar": "YourCustomToolbarConfig",
        # put selected toolbar config here
        "tabSpaces": 4,
        "extraPlugins": ",".join([
            "uploadimage",  # the upload image feature
            "div",
            "autolink",
            "autoembed",
            "embedsemantic",
            "autogrow",
            "widget",
            "lineutils",
            "dialog",
            "clipboard",
            "dialogui",
            "elementspath"
        ]),
    }
}
