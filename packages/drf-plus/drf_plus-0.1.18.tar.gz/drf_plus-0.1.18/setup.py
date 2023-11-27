from setuptools import setup, find_packages


setup(
    name="drf_plus",
    version="0.1.18",
    description="Django DRF 확장 도구",
    author="lee-lou2",
    author_email="lee@lou2.kr",
    url="https://github.com/lee-lou2/drf-plus",
    install_requires=[
        "django>=3.0.11",
    ],
    packages=find_packages(exclude=[]),
    keywords=["drf", "django", "tools", "django-rest-framework"],
    python_requires=">=3.6",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
