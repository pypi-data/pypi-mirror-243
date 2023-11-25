
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
            with open(tex_path, 'w') as f:
                f.write(cell)
            
            subprocess.run(['pdflatex', '-shell-escape', '-output-directory', tmpdir, tex_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            subprocess.run(["pdfcrop", "--margins", "0 0 0 0", pdf_path, pdf_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(pdf_path)
                num_pages = len(reader.pages)
                for page_num in range(1, num_pages + 1):
                    svg_path = pdf_path[:-4] + f"{page_num}.svg"    
                    # Convert PDF to SVG
                    subprocess.run(["pdf2svg", pdf_path, svg_path, str(page_num)])
                    
                    # full scale the SVG
                    replacement_string = replacement_string = """<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 469 621">\n"""
                    with open(svg_path, 'r') as file:
                        lines = file.readlines()
                    lines = [replacement_string] + lines[2:]
                    with open(svg_path, 'w') as file:
                        file.writelines(lines)  
                        
                    # display SVG
                    display(SVG(filename=svg_path))
    @cell_magic
    def texdebug(self, line, cell): # shows output from os commands for debugging purposes (e.g. if pdflatex fails, you can see the error log)
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_path = os.path.join(tmpdir, 'temp.tex')
            pdf_path = os.path.join(tmpdir, 'temp.pdf')
            cwd = os.getcwd()
            cell = cell.replace('{./', f'{{{cwd}/') # do this to fix include paths since using a temporary directory
            with open(tex_path, 'w') as f:
                f.write(cell)
            
            subprocess.run(['pdflatex', '-shell-escape', '-output-directory', tmpdir, tex_path])
            subprocess.run(["pdfcrop", "--margins", "0 0 0 0", pdf_path, pdf_path])
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(pdf_path)
                num_pages = len(reader.pages)
                for page_num in range(1, num_pages + 1):
                    svg_path = pdf_path[:-4] + f"{page_num}.svg"    
                    # Convert PDF to SVG
                    subprocess.run(["pdf2svg", pdf_path, svg_path, str(page_num)])
                    
                    # full scale the SVG
                    replacement_string = replacement_string = """<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 469 621">\n"""
                    with open(svg_path, 'r') as file:
                        lines = file.readlines()
                    lines = [replacement_string] + lines[2:]
                    with open(svg_path, 'w') as file:
                        file.writelines(lines)  
                        
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

