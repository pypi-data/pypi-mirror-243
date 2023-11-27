from setuptools import setup, find_packages

setup(
    name='hyper_param_opt',
    version='0.1',
    packages=find_packages(),
    description='這是一個超參數選擇的模組',
    author='YCLIU',
    author_email='johnathan2337@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scikit-learn',
        'xgboost',
    ],
)
