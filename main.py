
import xml.etree.ElementTree as ET
import os
import numpy as np
import sqlite3
import utils
import globals
from rich import print
import questionary



def make_some_presets(path: str) :
    tree = ET.parse(path)
    root = tree.getroot()

    input_knobs = [0 for _ in range(len(globals.CONTINUOUS_KNOB_ORDER))]
    input_switches = [0 for _ in range(len(globals.SWITCH_ORDER))]
    input_modes = [0 for _ in range(len(globals.MODES_ORDER_LENGTHS))]         

    for name, param in root.attrib.items() :
        if name in globals.CONTINUOUS_KNOB_ORDER :
            idx = globals.CONTINUOUS_KNOB_ORDER[name]
            input_knobs[idx] = np.float64(param)
        
        if name in globals.SWITCH_ORDER :
            idx = globals.SWITCH_ORDER[name]
            input_switches[idx] = np.float64(param)

        if name in globals.MODES_ORDER_LENGTHS :
            idx = globals.MODES_ORDER_LENGTHS[name]['index']
            length = globals.MODES_ORDER_LENGTHS[name]['num_options']
            norm_idx = globals.MODES_ORDER_LENGTHS[name]['unormalized'].index(param)
            norm_param = globals.NORMALIZED_MODES_VALUES[length][norm_idx]
            input_modes[idx] = np.float64(norm_param)





    print("============================================================================\n")
    # print("[bold]Find a new sound and save it to inference.atp[/bold]")
    done = str(questionary.text("Find a new sound and save it to inference.atp. Finished? (y/n)\n").ask())
    print("\n")
    while done != 'y' :
        done = input("Wrong Button...Press y when finished.\n")


    """
    Get all the descriptions
    """
    tweakDescriptions = []
    tweakDescriptions.append(str(questionary.text("First Tweak Description: Technical Changes\n", qmark="❯").ask()))
    tweakDescriptions.append(str(questionary.text("Second Tweak Description: Musical Language\n", qmark="❯").ask()))
    tweakDescriptions.append(str(questionary.text("Third Tweak Description: Poetic Language\n", qmark="❯").ask()))
    print("\n")
    patchDescriptions = []
    patchDescriptions.append(str(questionary.text("First Patch Description: Technical Language\n", qmark="❯").ask()))
    patchDescriptions.append(str(questionary.text("Second Patch Description: Musical Language\n", qmark="❯").ask()))
    patchDescriptions.append(str(questionary.text("Third Patch Description: Poetic Language\n", qmark="❯").ask()))
    print("\n")
    
    """
    Read the updated XML file
    """
    tree = ET.parse(path)
    root = tree.getroot()



    """
    Get the tweak data
    """
    final_knobs = [0 for _ in range(len(globals.CONTINUOUS_KNOB_ORDER))]
    final_switches = [0 for _ in range(len(globals.SWITCH_ORDER))]
    final_modes = [0 for _ in range(len(globals.MODES_ORDER_LENGTHS))]      

    active_mask_cont = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.int64)
    active_mask_switch = np.zeros(len(globals.SWITCH_ORDER), dtype=np.int64)
    active_mask_mode = np.zeros(len(globals.MODES_ORDER_LENGTHS), dtype=np.int64)

    polarity_cont = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.int64)
    polarity_switch = np.zeros(len(globals.SWITCH_ORDER), dtype=np.int64)
    level_cont = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.float32)   

    for name, param in root.attrib.items() :
        if name in globals.CONTINUOUS_KNOB_ORDER :
            idx = globals.CONTINUOUS_KNOB_ORDER[name]
            if np.float64(param) != input_knobs[idx] :
                final_knobs[idx] = np.float64(param) - input_knobs[idx] #itsa delta
                print(f"{name} has been changed")
                active_mask_cont[idx] = 1
                if(final_knobs[idx] > 0) :
                    polarity_cont[idx] = 1
                else :
                    polarity_cont[idx] = -1

                abs_delta = abs(final_knobs[idx])
                if 0 < abs_delta < 0.33:
                    level_cont[idx] = 0.33
                elif 0.33 <= abs_delta < 0.66:
                    level_cont[idx] = 0.66
                elif 0.66 <= abs_delta <= 1.0:
                    level_cont[idx] = 1.0
        
        if name in globals.SWITCH_ORDER :
            idx = globals.SWITCH_ORDER[name]
            final_switches[idx] = np.float64(param)
            if np.float64(param) != input_switches[idx] :
                active_mask_switch[idx] = 1
                print(f"{name} has been changed")
                if(final_switches[idx] == 1) : 
                    polarity_switch[idx] = 1
                else :
                    polarity_switch[idx] = -1

        if name in globals.MODES_ORDER_LENGTHS :
            idx = globals.MODES_ORDER_LENGTHS[name]['index']
            length = globals.MODES_ORDER_LENGTHS[name]['num_options']
            norm_idx = globals.MODES_ORDER_LENGTHS[name]['unormalized'].index(param)
            norm_param = globals.NORMALIZED_MODES_VALUES[length][norm_idx]
            final_modes[idx] = norm_idx

            if norm_param != input_modes[idx] : 
                print(f"{name} has been changed")
                active_mask_mode[idx] = 1


    init_list = np.concatenate((input_knobs, input_switches, input_modes), axis=0)
    
    try: 
        for d in tweakDescriptions :
            utils.write_to_database(d, utils.token_embed(d), init_list, 
                            final_knobs, final_switches, final_modes, 
                            level="", origin="homemade", 
                            request_type_text=globals.ROUTER_TYPE_LIST[0], request_type=0, 
                            description_name="", 
                            active_mask_cont=active_mask_cont, 
                            active_mask_switch=active_mask_switch, 
                            active_mask_mode=active_mask_mode,
                            polarity_cont=polarity_cont,
                            polarity_switch=polarity_switch,
                            level_cont=level_cont)
    except Exception as e:
        print(f"[bold red]Failed to save tweak descriptions: {e}[/bold red]")
        



    """
    Get the patch data
    """
    init_cont_list, init_switch_list, init_mode_list = utils.get_neutral_values() 
    init_list = np.concatenate((init_cont_list, init_switch_list, init_mode_list), axis=0)

    continuous_targets = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.float32)
    switch_targets = np.zeros(len(globals.SWITCH_ORDER), dtype=np.int64)
    mode_targets = np.zeros(len(globals.MODES_ORDER_LENGTHS), dtype=np.int64)

    active_mask_cont = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.int64)
    active_mask_switch = np.zeros(len(globals.SWITCH_ORDER), dtype=np.int64)
    active_mask_mode = np.zeros(len(globals.MODES_ORDER_LENGTHS), dtype=np.int64)

    polarity_cont = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.int64)
    polarity_switch = np.zeros(len(globals.SWITCH_ORDER), dtype=np.int64)
    level_cont = np.zeros(len(globals.CONTINUOUS_KNOB_ORDER), dtype=np.int64)

    neutral_param = utils.get_neutral_params() # get neutral params (all normalized)

    for name, param in root.attrib.items() :
        #if a knob
        if name in globals.CONTINUOUS_KNOB_ORDER :
            idx = globals.CONTINUOUS_KNOB_ORDER[name]
            continuous_targets[idx] = round(np.float32(param), globals.DECIMALS) # Store the value of the updated xml
            if neutral_param[name] != continuous_targets[idx] : # Check to see if the parameter is off-neutral, if so, mark it as actively changed
                active_mask_cont[idx] = 1 

            if neutral_param[name] < continuous_targets[idx] :
                polarity_cont[idx] = 1
            elif neutral_param[name] > continuous_targets[idx] :
                polarity_cont[idx] = -1
            
            level_cont[idx] = abs(neutral_param[name] - continuous_targets[idx])

        #if a switch
        elif name in globals.SWITCH_ORDER :
            idx = globals.SWITCH_ORDER[name]
            switch_targets[idx] = round(np.float32(param), globals.DECIMALS) # Store the value of the updated xml
            if neutral_param[name] != switch_targets[idx] :
                active_mask_switch[idx] = 1

            if switch_targets[idx] == 0 :
                polarity_switch[idx] = -1
            elif switch_targets[idx] == 1 :
                polarity_switch[idx] = 1

        
        elif name in globals.MODES_ORDER_LENGTHS :
            idx = globals.MODES_ORDER_LENGTHS[name]['index']
            length = globals.MODES_ORDER_LENGTHS[name]['num_options'] #get length of mode options
            norm_idx = globals.MODES_ORDER_LENGTHS[name]['unormalized'].index(param) #get index within mode (i.e. the target in this case)
            norm_param = globals.NORMALIZED_MODES_VALUES[length][norm_idx] #get normalized parameter value
            mode_targets[idx] = norm_idx #remember, the target here is the index in the respective mode bank...we are storing value of the current xml

            if neutral_param[name] != np.float32(norm_param) :
                active_mask_mode[idx] = 1


    try:
        for d in patchDescriptions :
            utils.write_to_database(d, utils.token_embed(d), init_list, 
                            continuous_targets, switch_targets, mode_targets, 
                            level="", origin="homemade", 
                            request_type_text=globals.ROUTER_TYPE_LIST[1], request_type=1, 
                            description_name="", 
                            active_mask_cont=active_mask_cont, 
                            active_mask_switch=active_mask_switch, 
                            active_mask_mode=active_mask_mode,
                            polarity_cont=polarity_cont,
                            polarity_switch=polarity_switch,
                            level_cont=level_cont)
    except Exception as e:
        print(f"[bold red]Failed to save patch descriptions: {e}[/bold red]")



if __name__=="__main__" :
    running = True
    session_count = 0

    while running :
        make_some_presets(globals.PATH_TO_INFERENCE)

        conn = sqlite3.connect(globals.PATH_TO_DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT COUNT (*) FROM training_data")
        count = cur.fetchone()[0]
        print(f"> [italic]Database Size: {count}[/italic]")
        session_count += 6
        conn.close()

        still_running = str(questionary.text("Go again?(y/n)\n").ask())
        if still_running != 'y' :
            running = False
    
    print(f"> [italic]Nice going, you made {session_count} new data points! See you next time.[/italic]\n")
