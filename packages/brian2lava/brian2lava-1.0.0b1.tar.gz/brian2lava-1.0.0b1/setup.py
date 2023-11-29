from setuptools import setup, Command
import subprocess

class SubmoduleUpdateCommand(Command):
	user_options = []
	def initialize_options(self) -> None:
		pass
	def finalize_options(self) -> None:
		pass
	def run(self) -> None:
		subprocess.call(['echo', 'Updating submodules'])
		# Check which submodules are there
		subprocess.call(['git','submodule'])
		# Update them
		subprocess.call(['git','submodule','init'])
		subprocess.call(['git','submodule','foreach','git pull origin main'])
		subprocess.call(['echo','updated submodules'])


setup(
	name='brian2lava',
	version=f'1.0.0b1',  # consider adding '__version__' to 'brian2lava.__init__.py', but requires unified management of versions
	author='Francesco Negri, Carlo Michaelis, Jannik Luboeinski, Winfried Oed, Tristan Stöber, Andrew Lehr, Christian Tetzlaff',  # starting with author order for paper
	author_email='mail@jlubo.net',
	cmdclass={
		'submodule_update': SubmoduleUpdateCommand,
	},
	packages=[
		'brian2lava', 
		'brian2lava.device', 
		'brian2lava.codegen', 
		'brian2lava.utils', 
		'brian2lava.preset_mode'
	],
	python_requires='>3.8',
	url='https://gitlab.com/brian2lava/brian2lava',
	license='MIT',
	description='An open source Brian2 interface for the neuromorphic computing framework Lava',
	long_description=open('README.md').read(),
	long_description_content_type="text/markdown",
	package_data = {
		"brian2lava/codegen/templates": ["*.py_"],
		"brian2lava/templates": ["*.py.j2"],
		"brian2lava": ["preset_mode/lib/*"]
	},
    include_package_data=True,
	install_requires=[
		"brian2>=2.5.1",
		"jinja2>=2.7",
		"numpy",
		"pytest",
		"scipy",
		"markupsafe==2.0.1",
		"lava-nc>=0.7.0",
		"matplotlib",
        "tabulate"
	],
	
)
