from setuptools import setup, find_packages

setup(
    name='cpat-audit',
    version='1.4.0',
    author='Arkhotech Spa',
    author_email='msilval@arkho.io',
    description='Collector de auditoria para CPATs',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

#License :: Other/Proprietary License