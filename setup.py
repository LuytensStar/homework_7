from setuptools import setup, find_namespace_packages

setup(
    name='clean',
    version='1',
    description='folder sorting',
    url='https://github.com/LuytensStar/homework_6',
    author='Artem',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:sort_files']}
)