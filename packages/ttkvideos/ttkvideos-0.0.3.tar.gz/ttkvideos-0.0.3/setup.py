from setuptools import setup,find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ttkvideos',
    version='0.0.3',
    description='playing video (with audio) in tkinter label',
    long_description=open('readme.txt').read() + '\n\n' + open('CHANGELOG.txt').read() + '\n\n' + open('design.html').read(),
    url='https://github.com/Vishal24102002/ttkvideos',
    author='Vishal Sharma',
    author_email='vishalsharma659615@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='videos',
    packages=find_packages(),
    python_requires = ">=3.6"


)