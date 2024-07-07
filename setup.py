from setuptools import setup, find_packages

setup(
    name='music-note',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'soundfile',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library to find the duration of a music file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/music_duration',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
