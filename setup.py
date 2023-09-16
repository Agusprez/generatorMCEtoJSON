from cx_Freeze import setup, Executable

executables = [Executable('generatorMCEtoJSON.py')]

setup(name='NombreDelEjecutable',
      version='1.0',
      description='Descripción del ejecutable',
      executables=executables)