#!/usr/bin/env python
import setuptools
from assistant import __version__

catchphrase = "Your very own Assistant. Because you deserve it."
fail_catchphrase = "Where am I? Hey! It's me Assistant."

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = fail_catchphrase

version = __version__

required_packages = [
        'ftfy',
        'pydub',
        'pygments',
        'xonsh',
        'attrs',
        'questionary',
#        'nest-asyncio',
        'datasets',
        'transformers',
        'sentencepiece',
        'sentence-transformers',
        'bitsandbytes',
        'accelerate',
        'peft',
        'einops',
        'langchain',
        'sanic',
        'websockets',
        'colorama',
        'rich',
        'halo',
        'duckduckgo-search',
        'wikipedia',
        'pexpect',
        'scipy',
        'chromadb',
        'pydantic<2.0', # https://github.com/huggingface/huggingface_hub/pull/1837#issuecomment-1827440687
        'fsspec>=2023.10.0', # See https://github.com/huggingface/huggingface_hub/issues/1872
    ]

packaged_modules = [
    'assistant', 
    'assistant.ptk_shell', 
    'assistant.nlp', 
    'assistant.nlp.chains', 
    'assistant.nlp.chains.agents', 
    'assistant.nlp.chains.callback_handlers', 
    'assistant.nlp.chains.data_loaders', 
    'assistant.nlp.chains.data_splitter',
    'assistant.nlp.chains.embeddings',
    'assistant.nlp.chains.memory',
    'assistant.nlp.chains.models',
    'assistant.nlp.chains.parsers',
    'assistant.nlp.chains.prompts',
    'assistant.nlp.chains.schema',
    'assistant.nlp.chains.tools',
    'assistant.nlp.chains.vectorstores',
    'assistant.manager',
    'assistant.api', 
    'assistant.say', 
    'assistant.listen', 
    'assistant.entry_points',
    'assistant.procs',
    'xontrib',
    ]

setuptools.setup(
    name='assistant',
    version=version,
    license='MIT',
    author='Danny Waser',
    author_email='danny@waser.tech',
    description=catchphrase,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8,<3.12',
    install_requires=required_packages,
    packages=packaged_modules,
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.xsh']},
    platforms='any',
    entry_points={
        'console_scripts': [
            'assistant = assistant.entry_points.run_assistant:run',
            # 'manager = assistant.manager.__main__:run'
        ]
    },
    url='https://gitlab.com/waser-technologies/technologies/assistant',
    project_urls={
        "Documentation": "https://gitlab.com/waser-technologies/technologies/assistant/blob/master/README.md",
        "Code": "https://gitlab.com/waser-technologies/technologies/assistant",
        "Issue tracker": "https://gitlab.com/waser-technologies/technologies/assistant/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: French",
        "Topic :: System :: Shells",
        "Programming Language :: Unix Shell",
        "Topic :: Terminals",
    ]
)
