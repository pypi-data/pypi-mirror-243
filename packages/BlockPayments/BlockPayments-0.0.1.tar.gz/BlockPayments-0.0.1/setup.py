from setuptools import setup, find_packages

setup(
    name='BlockPayments',
    version='0.0.1',
    description='A Python wrapper for the BlockPayments API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hexye',

    url='https://github.com/HexyeDev/BlockPayments.py',
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.9',
    ],

    keywords='blockpayments, blockpayments api, blockpayments python, blockpayments wrapper, blockpayments.py',

    packages=find_packages(),
    install_requires=['requests', 'aiohttp'],
)