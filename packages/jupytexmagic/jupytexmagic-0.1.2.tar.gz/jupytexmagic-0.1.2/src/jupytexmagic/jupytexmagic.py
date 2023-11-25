from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import SVG
from PyPDF2 import PdfReader
import subprocess
import tempfile
import os

# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.

# The class MUST call this class decorator at creation time
@magics_class
class Jupytex(Magics):
    @cell_magic
    def tex(self, line, cell):
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, 'temp.tex')
            pdf_path = os.path.join(tmpdir, 'temp.pdf')
            cwd = os.getcwd()
            cell = cell.replace('{./', f'{{{cwd}/') # do this to fix include paths since using a temporary directory
            
            with open(tex_path, 'a') as f: # standardize document class since pdfcrop expevts continous page
                f.write("\documentclass[varwidth, margin=1in]{standalone}")
                f.write("\pagenumbering{gobble}")
                f.write(cell)
            
            subprocess.run(['pdflatex', '-shell-escape', '-output-directory', tmpdir, tex_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            subprocess.run(["pdfcrop", pdf_path, pdf_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            svg_path = pdf_path[:-4] + ".svg"    
            # Convert PDF to SVG
            subprocess.run(["pdf2svg", pdf_path, svg_path])

            # full scale the SVG
            subprocess.run(["sed", "-i", """''""", """2s/width="[^"]*"/width="100%"/; 2s/height="[^"]*"/height="100%"/""", svg_path]) 

            # display SVG
            display(SVG(filename=svg_path))
    @cell_magic
    def texdebug(self, line, cell):
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, 'temp.tex')
            pdf_path = os.path.join(tmpdir, 'temp.pdf')
            cwd = os.getcwd()
            cell = cell.replace('{./', f'{{{cwd}/') # do this to fix include paths since using a temporary directory
            
            with open(tex_path, 'a') as f:
                f.write("\documentclass[varwidth, margin=1in]{standalone}")
                f.write("\pagenumbering{gobble}")
                f.write(cell)
            
            subprocess.run(['pdflatex', '-shell-escape', '-output-directory', tmpdir, tex_path], check=True)
            subprocess.run(["pdfcrop", pdf_path, pdf_path])
            
            svg_path = pdf_path[:-4] + ".svg"    
            # Convert PDF to SVG
            subprocess.run(["pdf2svg", pdf_path, svg_path])

            # full scale the SVG
            subprocess.run(["sed", "-i", """''""", """2s/width="[^"]*"/width="100%"/; 2s/height="[^"]*"/height="100%"/""", svg_path]) 

            # display SVG
            display(SVG(filename=svg_path))
# In order to actually use these magics, you must register them with a
# running IPython.

def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(Jupytex)

