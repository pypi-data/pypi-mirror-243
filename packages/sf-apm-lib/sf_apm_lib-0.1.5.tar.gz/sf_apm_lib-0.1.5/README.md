sf-apm-lib
==============
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![pypi-package](https://img.shields.io/badge/pypi-green)](https://pypi.org/project/sf-apm-lib/)

Snappyflow modules

Installation
------------
pip install sf-apm-lib

Then you should import the library.

```python 
from sf_apm_lib.snappyflow import Snappyflow
```

Usage
-----

Get trace config

```python    
sf = Snappyflow() # Initialize Snappyflow. By default intialization will pick profileKey, projectName and appName from sfagent config.yaml.

# Add below part to manually configure the initialization
project_name = '<Snappyflow Project Name>'
app_name = '<Snappyflow App Name>'
profile_key = '<Snappyflow Profile Key>'

sf.init(profile_key, project_name, app_name)
# End of manual configuration

trace_config = sf.get_trace_config() # Returns trace config

print(trace_config)
```
