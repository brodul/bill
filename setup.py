from setuptools import setup, find_packages
import os

if os.name == "nt":
      import py2exe

version = '0.1'

setup(name='bill',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
	  zipfile=None,
      install_requires=[
            "xlrd",
            "xlwt",
            "xlutils",
            "pyside"
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      console=["bill/qt.py"],
	  
	  # PY2EXE: modules to be included
	  modules = ["bill"],
	  # PY2EXE: script to be main executable
	  windows = [{ "script" : "bill/qt.py" }],
	  # PY2EXE: library requirements to be included (add excludes here)
	  options = { "py2exe" : { "includes" : ["xlrd", "xlwt", "xlutils", "pyside" ]} }
)
