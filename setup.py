from setuptools import setup, find_packages

setup(
    name='ciibm',
    version='0.1.0',
    packages=find_packages(),
    install=['SoftLayer','requests','time','json'],
    author="ghering90",
    author_email="ghering90@gmail.com",
    description="a simple library for creating infrastructure in classic infrastructure IBM Cloud",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ghering90/classic_infra_ibm_cloud",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',    
    ],
    python_requires='>=3.12.5',
)