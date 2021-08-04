
# Verbose nbdev (nbverbose)
> An add-on to nbdev that allows for explicit parameter documentation


## Install

`pip install nbverbose`

## How to use

This library acts as an in-place replacement for `nbdev`'s `show_doc` functionality, and extends it to allow for documentation of the inputs. 

Everything else with nbdev runs fine, and you should use normal nbdev conventions, however instead of doing `from nbdev.showdoc import *`, you should do `from nbverbose.showdoc import *`.

An example of what will happen can be found below

First we import the library:

```python
from nbverbose.showdoc import *
```

Next we'll write a very basic function, that has a new way to document the inputs.

Rather than needing to have a very long doc string, your code can follow this declaration format. Spacing etc is not needed, just each parameter must be on a new line:

```python
def addition(
    a:int, # The first number to be added
    b:(int, float), # The second number to be added
):
    "Adds two numbers together"
    return a+b
```

As you can see, the documentation format is `name` followed by  the `type` (as normal), but in a single-line comment afterwards you put a quick affiliated documentation string for it. 

When you call the `show_doc` or `doc` functions, wrapping around `addition`, it will look something like so:


<h4 id="addition" class="doc_header"><code>addition</code><a href="__main__.py#L1" class="source_link" style="float:right">[source]</a></h4>

> <code>addition</code>(**`a`**:`int`, **`b`**:`Union`\[`int`, `float`\])

Adds two numbers together




We can see that our types are properly formatted. This even works in cases such as `Union` or `List`:

```python
from typing import Union

def addition(
    a:int, # The first number to be added
    b:Union[int, float], # The second number to be added
):
    "Adds two numbers together"
    return a+b
```


<h4 id="addition" class="doc_header"><code>addition</code><a href="__main__.py#L1" class="source_link" style="float:right">[source]</a></h4>

> <code>addition</code>(**`a`**:`int`, **`b`**:`Union`\[`int`, `float`\])

Adds two numbers together




Any functions that normally don't follow this format can still work as well:

```python
def addition(
    a:int,
    b:Union[int, float],
):
    "Adds two numbers together"
    return a+b
```


<h4 id="addition" class="doc_header"><code>addition</code><a href="__main__.py#L1" class="source_link" style="float:right">[source]</a></h4>

> <code>addition</code>(**`a`**:`int`, **`b`**:`Union`\[`int`, `float`\])

Adds two numbers together




```python
def addition(a:int,b:Union[int, float]):
    "Adds two numbers together"
    return a+b
```


<h4 id="addition" class="doc_header"><code>addition</code><a href="__main__.py#L1" class="source_link" style="float:right">[source]</a></h4>

> <code>addition</code>(**`a`**:`int`, **`b`**:`Union`\[`int`, `float`\])

Adds two numbers together




{% include note.html content='The `[source]` button on these examples will not point to something existing. This is due to the fact that `addition` is not part of our library. This will work fine for anything done with your `nbdev`-built library.' %}

There may be mild issues with type decorators, if you find any specific breakage, please open an issue [here](https://github.com/muellerzr/nbverbose/issues)