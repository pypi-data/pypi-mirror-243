from setuptools import setup,find_packages
requires = [
    'Starco==2.3.2',
    'python-telegram-bot==13.14'
]

setup(
    name = 'tlg_bot_starco',
    version='1.2.2',
    author='Mojtaba Tahmasbi',
    packages=find_packages(),
    install_requires=requires,
)