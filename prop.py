class IProp:
    @property
    def name(self):
        return "IProp"


class Prop(IProp):
    @property
    def name(self):
        return "Prop"