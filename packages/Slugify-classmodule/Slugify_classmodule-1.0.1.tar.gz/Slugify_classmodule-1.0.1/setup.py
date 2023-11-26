from setuptools import setup, find_packages

setup(
    name='Slugify_classmodule',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    author='Picard Aïshael && Borgellas Samuel',
    author_email='aishael.picard@gmail.com',
    maintainer_email='borgellassamuel@gmail.com',
    description='Un separateur et modificateur de mots, SLUG',
    long_description="Un projet Python qui permet de convertir n'importe quelle chaîne de caractères en slug.",
    long_description_content_type='text/plain',
    url="https://github.com/Aishael20/Slugify_Project",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='Slugify security',
)