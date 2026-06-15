"""
@File: utils.py
@Author: Tom Garvey
@Version: 1.0
@Brief:
"""


import xml.etree.ElementTree as ET
import os
import numpy as np
from numpy.typing import NDArray
import globals
import copy
import sqlite3


"""
@Brief: Parses netural preset and gets parameters
@Params: 
@Return: a dictionary containing both params and name

"""
def get_neutral_params() :
    # localInputParams = []
    paramDict = {}
    tree = ET.parse("neutral.atp")
    root = tree.getroot()
    for name, param in root.attrib.items() :
        if name in globals.IGNORE or "Description" in name: 
            continue
        paramDict[name] = float(param) # neutral.atp is all normalized values
    return paramDict



"""
@Brief: Token and embed descriptions in XML files
@Params:
@Return: 
"""
def token_embed(description: str) :
    # print(f"Embedding ---------- {description}")
    embeddings = globals.TRANSFORMER_MODEL.encode(description, normalize_embeddings=True)
    return embeddings



def write_to_database(description: str, 
                      embedded_description: list, 
                      input_params: np.ndarray, 
                      cont_targs: np.ndarray, 
                      switch_targs: np.ndarray, 
                      mode_targs: np.ndarray, 
                      level: str, 
                      origin: str, 
                      request_type_text: str, 
                      request_type: int, 
                      description_name: str, 
                      active_mask_cont: np.ndarray,
                      active_mask_switch: np.ndarray,
                      active_mask_mode: np.ndarray,
                      polarity_cont: np.ndarray,
                      polarity_switch: np.ndarray,
                      level_cont: np.ndarray,
                      database=globals.PATH_TO_DATABASE) :

    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    command1 = """CREATE TABLE IF NOT EXISTS
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
                            level_cont BLOB
                            )"""
    
    cursor.execute(command1)

    embedded_description = np.array(embedded_description).copy()
    embedded_description = np.array(embedded_description, dtype=np.float32).tobytes()
    input_params = np.array(input_params, dtype=np.float32).tobytes()

    cont_targs = np.array(cont_targs, dtype=np.float32).tobytes()
    switch_targs = np.array(switch_targs, dtype=np.float32).tobytes() # Storing as float32 bc using BCE
    mode_targs = np.array(mode_targs, dtype=np.int64).tobytes()

    active_mask_cont =  np.array(active_mask_cont, dtype=np.float32).tobytes()
    active_mask_switch =  np.array(active_mask_switch, dtype=np.float32).tobytes()
    active_mask_mode =  np.array(active_mask_mode, dtype=np.float32).tobytes()
    
    polarity_cont = np.array(polarity_cont, dtype=np.float32).tobytes()
    polarity_switch = np.array(polarity_switch, dtype=np.float32).tobytes()
    level_cont = np.array(level_cont, dtype=np.float32).tobytes()


    cursor.execute("""INSERT INTO training_data (description, 
                                                embedded_description, 
                                                input_params, 
                                                cont_targs, 
                                                switch_targs, 
                                                mode_targs, 
                                                level, 
                                                origin, 
                                                request_type, 
                                                description_name, 
                                                request_type_text, 
                                                active_mask_cont,
                                                active_mask_switch,
                                                active_mask_mode,
                                                polarity_cont,
                                                polarity_switch,
                                                level_cont) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                                                (description, 
                                                 embedded_description, 
                                                 input_params, 
                                                 cont_targs, 
                                                 switch_targs, 
                                                 mode_targs, 
                                                 level, 
                                                 origin, 
                                                 request_type, 
                                                 description_name, 
                                                 request_type_text,
                                                 active_mask_cont,
                                                 active_mask_switch,
                                                 active_mask_mode,
                                                 polarity_cont,
                                                 polarity_switch,
                                                 level_cont ))

    connection.commit()
    connection.close()





def get_neutral_values() :

    continuous = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.float32)
    switch = np.zeros(len(globals.SWITCH_ORDER), dtype=np.float32)
    mode = np.zeros(len(globals.MODES_ORDER_LENGTHS), dtype=np.float32)

    tree = ET.parse("neutral.atp")
    root = tree.getroot()
    for name, param in root.attrib.items() :
        if name in globals.IGNORE :
            continue

        elif name in globals.CONTINUOUS_KNOB_ORDER :
            idx = globals.CONTINUOUS_KNOB_ORDER[name]
            continuous[idx] = round(np.float32(param), globals.DECIMALS)
        
        elif name in globals.SWITCH_ORDER :
            idx = globals.SWITCH_ORDER[name]
            switch[idx] = round(np.float32(param), globals.DECIMALS)
        
        elif name in globals.MODES_ORDER_LENGTHS :
            idx = globals.MODES_ORDER_LENGTHS[name]["index"]
            # print(f"FROM UTILS: {param}")
            mode[idx] = round(np.float32(param), globals.DECIMALS) #This is the normalized values here

    return continuous, switch, mode





