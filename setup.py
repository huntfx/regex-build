import os
from setuptools import setup, find_packages


# Get the README.md text
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    readme = f.read()

# Parse ftrack_query.py for a version
with open(os.path.join(os.path.dirname(__file__), 'regex_build.py'), 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = eval(line.split('=')[1].strip())
            break
    else:
        raise RuntimeError('no version found')

# Get the pip requirements
try:
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as f:
        requirements = [line.strip() for line in f]
except OSError:
    requirements = []

setup(
    name = 'regex-build',
    packages = find_packages(),
    version = version,
    license='MIT',
    description = 'Build complex one-line regex strings.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author = 'Peter Hunt',
    author_email='peter@huntfx.uk',
    py_modules=['regex_build'],
    url = 'https://github.com/huntfx/regex-build',
    download_url = 'https://github.com/huntfx/regex-build/archive/{}.tar.gz'.format(version),
    project_urls={
        'Documentation': 'https://github.com/huntfx/regex-build/wiki',
        'Source': 'https://github.com/huntfx/regex-build',
        'Issues': 'https://github.com/huntfx/regex-build/issues',
    },
    keywords = ['regex', 'build', 'generate', 're', 'auto', 'create'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires=('>=2.7'),
)