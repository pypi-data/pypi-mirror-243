# Markdown extensions
# Copyright 2019-2020 Gautam Iyer <gi1242+mdxmath@gmail.com>
# 
# Based on code originally written by Dmitry Shachnev <mitya57@gmail.com>
'''
Math and strike-through extensions for python-markdown

MathExtension: Ignores all elements between math markers. (Use MathJax/KaTeX in
    html to render the math)

DelExtension: Converts ~~text~~ to <del>text</del>

LinkExtension: [[WikiLinks]] modified so it allows [[link|label]] type links
'''

from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
from markdown.extensions.wikilinks import WikiLinkExtension, WikiLinksInlineProcessor
import xml.etree.ElementTree as etree

class inlineMathProcessor( InlineProcessor ):
    def handleMatch( self, m, _ ):
        # MathJAX handles all the math. Just set the uses_math flag, and
        # protect the contents from markdown expansion.
        setattr( self.md, 'uses_math',  True )
        return m.group(0), m.start(0), m.end(0)

class MathExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'enable_dollar_delimiter':
                [False, 'Enable single-dollar delimiter'],
        }
        super(MathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)

        mathRegExps = [
            r'(?<!\\)\\\((.+?)\\\)',    # \( ... \)
            r'(?<!\\)\$\$.+?\$\$',      # $$ ... $$
            r'(?<!\\)\\\[.+?\\\]',      # \[ ... \]
            r'(?<!\\)\\begin{([a-z]+?\*?)}.+?\\end{\1}',
        ]
        if self.getConfig('enable_dollar_delimiter'):
            md.ESCAPED_CHARS.append('$')
            mathRegExps.insert( 0, r'(?<!\\|\$)\$.+?\$' ) # $ ... $
        for i, pattern in enumerate(mathRegExps):
            # we should have higher priority than 'escape' which has 180
            md.inlinePatterns.register(
                inlineMathProcessor( pattern, md ), f'math-inline-{i}', 185)

        setattr( md, 'uses_math', False )
        self.md = md

    def reset(self):
        setattr( self.md, 'uses_math', False )


class DelInlineProcessor(InlineProcessor):
    def handleMatch(self, m, _):
        el = etree.Element('del')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class DelExtension(Extension):
    def extendMarkdown(self, md):
        DEL_PATTERN = r'~~(.*?)~~'  # like ~~del~~
        md.inlinePatterns.register(
            DelInlineProcessor(DEL_PATTERN, md), 'del', 175)

# Taken from markdown/extensions/wikilinks
class LinkExtension( WikiLinkExtension ):
    def extendMarkdown(self, md):
        self.md = md

        # append to end of inline patterns
        #WIKILINK_RE = r'\[\[([\w0-9_ -]+)\]\]'
        WIKILINK_RE = r'\[\[([\w0-9_ |:.(),/"-]+)\]\]'
        wikilinkPattern = LinksInlineProcessor(WIKILINK_RE, self.getConfigs())
        wikilinkPattern.md = md
        md.inlinePatterns.register(wikilinkPattern, 'wikilink', 75)

# Taken from markdown/extensions/wikilinks
class LinksInlineProcessor( WikiLinksInlineProcessor ):
    '''Modified so that build_url can return both URL and label'''
    def handleMatch( self, m, _ ):
        if m.group(1).strip():
            base_url, end_url, html_class = self._getMeta()
            label = m.group(1).strip()
            (url, label) = self.config['build_url'](label, base_url, end_url)
            a = etree.Element('a')
            a.text = label
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        else:
            a = ''
        return a, m.start(0), m.end(0)
