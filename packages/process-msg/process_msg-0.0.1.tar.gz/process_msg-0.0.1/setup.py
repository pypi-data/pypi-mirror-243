from setuptools import setup, find_packages

setup(
    name='process_msg',
    version='0.0.1',
    description='GPT 메세지 전처리 패키지',
    author='codusl100',
    author_email='codusl100@naver.com',
    url='https://github.com/codusl100/process_msg',
    install_requires=['openai',],
    packages=find_packages(exclude=[]),
    keywords=['gpt', 'message process', 'process message', 'gpt process'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)