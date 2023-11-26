from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lynx-flow',
    version='0.0.3',
    author='Toghrul Mirzayev',
    author_email='togrul.mirzoev@gmail.com',
    description='Lynx Flow is a streamlined and straightforward API requests library for building method call '
                'sequences. Simplify your code with clear and concise constructs using Lynx Flow.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'requests',
        'logstyle'
    ],
    keywords=[
        'testing',
        'api',
        'rest',
        'graphql',
        'backend',
        'qa',
        'test-automation',
        'automation'
    ],
    python_requires='>=3.7',
)
