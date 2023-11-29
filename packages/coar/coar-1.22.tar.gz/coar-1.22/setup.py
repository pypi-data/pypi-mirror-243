import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='coar',
    version='1.22',
    license='MIT',
    author='jmichalovcik',
    author_email='yee06.zones@icloud.com',
    description='Clustering of association rules based on user defined thresholds.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jmichalovcik/coar",
    packages=setuptools.find_packages(),
    keywords=[
        'coar', 'clustering of association rules', 'association rule clustering', 'association rules',
        'association rule processing'
        'clustering', 'cluster analysis',
        'database knowledge mining', 'data mining', 'data analysis',
    ],
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.11',
)
