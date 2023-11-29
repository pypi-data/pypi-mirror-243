from setuptools import setup,find_packages
requires = [
    'Starco==2.4',
    'python-telegram-bot==13.14',
    'Telethon==1.32.1',
    'phonenumbers',
    'pycountry',
    'nest-asyncio==1.5.8',
]

setup(
    name = 'tlg_starco',
    version='1.1',
    author='Mojtaba Tahmasbi',
    packages=find_packages(),
    install_requires=requires,
)