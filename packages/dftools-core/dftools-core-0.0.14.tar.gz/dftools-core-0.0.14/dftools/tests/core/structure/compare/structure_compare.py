import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core import Structure
from dftools.core.compare import ComparisonEvent
from dftools.core.structure.compare import StructureComparisonResult, StructureComparator


class StructureCompareTest(unittest.TestCase):
    maxDiff = 5000

    DFT_STRUCTURE_ORIG1_DICT = {
        "name": "df_product"
        , "desc": "Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'",
               "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}, {"name": "UID"}]}
        ]
    }

    DFT_STRUCTURE_ORIG2_DICT = {
        "name": "df_product"
        , "desc": "MD - Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'",
               "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}, {"name": "UID"}]}
        ]
    }

    DFT_STRUCTURE_ORIG3_DICT = {
        "name": "df_product"
        , "desc": "MD - Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "MD_PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}]}
            , {"name": "type", "desc": "Type of the product", "position": 3, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
        ]
    }

    DFT_STRUCTURE_ORIG4_DICT = {
        "name": "df_product"
        , "desc": "MD - Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "MD_PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}]}
            , {"name": "type1", "desc": "Type of the product", "position": 3, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
        ]
    }

    def test_compare_structure_desc_changed_and_std_methods(self):
        log_event_default(StdTestEvent("Structure Compare - Test Compare for Desc attribute change - Start"))
        str1 = Structure.from_dict(self.DFT_STRUCTURE_ORIG1_DICT)
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str1, str2)

        # Check that the only recorded difference is at structure attribute level on the attribute desc
        self.assertIsNotNone(str_comparison)
        changes = str_comparison.get_sub_comparison_for_all_changes()
        self.assertIsNotNone(changes)
        self.assertEqual(StructureComparisonResult, type(changes))
        self.assertEqual(1, changes.get_number_of_events())
        change_event = changes.get_events()[0]
        self.assertIsNotNone(change_event)
        self.assertEqual(tuple, type(change_event.key))
        self.assertEqual("UPDATE", change_event.status)
        self.assertEqual("MD - Product Table", change_event.new)
        self.assertEqual("Product Table", change_event.old)

        # There should be one leaf for the structure level, one leaf for the fields attribute (key length = 2) and one leaf per field
        # In this example, as there are 2 fields, the number of leafs is expected to be 4
        self.assertIsNotNone(str_comparison.get_keys_except_leafs())
        self.assertEqual(6, len(str_comparison.get_keys_except_leafs()))
        self.assertEqual([('df_product',), ('df_product', 'fields'), ('df_product', 'fields', 'id'),
                          ('df_product', 'fields', 'id', 'characterisations')
                             , ('df_product', 'fields', 'code'), ('df_product', 'fields', 'code', 'characterisations')]
                         , str_comparison.get_keys_except_leafs())

        # There are 5 structure-level attributes to be checked
        structure_att_events = str_comparison.get_events_on_structure_attributes()
        self.assertIsNotNone(structure_att_events)
        self.assertEqual(5, len(structure_att_events))
        structure_att_comp = str_comparison.get_comparison_of_structure_attributes()
        self.assertIsNotNone(structure_att_comp)
        self.assertEqual(5, len(structure_att_comp.events))
        self.assertEqual(4, len(structure_att_comp.get_events_by_status()[ComparisonEvent.NO_CHANGE_EVENT]))
        self.assertEqual(1, len(structure_att_comp.get_events_by_status()[ComparisonEvent.UPDATE_EVENT]))

        # There should be 2 field keys for this structure comparison
        field_keys = str_comparison.get_field_keys()
        self.assertIsNotNone(field_keys)
        self.assertEqual(2, len(field_keys))
        self.assertEqual([('df_product', 'fields', 'id'), ('df_product', 'fields', 'code')], field_keys)

        field_events = str_comparison.get_events_on_field_attributes()
        self.assertIsNotNone(field_events)
        self.assertEqual(2, len(field_events))
        field_id_events = field_events[('df_product', 'fields', 'id')]
        self.assertIsNotNone(field_id_events)
        self.assertEqual(11, len(field_id_events))

        field_comparison_dict = str_comparison.get_comparison_of_fields()
        self.assertIsNotNone(field_comparison_dict)
        self.assertEqual(2, len(field_comparison_dict.get_keys()))
        field_comparison = field_comparison_dict.get_comparison(('df_product', 'fields', 'id'))
        self.assertIsNotNone(field_comparison)
        self.assertEqual(11, field_comparison.get_number_of_events())
        self.assertEqual(11, len(field_comparison.get_events_by_status()[ComparisonEvent.NO_CHANGE_EVENT]))
        self.assertEqual(0, len(field_comparison.get_events_by_status()[ComparisonEvent.UPDATE_EVENT]))

        log_event_default(StdTestEvent("Structure Compare - Test Compare for Desc attribute change - Succeeded"))

    def test_compare_with_field_changes(self):
        log_event_default(StdTestEvent("Structure Compare - Test Compare with Field Changes (Comparator checks with "
                                       "and without characterisations) - Start"))
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str2, str3)

        # UC #1 : Check that the only recorded difference is at structure attribute level on the attribute desc 
        # and that field "code" is flagged as different due to the characterisations
        self.assertIsNotNone(str_comparison)
        str_att_comparison = str_comparison.get_comparison_of_structure_attributes()
        self.assertIsNotNone(str_att_comparison)
        str_att_changes = str_att_comparison.get_all_changes_events()
        self.assertIsNotNone(str_att_changes)
        self.assertEqual(1, len(str_att_changes))
        str_att_change = str_att_changes[0]
        self.assertIsNotNone(str_att_change)
        self.assertEqual(('df_product', 'options', 'func_domain'), str_att_change.key)
        self.assertEqual(ComparisonEvent.UPDATE_EVENT, str_att_change.status)
        self.assertEqual(str, str_att_change.type)
        self.assertEqual('MD_PRODUCT', str_att_change.new)
        self.assertEqual('PRODUCT', str_att_change.old)

        # Check that the field recorded differences match the difference in source json
        field_keys = str_comparison.get_field_keys()
        self.assertIsNotNone(field_keys)
        self.assertEqual(3, len(field_keys))
        self.assertEqual([('df_product', 'fields', 'id'), ('df_product', 'fields', 'code')
                             , ('df_product', 'fields', 'type')]
                         , field_keys)

        fld_att_comparison_dict = str_comparison.get_comparison_of_fields()
        self.assertIsNotNone(fld_att_comparison_dict)
        self.assertTrue(('df_product', 'fields', 'id') in fld_att_comparison_dict.get_keys())
        self.assertTrue(('df_product', 'fields', 'code') in fld_att_comparison_dict.get_keys())
        self.assertTrue(('df_product', 'fields', 'type') in fld_att_comparison_dict.get_keys())

        fld_att_comp_id = fld_att_comparison_dict.get_comparison(('df_product', 'fields', 'id'))
        self.assertIsNotNone(fld_att_comp_id)
        self.assertEqual(0, fld_att_comp_id.get_number_of_changes())

        # Only change on code is on the characterisations with a characterisation removed
        fld_att_comp_code = fld_att_comparison_dict.get_comparison(('df_product', 'fields', 'code'))
        self.assertIsNotNone(fld_att_comp_code)
        self.assertEqual(1, fld_att_comp_code.get_number_of_changes())
        fld_att_comp_code_change = fld_att_comp_code.get_all_changes_events()[0]
        self.assertIsNotNone(fld_att_comp_code_change)
        self.assertEqual(('df_product', 'fields', 'code', 'characterisations', 'UID'), fld_att_comp_code_change.key)

        # UC #2 : Check on the field "code" should return no differences in this use case 
        str_comparator = StructureComparator(field_characterisation_to_check=False)
        str_comparison = str_comparator.compare(str2, str3)
        self.assertIsNotNone(str_comparison)

        fld_att_comparison_dict = str_comparison.get_comparison_of_fields()
        self.assertIsNotNone(fld_att_comparison_dict)
        self.assertTrue(('df_product', 'fields', 'code') in fld_att_comparison_dict.get_keys())

        # No changes should be recorded and no comparison event should be available for attribute characterisations
        fld_att_comp_code = fld_att_comparison_dict.get_comparison(('df_product', 'fields', 'code'))
        self.assertIsNotNone(fld_att_comp_code)
        self.assertEqual(0, fld_att_comp_code.get_number_of_changes())
        self.assertFalse(('df_product', 'fields', 'code', 'characterisations') in fld_att_comparison_dict.get_keys())

        log_event_default(StdTestEvent("Structure Compare - Test Compare with Field Changes (Comparator checks with "
                                       "and without characterisations) - Succeeded"))

    def test_to_csv(self):
        log_event_default(StdTestEvent("Structure Compare - Test to_csv - Start"))
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str2, str3)

        file_path = './output/structure_comparison_output.csv'
        abs_file_path = os.path.abspath(file_path)
        if os.path.exists(abs_file_path):
            if os.path.isfile(abs_file_path):
                os.remove(abs_file_path)
            else:
                raise ValueError('Cannot remove object located at : ' + abs_file_path)

        self.assertFalse(os.path.exists(abs_file_path))

        str_comparison.to_csv(abs_file_path)

        self.assertTrue(os.path.exists(abs_file_path))
        with open(abs_file_path, "r") as file:
            file_data = file.read()
            self.assertEqual("""Root Key;Key;Status;Old;New
df_product;df_product.name;NOCHANGE;df_product;df_product
df_product;df_product.desc;NOCHANGE;MD - Product Table;MD - Product Table
df_product;df_product.type;NOCHANGE;BASE TABLE;BASE TABLE
df_product;df_product.options.func_domain;UPDATE;PRODUCT;MD_PRODUCT
df_product;df_product.content_type;NOCHANGE;[];[]
df_product;df_product.fields.id.name;NOCHANGE;id;id
df_product;df_product.fields.id.desc;NOCHANGE;ID of the product;ID of the product
df_product;df_product.fields.id.position;NOCHANGE;1;1
df_product;df_product.fields.id.data_type;NOCHANGE;NUMERIC;NUMERIC
df_product;df_product.fields.id.length;NOCHANGE;10;10
df_product;df_product.fields.id.precision;NOCHANGE;0;0
df_product;df_product.fields.id.default_value;NOCHANGE;-1;-1
df_product;df_product.fields.id.characterisations.MANDATORY.attributes;NOCHANGE;;
df_product;df_product.fields.id.characterisations.TEC_ID.attributes;NOCHANGE;;
df_product;df_product.fields.id.characterisations.UID.attributes;NOCHANGE;;
df_product;df_product.fields.id.characterisations.UNIQUE.attributes;NOCHANGE;;
df_product;df_product.fields.code.name;NOCHANGE;code;code
df_product;df_product.fields.code.desc;NOCHANGE;Code of the product;Code of the product
df_product;df_product.fields.code.position;NOCHANGE;2;2
df_product;df_product.fields.code.data_type;NOCHANGE;STRING;STRING
df_product;df_product.fields.code.length;NOCHANGE;30;30
df_product;df_product.fields.code.precision;NOCHANGE;0;0
df_product;df_product.fields.code.default_value;NOCHANGE;'#';'#'
df_product;df_product.fields.code.characterisations.FCT_ID.attributes;NOCHANGE;;
df_product;df_product.fields.code.characterisations.UID;REMOVE;{'attributes': {}};
df_product;df_product.fields.code.characterisations.UNIQUE.attributes;NOCHANGE;;
df_product;df_product.fields.type;NEW;;"{'name': 'type', 'desc': 'Type of the product', 'position': 3, 'data_type': 'STRING', 'length': 30, 'precision': 0, 'default_value': ""'#'"", 'characterisations': [{'name': 'FREE_TEXT', 'attributes': {}}], 'sourcing_info': None}"
""", file_data)

        log_event_default(StdTestEvent("Structure Compare - Test to_csv - Succeeded"))

    def test_get_event_dict(self):
        log_event_default(StdTestEvent("Structure Compare - Test Get Event Dict - Start"))
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str2, str3)
        event_dict = str_comparison.get_event_dict()

        self.assertIsNotNone(event_dict)
        self.assertTrue('events' in event_dict.keys())
        self.assertTrue('df_product' in event_dict['events'].keys())
        self.assertTrue('options' in event_dict['events']['df_product'].keys())
        self.assertTrue('func_domain' in event_dict['events']['df_product']['options'].keys())
        self.assertEqual("UPDATE", event_dict['events']['df_product']['options']['func_domain']['status'])
        self.assertEqual("PRODUCT", event_dict['events']['df_product']['options']['func_domain']['old'])
        self.assertEqual("MD_PRODUCT", event_dict['events']['df_product']['options']['func_domain']['new'])

        self.assertTrue('fields' in event_dict['events']['df_product'].keys())
        self.assertTrue('code' in event_dict['events']['df_product']['fields'].keys())
        self.assertTrue('characterisations' in event_dict['events']['df_product']['fields']['code'].keys())
        self.assertTrue('UID' in event_dict['events']['df_product']['fields']['code']['characterisations'].keys())
        self.assertEqual({'attributes': {}}
                         , event_dict['events']['df_product']['fields']['code']['characterisations']['UID']['old'])

        self.assertTrue('type' in event_dict['events']['df_product']['fields'].keys())
        self.assertEqual("NEW", event_dict['events']['df_product']['fields']['type']['status'])
        self.assertEqual(
            {'name': 'type', 'desc': 'Type of the product', 'position': 3, 'data_type': 'STRING'
                , 'length': 30, 'precision': 0, 'default_value': "'#'"
                , 'characterisations': [{'name': 'FREE_TEXT', 'attributes': {}}], 'sourcing_info': None}
                         , event_dict['events']['df_product']['fields']['type']['new'])

        log_event_default(StdTestEvent("Structure Compare - Test Get Event Dict - Succeeded"))

    def test_get_event_status(self):
        log_event_default(StdTestEvent("Structure Compare - Test Get Event Status - Start"))
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str2, str3)
        self.assertIsNotNone(str_comparison)

        self.assertEqual('UPDATE', str_comparison.get_event_status(['df_product']))
        self.assertEqual('NOCHANGE', str_comparison.get_event_status(['df_product', 'desc']))
        self.assertEqual('UPDATE', str_comparison.get_event_status(['df_product', 'options']))
        self.assertEqual('UPDATE', str_comparison.get_event_status(['df_product', 'options', 'func_domain']))
        self.assertEqual('UPDATE', str_comparison.get_event_status(['df_product', 'fields']))
        self.assertEqual('NOCHANGE', str_comparison.get_event_status(['df_product', 'fields', 'id']))
        self.assertEqual('UPDATE', str_comparison.get_event_status(['df_product', 'fields', 'code']))
        self.assertEqual('NEW', str_comparison.get_event_status(['df_product', 'fields', 'type']))

        log_event_default(StdTestEvent("Structure Compare - Test Get Event Status - Succeeded"))

    def test_is_methods(self):
        log_event_default(StdTestEvent("Structure Compare - Test Is Methods - Start"))
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str2, str3)
        self.assertIsNotNone(str_comparison)
        self.assertEqual(("df_product",), str_comparison.get_structure_level_key())
        self.assertTrue(str_comparison.is_updated(['df_product']))
        self.assertFalse(str_comparison.is_new(['df_product']))
        self.assertFalse(str_comparison.is_removed(['df_product']))

        str_comparison = str_comparator.compare(None, str3)
        self.assertIsNotNone(str_comparison)
        self.assertEqual(("df_product",), str_comparison.get_structure_level_key())
        self.assertFalse(str_comparison.is_updated(['df_product']))
        self.assertTrue(str_comparison.is_new(['df_product']))
        self.assertFalse(str_comparison.is_removed(['df_product']))

        str_comparison = str_comparator.compare(str2, None)
        self.assertIsNotNone(str_comparison)
        self.assertEqual(("df_product",), str_comparison.get_structure_level_key())
        self.assertFalse(str_comparison.is_updated(['df_product']))
        self.assertFalse(str_comparison.is_new(['df_product']))
        self.assertTrue(str_comparison.is_removed(['df_product']))

        log_event_default(StdTestEvent("Structure Compare - Test Is Methods - Succeeded"))

    def test_field_changes_methods(self):
        log_event_default(StdTestEvent("Structure Compare - Test Field Changes methods - Start"))
        str2 = Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(str2, str3)

        self.assertIsNotNone(str_comparison)
        new_fields = str_comparison.get_new_fields()
        self.assertIsNotNone(new_fields)
        self.assertEqual(1, len(new_fields))
        self.assertEqual(dict, type(new_fields[0]))
        self.assertEqual("type", new_fields[0]['name'])
        self.assertEqual(30, new_fields[0]['length'])

        removed_fields = str_comparison.get_removed_fields()
        self.assertIsNotNone(removed_fields)
        self.assertEqual(0, len(removed_fields))

        log_event_default(StdTestEvent("Structure Compare - Test Field Changes methods - Succeeded"))

    def test_compare_with_field_renaming(self):
        log_event_default(StdTestEvent("Structure Compare - Test Compare with Field Renaming - Start"))
        str4 : Structure = Structure.from_dict(self.DFT_STRUCTURE_ORIG4_DICT)
        str3 = Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT)

        str_comparator = StructureComparator()

        # UC #1 : Comparison without the renaming of fields
        # The comparison should detect a removal for field type1 and detect a new field for field type
        str_comparison = str_comparator.compare(str4, str3)


        self.assertIsNotNone(str_comparison)
        fld_att_comparison_dict = str_comparison.get_comparison_of_fields()
        self.assertIsNotNone(fld_att_comparison_dict)
        self.assertEqual(4, len(fld_att_comparison_dict.get_keys()))
        self.assertTrue(('df_product', 'fields', 'code') in fld_att_comparison_dict.get_keys())
        self.assertTrue(('df_product', 'fields', 'type1') in fld_att_comparison_dict.get_keys())
        self.assertTrue(('df_product', 'fields', 'type') in fld_att_comparison_dict.get_keys())

        self.assertTrue('REMOVE', str_comparison.get_event_status(('df_product', 'fields', 'type1')))
        self.assertTrue('NEW', str_comparison.get_event_status(('df_product', 'fields', 'type')))

        # UC #1 : Comparison with the renaming of fields
        # The comparison should detect an update of field type1 with a change in the name of the field
        str_comparison = str_comparator.compare(str4, str3, renaming_mappings={'field': {'type1': 'type'}})

        self.assertIsNotNone(str_comparison)
        fld_att_comparison_dict = str_comparison.get_comparison_of_fields()
        self.assertIsNotNone(fld_att_comparison_dict)
        self.assertEqual(3, len(fld_att_comparison_dict.get_keys()))
        self.assertTrue(('df_product', 'fields', 'code') in fld_att_comparison_dict.get_keys())
        self.assertTrue(('df_product', 'fields', 'type1') in fld_att_comparison_dict.get_keys())
        self.assertFalse(('df_product', 'fields', 'type') in fld_att_comparison_dict.get_keys())

        self.assertTrue('UPDATE', str_comparison.get_event_status(('df_product', 'fields', 'type1')))

        log_event_default(StdTestEvent("Structure Compare - Test Compare with Field Renaming - Succeeded"))


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
