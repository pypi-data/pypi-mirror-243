import setuptools

setuptools.setup(
    name="PyBulma",
    version='0.1.5',
    url="https://gitlab.com/mnealer-public/pybulma",
    author="Marc Nealer",
    author_email="marcnealer@gmail.com",
    license="GNU3",
    description="Python wrappers around html elements, with bulma.io css classes, to create Jinja2/django templates",
    long_description="""Allows for the creation of Something like web components using python classes.
    HTML components based on Bulma.io css component definitions are coded as python classes, allowing a python
    programmer to build html templates using python classes instead of having to code HTML. This allows for cleaner
    html to be built, with clear attributes, classes and styles being applied easily to different html elements.
    It also allows the programmer to define styles, attributes and html snippets that can be added in a custom form
    into multiple html sections, or files
    """,
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
