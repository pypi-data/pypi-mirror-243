from setuptools import setup, find_packages

VERSION = '2.0.2' 
DESCRIPTION = 'JBioSeqTools'
LONG_DESCRIPTION = 'JBioSeqTools is the Python library for biological sequence optimization (GC % content & codon frequency), restriction places removal, DNA/RNA structure prediction, and RNAi selection. It also allows the building of many plasmid vectors with the possibility of choosing sequences such as transcript, promoter, enhancer, molecular fluorescent tag, etc. Finally, the user obtains a ready-for-order construct with a whole sequence and visualization. Package description  on https://github.com/jkubis96/JBioSeqTools'

# Setting up
setup(
        name="JBioSeqTools", 
        version=VERSION,
        author="Jakub Kubis",
        author_email="jbiosystem@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['jbst'],
        include_package_data=True,
        install_requires=['pandas', 'tqdm', 'matplotlib', 'numpy', 'requests', 'openpyxl', 'pymsaviz', 'ViennaRNA', 'biopython', 'networkx', 'seaborn', 'scipy'],       
        keywords=['sequence', 'optimization', 'vectors', 'AAV', 'GC', 'restriction enzyme'],
        license = 'MIT',
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ],
        python_requires='>=3.8',
)


