from setuptools import setup


setup(
    name='ref_type',

    packages=['ref_type'],

    version='1.0.0',

    license='MIT',

    description='Referencable objects for Python.',

    long_description_content_type='text/x-rst',
    long_description=open('README.rst', 'r').read(),

    author='Ivan Perzhinsky.',
    author_email='name1not1found.com@gmail.com',

    url='https://github.com/xzripper/ref_type',
    download_url='https://github.com/xzripper/time_manager/archive/refs/tags/v1.0.0.tar.gz',

    keywords=['type', 'reference', 'utility'],

    classifiers=[
        'Development Status :: 5 - Production/Stable ',
        'Intended Audience :: Developers',
        'Typing :: Typed',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
