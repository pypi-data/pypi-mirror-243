from setuptools import setup, find_packages

setup(
    name='iconvert',
    version='1.0.9',
    author='nrdrch',
    description='Convert images to .ico format for icon use in Windows',
    keywords='image convert ico windows icon',
    url='https://github.com/nrdrch/iconvert',
    README='README.md',
    website='https://github.com/nrdrch/iconvert',
    packages=find_packages(where='src'),  # Ensure src directory is included
    package_dir={'': 'src'},
    py_modules=['iconvert'],
    entry_points={
        'console_scripts': [
            'iconvert=iconvert:main',
        ]
    },
    install_requires=[
        'Pillow',
    ],
)
