# coding: utf8
# try something like
import subprocess

def index(): 
    output = subprocess.check_output(['python3','/home/cpnogueira/Downloads/pyheston/heston_web2py.py'])
    results=output[1:-2].split(',')
    db.numeric_results.insert(energy=results[0],runtime_value=results[3],price=results[1],precision_value=results[2])
    return dict(message=results)
