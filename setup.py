from setuptools import setup

setup(
    name="scruml",
    version="1.0.0",
    description="A simple UML editor",
    url="http://github.com/mucs420f19/JJARS",
    author="Team JJARS",
    author_email="jahildeb@millersville.edu",
    license="MIT",
    packages=["scruml"],
    package_data={"scruml": ["assets/*"]},
    install_requires=["pyyaml>=5<6", "pywebview[qt]"],
    entry_points={"console_scripts": ["scruml = scruml:main"]},
    zip_safe=False,
)
