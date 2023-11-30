#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from owega.changelog import OwegaChangelog as oc


desc = open('README.md').read()
desc += '\n\n'
desc += "## CHANGELOG: "
desc += '\n```\n'
desc += oc.log
desc += '\n```\n'

requirements = [
	req.strip() for req in open('requirements.txt', 'r').read().split('\n')
	if req.strip()
]

setup(
	name='owega',
	version=oc.version_str,
	description="A command-line interface for conversing with GPT models (from OpenAI)",
	long_description=desc,
	long_description_content_type='text/markdown',
	author="darkgeem",
	author_email="darkgeem@pyrokinesis.fr",
	url="https://git.pyrokinesis.fr/darkgeem/owega",
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Science/Research',
		'Intended Audience :: System Administrators',
		'License :: Freely Distributable',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Topic :: File Formats :: JSON',
		'Topic :: Multimedia :: Sound/Audio :: Speech',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
	],
	packages=[
		'owega',
		'owega.changelog',
		'owega.config',
		'owega.OwegaFun',
		'owega.conversation',
	],
	entry_points={
		'console_scripts': [
			'owega = owega.owega:main',
		]
	},
	install_requires=requirements,
	license="WTFPL",
	license_files=["LICEN[CS]E*"],
	project_urls={
		'Source': 'https://git.pyrokinesis.fr/darkgeem/owega',
		'Support': 'https://discord.gg/KdRmyRrA48',
	},
)
