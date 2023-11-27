from setuptools import setup, find_packages

def load_readme():
    with open('README.md', 'r', encoding='utf-8') as file:
        return file.read()

setup(
    name='ntt-observable-list',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "ntt-signal"
    ],
    author='threezinedine',
    author_email='threezinedine@email.com',
    description='List with ntt signal mechanism',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/threezinedine/ntt-observable-list',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='signal, observable',
    project_urls={
        'Source': 'https://github.com/threezinedine/ntt-observable-list',
        'Tracker': 'https://github.com/threezinedine/ntt-observable-list/issues',
    },
)