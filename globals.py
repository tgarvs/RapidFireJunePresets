"""
@File: globals.py
@Author: Tom Garvey
@Version: 1.0
@Brief: Globals for this entire project
"""

from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()
PATH_TO_INFERENCE = os.getenv("PATH_TO_INFERENCE")
PATH_TO_DATABASE = "RapidFire.db"

TRANSFORMER_MODEL = SentenceTransformer("tgarvs/all-MiniLM-L6-v2-music-fine-tuned") #model is in hugging face
DECIMALS = 4
IGNORE = ["Hold", "Tune", "Bypass", "Version", "Module0", "Module1", "Module2", "Module3", "ChorusRate", "ChorusNoise"]


SWITCH_ORDER = {
    "LFOSync" : 0,
    "LFOTrigger" : 1,
    "DCOLFOExtended" : 2,
    "VCFEnvelopeMode" : 3,
    "VCAMode" : 4,
    "GlideLegato" : 5,
    "ChorusII" : 6,
    "DriveEnable" : 7,
    "EchoEnable" : 8,
    "SpringEnable" : 9,
    "ArpeggiatorEnable" : 10,
    "ArpeggiatorVelocity" : 11,
    "Monophonic" : 12,
    "Legato" : 13,
    "DCOPulse" : 14,
    "DCOSaw" : 15,
    "DCOSuboscillator" : 16,
    "VCFEnvelopeSource" : 17,
    "ChorusI" : 18,
    "ChorusModel" : 19,
    "EchoSync" : 20,
    "PhaserEnable" : 21,
    "ArpeggiatorSync" : 22
}

#example of how this would work
# output_array_of_continuous_values = [0.2, 0.54, 0.23, 0.52, 0.11, 0.65, 0.78]
# lfotrigger = output_array_of_continuous_values[SWITCH_ORDER["LFOTrigger"]]
# print(lfotrigger)

CONTINUOUS_KNOB_ORDER = {
    "LFORate" : 0,
    "LFODelay" : 1,
    "DCOLFO" : 2,
    "DCOPWM" : 3,
    "DCOSuboscillatorVolume" : 4,
    "DCONoise" : 5, 
    "Highpass" : 6,
    "VCFFrequency" : 7,
    "VCFResonance" : 8,
    "VCFEnvelope" : 9,
    "VCFLFO" : 10,
    "VCFKeyboardTracking" : 11,
    "VCFVelocity" : 12,
    "VCALevel" : 13,
    "Velocity" : 14,
    "ENV1Attack" : 15,
    "ENV1Decay" : 16,
    "ENV1Sustain" : 17,
    "ENV1Release" : 18,
    "ENV2Attack" : 19,
    "ENV2Decay" : 20,
    "ENV2Sustain" : 21,
    "ENV2Release" : 22,
    "Glide" : 23,
    "DriveAmount" : 24,
    "DriveMix" : 25,
    "DriveTone" : 26,
    "EchoRate" : 27,
    "EchoFeedback" : 28,
    "EchoMix" : 29,
    "SpringPreDelay" : 30,
    "SpringTone" : 31,
    "SpringMix" : 32,
    "PhaserRate" : 33,
    "PhaserFeedback" : 34,
    "PhaserMix" : 35,
    "ArpeggiatorRate" : 36,
    "BendDCO" : 37,
    "BendVCF" : 38,
    "ModDCO" : 39,
    "ModVCF" : 40,
    "Volume" : 41,
    "Age" : 42,
    "UnisonFat" : 43
}

MODES_ORDER_LENGTHS = {
    "LFOWave" : {"index" : 0, "num_options" :  6, "unormalized" : ["SINE", "TRIANGLE", "SQUARE", "SAW UP", "SAW DOWN", "S&H"]},
    "LFOTriggerMode" : {"index" : 1, "num_options" : 3, "unormalized" : ["MOD WHEEL", "MANUAL", "AUTO"]},
    "DCOModulation" : {"index" : 2, "num_options" : 4, "unormalized" : ["LFO", "MANUAL", "ENV1", "ENV2"]},
    "DCOSuboscillatorOctave" : {"index" : 3, "num_options" : 3, "unormalized" : ["-12", "-24", "-36"]},
    "ArpeggiatorMode" : {"index" : 4, "num_options" : 4, "unormalized" : ["RANDOM", "DOWN", "UP & DOWN", "UP"]},
    "ArpeggiatorRange" : {"index" : 5, "num_options" : 4, "unormalized": ["4 OCT", "3 OCT", "2 OCT", "1 OCT"]},
    "ArpeggiatorBarReset" : {"index" : 6, "num_options" : 4, "unormalized" : ["4 BARS", "2 BARS", "1 BAR", "OFF"]},
    "ArpeggiatorNoteOrder" : {"index" : 7, "num_options" : 3, "unormalized" : ["CHORD", "PLAY", "PITCH"]},
    "Octave" : {"index" : 8, "num_options" : 3, "unormalized" : ["DOWN", "NORMAL", "UP"]},
    "Voices" : {"index" : 9, "num_options" : 27, "unormalized" : ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32" ]},
    "UnisonAmount" : {"index" : 10, "num_options" : 6, "unormalized" : ["1", "2", "3", "4", "5", "6"]}
}



# amount of options in set : corresponding normalized values
NORMALIZED_MODES_VALUES = {
    3 : [0.0, 0.5, 1.0],
    4 : [0.0, 0.3333333432674408, 0.6666666865348816, 1.0],
    6 : [0.0, 0.2000000029802322, 0.4000000059604645, 0.6000000238418579, 0.800000011920929, 1.0],
    27 : [0.0, 0.03846153989434242, 0.07692307978868484, 0.115384615957737, 0.1538461595773697, 0.1923076957464218, 0.2307692319154739, 0.2692307829856873, 0.3076923191547394, 0.3461538553237915, 0.3846153914928436, 0.4230769276618958, 0.4615384638309479, 0.5, 0.5384615659713745, 0.5769230723381042, 0.6153846383094788, 0.6538461446762085, 0.692307710647583, 0.7307692170143127, 0.7692307829856873, 0.807692289352417, 0.8461538553237915, 0.8846153616905212, 0.9230769276618958, 0.9615384340286255, 1.0]
}

# EXAMPLE OF HOW THIS WOULD WORK
# lfo_wave_output = 2 # from the nn
# norm_output = NORMALIZED_SET_VALUES[SETS_ORDER_LENGTHS["LFOWave"]["num_options"]][lfo_wave_output]
# print(norm_output)

ROUTER_TYPE_LIST = ["tweak", "patch", "undo"]


# Things that effect general descriptions of sounds
STYLE_COMMANDS = [ 
"brightness", #dark - bright
"texture", #clean - gritty
"temperature", #cold - warm
"body", #thin - fat
"material", #organic - metallic/glassy
"air", #clean - airy
"wetness", #dry - wet
"attack", #swelling - percussive,  THIS IS EQUIVALENT TO "onset"
"release", #short/tight, + long/ringing, THIS IS EQUIVALENT TO "tail"
"modulation" #no modulation - total modulation, 
]


# single parameter changes
ATOMIC_COMMANDS = [
"reverb_engaged",
"reverb_level",
"delay_engaged",
"delay_level",
"delay_feedback_level",
"phaser_engaged",
"phaser_level",
"overdrive_engaged",
"overdrive_level",
"overdrive_tone",
"overdrive_drive",
"noise_level",
"glide_level",
"arp_engaged",
"arp_speed",
"arp_single_octave",
"arp_mode",
"reset"
]