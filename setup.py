from setuptools import setup, find_packages

setup(
    name = 'iss_moex',
    version = '0.1.0',
    url = '',
    description = '',
    packages = find_packages(),
    install_requires = [
        # Github Private Repository
        'iss_moex @ git+ssh://git@github.com:AleksandrShenshin/iss_moex.git'
    ]
)