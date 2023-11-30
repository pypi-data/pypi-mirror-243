from setuptools import setup, find_packages

setup(
    name='QuantSigns',
    version='0.0.0.3',
    description='An API client for Quantsigns data',
    author='QuantSigns',
    author_email='support@quantsigns.com',

    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
