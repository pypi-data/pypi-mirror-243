

import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

    setuptools.setup(
        name="AnimatedWordCloud",
        version="1.0.5",
        author="Petr Koráb",
        author_email="xpetrkorab@gmail.com",
        packages=["AnimatedWordCloud"],
        description="Animated version of classic word cloud for time-series text data",
        long_description=description,
        long_description_content_type="text/markdown",
        url="https://github.com/PetrKorab/AnimatedWordCloud",
        include_package_data = True,
        python_requires='>=3.8, <3.9',
        install_requires = ['arabica == 1.7.6',
                            'Box2D == 2.3.10',
                            'chardet == 3.0.4',
                            'beautifulsoup4 == 4.12.2',
                            'openpyxl == 3.1.2',
                            'pygame == 2.5.0',
                            'PyQt6 == 6.5.2',
                            'PyQt6-Qt6 == 6.5.2',
                            'PyQt6-sip == 13.5.2',
                            'SQLAlchemy == 1.3.2',
                            'ftfy == 6.1.1',
                            'pygame-pgu == 0.21'],
        license='OSI Approved :: Apache Software License'
    )