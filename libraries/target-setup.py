Import('env')

import os, shutil

variants = [
    { 'name': 'Flipper-Zero_WiFi-DevBoard',     'flag': 'MARAUDER_FLIPPER',       'tft_file': None                                 },
    { 'name': 'Flipper-Zero_MultiBoard_S3',     'flag': 'MARAUDER_MULTIBOARD_S3', 'tft_file': None                                 },
    { 'name': 'OG-Marauder',                    'flag': 'MARAUDER_V4',            'tft_file': 'User_Setup_og_marauder.h'           },
    { 'name': 'Marauder_v6',                    'flag': 'MARAUDER_V6',            'tft_file': 'User_Setup_og_marauder.h'           },
    { 'name': 'Marauder_v6_1',                  'flag': 'MARAUDER_V6_1',          'tft_file': 'User_Setup_og_marauder.h'           },
    { 'name': 'Marauder-Kit',                   'flag': 'MARAUDER_KIT',           'tft_file': 'User_Setup_og_marauder.h'           },
    { 'name': 'Marauder-Mini',                  'flag': 'MARAUDER_MINI',          'tft_file': 'User_Setup_marauder_mini.h'         },
    { 'name': 'ESP32-LDDB',                     'flag': 'ESP32_LDDB',             'tft_file': None                                 },
    { 'name': 'Marauder-DevBoard-Pro',          'flag': 'MARAUDER_DEV_BOARD_PRO', 'tft_file': None                                 },
    { 'name': 'M5StickCPlus',                   'flag': 'MARAUDER_M5STICKC',      'tft_file': 'User_Setup_marauder_m5stickc.h'     },
    { 'name': 'M5StickCPlus-2',                 'flag': 'MARAUDER_M5STICKCP2',    'tft_file': 'User_Setup_marauder_m5stickcp2.h'   },
    { 'name': 'Rev-Feather',                    'flag': 'MARAUDER_REV_FEATHER',   'tft_file': 'User_Setup_marauder_rev_feather.h'  },
    { 'name': 'Marauder_v7',                    'flag': 'MARAUDER_V7',            'tft_file': 'User_Setup_dual_nrf24.h'            },
    { 'name': 'Marauder_CYD_2432S028',          'flag': 'MARAUDER_CYD_MICRO',     'tft_file': 'User_Setup_cyd_micro.h'             },
    { 'name': 'Marauder_CYD_2432S024_GUITION',  'flag': 'MARAUDER_CYD_GUITION',   'tft_file': 'User_Setup_cyd_guition.h'           },
    { 'name': 'Marauder_CYD_2432W328C_GUITION', 'flag': 'MARAUDER_CYD_GUITION_W', 'tft_file': 'User_Setup_cyd_guition_w.h'         },
    { 'name': 'Marauder_CYD_2432S028_2USB',     'flag': 'MARAUDER_CYD_2USB',      'tft_file': 'User_Setup_cyd_2usb.h'              },
    { 'name': 'Marauder_CYD_3_5inch',           'flag': 'MARAUDER_CYD_3_5_INCH',  'tft_file': 'User_Setup_cyd_3_5_inch.h'          },
    { 'name': 'Marauder_v7_1',                  'flag': 'MARAUDER_V7_1',          'tft_file': 'User_Setup_dual_nrf24.h'            },
    { 'name': 'M5Cardputer',                    'flag': 'MARAUDER_CARDPUTER',     'tft_file': 'User_Setup_marauder_m5cardputer.h'  },
    { 'name': 'ESP32-C5_DevKitC-1',             'flag': 'MARAUDER_C5',            'tft_file': None                                 }
]


# get correct variant (build target == file_name)
variant = None
target = env.get('PIOENV')
for v in variants:
    if target == v['name']:
        variant = v
        break
if variant is None:
    Exit('Unsupported target: \'' + target + '\'')

# add compiler define for given variant
env.Append(CPPDEFINES = [ variant['flag'] ])

# copy correct User_Setup.h file for TFT_eSPI library
def copy_user_setup(env, node):
    assert str(node).endswith('TFT_eSPI.cpp')
    #with open('env.txt', 'w') as file:
    #    file.write(env.Dump())

    proj_dir = env.get('PROJECT_DIR')

    # replace User_Setup.h in TFT_eSPI library path with header for given target device
    for path in env.get('CPPPATH'):
        if (path.endswith('TFT_eSPI')):
            tft_file = variant['tft_file']
            if tft_file is not None:
                dst_file = os.path.relpath(os.path.join(path, 'User_Setup.h'), proj_dir)
                print('\'' + target + '\': Copy', tft_file, '->', dst_file)
                shutil.copy(tft_file, dst_file)
            break
    return node

# pre-step for TFT_eSPI library setup
env.AddBuildMiddleware(copy_user_setup, '*/TFT_eSPI.cpp')
