import setuptools
import os

DISTNAME = 'mlend'
DESCRIPTION = "MLEnd Datasets"
MAINTAINER =  "Nikesh Bajaj"
MAINTAINER_EMAIL =  "nikkeshbajaj@gmail.com"
AUTHER_EMAIL = "nikkeshbajaj@gmail.com"
AUTHER = "Jesús Requena Carrión and Nikesh Bajaj"
URL = 'https://MLEndDatasets.github.io'
LICENSE = 'BSD-3-Clause'
GITHUB_URL= 'https://github.com/MLEndDatasets'


with open("README.md", "r") as fh:
    long_description = fh.read()

top_dir, _ = os.path.split(os.path.abspath(__file__))
if os.path.isfile(os.path.join(top_dir, 'Version')):
    with open(os.path.join(top_dir, 'Version')) as f:
        version = f.readline().strip()
else:
    import urllib
    Vpath = 'https://raw.githubusercontent.com/Nikeshbajaj/MLEnd/master/Version'
    version = urllib.request.urlopen(Vpath).read().strip().decode("utf-8")


def parse_requirements_file(fname):
    requirements = list()
    with open(fname, 'r') as fid:
        for line in fid:
            req = line.strip()
            if req.startswith('#'):
                continue
            # strip end-of-line comments
            req = req.split('#', maxsplit=1)[0].strip()
            requirements.append(req)
    return requirements

if __name__ == "__main__":
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    install_requires = parse_requirements_file('requirements.txt')
    print('requirements',install_requires)

    setuptools.setup(
        name=DISTNAME,
        version= version,
        author=AUTHER,
        author_email = AUTHER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=URL,
        download_url = 'https://github.com/Nikeshbajaj/MLEnd/tarball/' + version,
        packages=setuptools.find_packages(),
        license = 'MIT',
        keywords = 'MLEndDatasets Datasets MachineLearning PrinciplesOfMachineLearning Data AI',
        classifiers=[
            "Programming Language :: Python :: 3",
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Natural Language :: English',
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            'Development Status :: 5 - Production/Stable',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Multimedia',
            'Topic :: Multimedia :: Sound/Audio :: Analysis',
            'Topic :: Multimedia :: Sound/Audio :: Speech',
            'Topic :: Scientific/Engineering :: Image Processing',
            'Topic :: Scientific/Engineering :: Visualization',

            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',

            'Development Status :: 5 - Production/Stable',
        ],
        project_urls={
        'Documentation': 'https://mlend.readthedocs.io/',
        'Say Thanks!': 'https://github.com/Nikeshbajaj',
        'Source': 'https://github.com/Nikeshbajaj/MLEnd',
        'Tracker': 'https://github.com/Nikeshbajaj/MLEnd/issues',
        },

        platforms='any',
        python_requires='>=3.5',
        install_requires = install_requires,
        setup_requires=["numpy>1.8","setuptools>=45", "setuptools_scm>=6.2"],
        include_package_data=True,
    )
