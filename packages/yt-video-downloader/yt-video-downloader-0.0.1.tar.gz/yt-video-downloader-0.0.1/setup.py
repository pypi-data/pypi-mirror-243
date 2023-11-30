import os
from setuptools import setup,find_packages
reqs=os.popen('pipreqs requirements.txt').read().splitlines()
with open('README.md', 'r') as f:
    ld = f.read()
setup(
    name='yt-video-downloader',
    version='0.0.1',
    author='sahaya valan',
    author_email='sahayavalanj1@gmail.com',
    packages=find_packages(),
    description='Download youtube videos by just paste the link',
    install_requires=reqs,
    long_description=ld,
    long_description_content_type='markdown',
entry_points={
    'console_scripts':['yt_vdo=do_yt.yt_vdo:main']
}

)