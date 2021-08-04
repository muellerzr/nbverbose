# AUTOGENERATED! DO NOT EDIT! File to edit: cli.ipynb (unless otherwise specified).

__all__ = ['execute_nb', 'convert_nb', 'notebook2html', 'nbdev_build_docs']

# Cell
import nbformat
from nbconvert.exporters.html import HTMLExporter

from functools import partial
import time, random, os, sys

from fastcore.basics import compose
from fastcore.foundation import Config
from fastcore.parallel import parallel
from fastcore.script import call_parse, Param, bool_arg
from fastcore.xtras import Path

from nbdev.export import read_nb, nbglob, find_default_export
from nbdev.export2html import (
    make_sidebar, make_readme,
    _gather_export_mods, ExecuteShowDocPreprocessor,
    ExecutePreprocessor, get_metadata, find_default_level,
    process_cells, add_show_docs, copy_images, process_cell,
    treat_backticks, execute_nb, clean_exports, nbdev_exporter,
    _nb2htmlfname,
)

# Cell
def _import_show_doc_cell(mods=None):
    "Add an import show_doc cell."
    source = f"from nbverbose.showdoc import show_doc"
    if mods is not None:
        for mod in mods: source += f"\nfrom {Config().lib_name}.{mod} import *"
    return {'cell_type': 'code',
            'execution_count': None,
            'metadata': {'hide_input': True},
            'outputs': [],
            'source': source}

# Cell
def execute_nb(nb, mod=None, metadata=None, show_doc_only=True):
    "Execute `nb` (or only the `show_doc` cells) with `metadata`"
    mods = ([] if mod is None else [mod]) + _gather_export_mods(nb['cells'])
    nb['cells'].insert(0, _import_show_doc_cell(mods))
    ep_cls = ExecuteShowDocPreprocessor if show_doc_only else ExecutePreprocessor
    ep = ep_cls(timeout=600, kernel_name='python3')
    metadata = metadata or {}
    pnb = nbformat.from_dict(nb)
    ep.preprocess(pnb, metadata)
    return pnb

# Cell
def convert_nb(fname, cls=HTMLExporter, template_file=None, exporter=None, dest=None, execute=True):
    "Convert a notebook `fname` to html file in `dest_path`."
    fname = Path(fname).absolute()
    nb = read_nb(fname)
    meta_jekyll = get_metadata(nb['cells'])
    meta_jekyll['nb_path'] = str(fname.relative_to(Config().path("lib_path").parent))
    cls_lvl = find_default_level(nb['cells'])
    mod = find_default_export(nb['cells'])
    nb['cells'] = compose(*process_cells,partial(add_show_docs, cls_lvl=cls_lvl))(nb['cells'])
    _func = compose(partial(copy_images, fname=fname, dest=Config().path("doc_path")), *process_cell, treat_backticks)
    nb['cells'] = [_func(c) for c in nb['cells']]
    if execute: nb = execute_nb(nb, mod=mod)
    nb['cells'] = [clean_exports(c) for c in nb['cells']]
    if exporter is None: exporter = nbdev_exporter(cls=cls, template_file=template_file)
    with open(_nb2htmlfname(fname, dest=dest),'w') as f:
        f.write(exporter.from_notebook_node(nb, resources=meta_jekyll)[0])

# Cell
def _notebook2html(fname, cls=HTMLExporter, template_file=None, exporter=None, dest=None, execute=True):
    time.sleep(random.random())
    print(f"converting: {fname}")
    try:
        convert_nb(fname, cls=cls, template_file=template_file, exporter=exporter, dest=dest, execute=execute)
        return True
    except Exception as e:
        print(e)
        return False

# Cell
def notebook2html(fname=None, force_all=False, n_workers=None, cls=HTMLExporter, template_file=None,
                  exporter=None, dest=None, pause=0, execute=True):
    "Convert all notebooks matching `fname` to html files"
    files = nbglob(fname)
    if len(files)==1:
        force_all = True
        if n_workers is None: n_workers=0
    if not force_all:
        # only rebuild modified files
        files,_files = [],files.copy()
        for fname in _files:
            fname_out = _nb2htmlfname(Path(fname).absolute(), dest=dest)
            if not fname_out.exists() or os.path.getmtime(fname) >= os.path.getmtime(fname_out):
                files.append(fname)
    if len(files)==0: print("No notebooks were modified")
    else:
        if sys.platform == "win32": n_workers = 0
        passed = parallel(_notebook2html, files, n_workers=n_workers, cls=cls,
                          template_file=template_file, exporter=exporter, dest=dest, pause=pause, execute=execute)
        if not all(passed):
            msg = "Conversion failed on the following:\n"
            print(msg + '\n'.join([f.name for p,f in zip(passed,files) if not p]))

# Cell
@call_parse
def nbdev_build_docs(fname:Param("A notebook name or glob to convert", str)=None,
                     force_all:Param("Rebuild even notebooks that haven't changed", bool_arg)=False,
                     mk_readme:Param("Also convert the index notebook to README", bool_arg)=True,
                     n_workers:Param("Number of workers to use", int)=None,
                     pause:Param("Pause time (in secs) between notebooks to avoid race conditions", float)=0.5):
    "Build the documentation by converting notebooks matching `fname` to html"
    notebook2html(fname=fname, force_all=force_all, n_workers=n_workers, pause=pause)
    if fname is None: make_sidebar()
    if mk_readme: make_readme()