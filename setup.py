"""setup.py file."""
from setuptools import setup, find_packages


with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]
    
    
setup(
    name="Lazylab",
    version="0.2",
    packages=find_packages(exclude=("test*",)),
    author="Alex Groshev",
    author_email="haddystuff@gmail.com",
    description="Network lab deployment automation tool",
    install_requires=reqs,
    url="https://github.com/haddystuff/Lazylab",
#    classifiers=[
#    ]
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'lazylab-deploy = lazylab.cli.cli_deploy:main',
            'lazylab-delete = lazylab.cli.cli_delete:main',
            'lazylab-save = lazylab.cli.cli_save:main'
        ],
    }
)
