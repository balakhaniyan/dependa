# Dependa

## A simple Dependency Injection Library

You can use it as simple as you think:

Just import it:

```python
from dependa import Inject, InjectClass
```

And define your classes:

```python
class IProp:
    @property
    def name(self):
        return "IProp"


class Prop(IProp):
    @property
    def name(self):
        return "Prop"


class ICode:
    prop: IProp


@Inject
class Code(ICode):
    prop: IProp


class Data(metaclass=InjectClass):
    code: ICode
    name: IName
```

As you can see, you can
use both `metaclass` and `decorator` versions together.

And add dependency using appropriate static method:

```python
Inject.add_transient(ICode, Code)
Inject.add_singleton(IProp, Prop)
```

> Note that you can only use transient... other versions are implementing

### And finally you get what you get:

```python
print(Data().code.prop.name)
```

Dependa fill properties as you defined

Enjoy!

## TODO

* [ ] Add singleton and scoped versions
* [ ] Add life time checking