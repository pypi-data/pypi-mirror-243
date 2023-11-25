# Convert Markdown to HTML using Jinja2 templates

This converts a markdown file to a full HTML file by using a template.
The default templates are:

1. `simple`: A simple one column layout using [Bootstrap], with support for math (using [MathJax]), syntax highlighting, and automatic light/dark theme switching.
  (See a demo [here](https://gi1242.codeberg.page/md-to-html/README.html).)

2. `revealjs`: A [RevealJS] presentation. (See a demo [here](https://gi1242.codeberg.page/md-to-html/examples/presentation/).)

3. A [LightGallery] slideshow. (See a demo [here](https://gi1242.codeberg.page/md-to-html/examples/slideshow/).) 
   (This script can also resize your original images and create thumbnails / web versions for your slideshow. See the demo for instructions.)

## Installation

* Clone the repository [https://codeberg.org/gi1242/md-to-html.git](https://codeberg.org/gi1242/md-to-html)

* If you use `pip`, then install by:

        pip install '/path/to/md-to-html[resize,codehilite]'

* If you don't use `pip`, create a symlink to `src/md-to-html` from somewhere in your path.
  In this case you may also have to install the dependencies:
    - Required dependencies:
      [python](https://www.python.org/),
      [python-frontmatter](https://pypi.org/project/python-frontmatter/),
      [python-jinja](https://pypi.org/project/Jinja2/),
      [python-markdown](https://python-markdown.github.io/),
      [python-pyxdg](http://freedesktop.org/Software/pyxdg).
    - Optional dependencies:
      [python-pillow](https://pypi.org/project/Pillow/) (for resizing images),
      [python-pygments](https://pygments.org/) (for syntax highlighting output).

## Usage

### Simple one file use case

Just run `md-to-html file.md` to produce `file.html`.
(Optionally choose template / set options in the YAML front matter.)

### More complicated multi-file use case

To build more complicated sites, this will do two things for you:

1.  Recurse directories and create HTML files (either in the same location, or in a specified destination directory preserving the hierarchy).

2.  Recurse through the destination directory, and purge all HTML files that don't correspond to markdown source files. (You can set exclude / preserve lists.)

To build a website, you may need a few other things.
This script doesn't do them because there are other tools that do them excellently.
For example:

1. Copying static files, or uploading to your web server.
  I use `rsync` for this. (You can configure this script to run `rsync` or any external command on successful completion using the `exec` option in config files.)

2. Automatically watch files and compile HTML when the source is changed.
  I configured my editor (Neovim) to do this automatically every time a source file is changed (instructions [[examples/livereload/index.html|here]]).

3. Automatically reload the HTML preview when the HTML is compiled.
  I use a `livereload` server (instructions [[examples/livereload/index.html|here]]).

### Command line options

```
usage: md-to-html [-h] [-c CONFIG] [-d] [-f] [-F] [-n] [-q] [-R] [-r] [-s]
                  [-p PREVIEW] [-t THREADS] [-u] [-v]
                  [files ...]

Convert markdown files to HTML using Jinja2 templates

positional arguments:
  files                 Markdown (or YAML config) files

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file (YAML)
  -d, --delete-extra    Delete extra html files
  -f, --force           Render whether or not source is newer
  -F, --force-resize    Resize images whether or not source is newer
  -n, --no-exec         Show extra html files
  -q, --quiet           Suppress info messages
  -R, --no-recurse      Recurse subdirectories for *.md files
  -r, --resize-images   Resize images for slideshows
  -s, --show-extra      Show extra html files
  -p PREVIEW, --preview PREVIEW
                        Launch preview for output file (no output is
                        generated)
  -t THREADS, --threads THREADS
                        Number of threads. Use 0 (default) to let the system
                        decide automatically.
  -u, --update          Only render if source is newer
  -v, --verbose         Show debug messages
```

### Configuration (from YAML config files)

The following directories are searched for configuration.

1. The directory this script was installed in
2. `/etc/xdg/md-to-html`
3. `~/.config/md-to-html`
4. The directory of the input file.

Global options should be in a `config.yaml` file.
The default (hardcoded) options are:

    :::yaml
    enable_mathjax: true
    enable_codehilite: true
    enable_jinja: false
    jinja_header: |
      {%- import 'lightgallery.j2' as LightGallery -%}
    template: simple
    encoding: utf-8
    absolute_links: False
    update: False
    exclude_dirs: [
      '.git'
      '__pycache__'
      'templates'
      'reveal.js'
    ]
    exclude_files: []
    protect_dirs: [
      'reveal.js'
    ]
    protect_files: []

* `base_dir`: Base of the source directory hierarchy. Source file outside this directory will raise an exception. (Default `.`.) It is treated as a relative path from the file it was defined in, so that `base_dir: .` works as expected.
* `dst_dir` : All output goes in this directory, preserving the directory hierarchy up to `base_dir`.
  That is `base_dir/path/file.md` becomes `dst_dir/path/file.html`.
  It is treated as a relative path from the file it was defined in.
* `exclude_files` / `exlcude_dirs`: List of glob patterns of source files / directories to ignore when recursing through directories. (Values are appended to existing values; to clear the list use `!!reset` as the first entry.)
* `protect_files` / `protect_dirs`: List of glob patterns of destination files / directories to protect from deletion. When `-d` is used, all HTML files in the destination directory that do not correspond to source markdown files are deleted. `protect_files` / `protect_dirs` can be used to protect some of these files from deletion. (Values are appended to existing values; to clear the list use `!!reset` as the first entry.)
* `sources`: List of source files / directories to convert to HTML / recurse into.
* `update`: Only compile source if it is newer than the target HTML (overridden by `-u` / `-f` on command line)
* `exec`: Commands to run if all files are processed without error (must be defined in a YAML config file specified with `-c`)
   Useful to start `rsync` to transfer static files.
   Multiple commands can be given if separated by newlines.
   All commands are passed through a shell, and run in `base_dir`.

### Configuration (from YAML front matter)

All metadata, including the template name, can also be specified as [YAML] front matter surrounded by `---`:

    ---
    template: simple
    encoding: utf-8
    enable_jinja: true
    ---
    Markdown content starts here.

## Markdown Syntax and Extensions

We use [python-markdown](https://python-markdown.github.io/) to render the HTML, with the following extensions enabled:

* [Extra](https://python-markdown.github.io/extensions/extra/): A compilation of various Python-Markdown extensions that (mostly) imitates PHP Markdown Extra.
The supported extensions include: Abbreviations, Attribute Lists, Definition Lists, Fenced Code Blocks, Footnotes, Tables, Markdown in HTML.


* [Sane Lists](https://python-markdown.github.io/extensions/sane_lists/): The Sane Lists extension alters the behavior of the Markdown List syntax to be less surprising.

* [SmartyPants](https://python-markdown.github.io/extensions/smarty/): The SmartyPants extension converts ASCII dashes, quotes and ellipses to their HTML entity equivalents.

* [Table of Contents](https://python-markdown.github.io/extensions/toc/): The Table of Contents extension generates a Table of Contents from a Markdown document and adds it into the resulting HTML document. (Use it either in templates via `{{toc}}` or in markdown after setting `enable_jinja: true`.)

* `Strikethrough:` Produce ~~strike through~~ text using `~~text~~`

* [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/): The CodeHilite extension adds code/syntax highlighting to standard Python-Markdown code blocks using [Pygments](http://pygments.org/). (Disable it with `enable_codehilite: false`)

* `Wiki Links:` To use `[[link.html|label]]` syntax (and provide warnings if the link is to a local find and isn't found.

* `Math`: Render math using [MathJax]

* [Jinja2] expressions if `enable_jinja` is true (default is false).

### MathJax Macros and options

A few [MathJax] options and LaTex macros are defined in the `simple.j2` template.
To add your own macros or change the mathjax configuration, you have a few options:

1. For new macros in one document use this at the start of the file:

        $
          \newcommand{\mymacro}{expansion}
          ...
        $

2. For per document configuration changes use the `mathjax_config` YAML metadata.

        :::yaml
        ---
        mathjax_config: |
          MathJax.tex.tags = 'ams'
          MathJax.tex.macros = {
            ...MathJax.tex.macros,
            sign: '\\operatorname{sign}',
            abs: [ '#1\\lvert#2#1\\rvert', 2, '' ]
          }
        ---

    The
   contents of `mathjax_config` are treated as JavaScript and included right after the `MathJax` configuration object is defined.
   You can, for instance, also define (or undefine) macros using `MathJax.tex.macros`.
   (If you put this in `config.yaml`, then it will be used for all files in that directory.)

3. For more global settings, you can extend the template and override  the `mathjax` block (look at `tests/templates/custom.j2` for an example).


### WikiLinks

Use `[[file.html|label]]` to generate a link to `file.html` with label `label`.
To use the file name as the label, just use `[[file.html]]`

* Link to files which don't exist produce a warning.
* `[[/absolute/path]]` links to `base_url/absolute/path`.
* If `absolute_links` is set, then all wiki-links are converted to absolute links using `base_url/absolute/path`.

### Using Jinja2 commands in the markdown file.

By default [Jinja2] expressions are only available in templates, and not in the markdown file.
If you want to use them, set `enable_jinja=true` in either the metadata or global configuration options.
For example:

    :::markdown
    ---
    title: Document tile
    author: Author
    template: simple
    enable_jinja: true
    user_flag: true
    ---

    # {{title}}

    *{{author}}, 2023-10-06*

    You can use Jinja2 expressions: 1 + 1 = {{1 + 1}}.

    {% if user_flag %}
    You can set conditionals in metadata
    {% else %}
    and render content based on the values.
    {% endif %}

**Note:** `enable_jinja=false` by default so invalid Jinja2 expressions don't surprise users.

## Templates

A file is converted to HTML using a [Jinja2] template.
Templates should be in the `templates` subdirectory of one of the configuration folders, and should have a `.j2` extension.
A bare bones example of a template is:

    :::jhtml
    <!DOCTYPE html>
    <html>
      <head><title>{{title}}</title></head>
      <body>{{content}}</body>
    </html>

All YAML metadata and global options are accessible as template variables.
The following additional variables are defined while processing:

* **uses_math**: True if math was detected when rendering the file
* **uses_codehilite**: True if syntax highlighted code was detected when rendering the file
* **toc**: HTML table of contents obtained from the file
* **title**: Contents of the first `<h1>` element, if not previously set.
* **content**: Document content after conversion from Markdown to HTML

### Template specific options

There are various template specific options that can be set from YAML front matter (or config files).For instance, to add a style sheet, you can use

    end_head: <link href="..." rel="stylesheet" integrity="..." crossorigin="anonymous">

These are only documented in the source 😄

## Live Previews

You can have the web browser automatically reload the HTML preview every time you make a change.
Two ways of doing this are described in [examples/livereload/index.md](examples/livereload/index.html)

<footer class="pt-4 small">
  <hr>
  <p class="text-body-secondary">
    Copyright 2023, Gautam Iyer.
    MIT Licence.
  </p>
</footer>

[MathJax]: https://www.mathjax.org/
[Bootstrap]: https://getbootstrap.com/
[RevealJS]: https://revealjs.com/
[YAML]: https://yaml.org/
[Jinja2]: https://pypi.org/project/Jinja2/
[LightGallery]: https://www.lightgalleryjs.com/
