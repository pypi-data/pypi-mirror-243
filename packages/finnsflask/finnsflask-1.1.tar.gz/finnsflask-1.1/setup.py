from distutils.core import setup
with open("README.md", "r") as f:
    readme = f.read()
setup(
    name="finnsflask",
    packages=['finnsflask'],
    version='1.1',
    license="MIT",
    description='This is a recreation of the popular python package, Flask.',
    author='Real Finnventor',                   # Type in your name
    author_email='finnventor@everspaugh.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/the-real-finnventor/finnsflask',
    # I explain this later on
    download_url='https://github.com/the-real-finnventor/finnsflask/archive/refs/tags/1.1.tar.gz',
    # Keywords that define your package best
    keywords=['FLASK', 'WEBSERVER', "JINJA2"],
    install_requires=[            # I get to this in a second
        'Jinja2'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ],
    long_description=readme
)
