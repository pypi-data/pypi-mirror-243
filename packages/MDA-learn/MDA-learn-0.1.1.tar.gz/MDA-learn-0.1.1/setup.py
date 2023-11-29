from setuptools import setup, find_packages

setup(
    name='MDA-learn',
    version='0.1.1',
    author='Md Tauhidul Islam and Zixia Zhou et al.',
    author_email='lei@stanford.edu',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib',
        'pandas',
        'umap-learn'
    ],
    description='Manifold Discovery and Analysis (MDA) algorithm for deep learning feature space analysis.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_github_repo',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)