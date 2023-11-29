import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="llmfeedback",
	version="0.0.5",
	author="Kunal Tangri, Noah Faro",
	description="Package to integrate feedback into LLMs",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires='>=3.6',
	py_modules=["llmfeedback"],
	package_dir={'':'llmfeedback/src'},
	install_requires=['openai', 'numpy', 'pinecone-client', 'supabase']
)
