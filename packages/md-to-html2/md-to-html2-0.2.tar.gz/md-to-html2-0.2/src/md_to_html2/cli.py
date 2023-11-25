#! /usr/bin/python
# Command line interface to md-to-html
# Copyright 2023, Gautam Iyer. MIT Licence

import argparse, logging, sys, subprocess, time
import concurrent.futures
from pathlib import Path
from types import SimpleNamespace
from multiprocessing import Pool

# May need installing
from jinja2.exceptions import TemplateSyntaxError, TemplateNotFound, \
    TemplateError
from yaml.parser import ParserError
from yaml.scanner import ScannerError
from xdg.BaseDirectory import load_config_paths

from .mdconvert import MarkdownConverter, merge_meta

def process_file_or_dir( fn ):
  if type( fn ) == str: fn = Path(fn)
  if fn.is_dir(): process_dir( fn )
  elif fn.is_file(): process_file_bg( fn )

def process_dir( dir:Path, root=None ):
  if root is None: root = getattr( md.globals, 'base_dir', dir )
  dir_config = md.read_config_file( dir / 'config.yaml', meta=md.globals )
  meta = merge_meta( md.globals, dir_config )
  #md.log.debug( f'dir={dir}, dir_config={meta}' )
  for child in dir.iterdir():
    c = '/'/child.relative_to(root)
    #md.log.debug( f'Examining {c} (root={root})' )
    if child.is_dir() and not child.is_symlink():
      if all( [ not c.match( pat ) for pat in meta.exclude_dirs ] ):
        # Descend
        process_dir( child, root )

    elif child.suffix == '.md' and child.is_file() and \
        all( [ not c.match( pat ) for pat in meta.exclude_files ] ):
      process_file_bg( child, dir_config=dir_config )

def store_processed_files( job ):
  res = job.result()
  if res is not None: outputs.append( res )

def process_file_bg( fn, dir_config=None ):
  #md.log.debug( f'process_file_bg( fn={fn} )' )
  job = executor.submit( process_file, fn, dir_config )
  job.add_done_callback( store_processed_files )

def process_file( fn:Path, dir_config=None ):
  try:
    if fn.suffix == '.md':
      meta = md.read_frontmatter( fn )
      #md.log.debug( f'Metadata in {fn}: {meta}' )
      if args.resize and getattr( meta, 'resize_images', False):
        resize_images( fn, meta )

      return md.convert( fn, meta=meta, dir_config=dir_config )

    elif fn.suffix == '.yaml':
      md.globals = md.read_config_file( fn, meta=md.globals,
          allow_exec=True, ignore_errors=False )

    else:
      md.log.warning( f'Ignoring {fn} (not .yaml or .md)' )
      
  except (TemplateError, TemplateNotFound, TemplateSyntaxError) as e:
    lineno = f':{e.lineno-2}' if hasattr( e, 'lineno' ) else '' #type: ignore
    md.log.error( f'{fn}{lineno} {e.__class__.__name__}: {e.message}' )

  except FileNotFoundError as e:
    md.log.error( f'{fn}: {e.strerror}' )

  except (ParserError, ScannerError) as e:
    md.log.error( f'{fn}: {str(e)}' )
    if fn.suffix == '.yaml':
      sys.exit()

def delete_empty_dirs( root:Path, dir:Path ):
  while dir.is_relative_to( root ):
    try:
      dir.rmdir()
      dir = dir.parent
    except OSError:
      break

def delete_extra_files( root:Path, dir:Path ):
  count = 0
  for child in dir.iterdir():
    count += 1
    c = '/' / child.relative_to(root)
    if child.is_dir() and not child.is_symlink():
      if all( [ not c.match( pat ) for pat in md.globals.protect_dirs ] ):
        # Descend
        delete_extra_files( root, child )
    elif child.suffix == '.html' and child.is_file() and \
        all( [ not c.match( pat ) for pat in md.globals.protect_files ] ) and \
        child not in outputs:
      if args.delete_extra:
        md.log.warning( f'Removing extra file {child}' )
        child.unlink()
      else:
        md.log.warning( f'Extra file {child}' )
      count -= 1

  if count == 0:
      if args.delete_extra:
        md.log.warning( f'Removing empty directory {dir}' )
        delete_empty_dirs( root, dir )
      else:
        md.log.warning( f'Empty directory {dir}' )

def resize( img_file, d ):
  orig = d.orig_dir / img_file
  img = d.img_dir / img_file
  thumb = d.thumb_dir / img_file

  if orig.exists():
    im = None
    if args.force_resize or not img.exists() or \
        (img.stat().st_mtime < orig.stat().st_mtime):
      md.log.info( f'Generating {img}' )
      im = Image.open( orig )
      rescaled = im.copy()
      rescaled.thumbnail( (d.img_width, d.img_height) )
      rescaled.save( img, quality=d.img_quality )

    if args.force_resize or not thumb.exists() or \
        (thumb.stat().st_mtime < orig.stat().st_mtime):
      md.log.info( f'Generating {thumb}' )
      if im is None: im = Image.open( orig )

      if d.thumb_method == 'crop':
        # Crop so that thumbnail is exactly the given size
        ow, oh = im.size
        new_width = int( oh * d.thumb_width / d.thumb_height )
        if new_width <= ow:
          offset = int( (ow - new_width) / 2 )
          im = im.resize( (d.thumb_width, d.thumb_height),
              box=( offset, 0, new_width+offset, oh ) )
        else:
          new_height = int( ow * d.thumb_height / d.thumb_width )
          offset = int( (oh - new_height) / 2 )
          im = im.resize( (d.thumb_width, d.thumb_height),
              box=( 0, offset, ow, new_height+offset ) )
      else:
        # Scale so that largest dimension is at most whats given
        im.thumbnail( (d.thumb_width, d.thumb_height) )
      im.save( thumb, quality=d.thumb_quality )
  else:
    md.log.error( f"Couldn't find {orig}" )

def resize_images( fn, meta ):
  global Image
  try: 
    import PIL.Image as Image
  except:
    md.log.error( 'Need module Pillow to resize images' )
    return


  md.log.debug( f'Resizing images in {fn}' )
  try:
    data = SimpleNamespace( 
      fn = fn,
      thumb_dir = fn.parent / meta.thumb_dir,
      img_dir = fn.parent / meta.img_dir,
      orig_dir = fn.parent / meta.orig_dir,

      thumb_width = int( getattr( meta, 'thumb_width', 150 ) ),
      thumb_height = int( getattr( meta, 'thumb_width', 150 ) ),
      thumb_quality = int( getattr( meta, 'thumb_quality', 95 ) ),
      thumb_method = getattr( meta, 'thumb_method', 'max-dim' ),

      img_width = int( getattr( meta, 'img_width', 1920 ) ),
      img_height = int( getattr( meta, 'img_width', 1080 ) ),
      img_quality = int( getattr( meta, 'img_quality', 95 ) ),
    )

  except AttributeError as e:
    md.log.debug( str(e) )
    md.log.error( f'{fn}: thumb_dir and img_dir must be specified' )
    raise

  data.img_dir.mkdir( parents=True, exist_ok=True )
  data.thumb_dir.mkdir( parents=True, exist_ok=True )
  with Pool() as p:
    p.starmap( resize, [ (f, data) for f in meta.files ] )

def run():
  global md, args, outputs, executor

  start = time.monotonic()

  p = argparse.ArgumentParser( prog='md-to-html',
      description='Convert markdown files to HTML using Jinja2 templates' )
  p.add_argument( '-c', '--config', action='store',
                 help='Config file (YAML)' )
  p.add_argument( '-d', '--delete-extra', dest='delete_extra',
                 action='store_true', default=False,
                 help='Delete extra html files' )
  p.add_argument( '-f', '--force', dest='update', action='store_false', default=None,
                 help='Render whether or not source is newer' )
  p.add_argument( '-F', '--force-resize', action='store_true',
                 help='Resize images whether or not source is newer' )
  p.add_argument( '-n', '--no-exec', dest='exec', action='store_false',
                 default=True,
                 help="Don't run commands specified by 'exec'" )
  p.add_argument( '-q', '--quiet', action='store_true', default=False,
                 help='Suppress info messages' )
  p.add_argument( '-R', '--no-recurse', dest='recurse', action='store_false',
                 default=True,
                 help='Recurse subdirectories for *.md files' )
  p.add_argument( '-r', '--resize-images', dest='resize', action='store_true',
                 help='Resize images for slideshows' )
  p.add_argument( '-s', '--show-extra', dest='show_extra', action='store_true',
                 default=False,
                 help='Show extra html files' )
  p.add_argument( '-p', '--preview', dest='preview', action='store',
                 help='Launch preview for output file (no output is generated)' )
  p.add_argument( '-t', '--threads', action='store', type=int, default=0,
                 help='Number of threads. Use 0 (default) to let the system decide automatically.' )
  p.add_argument( '-u', '--update', action='store_true', default=None,
                 help='Only render if source is newer' )
  p.add_argument( '-v', '--verbose', action='store_true', default=False,
                 help='Show debug messages' )
  p.add_argument( 'files', action='store', nargs='*',
                 help='Markdown (or YAML config) files' )
  args = p.parse_intermixed_args()

  config_dirs = list( load_config_paths( 'md-to-html' ) )
  md = MarkdownConverter( config_dirs=config_dirs )

  if args.verbose: md.log.setLevel( logging.DEBUG )
  if args.quiet: md.log.setLevel( logging.WARNING )
  if args.config:
    process_file( Path(args.config) )

  if args.update is not None: md.globals.update = args.update

  #md.log.debug( f'Arguments: {args}' )
  #md.log.debug( f'Configuration: {md.globals}' )

  if args.preview:
    meta = md.read_frontmatter( Path(args.preview) )
    md.log.debug( f'Running xdg-open {meta.dst_file}' )
    subprocess.Popen( ['xdg-open', meta.dst_file] )
    sys.exit()

  outputs = []
  n_threads = args.threads if args.threads > 0 else None
  with concurrent.futures.ProcessPoolExecutor(max_workers=n_threads) as executor:
    for f in args.files: process_file_or_dir(f)

    if hasattr( md.globals, 'sources' ):
      if hasattr( md.globals, 'base_dir' ):
        for s in md.globals.sources:
          process_file_or_dir( md.globals.base_dir/s )
      else:
        md.log.error( 'Ignoring "sources"; no base_dir specified' )

  md.log.debug( f'Outputs:\n' +
    "\n".join([str(o) for o in outputs]) )

  # Delete files / run commands
  if md.log.error.counter == 0:
    if ( args.show_extra or args.delete_extra ) and hasattr( md.globals, 'dst_dir' ):
      delete_extra_files( md.globals.dst_dir, md.globals.dst_dir )

    try:
      if args.exec:
        for cmd in getattr( md.globals, 'exec', "" ).splitlines():
          md.log.info( 'Running ' + cmd )
          subprocess.run( cmd, shell=True, cwd=md.globals.base_dir )
    except AttributeError:
      md.log.error( 'Ignoring "exec"; no base_dir specified' )

  if md.log.error.counter > 0:
    md.log.info( f'Found {md.log.error.counter} error(s)' )

  md.log.debug( f'Processed {len(outputs)} files in {(time.monotonic() - start)*1000:.0f}ms' )
# vim: set sw=2 :
