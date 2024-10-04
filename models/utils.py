from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
    
def merge_metadata(*original_metadata) -> MetaData:
    merged = MetaData()

    for original_metadatum in original_metadata:
        for table in original_metadatum.metadata.tables.values():
            table.to_metadata(merged)
    
    return merged

