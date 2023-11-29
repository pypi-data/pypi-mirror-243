import csv
from typing import Dict, List, Tuple

from dftools.utils.list_util import get_all_sub_sets_from_start
from dftools.utils.dict_util import get_unique_key_list
from dftools.events import log_event
from dftools.events.events import CSVFileWriteSuccessful


class ComparisonEvent:
    """
        Comparison Event - Standard class
        Provides a standard way to store the outcome of a comparison between an original and a new object

        An event as UPDATE will have fields info, old and new filled
        An event as NEW will only have the field info filled
        
        {'event':"NEW", info : {FieldDescription}, _type : "FieldStructure"}
        {'event':"UPDATE", info : 'type', 'old' : 'TEXT', 'new' : "VARCHAR"}
        {'event':'UPDATE', info : 'desc', 'old' : null, 'new' : 'Entity - Scope'}
        {'event':'NOCHANGE', info : 'desc', 'old' : 'Entity - Scope', 'new' : 'Entity - Scope'}
        {'event':"REMOVE", info : {FieldDescription}, _type : "FieldStructure"}

    """
    UPDATE_EVENT = 'UPDATE'
    NO_CHANGE_EVENT = 'NOCHANGE'
    NEW_EVENT = 'NEW'
    REMOVE_EVENT = 'REMOVE'

    status_list = [UPDATE_EVENT, NO_CHANGE_EVENT, NEW_EVENT, REMOVE_EVENT]

    def __init__(self
                 , status: str
                 , key: Tuple[str]
                 , old
                 , new
                 , _type
                 ) -> None:
        if status not in self.status_list:
            raise ValueError('Event status : ' + status + ' is not authorized')
        self.status = status
        self.key = key
        self.old = old
        self.new = new
        self.type = _type

    def is_new(self):
        return self.status == ComparisonEvent.NEW_EVENT

    def is_removed(self):
        return self.status == ComparisonEvent.REMOVE_EVENT

    def is_identical(self):
        return self.status == ComparisonEvent.NO_CHANGE_EVENT

    def is_updated(self):
        return self.status == ComparisonEvent.UPDATE_EVENT

    def get_key_string(self) -> str:
        return 'root' + ''.join(['[\'' + key_entry + '\']' for key_entry in self.key])

    def get_key_level(self) -> int:
        return len(self.key)


class ComparisonResult:
    """
        Comparison Event - Standard class
        Provides a standard way to store the outcome of the comparison of 2 objects with 1 to many comparison events
    """

    def __init__(self
                 , obj1
                 , obj2
                 , root_key_path: Tuple[str] = None
                 , events: List[ComparisonEvent] = None
                 ) -> None:
        self.obj1 = obj1
        self.obj2 = obj2
        self.root_key_path = root_key_path
        self.events: List[ComparisonEvent] = events if events is not None else []
        self.keys = []
        for event in self.events:
            self.update_keys(event.key)

    def get_root_key_length(self) -> int:
        """
        Get the root key length

        Returns
        -------
            The length of root key
        """
        return len(self.root_key_path)

    def get_ref_object(self):
        """
        Get the reference object of the comparison result.
        Returns the obj1, which is considered as the baseline/reference if it is not null
            , otherwise the obj2 is considered as the baseline/reference

        Returns
        -------
            The reference object of the comparison
        """
        return self.obj1 if self.obj1 is not None else self.obj2

    def add_event(self, event: ComparisonEvent) -> None:
        """
        Adds a Comparison Event to this result object.
        Updates the keys stored locally.

        Parameters
        ----------
        event : ComparisonEvent
            The Comparison Event to be added
        """
        self.events.append(event)
        self.update_keys(event.key)

    def add_events(self, event_list: List[ComparisonEvent]) -> None:
        """
        Adds a list of Comparison Event to this result object
        Updates the keys stored locally.

        Parameters
        ----------
        event_list : List[ComparisonEvent]
            The list of Comparison Event to be added
        """
        for event in event_list:
            self.add_event(event)

    def update_keys(self, event_key: Tuple[str]) -> None:
        """
        Updates the keys locally stored from a list of Comparison Event

        Parameters
        ----------
        event_key : Tuple[str]
            The event key to be added in the locally stored key list
        """
        for key in get_all_sub_sets_from_start(event_key):
            if key not in self.keys:
                self.keys.append(key)

    def get_event_status(self, root_key: List[str]) -> str:
        """
        Get the event status for a specific root key.

        Parameters
        ----------
        root_key : List[str]
            The root key

        Returns
        -------
            The comparison event status, out of the possible statuses NEW, REMOVE, NOCHANGE, UPDATE
            and NoEventsAvailable, if the root key provided does not have any event in this comparison result
        """
        if self.get_sub_comparison(key_filter=root_key).get_number_of_events() == 0:
            return 'NoEventsAvailable'
        if self.is_new(root_key):
            return ComparisonEvent.NEW_EVENT
        if self.is_removed(root_key):
            return ComparisonEvent.REMOVE_EVENT
        if self.is_identical(root_key):
            return ComparisonEvent.NO_CHANGE_EVENT
        return ComparisonEvent.UPDATE_EVENT

    def is_new(self, root_key: List[str] = None) -> bool:
        """
        Checks if the root key provided is new, e.g. that the event for the root key level is in NEW status

        If None is provided as root key, the root key is default to the comparison result root key path

        Parameters
        ----------
        root_key : List[str], Optional
            The root key to check

        Returns
        -------
            True, if the root key provided is considered as new in this result.
            False, otherwise
        """
        if root_key is None:
            root_key = self.root_key_path
        root_event = self.get_event(tuple(root_key))
        if root_event is not None:
            if root_event.is_new():
                return True
        for evt in self.get_sub_comparison(key_filter=root_key).events:
            if (evt.get_key_string() == root_key) & evt.is_new():
                return True
        return False

    def is_removed(self, root_key: List[str] = None) -> bool:
        """
        Checks if the root key provided is removed, e.g. that the event for the root key level is in REMOVE status

        If None is provided as root key, the root key is default to the comparison result root key path

        Parameters
        ----------
        root_key : List[str], Optional
            The root key to check

        Returns
        -------
            True, if the root key provided is considered as removed in this result.
            False, otherwise
        """
        if root_key is None:
            root_key = self.root_key_path
        root_event = self.get_event(tuple(root_key))
        if root_event is not None:
            if root_event.is_removed():
                return True
        for evt in self.get_sub_comparison(key_filter=root_key).events:
            if (evt.get_key_string() == root_key) & evt.is_removed():
                return True
        return False

    def is_identical(self, root_key: List[str] = None) -> bool:
        """
        Checks if the root key provided is identical, e.g. that all the events for this root key
        and all its children are identical.

        If None is provided as root key, the root key is default to the comparison result root key path

        Parameters
        ----------
        root_key : List[str], Optional
            The root key to check

        Returns
        -------
            True, if the root key provided is considered as identical in this result.
            False, otherwise
        """
        if root_key is None:
            root_key = self.root_key_path
        root_event = self.get_event(tuple(root_key))
        if root_event is not None:
            if root_event.is_removed() | root_event.is_new():
                return False
        if self.get_sub_comparison(
                key_filter=root_key).get_sub_comparison_for_all_changes().get_number_of_events() == 0:
            return True
        return False

    def is_updated(self, root_key: List[str] = None):
        """
        Checks if the root key provided is updated, e.g. that at least one of the events for this root key
        and all its children is updated and that the root key is not considered in statuses NEW or REMOVE.

        If None is provided as root key, the root key is default to the comparison result root key path

        Parameters
        ----------
        root_key : List[str], Optional
            The root key to check

        Returns
        -------
            True, if the root key provided is considered as updated in this result.
            False, otherwise
        """
        if root_key is None:
            root_key = self.root_key_path
        if (not self.is_new(root_key)) & (not self.is_removed(root_key)) & (not self.is_identical(root_key)):
            return True
        return False

    def get_keys(self, level: int = None) -> List[List[str]]:
        """
        Get the list of keys for a given level.
        The root level is 1

        Parameters
        ----------
        level : int
            The level of key

        Returns
        -------
            The list of keys for the given level
        """
        if level is None:
            return self.keys
        return [key for key in self.keys if len(key) == level]

    def get_keys_except_leafs(self) -> list:
        """
        Get the keys list except for the leaf events (the keys without any children)

        Returns
        -------
            The list of keys, except leafs
        """
        return [tuple(key) for key in self.get_keys() if len(self.get_sub_comparison(key_filter=key).events) > 1]

    def get_keys_of_leafs(self) -> list:
        """
            Get all the keys for the leaf events (the keys without any children)

        Returns
        -------
            The list of keys for all the leafs
        """
        return [key for key in self.get_keys() if key not in self.get_keys_except_leafs()]

    def get_min_key_length(self) -> int:
        """
        Gets the min key length

        Returns
        -------
            The min key length
        """
        return min([len(key) for key in self.get_keys()])

    def get_min_length_keys(self) -> List[List[str]]:
        """
        Gets all the keys with the minimum length of keys

        Returns
        -------
            The list of keys with the minimum length of keys
        """
        return [key for key in self.get_keys() if len(key) == self.get_min_key_length()]

    def get_first_min_length_key(self) -> List[List[str]]:
        """
        Gets the first key found with the minimum length of keys

        Returns
        -------
            The first key found with the minimum length of keys
        """
        return [key for key in self.get_keys() if len(key) == self.get_min_key_length()]

    # Sub Comparison methods
    def get_sub_comparison_events(self, key_filter: List[str] = None) -> List[ComparisonEvent]:
        """
        Get all the comparison events with a key starting with the provided key filter.

        Parameters
        ----------
        key_filter : List[str]
            A key

        Returns
        -------
            A list of comparison events
        """
        key_filter_tuple = tuple(key_filter) if key_filter is not None else ()
        return [event for event in self.events if event.key[0:len(key_filter_tuple)] == key_filter_tuple]

    def get_sub_comparison(self, key_filter: List[str] = None):
        """
        Get a sub comparison for the provided key filter, e.g. a Comparison Result
        containing only the events linked to the key filter provided

        Parameters
        ----------
        key_filter : List[str]
            A key

        Returns
        -------
            A new Comparison Result
        """
        return ComparisonResult(self.obj1, self.obj2, root_key_path=self.root_key_path,
                                events=self.get_sub_comparison_events(key_filter=key_filter))

    def get_sub_comparison_for_all_changes(self):
        """
        Get all the change events, e.g. excluding all the events without any changes

        Returns
        -------
            A new Comparison Result containing only the events with changes
        """
        return ComparisonResult(obj1=None, obj2=None
                                , root_key_path=self.root_key_path, events=self.get_all_changes_events())

    def get_events(self) -> List[ComparisonEvent]:
        """
        Get all the events available in this Comparison Result

        Returns
        -------
            The list of Comparison Event
        """
        return self.events

    def get_event(self, key: Tuple[str], leaf_only: bool = False) -> ComparisonEvent:
        """
        Get a specific event, with possibility to look for leafs only

        Parameters
        ----------
        key : Tuple[str]
            The key
        leaf_only : bool
            Flag to indicate if only leafs should be looked into (when True)

        Returns
        -------
            The Comparison Event found
        """
        lkp_key_list = self.get_keys_of_leafs() if leaf_only else self.get_keys()
        if key not in lkp_key_list:
            raise ValueError("Comparison does not contain an event for key : " + ".".join(key))
        event_list = [event for event in self.get_events() if event.key == key]
        return event_list[0] if len(event_list) > 0 else None

    def get_number_of_events(self) -> int:
        """
        Get the number of events

        Returns
        -------
            The number of events
        """
        return len(self.get_events())

    def get_number_of_changes(self) -> int:
        """
        Get the number of changes

        Returns
        -------
            The number of changes
        """
        return len(self.get_all_changes_events())

    def get_no_change_events(self, root_key: List[str] = None):
        """
        Get all the events in NOCHANGE status for the root key

        Parameters
        ----------
        root_key : List[str]
            The root key to look into

        Returns
        -------
            The list of all the NOCHANGE events under the root key provided
        """
        return [event for event in self.get_sub_comparison(key_filter=root_key).get_events() if
                event.status == ComparisonEvent.NO_CHANGE_EVENT]

    def get_new_events(self, root_key: List[str] = None):
        """
        Get all the events in NEW status for the root key

        Parameters
        ----------
        root_key : List[str]
            The root key to look into

        Returns
        -------
            The list of all the NEW events under the root key provided
        """
        return [event for event in self.get_sub_comparison(key_filter=root_key).get_events() if
                event.status == ComparisonEvent.NEW_EVENT]

    def get_removed_events(self, root_key: List[str] = None):
        """
        Get all the events in REMOVE status for the root key

        Parameters
        ----------
        root_key : List[str]
            The root key to look into

        Returns
        -------
            The list of all the REMOVE events under the root key provided
        """
        return [event for event in self.get_sub_comparison(key_filter=root_key).get_events() if
                event.status == ComparisonEvent.REMOVE_EVENT]

    def get_updated_events(self, root_key: List[str] = None):
        """
        Get all the events in UPDATE status for the root key

        Parameters
        ----------
        root_key : List[str]
            The root key to look into

        Returns
        -------
            The list of all the UPDATE events under the root key provided
        """
        return [event for event in self.get_sub_comparison(key_filter=root_key).get_events() if
                event.status == ComparisonEvent.UPDATE_EVENT]

    def get_all_changes_events(self, root_key: List[str] = None) -> List[ComparisonEvent]:
        """
        Get all the events with changes (all changes except the ones in NOCHANGE status) for the root key

        Parameters
        ----------
        root_key : List[str]
            The root key to look into

        Returns
        -------
            The list of all the events with changes under the root key provided
        """
        return [event for event in self.get_sub_comparison(key_filter=root_key).get_events() if
                event.status != ComparisonEvent.NO_CHANGE_EVENT]

    def get_events_by_status(self) -> Dict[str, List[ComparisonEvent]]:
        """
        Get the events stored by status

        Returns
        -------
            A dictionary with as key the comparison event statuses and as values a list of the events of this status
        """
        events_by_status_dict = {ComparisonEvent.NO_CHANGE_EVENT: self.get_no_change_events(),
                                 ComparisonEvent.NEW_EVENT: self.get_new_events(),
                                 ComparisonEvent.REMOVE_EVENT: self.get_removed_events(),
                                 ComparisonEvent.UPDATE_EVENT: self.get_updated_events()}
        return events_by_status_dict

    def get_event_dict(self, only_changes: bool = True) -> dict:
        """
        Create an event dictionary containing all the events (or only events with changes).

        Event Dictionary structure is :
        - Root Key
            - Root Key Value
        - Events
            - Key Level 0 / Value
                - Key Level 1 / Value 1
                    - Key Level 2 / Value 1
                        - Event information with information "status", "old", "new"
                    - Key Level 2 / Value 2
                        - Key Level 3 / Value 1
                            - Event information with information "status", "old", "new"
                        - Key Level 3 / Value 2
                            - Event information with information "status", "old", "new"

        Parameters
        ----------
        only_changes : bool, defaulted to True
            If True, considers only the events with changes.

        Returns
        -------
        A dictionary containing the comparison events
        """
        event_dict = {}
        event_dict.update({"root_key": '.'.join(self.root_key_path)})
        event_dict.update({"events": {}})
        events_to_consider = self.get_all_changes_events() if only_changes else self.events
        for event in events_to_consider:
            current_change_dict = event_dict['events']
            for key_index in range(0, len(event.key)):
                current_level_key = event.key[key_index]
                if key_index != (len(event.key) - 1):
                    # When not a leaf and not available in the event dictionary, create a new empty dictionary
                    if current_level_key not in current_change_dict:
                        current_change_dict.update({current_level_key: {}})
                    current_change_dict = current_change_dict[current_level_key]
                else:
                    # Leaf
                    current_change_dict.update(
                        {current_level_key: {'status': event.status, 'old': event.old, 'new': event.new}})
        return event_dict

    def to_csv(self, file_path: str, newline: str = '', delimiter: str = ';', quotechar: str = '"') -> None:
        """
        Writes the content of this comparison result to a csv file format.

        Output CSV contains 1 header line and 1 line per Comparison Event
        Output CSV contains 5 columns :
            - 'Root Key' : The root key of the comparison
            - 'Key' : The key of the event
            - 'Status' : The event status
            - 'Old' : The old value
            - 'New' : The new value

        Parameters
        -----------
            file_path : the csv file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)

        """
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['Root Key', 'Key', 'Status', 'Old', 'New'])
            # Data row
            for event in self.events:
                writer.writerow(['.'.join(self.root_key_path), '.'.join(event.key), event.status, event.old, event.new])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=ComparisonResult.__name__))


class ComparisonResults(List[ComparisonResult]):

    def get_identical(self):
        """
        Get the list of comparison result with identical outcome

        Returns
        -------
            The list of comparison result with identical outcome
        """
        return [comparison_result for comparison_result in self if comparison_result.is_identical()]

    def get_new(self):
        """
        Get the list of comparison result with new outcome

        Returns
        -------
            The list of comparison result with new outcome
        """
        return [comparison_result for comparison_result in self if comparison_result.is_new()]

    def get_removed(self):
        """
        Get the list of comparison result with removed outcome

        Returns
        -------
            The list of comparison result with removed outcome
        """
        return [comparison_result for comparison_result in self if comparison_result.is_removed()]

    def get_updated(self):
        """
        Get the list of comparison result with updated outcome

        Returns
        -------
            The list of comparison result with updated outcome
        """
        return [comparison_result for comparison_result in self if comparison_result.is_updated()]

    def get_changes(self):
        """
        Get the list of comparison result with any change outcome (all except identical outcome)

        Returns
        -------
            The list of comparison result with any change outcome
        """
        return [comparison_result for comparison_result in self if not comparison_result.is_identical()]

    def to_csv(self, file_path: str, newline: str = '', delimiter: str = ';', quotechar: str = '"') -> None:
        """
        Writes the content of this comparison results to a csv file format.

        Output CSV contains 1 header line and 1 line per Comparison Event
        Output CSV contains 5 columns :
            - 'Root Key' : The root key of the comparison
            - 'Key' : The key of the event
            - 'Status' : The event status
            - 'Old' : The old value
            - 'New' : The new value

        Parameters
        -----------
            file_path : the csv file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)

        """
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['Root Key', 'Key', 'Status', 'Old', 'New'])
            # Data row
            for comparison_result in self:
                for comparison_event in comparison_result.events:
                    writer.writerow(['.'.join(comparison_result.root_key_path), '.'.join(comparison_event.key)
                                        , comparison_event.status, comparison_event.old, comparison_event.new])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=ComparisonResult.__name__))

    def to_csv_summary(self, file_path: str, newline: str = '', delimiter: str = ';', quotechar: str = '"') -> None:
        """
        Writes the summary of this comparison results to a csv file format.

        Output CSV contains 1 header line and 1 line per Comparison Result
        Output CSV contains 2 columns :
            - 'Root Key' : The root key of the comparison
            - 'Status' : The comparison status

        Parameters
        -----------
            file_path : the csv file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)

        """
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['Root Key', 'Status'])
            # Data row
            for comparison_result in self:
                writer.writerow(['.'.join(comparison_result.root_key_path)
                                    , comparison_result.get_event_status(comparison_result.root_key_path)])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=ComparisonResults.__name__))


class ComparisonDict:
    def __init__(self, comparisons: Dict[Tuple[str], ComparisonResult] = None) -> None:
        self.comparisons: Dict[Tuple[str], ComparisonResult] = comparisons if comparisons is not None else {}

    def get_keys(self) -> List[Tuple[str]]:
        return list(self.comparisons.keys())

    def add_comparison(self, key: Tuple[str], comparison_result: ComparisonResult):
        self.comparisons.update({key: comparison_result})

    def get_comparison(self, key: Tuple[str]) -> ComparisonResult:
        if key not in self.get_keys():
            raise ValueError('Comparison Dictionary does not contain the requested key : ' + key)
        return self.comparisons[key]


class ComparisonEventHelper:
    """
    Helper class for standard methods involving Comparison Event object

    """

    @classmethod
    def get_comparison_key_string(cls, key_list: List[str]):
        return 'root' + ''.join(['[\'' + key_entry + '\']' for key_entry in key_list])

    @classmethod
    def dfcompare_values(cls, val1, val2) -> str:
        """
        Compares 2 values by checking if they are valued and if their value is different.
        Tested and validated for types : str, int, bool, float
        Any type with "!=" implemented will work

        Parameters
        -----------
        val1
            The original value

        val2
            The new value

        Returns
        -----------
        comparison_result : a string representing the comparison event change
            The comparison result will be :
                - Raises an error if types of both values are not equal
                - ComparisonEvent.NO_CHANGE_EVENT if both values are not valued or if both values are valued and equal
                - ComparisonEvent.NEW_EVENT if val1 is None and val2 is valued
                - ComparisonEvent.UPDATE_EVENT if both values are valued but are not equal
                - ComparisonEvent.REMOVE_EVENT if val1 is valued and val2 is None
        """
        if val1 is None:
            if val2 is None:
                return ComparisonEvent.NO_CHANGE_EVENT
            else:
                return ComparisonEvent.NEW_EVENT
        elif val2 is None:
            return ComparisonEvent.REMOVE_EVENT
        if type(val1) != type(val2):
            raise ValueError('Types of the values are not the same : ' + val1 + ' and ' + val2)
        if val1 != val2:
            return ComparisonEvent.UPDATE_EVENT
        return ComparisonEvent.NO_CHANGE_EVENT

    @classmethod
    def create_comparison_event(cls, key: Tuple[str], val1, val2) -> List[ComparisonEvent]:
        """
        Creates a list of standard event comparison based on the comparison of both values provided.

        Both values to compare need to be of the same type.
        Standard comparison compared original and new values/objects in their entirety and one
        Specific comparison for dict type values/objects. In this case, the method works recursively
        to compare each dictionary key-value pair.

        This method works recursively, when comparison type is dict

        Parameters
        ----------
        key : Tuple[str]
            The key for comparison
        val1
            The original value
        val2
            The new value

        Returns
        -------
            The list of Comparison Event for the comparison between val1 and val2
        """
        if (val1 is None) & (val2 is None):
            return [ComparisonEvent(cls.dfcompare_values(val1, val2), key, val1, val2, None)]
        if (val1 is None) | (val2 is None):
            return [ComparisonEvent(cls.dfcompare_values(val1, val2), key, val1, val2
                                    , type(val1) if val1 is not None else type(val2))]
        if not (type(val1) is type(val2)):
            raise ValueError('Types of the values are not the same : ' + val1 + ' and ' + val2)
        if type(val1) is dict:
            if (len(val1.keys()) == 0) & (len(val2.keys()) == 0):
                return [ComparisonEvent(ComparisonEvent.NO_CHANGE_EVENT, key, None, None, dict)]
            lcl_dict_keys = get_unique_key_list(val1, val2)
            lcl_dict_keys.sort()
            comparison_events = []
            for lcl_key in lcl_dict_keys:
                lcl_key_path = key + (lcl_key,)
                comparison_events.extend(
                    cls.create_comparison_event(lcl_key_path, val1.get(lcl_key), val2.get(lcl_key)))
            return comparison_events
        return [
            ComparisonEvent(cls.dfcompare_values(val1, val2), key, val1, val2, type(val1)
            if val1 is not None else type(val2))]

    @classmethod
    def create_new_event(cls, key, val, _type) -> ComparisonEvent:
        """
        Creates a standard event with NEW status

        Parameters
        ----------
        key
            The key of the event
        val
            The new value
        _type
            The type of the value

        Returns
        -------
            A standard event with NEW status with information provided
        """
        return ComparisonEvent(ComparisonEvent.NEW_EVENT, key, None, val, _type)

    @classmethod
    def create_remove_event(cls, key, val, _type) -> ComparisonEvent:
        """
        Creates a standard event with REMOVE status

        Parameters
        ----------
        key
            The key of the event
        val
            The original value
        _type
            The type of the value

        Returns
        -------
            A standard event with REMOVE status with information provided
        """
        return ComparisonEvent(ComparisonEvent.REMOVE_EVENT, key, val, None, _type)
