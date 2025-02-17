Python version: <span style="color: aqua;">__3.13__</span> (Support includes Python <span style="color: white;">__3.11__</span> and <span style="color: white;">__3.12__</span>)
## <span style="color: white;">Installing with an external directory</span>

```git clone https://github.com/MothScientist/SwiftPipRedis.git```

## <span style="color: white;">Install (pip)</span>

`pip install git+https://github.com/MothScientist/SwiftPipRedis.git`</br></br>

#### Future updates are described in detail in the [roadmap.md](https://github.com/MothScientist/SwiftPipRedis/blob/master/roadmap.md) file

### <span style="color: white;">How does this library differ from [redis-py](https://github.com/redis/redis-py), on which it is built?</span>

__For quick connection to your Python projects and easy usage.__ <span style="color: violet;">__«Plug and Play»__ :)</span></br>

1. The methods have a more flexible type system, you can get both a number and a list using one r_set function, without worrying about what exactly is being treated in a given key.
2. Scenarios that require 2 or more calls to the Redis service are built on the basis of Lua scripts that perform all operations in 1 call to the server.
3. The methods have additional parameters that are not in the standard library, for example, an analogue of RETURNING (like in Postgres), which also allows you not to worry about the type of the variable that lies in a given key.
4. Pluggable flexible logging with many settings that allow you to customize it "for yourself"
5. It helps in the development of applications following the [12-factor](https://12factor.net/) principles.
* It is assumed that you already have the <span style="color: red;">__Redis__</span> service installed and running.
* There is no need to install <span style="color: DodgerBlue;">__Lua__</span> as it is built into <span style="color: red;">__Redis__</span>.

<span style="color: aqua;">**Supported Python types:**</span>
* integer
* float
* string
* boolean
* list
* tuple
* set
* frozenset

The number of supported methods and data types increases as the project develops, <span style="color: aqua;">**but it has all the basic methods for working with Redis**</span> (see the list and description of current commands with examples in the `example.py` file in the root of the repository).

<span style="color: white;"><u>Backward compatibility of functions is also preserved, which allows you to avoid problems when 
using the library in your projects</u></span>

<div style="text-align: center;">
    <img src="logo1.jpg" alt="PyRedisImage" style="width: 500px; height: 500px;" />
</div>