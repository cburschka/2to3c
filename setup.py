from setuptools import setup, find_packages

setup(name="2to3c",
      version="0.1",
      description="",
      author="David Malcolm",
      author_email="dmalcolm@redhat.com",
      packages=['lib2to3c'],
      package_data={'lib2to3c': ['*.cocci']},
      url="http://fedorahosted.org/2to3c/",
      scripts=['2to3c']
      )

