import csv
from typing import Dict
import os
from datetime import datetime

from dftools.events import log_event
from dftools.events.events import CSVFileWriteSuccessful
from dftools.core.compare import ComparisonResult, ComparisonResults
from dftools.core.structure.compare.structure_compare import StructureComparator
from dftools.core.structure.core import Namespace, StructureCatalog
from dftools.utils.list_util import concat_list_and_deduplicate


class StructureCatalogComparisonResult:
    def __init__(self, orig: StructureCatalog, new: StructureCatalog, comparison: Dict[Namespace, ComparisonResults]):
        self.orig = orig
        self.new = new
        self.comparison = comparison


class StructureCatalogComparator:
    def __init__(self, structure_comparator: StructureComparator):
        self.structure_comparator = structure_comparator
        self.comparison_results: StructureCatalogComparisonResult = None

    def compare(self, orig: StructureCatalog, new: StructureCatalog) -> StructureCatalogComparisonResult:
        namespace_list = concat_list_and_deduplicate(orig.get_namespaces(), new.get_namespaces())
        comparison_results = {}
        for namespace in namespace_list:
            str_comparison_results = self.structure_comparator.compare_multiple(
                orig.get_structures(namespace) if orig.has_namespace(namespace) else {}
                , new.get_structures(namespace) if new.has_namespace(namespace) else {}
            )
            comparison_results.update({namespace: str_comparison_results})

        self.comparison_results = StructureCatalogComparisonResult(orig, new, comparison_results)
        return self.comparison_results

    def to_csv_complete(self, output_folder_path: str, comparison_name: str):
        if self.comparison_results is not None:
            now = datetime.now()
            now_str = now.strftime("%Y%m%d_%H%M%S")

            os.makedirs(output_folder_path, exist_ok=True)

            output_file_name = f'{comparison_name}_{now_str}.csv'
            output_file_path = os.path.abspath(os.path.join(output_folder_path, output_file_name))
            output_summary_file_name = f'{comparison_name}_{now_str}.Summary.csv'
            output_summary_file_path = os.path.abspath(os.path.join(output_folder_path, output_summary_file_name))

            self.to_csv(file_path=output_file_path)
            self.to_csv_summary(file_path=output_summary_file_path)

    def to_csv(self, file_path: str, newline: str = '', delimiter: str = ';', quotechar: str = '"') -> None:
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['DataBank', 'Catalog', 'Namespace', 'Structure Name', 'Key', 'Event', 'Old', 'New'])
            # Data row
            for namespace, comparison_results in self.comparison_results.comparison.items():
                for comparison_result in comparison_results:
                    for comparison_event in comparison_result.events:
                        writer.writerow([namespace.databank_name, namespace.catalog, namespace.namespace
                                        , '.'.join(comparison_result.root_key_path), '.'.join(comparison_event.key)
                                        , comparison_event.status, comparison_event.old, comparison_event.new])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=ComparisonResult.__name__))

    def to_csv_summary(self, file_path: str, newline: str = '', delimiter: str = ';', quotechar: str = '"') -> None:
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            # Header row
            writer.writerow(['DataBank', 'Catalog', 'Namespace', 'Structure Name', 'Event'])
            # Data row
            for namespace, comparison_results in self.comparison_results.comparison.items():
                for comparison_result in comparison_results:
                    writer.writerow([namespace.databank_name, namespace.catalog, namespace.namespace
                                    , '.'.join(comparison_result.root_key_path)
                                    , comparison_result.get_event_status(comparison_result.root_key_path)])
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=ComparisonResults.__name__))
