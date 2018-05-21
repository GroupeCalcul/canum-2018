import shutil
from glob import glob
import os
import nbformat

chapter_path = './AeroPython/lessons/'
build_dir = './output/'

file2copy = [
    'book.tplx',
    'mystyle.tex',
    'SIAMGHbook2016.cls',
    'svmono.cls'
]

if os.path.exists(build_dir):
   shutil.rmtree(build_dir)

shutil.copytree(chapter_path, build_dir)
for f in file2copy:
    shutil.copyfile(f, build_dir + f)

old_notebooks = glob(build_dir + '*.ipynb')
notebooks = []
for i, n in enumerate(old_notebooks):
    tmp = n.replace('_', '-')
    os.rename(n, tmp)
    notebooks.append(tmp)

for n in notebooks:
    nb = nbformat.read(n, as_version=4)
    # remove license and style
    nb.cells = nb.cells[2:-2]
    for old, new in zip(old_notebooks, notebooks):
        for c in nb.cells:
            if c.cell_type == 'markdown':
                c.source = c.source.replace(os.path.basename(old), os.path.basename(new))
                c.source = c.source.replace('---', '')
    nbformat.write(nb, n)

print(notebooks)
os.chdir(build_dir)
os.system('python -m bookbook.latex --output-file mybook --template book.tplx')
os.system('pdflatex mybook.tex')
os.system('pdflatex mybook.tex')
shutil.copyfile('mybook.pdf', '../mybook.pdf')
os.chdir('..')


#if os.path.exists(build_dir):
#    shutil.rmtree(build_dir)
