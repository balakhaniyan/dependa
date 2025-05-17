from inject import Inject
from code import ICode, Code
from prop import IProp, Prop

Inject.add_transient(ICode, Code)
Inject.add_singleton(IProp, Prop)


class IName:
    ...


@Inject
class Data:
    code: ICode
    name: IName


if __name__ == "__main__":
    print(Data().code.prop.name)