from __future__ import annotations

from collections import namedtuple
from enum import Enum

    
class TagEnum(namedtuple('Tag', 'tagname void unique semantic structure headonly bodyonly metadata '
                                'formonly formattag attributes'), Enum):
    A = "a", False, False, False, False, False, True, False, False, False, ['download', 'href', 'hreflang', 'media',
                                                                            'rel', 'target', 'type']
    ABBR = "abbr", False, False, False, False, False, True, False, False, False, []
    ADDRESS = "address", False, False, False, False, False, True, False, False, False, []
    AREA = "area", True, False, False, False, False, True, False, False, False, ['alt', 'coords', 'download', 'href',
                                                                                 'hreflang', 'media', 'rel', 'shape',
                                                                                 'target']
    ARTICLE = "article", False, False, True, False, False, True, False, False, False, []
    ASIDE = "aside", False, False, True, False, False, True, False, False, False, []
    AUDIO = "audio", False, False, False, False, False, True, False, False, False, ['autoplay', 'controls', 'loop',
                                                                                    'muted', 'popovertargetaction',
                                                                                    'preload', 'src']
    B = "b", False, False, False, False, False, True, False, False, True, []
    BASE = "base", True, True, False, False, True, False, False, False, False, ['href', 'target']
    BDI = "bdi", False, False, False, False, False, True, False, False, False, []
    BDO = "bdo", False, False, False, False, False, True, False, False, False, []
    BLOCKQUOTE = "blockquote", False, False, False, False, False, True, False, False, False, ['cite']
    BODY = "body", False, True, False, True, False, False, False, False, False, ['link', 'alink', 'vlink', 'background',
                                                                                 'bgcolor', 'text']
    BR = "br", True, False, False, False, False, True, False, False, False, []
    BUTTON = "button", False, False, False, False, False, True, False, True, False, ['autofocus', 'disable',
                                                                                     'formaction', 'name',
                                                                                     'popovertarget', 'type', 'value']
    CANVAS = "canvas", False, False, False, False, False, True, False, False, False, ['height', 'width']
    CAPTION = "caption", False, False, False, False, False, True, False, False, False, []
    CITE = "cite", False, False, False, False, False, True, False, False, False, []
    CODE = "code", False, False, False, False, False, True, False, False, False, []
    COL = "col", True, False, False, False, False, True, False, False, False, ['span']
    COLGROUP = "colgroup", False, False, False, False, False, True, False, False, False, ['span']
    DATA = "data", False, False, False, False, False, True, False, False, False, []
    DATALIST = "datalist", False, False, False, False, False, True, False, False, False, []
    DD = "dd", False, False, False, False, False, True, False, False, False, []
    DEL = "del", False, False, False, False, False, True, False, False, True, ['cite', 'datetime']
    DETAILS = "details", False, False, False, False, False, True, False, False, False, ['open']
    DFN = "dfn", False, False, False, False, False, True, False, False, False, []
    DIALOG = "dialog", False, False, False, False, False, True, False, False, False, []
    DIV = "div", False, False, False, False, False, True, False, False, False, []
    DL = "dl", False, False, False, False, False, True, False, False, False, []
    DT = "dt", False, False, False, False, False, True, False, False, False, []
    EM = "em", False, False, False, False, False, True, False, False, True, []
    EMBED = "embed", True, False, False, False, False, True, False, False, False, ['height', 'src', 'type', 'width']
    FIELDSET = "fieldset", False, False, False, False, False, True, False, True, False, ['name']
    FIGCAPTION = "figcaption", False, False, False, False, False, True, False, False, False, []
    FIGURE = "figure", False, False, False, False, False, True, False, False, False, []
    FOOTER = "footer", False, False, True, False, False, True, False, False, False, []
    FORM = "form", False, False, False, False, False, True, False, False, False, ['accept-charset', 'action',
                                                                                  'autocomplete', 'enctype', 'method',
                                                                                  'name', 'nonvalidate', 'rel',
                                                                                  'target']
    H1 = "h1", False, False, False, False, False, True, False, False, False, []
    H2 = "h2", False, False, False, False, False, True, False, False, False, []
    H3 = "h3", False, False, False, False, False, True, False, False, False, []
    H4 = "h4", False, False, False, False, False, True, False, False, False, []
    H5 = "h5", False, False, False, False, False, True, False, False, False, []
    H6 = "h6", False, False, False, False, False, True, False, False, False, []
    HEAD = "head", False, True, False, True, False, False, False, False, False, []
    HR = "hr", True, False, False, False, False, True, False, False, False, ['noshade', 'size', 'width']
    HTML = "html", False, True, False, True, False, False, False, False, False, []
    I = "i", False, False, False, False, False, True, False, False, True, []
    IFRAME = "iframe", False, False, False, False, False, True, False, False, False, ['height', 'name', 'sandbox',
                                                                                      'src', 'srcdoc', 'width']
    IMG = "img", True, False, False, False, False, True, False, False, False, ['alt', 'height', 'ismap', 'sizes', 'src',
                                                                               'srcset', 'usermap', 'width', 'border',
                                                                               'hspace', 'vspace']
    INPUT = "input", True, False, False, False, False, True, False, True, False, ['accept', 'alt', 'autocomplete',
                                                                                  'autofocus', 'checked', 'dirname',
                                                                                  'disable', 'formaction', 'height',
                                                                                  'list', 'max', 'maxlenght', 'min',
                                                                                  'multiple', 'name', 'pattern',
                                                                                  'placeholder', 'popovertarget',
                                                                                  'readonly', 'required', 'size', 'src',
                                                                                  'step', 'type', 'value', 'width']
    INS = "ins", False, False, False, False, False, True, False, False, True, ['cite', 'datetime']
    KBD = "kbd", False, False, False, False, False, True, False, False, False, []
    LABEL = "label", False, False, False, False, False, True, False, True, False, []
    LEGEND = "legend", False, False, False, False, False, True, False, False, False, []
    LI = "li", False, False, False, False, False, True, False, False, False, ['value']
    LINK = "link", True, False, False, False, True, False, False, False, False, ['href', 'hreflang', 'media', 'rel',
                                                                                 'sizes', 'type']
    MAIN = "main", False, True, False, False, False, True, False, False, False, []
    MAP = "map", False, False, False, False, False, True, False, False, False, ['name']
    MARK = "mark", False, False, False, False, False, True, False, False, True, []
    META = "meta", True, False, False, False, True, False, True, False, False, ['charset', 'content', 'http-equiv',
                                                                                'name']
    METER = "meter", False, False, False, False, False, True, False, False, False, ['high', 'low', 'max', 'min',
                                                                                    'optimum', 'value']
    NAV = "nav", False, False, True, False, False, True, False, False, False, []
    NONSCRIPT = "nonscript", False, False, False, False, False, True, False, False, False, []
    OBJECT = "object", False, False, False, False, False, True, False, False, False, ['data', 'height', 'name', 'type',
                                                                                      'usermap', 'width']
    OL = "ol", False, False, False, False, False, True, False, False, False, ['reversed', 'start']
    OPTGROUP = "optgroup", False, False, False, False, False, True, False, False, False, ['disable', 'label']
    OPTION = "option", False, False, False, False, False, True, False, False, False, ['value']
    OUTPUT = "output", False, False, False, False, False, True, False, False, False, ['name']
    P = "p", False, False, False, False, False, True, False, False, False, []
    PARAM = "param", True, False, False, False, False, True, False, False, False, ['name', 'value']
    PICTURE = "picture", False, False, False, False, False, True, False, False, False, []
    PRE = "pre", False, False, False, False, False, True, False, False, False, ['width']
    PROGRESS = "progress", False, False, False, False, False, True, False, False, False, ['max', 'value']
    Q = "q", False, False, False, False, False, True, False, False, False, ['cite']
    RP = "rp", False, False, False, False, False, True, False, False, False, []
    RT = "rt", False, False, False, False, False, True, False, False, False, []
    RUBY = "ruby", False, False, False, False, False, True, False, False, False, []
    S = "s", False, False, False, False, False, True, False, False, False, []
    SAMP = "samp", False, False, False, False, False, True, False, False, False, []
    SCRIPT = "script", False, False, False, False, False, False, True, False, False, ['async', 'charset', 'defer',
                                                                                      'src', 'type']
    SECTION = "section", False, False, True, False, False, True, False, False, False, []
    SELECT = "select", False, False, False, False, False, True, False, True, False, ['autofocus', 'disable', 'multiple',
                                                                                     'name', 'required', 'size']
    SMALL = "small", False, False, False, False, False, True, False, False, True, []
    SOURCE = "source", True, False, False, False, False, True, False, False, False, ['media', 'sizes', 'src', 'srcset',
                                                                                     'type']
    SPAN = "span", False, False, False, False, False, True, False, False, False, []
    STRONG = "strong", False, False, False, False, False, True, False, False, True, []
    STYLE = "style", False, False, False, False, False, False, True, False, False, ['media', 'type']
    SUB = "sub", False, False, False, False, False, True, False, False, True, []
    SUMMARY = "summary", False, False, False, False, False, True, False, False, False, []
    SUP = "sup", False, False, False, False, False, True, False, False, True, []
    SVG = "svg", False, False, False, False, False, True, False, False, False, []
    TABLE = "table", False, False, False, False, False, True, False, False, False, ['bgcolor', 'border', 'cellpadding',
                                                                                    'frame', 'rules', 'summary', 'width']
    TBODY = "tbody", False, False, False, False, False, True, False, False, False, []
    TD = "td", False, False, False, False, False, True, False, False, False, ['colspan', 'headers', 'rowspan']
    TEMPLATE = "template", False, False, False, False, False, True, False, False, False, []
    TEXTAREA = "textarea", False, False, False, False, False, True, False, True, False, ['autofocus', 'cols', 'dirname',
                                                                                         'disable', 'maxlenght', 'name',
                                                                                         'placeholder', 'readonly',
                                                                                         'required', 'rows', 'wrap']
    TFOOT = "tfoot", False, False, False, False, False, True, False, False, False, []
    TH = "th", False, False, False, False, False, True, False, False, False, ['colspan', 'headers', 'rowspan', 'scope']
    THEAD = "thead", False, False, False, False, False, True, False, False, False, []
    TIME = "time", False, False, False, False, False, True, False, False, False, ['datetime']
    TITLE = "title", False, True, False, True, True, False, False, False, False, []
    TR = "tr", False, False, False, False, False, True, False, False, False, []
    TRACK = "track", True, False, False, False, False, True, False, False, False, ['default', 'kind', 'label', 'src',
                                                                                   'srclang']
    U = "u", False, False, False, False, False, True, False, False, True, []
    UL = "ul", False, False, False, False, False, True, False, False, False, []
    VAR = "var", False, False, False, False, False, True, False, False, False, []
    VIDEO = "video", False, False, False, False, False, True, False, False, False, ['autoplay', 'controls', 'height',
                                                                                    'loop', 'muted',
                                                                                    'popovertargetaction', 'poster',
                                                                                    'preload', 'src', 'width']
    WBR = "wbr", True, False, False, False, False, True, False, False, False, []
    
    @property
    def head(self):
        return self.tagname == 'head'
    
    @property
    def body(self):
        return self.tagname == 'body'
    
    @property
    def form(self):
        return self.tagname == 'form'
    
    @property
    def html(self):
        return self.tagname == 'html'
    
