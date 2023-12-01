from typing import Callable
def override(names: set[str]) -> Callable[[type], type]:
    def override_deco(cls: type) -> type:
        @classmethod
        def __init_subclass__(self: type, *args, **kwargs):
            super(self).__init_subclass__(*args, **kwargs)
            for name in names:
                if not hasattr(self, name) or getattr(cls, name, None) is getattr(self, name, None):
                    raise TypeError(f"Child classes need to have & override {name}")
        cls.__init_subclass__ = __init_subclass__
        return cls
    return override_deco