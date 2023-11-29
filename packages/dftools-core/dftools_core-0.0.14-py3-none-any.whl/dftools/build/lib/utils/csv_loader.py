import csv
from typing import List

class CsvLoader():
    """
        Standard Class to read/write csv files
    """
    def __init__(self) -> None:
        pass

    def _get_csv_input_parameters(self) -> dict:
        return NotImplementedError('The _get_csv_input_parameters method is not implemented')
    
    def _get_csv_row_types(self) -> str:
        return self._get_csv_input_parameters()["row_types"]

    def _get_csv_row_first_element(self) -> str:
        return self._get_csv_input_parameters()["first_element"]

    def _get_csv_row_type_column_position(self) -> str:
        return self._get_csv_input_parameters()["row_type_column_position"]

    def read_csv_to_list(self, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"'
        , encoding: str = 'ISO 8859-1') -> None:
        """
        Reads csv format with the standard description of structures and returns a list of the class
        
        Parameters
        -----------
            file_path : the csv data dictionnary file path
            newline : the newline string describing the file, defaulted to "" (empty string)
            delimiter : the delimiter string describing the file, defaulted to ";"
            quotechar : the quotechar string describing the file, defaulted to "\"" (double quote)
            encoding : the encoding of the file to read

        Returns
        -----------
            A list of objects based on the data available in the csv file
        """
        row_type_column=self._get_csv_row_type_column_position()
        row_types=self._get_csv_row_types()
        first_row_type=self._get_csv_row_first_element()
        objects_read=[]
        current_object={}
        with open(file_path, newline=newline, encoding=encoding) as csvfile:
            next(csvfile)
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            i=0
            for row in reader:
                row_type = row[row_type_column]
                if str(row_type) ==  first_row_type:
                    if i != 0 : 
                        objects_read.append(current_object)
                    current_object = {}
                row_type_info = row_types[row_type]
                current_row_type_name = row_type_info['name']
                new_object = eval(row_type_info['method_rule'])
                if current_row_type_name in current_object.keys():
                    current_list : list=current_object[current_row_type_name]
                    current_list.append(new_object)
                else :
                    current_object.update({current_row_type_name : [new_object]})
                i+=1
            
            # After the read, add the last found structure to the structures read
            objects_read.append(current_object)
        return objects_read

    def get_header_row_list(self) -> List[str]:
        return NotImplementedError('The get_header_row_list method is not implemented')

    def as_list(self) -> list:
        return NotImplementedError('The as_list method is not implemented')
    
    def to_csv(self, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"') -> None:
        """
        Writes to a csv file format
        
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
            writer.writerow(self.get_header_row_list())
            # Data row
            for row in self.as_list():
                writer.writerow(row)
    
    # Read / Write Methods
    
    def _get_list_from_single_cell(input_str : str, delimiter : str = ',') -> list:
        return [entry.strip() for entry in input_str.split(delimiter) if entry.strip() != '']
    
    def _get_int_from_single_cell(input_str : str) -> int:
        return int(input_str) if (input_str is not None) & (input_str.strip() != '') else None
    
    def _get_int_from_bool_single_cell(input_str : str) -> int:
        if input_str is None:
            return False
        if input_str == '':
            return False
        return True if int(input_str) == 1 else False

    def _get_nullable_string_from_single_cell(input_str : str) -> str:
        return input_str if input_str != '' else None

    def _get_str_from_str_single_cell(input_str : str) -> str:
        if input_str is None:
            return None
        if input_str.strip() == '':
            return None
        return input_str