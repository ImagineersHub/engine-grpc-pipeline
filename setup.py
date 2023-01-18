from setuptools import setup, find_packages

setup(
    name='unity-grpc-build-pipeline',
    version='0.0.3',
    license='MIT',
    description='grpc pipeline interfaces',
    author='esun',
    author_email='esun@voteb.com',
    url='https://github.com/ImagineersHub/unity-grpc-build-pipeline',
    keywords=['python', 'grpc', 'unity', 'unreal'],
    packages=find_packages(),
    install_requires=[
        'grpcio==1.50.0',
        'grpcio-tools==1.50.0',
        'protobuf==4.21.8',
        'betterproto[compiler]>=2.0.*'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.10'
    ]
)
