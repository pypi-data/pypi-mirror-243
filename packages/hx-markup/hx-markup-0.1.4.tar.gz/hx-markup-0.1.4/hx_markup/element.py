from __future__ import annotations

import dataclasses
import io
from collections.abc import Sequence
from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, TypeVar

from hx_markup import functions
from hx_markup import enums


@dataclasses.dataclass
class RenderBase(ABC):
    
    def __str__(self):
        return functions.remove_extra_whitespaces(self.render())
    @abstractmethod
    def render(self) -> str:...
    
    def __html__(self):
        return str(self)
    
    
@dataclasses.dataclass
class StyleStatement(RenderBase):
    target: str
    properties: dict[str, str]
    
    def render(self) -> str:
        return f'{self.target} {{{functions.join_style_attrs(self.properties)}}}'


@dataclasses.dataclass
class ScriptFunction(RenderBase):
    name: str | None = None
    args: str | None = None
    statements: list[str, ScriptFunction] = dataclasses.field(default_factory=list)
    
    def render(self) -> str:
        with io.StringIO() as f:
            if self.name:
                f.write(f'function {self.name}')
            else:
                f.write(f'function')
            if self.args:
                f.write(f'({functions.join(self.args.split(), sep=", ")})')
            else:
                f.write('()')
            f.write(f'{{{functions.join(self.statements, sep="; ")}}}')
            return f.getvalue()
    
    
@dataclasses.dataclass
class BaseElement(RenderBase):

    def __post_init__(self):
        if booleans:= getattr(self, 'booleans'):
            if isinstance(booleans, str):
                self.booleans = functions.split_words(booleans)


ElementType = TypeVar('ElementType', bound=BaseElement)


@dataclasses.dataclass
class Script(BaseElement):
    id: Optional[str] = None
    booleans: list[str] | str |  None = dataclasses.field(default_factory=list)
    keywords: dict[str, str] | None = dataclasses.field(default_factory=dict)
    statements: list[str, ScriptFunction] | None = dataclasses.field(default_factory=list)
    
    @property
    def render_booleans(self):
        return functions.join([
                i for i in self.booleans
                if all([functions.is_boolean_attr(i), functions.attr_element_match(i, 'script')])])
    
    @property
    def render_keywords(self):
        return functions.join_html_keyword_attrs(self.keywords)
    
    @property
    def render_config(self):
        with io.StringIO() as f:
            if self.id:
                f.write(f' id="{self.id}"')
            if self.booleans:
                f.write(f' {self.render_booleans}')
            if self.keywords:
                f.write(f' {self.render_keywords}')
            return f.getvalue()
            
    def render(self) -> str:
        with io.StringIO() as f:
            f.write(f'<script {self.render_config}>')
            if self.statements:
                f.write(' ')
                f.write(functions.join(self.statements, sep="; "))
            f.write('</script>')
            return f.getvalue()

@dataclasses.dataclass
class Style(BaseElement):
    id: Optional[str] = None
    booleans: list[str] | str |  None = dataclasses.field(default_factory=list)
    keywords: dict[str, str] | None = dataclasses.field(default_factory=dict)
    vars: dict[str, str] | None = dataclasses.field(default_factory=dict)
    statements: list[StyleStatement] | None = dataclasses.field(default_factory=list)
    
    @property
    def render_booleans(self):
        return functions.join([
                i for i in self.booleans
                if all([functions.is_boolean_attr(i), functions.attr_element_match(i, 'style')])])
    
    @property
    def render_keywords(self):
        return functions.join_html_keyword_attrs(self.keywords)
    
    @property
    def render_config(self):
        with io.StringIO() as f:
            if self.id:
                f.write(f' id="{self.id}"')
            if self.booleans:
                f.write(f' {self.render_booleans}')
            if self.keywords:
                f.write(f' {self.render_keywords}')
            return f.getvalue()
            
    
    @classmethod
    def var_name(cls, key: str):
        return f'--{functions.slug_to_kebab_case(key)}'
        
    def render(self) -> str:
        with io.StringIO() as f:
            f.write(f'<style {self.render_config}>')
            if self.vars:
                f.write(' ')
                f.write(f':root {{{functions.join({self.var_name(k): v for k, v in self.vars.items()}, sep="; ", junction=": ")}}}')
            if self.statements:
                f.write(' ')
                f.write(functions.join(self.statements))
            f.write('</style>')
            return f.getvalue()
            

@dataclasses.dataclass
class Element(BaseElement):
    tag: str
    id: Optional[str] = None
    booleans: list[str] | str |  None = dataclasses.field(default_factory=list)
    classlist: list[str] | str | None = dataclasses.field(default_factory=list)
    keywords: dict[str, str] | None = dataclasses.field(default_factory=dict)
    htmx: dict[str, str] | None = dataclasses.field(default_factory=dict)
    dataset: dict[str, str] | None = dataclasses.field(default_factory=dict)
    styles: dict[str, str] | None = dataclasses.field(default_factory=dict)
    content: deque[str | ElementType] | list[str | ElementType] | str | ElementType = dataclasses.field(default_factory=deque)
    
    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.classlist, str):
            self.classlist = functions.split_words(self.classlist)
        if not isinstance(self.content, deque):
            if isinstance(self.content, (str, Element)):
                self.content = deque([self.content])
            elif isinstance(self.content, Sequence):
                self.content = deque([*self.content])

    @property
    def tag_enum(self):
        return enums.TagEnum[self.tag.upper()]

    @property
    def render_config(self):
        with io.StringIO() as f:
            if self.id:
                f.write(f' id="{self.id}"')
            if self.booleans:
                f.write(' ')
                f.write(functions.join([
                        i for i in self.booleans
                        if all([functions.is_boolean_attr(i), functions.attr_element_match(i, self.tag_enum.tagname)])]))
            if self.keywords:
                f.write(' ')
                f.write(functions.join_html_keyword_attrs({
                        functions.slug_to_kebab_case(k): v
                        for k, v in self.keywords.items()
                        if k != 'id'
                        if all([not functions.is_boolean_attr(k), functions.attr_element_match(k, self.tag_enum.tagname)])}))
            if self.classlist:
                f.write(' ')
                f.write(f'class="{functions.join(functions.filter_uniques(self.classlist))}"')
            if self.dataset:
                f.write(' ')
                f.write(functions.join_html_dataset_attrs(self.dataset))
            if self.htmx:
                f.write(' ')
                f.write(functions.join_htmx_attrs({k:v for k, v in self.htmx.items() if functions.is_htmx_attr(k)}))
            if self.styles:
                f.write(' ')
                f.write(f'style="{functions.join_style_attrs(self.styles)}"')
            return f.getvalue()

    @property
    def render_content(self):
        with io.StringIO() as f:
            if self.tag_enum.tagname == 'script':
                f.write(functions.join(self.content, sep="; "))
            else:
                f.write(functions.join(self.content))
            return f.getvalue()
        
    def render(self) -> str:
        with io.StringIO() as f:
            f.write(f'<{self.tag_enum.tagname} {self.render_config}>')
            if not self.tag_enum.void:
                f.write(self.render_content)
                f.write(f'</{self.tag_enum.tagname}>')
            return f.getvalue()
            



