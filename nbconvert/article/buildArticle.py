import shutil
from glob import glob
import os
import nbformat

build_dir = './output/'

file2copy = [
    'spline.bib',
    'cedram-smai-jcm.cls',
    'spline.ipynb',
    'spline.tplx',
    'logo_smai.jpg'
]

if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

os.makedirs(build_dir)

for f in file2copy:
    shutil.copyfile(f, build_dir + f)

os.chdir(build_dir)
os.system('jupyter nbconvert --to latex spline.ipynb --template spline.tplx')
os.system('pdflatex spline.tex')
os.system('bibtex spline')
os.system('pdflatex spline.tex')
os.system('pdflatex spline.tex')
shutil.copyfile('spline.pdf', '../spline.pdf')
os.chdir('..')