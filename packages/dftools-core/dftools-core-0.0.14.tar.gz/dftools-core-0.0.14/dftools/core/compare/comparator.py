from typing import Tuple, Dict, TypeVar, Generic, Any

from dftools.core.compare.compare_events import ComparisonResult, ComparisonResults
from dftools.utils.dict_util import get_unique_key_list

T = TypeVar('T')
C = TypeVar('C', bound=ComparisonResult)


class Comparator(Generic[T, C]):
    """
        Comparator class provides an abstract base class for comparators.
        Comparator applies to a specific type T with a comparison output object for compare method as type C
        , which can be the ComparisonResult or one of its children classes

        Object of type T should have a name attribute, which is also used as the key in the comparison dictionaries
        On multiple compare method, the renaming mapping uses this name attribute to determine the correct structures
        to compare
    """

    RENAMING_ORIGINAL_KEY = 'orig_key'

    def __init__(self) -> None:
        pass

    def compare(self, obj1: T, obj2: T, root_key_path: Tuple[str] = ()
                , renaming_mappings: Dict[str, Any] = {}) -> C:
        """
        Compares 2 objects of the same type and returns a Comparison Result object with the output of the comparison

        Parameters
        ----------
        obj1 : T
            The original object
        obj2 : T
            The new object
        root_key_path : str
            The root key path for the comparison, for informational and reporting purposes
        renaming_mappings : Dict[str, Any]
            A dictionary for renaming of attributes

        Returns
        -------
            The comparison result
        """
        return NotImplementedError('The compare method is not implemented for class : ' + str(type(self)))

    @classmethod
    def _adapt_objects2_with_renaming_mapping(cls, objects2: Dict[str, T], renaming_mapping: Dict[str, str]) \
            -> Dict[str, T]:
        """
        Adapts the objects 2 Dictionary with a renaming mapping.
        Creates a new dictionary where all objects are stored on the original key, e.g. if there is no renaming,
        the key will be the object's name, but if there is a renaming the object will be stored on the original key,
        instead of the current object's name.

        Example with the renaming of object Obj2 to Obj3 :
            Objects2 (the target object dictionary): {
                'Obj1' : {'name' : 'Obj1', value : '1'}
                , 'Obj3' : {'name' : 'Obj3', value : '2'}
            }
            Renaming mapping : {'Obj2' : 'Obj3'}

            Output : {
                'Obj1' : {'name' : 'Obj1', value : '1'}
                , 'Obj2' : {'name' : 'Obj3', value : '2'}
                    --> The same object is stored on key Obj2 instead of Obj3
            }

        Parameters
        ----------
        objects2 : Dict[str, T]
            A dictionary linking key (as object name) to its corresponding object
        renaming_mapping : Dict[str, str]
            A string to string dictionary linking the original key (name) to the new key (name)

        Returns
        -------
            A dictionary of the objects dictionary provided with all objects stored on the original key
        """
        if (renaming_mapping is None) or (len(list(renaming_mapping.keys())) == 0):
            return objects2
        tgt_from_src_renaming_mapping = {new: orig for orig, new in renaming_mapping.items()}
        new_objects2 = {}
        for key, object2 in objects2.items():
            if key in list(tgt_from_src_renaming_mapping.keys()):
                new_objects2.update({tgt_from_src_renaming_mapping[key]: object2})
            else:
                new_objects2.update({key: object2})
        return new_objects2

    def compare_multiple(self, objects1: Dict[str, T], objects2: Dict[str, T]
                         , renaming_mappings: Dict[str, dict] = {}) -> ComparisonResults:
        """
        Compares 2 object dictionaries, with objects1 considered as the original dictionary and objects2 the new
        dictionary

        Parameters
        ----------
        objects1 : Dict[str, T]
            The original object dictionary
        objects2 : Dict[str, T]
            The new object dictionary
        renaming_mappings : Dict[str, dict]
            The renaming mapping storing all the renaming to consider for comparison, storing for each object ref
            key, a dictionary of all the renaming to apply.

        Returns
        -------
            The comparison Results
        """
        results = ComparisonResults()

        key_renaming_mapping = {}
        obj_specific_renaming_mapping = {}
        for key, renaming_dict in renaming_mappings.items():
            if self.RENAMING_ORIGINAL_KEY in renaming_dict.keys():
                key_renaming_mapping.update({key: renaming_dict[self.RENAMING_ORIGINAL_KEY]})
            if set(self.RENAMING_ORIGINAL_KEY).isdisjoint(set(renaming_dict.keys())):
                obj_specific_renaming_mapping.update({
                    key:
                        {val_key: val_value
                         for val_key, val_value in renaming_dict.items()
                         if key != self.RENAMING_ORIGINAL_KEY}
                })

        objects2_for_compare = self._adapt_objects2_with_renaming_mapping(objects2, key_renaming_mapping)
        key_list = get_unique_key_list(objects1, objects2_for_compare)
        for key in key_list:
            results.append(self.compare(
                objects1[key] if key in objects1 else None
                , objects2_for_compare[key] if key in objects2_for_compare else None
                , ()
                , obj_specific_renaming_mapping[key] if key in obj_specific_renaming_mapping.keys() else {}
            ))

        return results
