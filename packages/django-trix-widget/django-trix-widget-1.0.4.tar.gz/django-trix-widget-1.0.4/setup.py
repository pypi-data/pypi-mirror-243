from setuptools import setup, find_namespace_packages
from trix_widget.version import Version


setup(name='django-trix-widget',
     version=Version('1.0.4').number,
     description='Trix widget for Django',
     long_description=open('README.md').read().strip(),
     long_description_content_type="text/markdown",
     author='Bram Boogaard',
     author_email='padawan@hetnet.nl',
     url='https://github.com/bboogaard/django-trix-widget',
     packages=find_namespace_packages(include=['trix_widget', 'trix_widget.static.trix', 'trix_widget.templates']),
     include_package_data=True,
     install_requires=[
         'pytest',
         'pytest-cov',
         'pytest-django~=4.5.2',
         'django~=3.2.23',
         'pyquery~=2.0.0',
         'bleach~=6.1.0'
     ],
     license='MIT License',
     zip_safe=False,
     keywords='Django Trix widget',
     classifiers=['Development Status :: 3 - Alpha'])
