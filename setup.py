from setuptools import setup, find_packages

setup(name="2to3c",
      version="0.1",
      description="",
      author="David Malcolm",
      author_email="dmalcolm@redhat.com",
      packages=find_packages(exclude='tests'),
      url="http://fedorahosted.org/2to3c/",
      scripts=['2to3c']
      )

