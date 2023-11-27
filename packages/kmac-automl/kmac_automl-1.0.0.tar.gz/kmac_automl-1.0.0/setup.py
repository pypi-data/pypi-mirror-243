from setuptools import setup, find_packages


setup(
    name='kmac_automl',
    version='1.0.0',
    packages=find_packages(where='src'),
    install_requires=['pycaret[full]'],
    package_data={'kmac_automl':['fonts/NanumBarunGothic.ttf']},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    author='KMAC-DX',
    author_email='yyam1020@kmac.co.kr',
    description='KMAC AutoML Solution',
    license='KMAC',
    # keywords='AutoML machine-learning',
    package_dir={"": "src"},
    url='https://github.com/yyam1020-kmac/automl'
)

