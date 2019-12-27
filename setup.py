from setuptools import setup, find_packages


with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]
    
    
setup(
    name="Lazylab",
    version="0.2",
    packages=find_packages(),
    #scripts=['lazylab/lazylab.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=reqs,

    #package_data=True,

    # metadata to display on PyPI
    author="Alex Groshev",
    author_email="haddystuff@gmail.com",
    url="https://github.com/haddystuff/Lazylab",
#    classifiers=[
#    ]
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'lazylab = lazylab.lazylab:main',
        ],
    }
)
