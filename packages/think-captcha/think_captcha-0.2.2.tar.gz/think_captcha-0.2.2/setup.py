from setuptools import setup, find_packages

setup(
    name="think_captcha",
    version="0.2.2",
    description="A simple Python package for solving captcha",
    author='Ibrohim Fayzullayev',
    author_email='info@thinkland.uz',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['pytesseract', 'scipy', 'pillow', 'numpy']
)
