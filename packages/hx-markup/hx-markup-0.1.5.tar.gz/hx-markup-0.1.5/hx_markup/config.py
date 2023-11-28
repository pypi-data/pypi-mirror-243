import re
from collections import defaultdict

__all__ = ['TAGS', 'LIST_TAGS', 'SELECT_TAGS', 'DATALIST_TAGS', 'SEMANTIC_TAGS', 'STRUCTURE_TAGS', 'HEAD_ONLY_TAGS',
           'METADATA_TAGS', 'HEAD_AND_BODY_TAGS', 'HTML_NON_GLOBAL_ATTRIBUTES_ELEMENT_MAP', 'HTML_ENUMERATED_ATTRIBUTES',
           'VOID_TAGS', 'TABLE_TAGS', 'FORMAT_TAGS', 'FORM_TAGS', 'FORM_FIELD_TAGS', 'CONTENT_TAGS', 'DETAILS_TAGS',
           'GLOBAL_ATTRIBUTES', 'LIST_ITEM_TAGS', 'UNIQUE_TAGS', 'BOOLEAN_ATTRIBUTES', 'BODY_TAGS', 'BODY_ONLY_TAGS',
           'WAI_AREA_ENUMERATED_ATTRIBUTES', 'ENUMERATED_ATTRIBUTES', 'INPUT_TYPES', 'HTMX_CORE_ATTRIBUTES',
           'HTMX_ADDITIONAL_ATTRIBUTES', 'HTMX_ATTRIBUTES']


TAGS: tuple[str, ...] = tuple(sorted(
        ['a', 'address', 'area', 'abbr', 'article', 'aside', 'audio', 'body', 'b', 'base', 'bdi', 'bdo', 'blockquote',
        'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del',
        'details', 'dfn', 'div', 'dialog', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'footer',
        'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'hr', 'html', 'i', 'iframe', 'img', 'input',
        'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'nonscript',
        'object', 'ol', 'optgroup', 'option',  'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby',
        's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary',
        'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
        'track', 'u', 'ul', 'var', 'video', 'wbr']
))

LIST_TAGS: tuple[str, ...] = ('ul', 'ol')

LIST_ITEM_TAGS = ('li', )

SELECT_TAGS: tuple[str, ...] = ('option', 'optgroup')

DATALIST_TAGS: tuple[str, ...] = ('option',)

STRUCTURE_TAGS: tuple[str, ...] = ("html", "head", "title", "body")

HEAD_AND_BODY_TAGS: tuple[str, ...] = ("style", "script")

METADATA_TAGS: tuple[str, ...] = ('meta', 'script', 'style', 'noscript')

HEAD_ONLY_TAGS: tuple[str, ...] = ("meta", "link", "title", "base")

UNIQUE_TAGS: tuple[str, ...] = ("html", "body", "head", "title", "base", "main")

TABLE_TAGS: tuple[str, ...] = ('thead', 'tbody', 'td', 'tr', 'tfoot', 'th')

FORMAT_TAGS: tuple[str, ...] = ('b', 'em', 'strong', 'i', 'mark', 'small', 'del', 'ins', 'sub', 'sup', 'u')

BODY_TAGS: tuple[str, ...] = tuple([tag for tag in TAGS if not tag in [*STRUCTURE_TAGS, *HEAD_ONLY_TAGS]])

BODY_ONLY_TAGS: tuple[str, ...] = tuple([tag for tag in BODY_TAGS if not tag in HEAD_AND_BODY_TAGS])

VOID_TAGS: tuple[str, ...] = (
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source',
        'track', 'wbr'
)
SEMANTIC_TAGS: tuple[str, ...] = ('nav', 'section', 'footer', 'header', 'aside', 'article')

CONTENT_TAGS: tuple[str, ...] = ('div', 'table', 'ul', 'ol', 'details')

DETAILS_TAGS: tuple[str, ...] = ('sumary', 'p')

FORM_FIELD_TAGS: tuple[str, ...] = ('input', 'select', 'textarea')

INPUT_TYPES: tuple[str, ...] = ('button', 'checkbox', 'color', 'date', 'datetime-local', 'email', 'file', 'hidden',
                                'image', 'month', 'number', 'password', 'radio', 'range', 'reset', 'search', 'submit',
                                'tel', 'text', 'time', 'url', 'week')

FORM_TAGS: tuple[str, ...] = (*FORM_FIELD_TAGS, 'label', 'fieldset', 'button')

GLOBAL_ATTRIBUTES = ('accesskey', 'class', 'contenteditable', 'data-*', 'dir', 'draggable', 'enterkeyhint', 'hidden',
                     'id', 'inert', 'inputmode', 'lang', 'popover', 'spellcheck', 'style', 'tabindex', 'title',
                     'translate')

BOOLEAN_ATTRIBUTES = ("allowfullscreen", "async", "autofocus", "autoplay", "checked", "controls", "default", "defer",
                      "disabled", "formnovalidate", "inert", "ismap", "itemscope", "loop", "multiple", "muted",
                      "nomodule", "novalidate", "open", "playsinline", "readonly", "required", "reversed", "selected")

HTML_NON_GLOBAL_ATTRIBUTES_ELEMENT_MAP = {
        "accept": ['input'],
        "accept-charset": ['form'],
        "action": ["form"],
        "allow": ["iframe"],
        "alt": ["area", "img", "input"],
        "async": ["script"],
        "autocomplete": ["form", "input", "select", "textarea"],
        "autofocus": ["button", "input", "select", "textarea"],
        "autoplay": ["audio", "video"],
        "background": ["body", "table", "td", "th"],
        "bgcolor": ["body", "col", "colgroup", "marquee", "table", "tbody", "tfoot", "td", "th", "tr"],
        "boder": ["img", "object", "table"],
        "capture": ["input"],
        "charset": ["meta", "script"],
        "checked": ["input"],
        "cite": ["blockquote", "del", "ins", "q"],
        "color": ["font", "hr"],
        "cols": ["textarea"],
        "colspan": ["td", "th"],
        "children": ["meta"],
        "controls": ["audio", "video"],
        "coords": ["area"],
        "crossorigin": ["link", "script", "audio", "img", "video"],
        "csp": ["iframe"],
        "data": ["object"],
        "datetime": ["del", "ins", "time"],
        "decoding": ["img"],
        "default": ["track"],
        "defer": ["script"],
        "dirname": ["textarea", "input"],
        "disabled": ["button", "fildset", "input", "optgroup", "option", "select", "textarea"],
        "download": ["a", "area"],
        "enctype": ["form"],
        "enterkeyhint": ["textarea", "contenteditable"],
        "for": ["label", "output"],
        "form": ["button", "fieldset", "input", "label", "meter", "object", "output", "progress", "select", "textarea"],
        "formaction": ["button", "input"],
        "formenctype": ["button", "input"],
        "formethod": ["button", "input"],
        "formnovalidate": ["button", "input"],
        "formtarget": ["button", "input"],
        "headers": ["td", "th"],
        "height": ["canvas", "embed", "iframe", "img", "input", "object", "video"],
        "high": ["meter"],
        "href": ["a", "area", "base", "link"],
        "hreflang": ["a", "link"],
        "http-equiv": ["meta"],
        "integrity": ["link", "script"],
        "intrinsicsize": ["img"],
        "inputmode": ["textarea", "contenteditable"],
        "ismap": ["img"],
        "kind": ["track"],
        "label": ["track", "option", "optgroup"],
        "language": ["script"],
        "loading": ["img", "iframe"],
        "list": ["input"],
        "loop": ["audio", "video", "marquee"],
        "low": ["meter"],
        "manifest": ["html"],
        "max": ["input", "meter", "progress"],
        "maxlenght": ["input", "textarea"],
        "minlenght": ["input", "textarea"],
        "media": ["a", "area", "link", "source", "style"],
        "method": ["form"],
        "min": ["input", "meter"],
        "multiple": ["input", "select"],
        "muted": ["video", "audio"],
        "name": ["button", "fieldset", "form", "iframe", "input", "map", "meta", "object", "output", "param", "select", "textarea"],
        "nonvalidate": ["form"],
        "open": ["details", "dialog"],
        "optimum": ["meter"],
        "pattern": ["input"],
        "ping": ["a", "area"],
        "placeholder": ["input", "textarea"],
        "playsinline": ["video"],
        "popovertarget": ["button", "input"],
        "popovertargetaction": ["audio", "video"],
        "poster": ["video"],
        "preload": ["audio", "video"],
        "readonly": ["input", "textarea"],
        "referrerpolicy": ["a", "area", "iframe", "img", "link", "script"],
        "rel": ["a", "area", "form", "link"],
        "required": ["input", "select", "textarea"],
        "reversed": ["ol"],
        "rows": ["textarea"],
        "rowspan": ["td", "th"],
        "sandbox": ["iframe"],
        "scope": ["th"],
        "scoped": ["style"],
        "selected": ["option"],
        "shape": ["area"],
        "size": ["input", "select"],
        "sizes": ["img", "link", "source"],
        "slot": ["col", "colgroup"],
        "span": ["col", "colgroup"],
        "src": ["audio", "embed", 'iframe', "img", "input", "script", "source", "track", "video"],
        "srcdoc": ["iframe"],
        "srclang": ["track"],
        "srcset": ["img", "source"],
        "start": ["ol"],
        "step": ["input"],
        "sumary": ["tagle"],
        "target": ["a", "area", "base", "form"],
        "type": ["button", "embed", "input", "link", "menu", "object", "script", "source", "style"],
        "usermap": ["img", "object", "input"],
        "value": ["button", "input", "li", "option", "meter", "progress", "param", "data"],
        "width": ["canvas", "embed", "iframe", "img", "input", "object", "video"],
        "wrap": ["textarea"],
    
}

ENUMERATED_ATTRIBUTES = {
        "html": {
                "autocomplete": ["on", "off"],
                "border": ["1", ""],
                "contenteditable": ["true", "false", ""],
                "crossorigin": ["anonymous", "use-credentials"],
                "dir": ["ltr", "rtl", "auto"],
                "draggable": ["true", "false", "auto"],
                "enctype": ["application/x-www-form-urlencoded", "multipart/form-data", "text/plain"],
                "formenctype": ["application/x-www-form-urlencoded", "multipart/form-data", "text/plain"],
                "formmethod": ["get", "post", "dialog"],
                "formtarget": ["_blank", "_self", "_parent", "_top"],
                "inputmode": ["verbatim", "latin", "latin-name", "latin-prose", "full-width-latin", "kana", "kana-name",
                              "katakana", "numeric", "tel", "email", "url"],
                "kind": ["subtitles", "captions", "descriptions", "chapters", "metadata"],
                "link": ["alternate", "author", "bookmark", "external", "help", "icon", "license", "next", "nofollow",
                         "noopener", "noreferrer", "prefetch", "prev", "search", "stylesheet", "tag"],
                "method": ["get", "post", "dialog"],
                "preload": ["none", "metadata", "auto"],
                "referrerpolicy": ["no-referrer", "no-referrer-when-downgrade", "same-origin", "origin",
                                   "strict-origin", "origin-when-cross-origin", "strict-origin-when-cross-origin",
                                   "unsafe-url", ""],
                "rel": {
                        "a": ["alternate", "author", "bookmark", "external", "help", "icon", "license", "next",
                              "nofollow", "noopener", "noreferrer", "prefetch", "prev", "search", "stylesheet", "tag"],
                        "area": ["alternate", "author", "bookmark", "external", "help", "icon", "license", "next",
                                 "nofollow", "noopener", "noreferrer", "prefetch", "prev", "search", "stylesheet",
                                 "tag"],
                        "link": ["alternate", "dns-prefetch", "icon", "next", "pingback", "preconnect", "prefetch",
                                 "preload", "prerender", "search", "serviceworker", "stylesheet"]
                },
                "rev": ["alternate", "author", "bookmark", "external", "help", "icon", "license", "next", "nofollow",
                        "noopener", "noreferrer", "prefetch", "prev", "search", "stylesheet", "tag"],
                "role": ["alert", "alertdialog", "application", "article", "banner", "button", "cell", "checkbox",
                         "columnheader", "combobox", "complementary", "contentinfo", "definition", "dialog",
                         "directory", "document", "feed", "figure", "form", "grid", "gridcell", "group", "heading",
                         "img", "link", "list", "listbox", "listitem", "log", "main", "marquee", "math", "menu",
                         "menubar", "menuitem", "menuitemcheckbox", "menuitemradio", "navigation", "none", "note",
                         "option", "presentation", "progressbar", "radio", "radiogroup", "region", "row", "rowgroup",
                         "rowheader", "scrollbar", "search", "searchbox", "separator", "slider", "spinbutton", "status",
                         "switch", "tab", "table", "tabpanel", "term", "textbox", "timer", "toolbar", "tooltip", "tree",
                         "treegrid", "treeitem"],
                "sandbox": ["allow-forms", "allow-pointer-lock", "allow-popups", "allow-presentation",
                            "allow-same-origin", "allow-scripts", "allow-top-navigation"],
                "shape": ["circle", "circ", "default", "poly", "polygon", "rect", "rectangle"],
                "spellcheck": ["true", "false", ""],
                "target": ["_blank", "_self", "_parent", "_top"],
                "translate": ["yes", "no", ""],
                "type": {
                        "input": ["hidden", "text", "search", "tel", "url", "email", "password", "date", "month",
                                  "week", "time", "datetime-local", "number", "range", "color", "checkbox", "radio",
                                  "file", "submit", "image", "reset", "button"],
                        "ol": ["decimal", "lower-alpha", "upper-alpha", "lower-roman", "upper-roman"]
                },
                "wrap": ["soft", "hard", "off"]
        },
        "wai-aria": {
                "aria-autocomplete": ["inline", "list", "both", "none"],
                "aria-busy": ["true", "false"],
                "aria-checked": ["true", "false", "mixed", "undefined"],
                "aria-current": ["page", "step", "location", "date", "time", "true", "false"],
                "aria-disabled": ["true", "false"],
                "aria-expanded": ["true", "false", "undefined"],
                "aria-haspopup": ["true", "false", "menu", "listbox", "tree", "grid", "dialog"],
                "aria-hidden": ["true", "false", "undefined"],
                "aria-invalid": ["true", "false", "grammar", "spelling"],
                "aria-polite": ["assertive", "off", "polite"],
                "aria-modal": ["true", "false"],
                "aria-multiline": ["true", "false"],
                "aria-multiselectable": ["true", "false"],
                "aria-orientation": ["horizontal", "vertical", "undefined"],
                "aria-pressed": ["true", "false", "mixed", "undefined"],
                "aria-readonly": ["true", "false"],
                "aria-relevant": ["additions", "additions text", "all", "removals", "text"],
                "aria-required": ["true", "false"],
                "aria-selected": ["true", "false", "undefined"],
                "aria-sort": ["ascending", "descending", "none", "other"]
        }
}

HTML_ENUMERATED_ATTRIBUTES = ENUMERATED_ATTRIBUTES['html']

WAI_AREA_ENUMERATED_ATTRIBUTES = ENUMERATED_ATTRIBUTES['wai-aria']

HTMX_CORE_ATTRIBUTES = ('boost', 'get', 'on', 'post', 'push-url', 'select', 'select-oob', 'swap', 'swap-oob', 'target',
                        'trigger', 'vals')

HTMX_ADDITIONAL_ATTRIBUTES = ('confirm', 'delete', 'disable', 'disabled-elt', 'disiherit', 'encoding', 'ext', 'headers',
                              'history', 'history-elt', 'include', 'indicator', 'params', 'patch', 'preserve', 'prompt',
                              'put', 'replace-url', 'request', 'sse', 'sync', 'validate', 'vars', 'ws')

HTMX_ATTRIBUTES = tuple([*HTMX_CORE_ATTRIBUTES, *HTMX_ADDITIONAL_ATTRIBUTES])

