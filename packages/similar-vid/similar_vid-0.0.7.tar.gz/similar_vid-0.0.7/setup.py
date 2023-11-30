from setuptools import setup, find_packages


def read_file(path_to_file):
    with open(path_to_file, 'r') as f:
        return f.read()


setup(
    name='similar_vid',
    version='0.0.7',
    url='https://github.com/supermakc/similar-vid',
    license='MIT',
    author='Maxim Baryshev',
    author_email='supermakc@gmail.com',
    description='Similar-vid is a library for finding similar frames between videos',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',

    packages=find_packages(),
    keywords='video similar skip intro',
    install_requires=['decord',
                      'ImageHash',
                      'numpy',
                      'opencv-python',
                      'Pillow',
                      'PyWavelets',
                      'scipy',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10'
    ]
)
