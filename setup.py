# import setuptools
from setuptools import setup, find_packages

# with open("README.md", "r") as fh:
# long_description = fh.read()

setup(
	name="RedditDesktopCapture",
	version="0.0.1",
	author="Matthew Harris",
	author_email="matthew.harris@wsu.edu",
	description=	"A simple program that prompts the user for a series of subreddits and\
			sets that user's desktop to images from those subreddits, modifying\
			the images according to the user settings",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.7",
		"License :: None",
		"Operating System :: Mac OS",
	],
)
