from setuptools import find_packages, setup


setup(
    name='uni_active',
    version="0.0.2",
    keywords=["Active Learning", "selection"],
    description='machine learning',
    long_description="",
    long_description_content_type="text/markdown",
    author="dp",
    author_email="wangchangxin@dp.tech",
    url="https://git.dp.tech/ai/zw_project",
    platforms=[
        "Windows",
        "Unix",
    ],
    license="LGPLv3",
        classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(
        exclude=["test", "*.test", "*.*.test", "*.*.*.test",
                 "test*", "*.test*", "*.*.test*", "*.*.*.test*", 
                 "instances*", "Instances", "Instance*","examples"],
    ),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        "six",
        "pandas",
        "scikit-learn",
        "mgetool",
    ],
    # entry_points={
    #     'console_scripts': ['autozw=autozw.cli.main:main'],
    # },
)
