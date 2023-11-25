# Copyright 2023, Gautam Iyer. MIT Licence

import time, sys, re, logging
from html import escape
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy

# May need installation
import markdown, frontmatter, yaml
import jinja2 as j2

from . import mdx

# {{{ Logging
class CallCounted:
    """Decorator to determine number of calls for a method"""

    def __init__(self,method):
        self.method=method
        self.counter=0

    def __call__(self,*args,**kwargs):
        self.counter+=1
        return self.method(*args,**kwargs)

class CustomFormatter(logging.Formatter):
  """Logging Formatter to add colors and count warning / errors"""

  if sys.stdout.isatty():
    RE='\033[0m'
    ER='\033[0;31m'
    BD='\033[0;36m'
    UL='\033[0;32m'
    IT='\033[0;33m'
  else:
    (RE, ER, BD, UL, IT) = ['']*5

  fmt = "{levelname:.1s}: {message}"
  formatters = {
    logging.INFO: logging.Formatter(UL+fmt+RE, style='{' ),
    logging.WARNING: logging.Formatter(IT+fmt+RE, style='{' ),
    logging.ERROR: logging.Formatter(ER+fmt+RE, style='{' )
  }
  default_formatter = logging.Formatter( fmt, style='{' )

  def format(self, record):
    formatter = self.formatters.get( record.levelno, self.default_formatter )
    return formatter.format(record)
#}}}

# Helper functions
def merge_meta( old, new ):
  '''Merge new meta data (dict or namespace) with current (namespace)'''
  d = vars( deepcopy(old) )
  new_dict = vars(new) if type(new) == SimpleNamespace else new

  # Make lists extend old value, unless first element is '!!reset'
  for k, v in new_dict.items():
    if type(v) == list:
      if len(v) >= 1  and v[0] == '!!reset':
        # Clear old value
        del v[0]
      elif k in d and type(d[k]) == list and d[k] != v:
        # Extend old value
        #print( f'k={k}, new_dict[k]={v}, d[k] = {d[k]} (len={len(d[k])})' )
        d[k].extend( [x for x in v if x not in d[k]] ) 
        new_dict[k] = d[k]

  d.update( new_dict )
  return SimpleNamespace( **d )

def normalize_dirs( opts, cwd ):
  '''make directories relative to cwd'''
  if 'base_dir' in opts:
    opts['base_dir'] = cwd / opts['base_dir']
  if 'dst_dir' in opts:
    opts['dst_dir'] = cwd / opts['dst_dir']


class MarkdownConverter:
  globals = SimpleNamespace( 
    enable_mathjax=True,
    enable_codehilite=True,
    enable_jinja=False,
    jinja_header='''
      {%- import 'lightgallery.j2' as LightGallery -%}
    ''',
    template='simple',
    encoding='utf-8',
    base_url='',
    absolute_links=False,
    update=False,
    exclude_dirs=[
      '.git',
      '__pycache__',
      'templates',
      'reveal.js',
    ],
    exclude_files=[],
    protect_dirs=[
      'reveal.js',
    ],
    protect_files=[],
  )

  def __init__( self, globals={}, config_dirs=[] ):
    # Setup logging
    self.log = logging.getLogger("md-to-html")
    self.log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter() )
    self.log.addHandler( ch )
    self.log.error = CallCounted( self.log.error )

    self.globals = merge_meta( self.globals, globals )

    config_dirs.insert( 0, Path(__file__).parent )
    self.template_dirs = [ d / 'templates'  for d in config_dirs]
    self.env = j2.Environment(
      autoescape=j2.select_autoescape()
    )

    for d in config_dirs:
      cfgfile =  d / 'config.yaml'
      self.globals = self.read_config_file( cfgfile, self.globals )

  def resolve( self, attr, meta):
    '''Adds abs_{attr} to meta, pointing to resolved location of meta.{attr}'''
    if not hasattr( meta, f'abs_{attr}' ):
      setattr( meta, f'abs_{attr}', getattr( meta, attr ).resolve() )

  def build_url( self, meta, text ):
    '''Returns a URL and label given text of a wiki link'''
    sep = text.find('|')
    if( sep >= 0 ):
      link = text[:sep]
      label = text[sep+1:]
    else:
      link = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', text)
      label = Path( text ).name
      #label = os.path.basename(text)
    if link[0] == '/':
      src_path = meta.base_dir / link[1:]
      link = meta.base_url  + link
    else:
      src_path = meta.base_dir / meta.rel_src_dir / link
      if meta.absolute_links:
        self.resolve( 'base_dir', meta )
        link = meta.base_url + '/' + str(
            src_path.resolve().relative_to( meta.abs_base_dir ) )

    if not src_path.exists() or ( src_path.suffix == '.html' 
            and not src_path.with_suffix( '.md' ).exists() ):
      self.log.warning( f'{meta.src_file}: link {src_path} not found' )

    return ( link, label)

  def read_config_file( self, cfgfile:Path, meta=None, allow_exec=False, ignore_errors=True ):
    '''
    Merges new values from the config and meta, and returns the result
    '''
    if meta == None: meta = self.globals
    try:
      with cfgfile.open() as f:
        opts = yaml.load( f, Loader=yaml.CLoader )
        if allow_exec == False and 'exec' in opts:
          del opts['exec']

      normalize_dirs( opts, cfgfile.parent )
      return merge_meta( meta, opts )
    except FileNotFoundError:
      if ignore_errors==False:
        self.log.warning( f"Couldn't find {cfgfile}" )
      return meta


  def read_frontmatter( self, src:Path, dir_config=None ):
    """
    Read frontmatter from src, and return the metadata.
    Content is in meta.content
    """
    fm = frontmatter.load( src )

    src_dir = src.parent
    normalize_dirs( fm, src_dir )

    meta = self.read_config_file( src_dir / 'config.yaml' ) \
        if dir_config is None else dir_config
    meta = merge_meta( meta, fm.metadata )
    meta.content = fm.content

    # Put the destination file name in dst_filename
    meta.src_file = src
    if not hasattr( meta, 'base_dir' ): meta.base_dir = src_dir
    if not hasattr( meta, 'dst_dir' ): meta.dst_dir = meta.base_dir
    #if src.is_relative_to( meta['base_dir'] ):
    try:
      meta.rel_src_dir = src_dir.relative_to( meta.base_dir )
    except ValueError:
      # Normalize and try again
      self.resolve( 'base_dir', meta )
      meta.rel_src_dir = src_dir.resolve().relative_to( meta.abs_base_dir )

    meta.rel_dst_file = meta.rel_src_dir / src.with_suffix( '.html' ).name
    meta.dst_file = meta.dst_dir / meta.rel_dst_file

    return merge_meta( self.globals, meta )

  def convert( self, src:Path, meta=None, dir_config=None ):
    '''
    Convert src (markdown) into html. If meta is not provided, it is
    got from read_frontmatter().
    '''

    start = time.monotonic()
    #self.log.debug( f'Rendering {str(src)}...' )

    if meta is None: meta=self.read_frontmatter( src, dir_config )
    if meta.update and meta.dst_file.exists() and \
        (meta.src_file.stat().st_mtime < meta.dst_file.stat().st_mtime):
      #self.log.debug( f'{src} newer than {meta.dst_dir.name / meta.rel_dst_file}, skipping. '
      #    f'({(time.monotonic() - start)*1000:.0f}ms)' )
      return meta.dst_file

    # Fix template dirs
    template_dirs = self.template_dirs.copy()
    template_dirs.insert( 0,  src.parent / 'templates' )
    self.env.loader = j2.FileSystemLoader( template_dirs,
        followlinks=True )

    extensions = [
        'extra',
        'sane_lists',
        'smarty',
        'toc',
        mdx.LinkExtension(html_class='',
            build_url=lambda text, *_: self.build_url( meta, text ) ),
        mdx.DelExtension(),
      ]
    if meta.enable_codehilite:
      extensions.append( 'codehilite' )
    if meta.enable_mathjax:
      extensions.append( mdx.MathExtension(enable_dollar_delimiter=True) )

    md = markdown.Markdown( extensions=extensions )

    #self.md.reset()
    if meta.enable_jinja:
      meta.content = md.convert(
          self.env.from_string( meta.jinja_header + meta.content )
            .render( vars(meta) ) )
    else:
      meta.content = md.convert( meta.content )
    meta.toc = getattr( md, 'toc' )

    # Get title if needed
    if not hasattr( meta, 'title' ):
      for t in getattr( md, 'toc_tokens' ):
        if t['level'] == 1:
          meta.title = escape( t['name'], quote=False )
          break

    meta.uses_math = getattr( md, 'uses_math', False )
    meta.uses_codehilite = (meta.content.find( 'class="codehilite"' ) >= 0 )

    # Render the HTML
    template = self.env.get_template( meta.template + '.j2' )

    meta.dst_file.parent.mkdir( parents=True, exist_ok=True )
    template.stream( vars(meta) ).dump( str(meta.dst_file), meta.encoding )

    #self.log.debug( f'dst_file={meta.dst_file.resolve()}' )
    self.log.info( f'{src} → {meta.dst_dir.name / meta.rel_dst_file} '
        f'({(time.monotonic() - start)*1000:.0f}ms)' )
    return meta.dst_file

# vim: set sw=2 :
