
import globals
import xml.etree.ElementTree as ET
from pathlib import Path
import sqlite3

def validate_inference_path() :
    """
    How to validate this xml file...
    - check that it exists
    - check that it holds all necessary values
    """
    p = Path(globals.PATH_TO_INFERENCE)
    if not p.is_file() :
        raise RuntimeError("Inference.xml file does not exist, please create or update path in globals.py")

    tree = ET.parse(globals.PATH_TO_INFERENCE)
    root = tree.getroot()
    for name, _ in root.attrib.items() :
        if name not in globals.IGNORE  \
                and name not in globals.CONTINUOUS_KNOB_ORDER \
                and name not in globals.SWITCH_ORDER \
                and name not in globals.MODES_ORDER_LENGTHS \
                and "Description" in name: 
            raise RuntimeError(f"Invalid Inference.xml file. '{name}' is not recognized.")



def validate_database():
    conn = sqlite3.connect(globals.PATH_TO_DATABASE)
    curs = conn.cursor()

    curs.execute("""
                 CREATE TABLE IF NOT EXISTS                 
                 training_data(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            description TEXT, 
                            embedded_description BLOB, 
                            input_params BLOB, 
                            cont_targs BLOB, 
                            switch_targs BLOB, 
                            mode_targs BLOB, 
                            level TEXT, 
                            origin TEXT, 
                            request_type INTEGER, 
                            description_name TEXT, 
                            request_type_text TEXT,
                            active_mask_cont BLOB,
                            active_mask_switch BLOB,
                            active_mask_mode BLOB,
                            polarity_cont BLOB,
                            polarity_switch BLOB,
                            level_cont BLOB)
                 """)
    
    conn.commit()
    conn.close()



if __name__=="__main__" :
    validate_inference_path()
    validate_database()
    print("Valid")


