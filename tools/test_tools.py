import types
import inspect

def mock_sub_object_public_methods(parent_object, sub_object_names, failure=None):
    """Replace public methods in composed objects with one that either:
        1- raises Exception, or
        2- returns {"message": "Success!"}

    This proves useful when testing modules that are dependent on composed
    objects in case of these object's failure.

        Args:
        parent_object (class instance):
            Instance that has composed object as dependency
        
        sub_object_names (set):
            Set with names of composed objects whose public methods will be replaced
        
        failure (bool):
            If true public methods will be replaced for "raise Exception"
            Else public methods will be replace for "return {"message": "Success!"}"

    """
    class SubscriptableObject(types.ModuleType):
        """this object is instanced to copy the "__getitem__" method"""
        def __getitem__(self, attr):
            return getattr(self, attr)

    def replace_for_mock_method(method, method_name, sub_object):
        """replace the named method in sub_object with the declared new_method"""
        def new_method(*args, **kwargs):
            if failure:
                print("Test_tools made this exception!")
                raise Exception
            else:
                print("Test_tools made this message!")
                return {"message": "Success!"}

        setattr(sub_object, method_name, new_method)

    """make object properties mutable"""
    subscritable_object = SubscriptableObject
    parent_object.__getitem__ = subscritable_object.__getitem__

    for sub_object_name in sub_object_names:
        """get sub_object and make sub_objects properties mutable"""
        sub_object = parent_object.__getitem__(parent_object, sub_object_name)
        sub_object.__getitem__ = subscritable_object.__getitem__


        for attribute_name in dir(sub_object):
            """get all attributes in sub_object instance"""
            attribute = sub_object.__getitem__(sub_object, attribute_name)
            if attribute_name.startswith("_"):
                """skip dunder methods and private methods"""
                pass
            elif inspect.ismethod(attribute):
                """if attribute is a public method, replace it with "raise Exception" """
                replace_for_mock_method(attribute, attribute_name, sub_object)