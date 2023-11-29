import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="cameo_eco_query",
    version="1.0.3",
    author="JcXGTcW",
    author_email="jcxgtcw@cameo.tw",
    description="cameo_eco_query",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bohachu/cameo-eco-query",  # 維持原本的repo URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'openai==0.27.4',
        'python-dotenv==0.15.0',
    ],
)
