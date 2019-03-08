'''
Created on Mar 2, 2019

@author: brendep
'''

n_strips = 16
# Number of LEDs per strip:
n_leds = 32
leds_per_global_row = 64

# This is the amount of white space that will be included on each line before a quad tuple
line_prefix = "               "

json_template = """
{
    "listen": [null, 7890],
    "relay": null,
    "verbose": true,

    "color": {
        "gamma": 2.5,
        "whitepoint": [1.0, 1.0, 1.0]
    },

    "devices": [
        {
            "type": "fadecandy",
            "serial": "IIJRDVHBZJSEIEFL",
            "map": [
Q_NW
            ]
        },
        {
            "type": "fadecandy",
            "serial": "...",
            "map": [
Q_NE
            ]
        },
        {
            "type": "fadecandy",
            "serial": "VPWYRFOMPNASAQXT",
            "map": [
Q_SW
            ]
        },
        {
            "type": "fadecandy",
            "serial": "ZRGUDLCUZHEMSSJZ",
            "map": [
Q_SE
            ]
        }
    ]
}
"""

# Quadrant parameters schema: (
#  q_vertical:  quadrant vertical index (0 or 1 for 2x2 dance floor).  0 is at the top.
#  q_horizontal:  analogous to q_vertical
#  pins_go_upward:  1 if and only if increasing order of the breakout board pins is in the upward (North) direction
#  bus_is_on_right:  1 if and only if the bus is on the right side of this quadrant
#  pairs_are_flipped: 1 if and only if pin-1 for this fade-candy chip controls the second strip instead of the first on this quadrant
#  json_placeholder:  string sequence in the json_template above that will be replaced by the generated tuples
def render_quadrant(q_vertical, q_horiz, pins_go_upward, bus_is_on_right, pairs_are_flipped, json_placeholder):
    #print "\n\n"
    lines = []
    for pin in range(8):
        for out_or_back in range(2):
            chip_row_offset = 2 * pin + (out_or_back if not pairs_are_flipped else 1 - out_or_back)
            global_row = q_vertical * n_strips + (chip_row_offset if not pins_go_upward else (n_strips - chip_row_offset - 1))
            global_col = q_horiz * n_leds 
            
            opc_led_offset = global_row * leds_per_global_row + global_col
            strip_is_running_left = bus_is_on_right ^ out_or_back
            chip_led_offset = (2 * pin + out_or_back) * n_leds + (n_leds - 1 if strip_is_running_left else 0)
            
            quad_tuple = "[0, %d, %d, %d]" % (opc_led_offset, chip_led_offset, -n_leds if strip_is_running_left else n_leds)
            #print "# pin %d, %s" % (pin, "back" if out_or_back else "out")
            lines.append(quad_tuple)
            #print quad_tuple
    global json_template
    json_template = json_template.replace(json_placeholder, ',\n'.join(line_prefix + line for line in lines))
    
    
render_quadrant(0, 0, pins_go_upward=1, bus_is_on_right=1, pairs_are_flipped=1, json_placeholder="Q_NW")
render_quadrant(0, 1, pins_go_upward=1, bus_is_on_right=1, pairs_are_flipped=1, json_placeholder="Q_NE")
render_quadrant(1, 0, pins_go_upward=1, bus_is_on_right=1, pairs_are_flipped=1, json_placeholder="Q_SW")
render_quadrant(1, 1, pins_go_upward=0, bus_is_on_right=0, pairs_are_flipped=1, json_placeholder="Q_SE")

print json_template
    
