# -*- coding: utf-8 -*-


from distutils.core import setup



setup(
  name = 'E2EPyPPG',         
  packages = ['E2EPyPPG'],   
  version = '0.1',      
  license='MIT',        
  description = 'End-to-End PPG processing pipeline: from quality assessment and motion artifacts romval to HR/HRV extraction',   
  author = 'ohammad Feli, Iman Azimi, Kianoosh Kazemi, Yuning Wang',                   
  author_email = 'mohammad.feli@utu.fi, azimii@uci.edu, kianoosh.k.kazem@utu.fi, yuning.y.wang@utu.fi',      
  url = 'https://github.com/HealthSciTech/E2E-PPG',   
  download_url = 'https://github.com/HealthSciTech/E2E-PPG/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['PPG', 'Photoplethysmography', 'Quality assessment', 'Signal reconstruction', 'Peak detection', 'Heart rate', 'HR', 'Heart rate variability', 'HRV', 'Wearable devices'],
  install_requires=[            
    'heartpy',
    'joblib',
    'matplotlib',
    'more_itertools',
    'neurokit2',
    'numpy',
    'pandas',
    'scikit-learn',
    'scipy',
    'tensorflow',
    'torch',
    'torchvision',
    'wfdb',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)

