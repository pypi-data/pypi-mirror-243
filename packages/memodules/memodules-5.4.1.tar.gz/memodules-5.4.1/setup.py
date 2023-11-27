from setuptools import setup, find_packages

setup(
    name='memodules',
    version='5.4.1',
    author='mie31',
    author_email='mie.mey.master@icloud.com',
    description='local use functions',
    long_description="We do not consider the use of it by third parties.",
    long_description_content_type="text/plain",
    license="MIT",
    keywords='No redistribution!',
    packages=find_packages(),  # インポートするパッケージのリスト
    package_data={
        '': ['*.pyi'],
    },
    python_requires=">=3.11",
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
)
