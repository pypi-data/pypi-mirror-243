__all__ = ('Icon')
class Icon:
    def __init__(self, 
        statemap: dict,
        default: Any,
    ) -> None:
        self.update(statemap)
        self.default = default

    # interpret = dict.__getitem__

