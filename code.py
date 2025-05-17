from dependa import Inject
from prop import IProp


class ICode:
    prop: IProp


@Inject
class Code(ICode):
    prop: IProp
