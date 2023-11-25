import setuptools

setuptools.setup(
    name="PyBulma",
    version='0.1.4',
    url="https://gitlab.com/mnealer-public/pybulma",
    author="Marc Nealer",
    author_email="marcnealer@gmail.com",
    license="GNU3",
    description="Python wrappers around html elements, with bulma.io css classes, to create Jinja2/django templates",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "jinja2"
        "beautifulsoup4",
        "pydoc",
        "typing-extensions"
    ],
    python_requires=">=3.10"
)
