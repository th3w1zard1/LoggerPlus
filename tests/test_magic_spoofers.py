from __future__ import annotations

from contextlib import contextmanager
import unittest

try:
    from loggerplus import _SpoofTypeAttributeAccess, _SpoofTypeAttributeAccess, _SpoofObjectAttributeAccess, _SpoofObjectAttributeAccess
except ImportError:
    # this error will happen when running from src without the pip package installed.
    import os
    import sys

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(path)  # noqa: PTH120, PTH100
    from loggerplus import _SpoofTypeAttributeAccess, _SpoofObjectAttributeAccess, _SpoofObjectAttributeAccess, _SpoofObjectAttributeAccess


class FaultyMeta(type):
    faulty: str
    def __getattribute__(cls, name):
        raise AttributeError("ERROR! FaultyMeta __getattribute__ triggered!")

    def __setattr__(cls, name, value):
        raise AttributeError("ERROR! FaultyMeta __setattr__ triggered!")


class FaultyObject(object, metaclass=FaultyMeta):
    def __getattribute__(self, name):
        raise AttributeError("ERROR! FaultyObject __getattribute__ triggered!")

    def __setattr__(self, name, value):
        raise AttributeError("ERROR! FaultyObject __setattr__ triggered!")


if __name__ == "__main__":
    assertRaises = unittest.TestCase().assertRaises
    
    _some_obj: FaultyObject = None  # pyright: ignore[reportAssignmentType]
    _some_class: type[FaultyObject] | FaultyMeta = None  # pyright: ignore[reportAssignmentType]
    _some_metaclass: type[type[FaultyObject]] | type[FaultyMeta] = None  # pyright: ignore[reportAssignmentType]
    
    # Construct them and test the construction understanding
    def reset():
        global _some_obj, _some_class, _some_metaclass
        _some_obj = FaultyObject()
        with assertRaises(AttributeError):
            _some_class = _some_obj.__class__
        with assertRaises(Exception):
            _some_class = type.__getattribute__(_some_obj, "__class__")  # pyright: ignore[reportArgumentType]
        _some_class = object.__getattribute__(_some_obj, "__class__")  # TODO(th3w1zard1): Figure out why this doesn't raise??
        with assertRaises(AttributeError):
            _some_metaclass = _some_class.__class__
        _some_metaclass = type.__getattribute__(_some_class, "__class__")
        _some_metaclass = object.__getattribute__(_some_class, "__class__")  # TODO(th3w1zard1): Figure out why this doesn't raise??
        assert _some_metaclass is FaultyMeta
        assert _some_class is FaultyObject, f"{_some_class} is not {FaultyObject}"

    # Attempt to access and set attributes safely using spoofers
    reset()
    with assertRaises(AttributeError):
        print("test1. this should not be printed, an error should be thrown instead!:", _some_class.__name__)
    with _SpoofTypeAttributeAccess(_some_class):
        assert _some_class.__name__ == "FaultyObject", f"{_some_class.__name__} != \"FaultyObject\""
    with assertRaises(AttributeError):
        print("test3. this should not be printed, an error should be thrown instead!:", _some_class.__name__)
    with _SpoofTypeAttributeAccess(FaultyMeta):
        FaultyMeta.faulty = "success! This did not trigger an error"
    with _SpoofTypeAttributeAccess(FaultyMeta):
        value = FaultyMeta.faulty

    # Attempt to access attributes using spoofers
    reset()
    with assertRaises(AttributeError):
        assert _some_class.__name__ == "FaultyObject", f"{_some_class} != \"FaultyObject\""
    with _SpoofTypeAttributeAccess(_some_class):
        assert _some_class.__name__ == "FaultyObject", f"{_some_class} != \"FaultyObject\""
    with assertRaises(AttributeError):
        assert _some_class.__name__ == "FaultyObject", f"{_some_class} != \"FaultyObject\""
    # Attempt to set attributes
    with _SpoofTypeAttributeAccess(FaultyMeta):
        FaultyMeta.faulty = "success! This did not trigger an error"
    with _SpoofTypeAttributeAccess(FaultyMeta):
        value = FaultyMeta.faulty
    print("_spoof_type_setattr result?", value)

    reset()
    with _SpoofObjectAttributeAccess(_some_obj):
        with assertRaises(AttributeError):
            value = _some_obj.faulty
    with _SpoofObjectAttributeAccess(_some_obj):
        _some_obj.faulty = "success! This did not trigger an error"
    with _SpoofObjectAttributeAccess(_some_obj):
        value = _some_obj.faulty
        print("_spoof_object_setattr result?", value)
            
