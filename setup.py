import setuptools
from setuptools import find_packages, setup 
from typing import List 

def get_requirements()-> List[str]:
    """ 
    This function will return list of requirements
    """
    requirement_lst:List[str]=[]
    try: 
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                # ignore empty lines and -e . 
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('requirements.txt file not find')
    return requirement_lst

# print(get_requirements())


with open('README.md','r', encoding='utf-8') as f:
    long_description=f.read()

__version__='0.0.0'

REPO_NAME='NetworkSecurity'
AUTHOR_USER_NAME='Immortal-Pi'
SRC_REPO='NetworkSecurity'
AUTHOR_EMAIL='26.amruth@gmail.com'

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description='A python package for networkSecurity',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}',
    project_urls={
        'Bug Tracker': f'https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues',
    },
    package_dir={'':'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=get_requirements()
    
)