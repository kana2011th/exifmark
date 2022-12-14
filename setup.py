from setuptools import setup, find_packages

setup(
    name='exifstamp',
    version='0.1.1',
    description='another watermarking tools',
    url='https://github.com/kana2011th/exifstamp',
    author='Khanaphon Kana Phaengtan',
    author_email='khwd.2007@gmail.com',
    license='BSD 2-clause',
    packages=['exifstamp', 'exifstamp.utils'],
    install_requires=[
        'ExifRead==3.0.0',
        'Pillow==9.2.0',
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "exifstamp = exifstamp.main:exifstamp",
        ],
    },
    # packages=find_packages(where="src")
    package_data={'': ['license.txt', 'themes/**']},
    include_package_data=True,
)
