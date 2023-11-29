from setuptools import setup, find_packages

setup(
    name='notifyall',
    version='1.0',
    packages=find_packages(),
    description='A multi-channel notification library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Laura Mendez',
    author_email='malaura_404@hotmail.com',
    url='https://github.com/gibran-toriz/lalakiri-notification-library.git',
    install_requires=[
        'PyYAML==6.0.1',
        'boto3==1.29.3',
        'botocore==1.32.3',
        'requests==2.31.0',
        'requests-toolbelt==1.0.0'
    ],
    classifiers=[
        # Choose classifiers from https://pypi.org/classifiers/
    ],
)
