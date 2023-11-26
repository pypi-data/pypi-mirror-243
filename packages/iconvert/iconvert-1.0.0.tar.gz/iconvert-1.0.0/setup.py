from setuptools import setup, find_packages

setup(
    name='iconvert',
    version='1.0.0',
    author='nrdrch',
    description='Convert images to .ico format for icon use in Windows',
    keywords='image convert ico windows icon',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'iconvert = iconvert:main'
        ]
    },
    install_requires=[
        'Pillow'
    ]
    # Add other metadata like author, description, etc.
)
