# <span style="color: white;">Installing with an external directory</span>
Run the ```pyredis_install.sh``` script with the ```--requirements-install``` parameter.

It will __clone the repository__, __install Lua5.4__ and, if the parameter is specified, __install the libraries__ required for operation.

# <span style="color: white;">Install (pip)</span>

`pip install git+https://github.com/MothScientist/SwiftPipRedis.git`

Python version: __3.13.1__ (Support includes Python __3.11__ and __3.12__)

## <span style="color: white;">For what?</span>

For quick connection to your Python projects and easy usage. <span style="color: violet;">__«Plug and Play»__ :)</span></br>
* It is assumed that you already have the <span style="color: red;">Redis</span> service installed and running.

#### <span style="color: orange;">Please note that the library does not support all data types and methods available in the original library. Pay attention to the annotation of types and description of functions and their parameters!</span>
The number of supported methods and data types increases as the project develops, <span style="color: aqua;">**but it has all the basic methods for working with Redis**</span> (see the list and description of current commands with examples in the `example.py` file in the root of the repository).

<span style="color: white;"><u>Backward compatibility of functions is also preserved, which allows you to avoid problems when 
using the library in your projects</u></span>

It helps in the development of applications following the [12-factor](https://12factor.net/) principles.

#### It is based on the library https://github.com/redis/redis-py

<div style="text-align: center;">
    <img src="logo1.jpg" alt="PyRedisImage" style="width: 500px; height: 500px;" />
</div>