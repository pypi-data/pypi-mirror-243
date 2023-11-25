from setuptools import setup, find_packages

setup(
    name='evercycle_models',  # Replace with your app's name
    version='0.0.11',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Everycle Models',
    url='https://github.com/evercycle-org/evercycle-models/tree/main/eve_models',
    author='Evercycle',
    author_email='mija@evercycle.io',
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        # Other classifiers...
    ],
    install_requires=[
        'django>=3.0',
        # Other dependencies...
    ],
)
