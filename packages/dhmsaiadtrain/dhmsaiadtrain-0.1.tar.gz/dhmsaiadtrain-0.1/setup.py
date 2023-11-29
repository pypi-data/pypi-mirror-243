from setuptools import setup, find_packages

setup(
    name='dhmsaiadtrain',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.2',
        'tensorflow>=2.12.0',
        'keras>=2.12.0',
        'scikit-learn>=1.2.1',
        'pandas>=1.5.3',
        'matplotlib>=3.7.1',
    ],
    python_requires='>=3.8',
    author='Daijie Bao',
    author_email='daijiebao0617@outlook.com',
    description='AI Training Script Owned by Suzhou DHMS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.dhms.net/aidiagnosis/ai_alert_training',
)
