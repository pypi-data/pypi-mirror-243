from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='pum_def_9_1',
    version='0.1.5',
    author='USEK',
    description='Все необходимые команды для уроков информатики в 9 классе 2023-2024 года обучения. *Сделано учеником ПУМа',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
)
