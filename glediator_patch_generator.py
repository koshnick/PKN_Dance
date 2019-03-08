"""
Project: PKN Lighted dance floor / LED Art 

"""

# Optionally, redirect sstandard output to file:
import sys
import codecs

filepath_and_name = sys.argv[1]
f = codecs.open(filepath_and_name, 'w', 'utf-8')
sys.stdout = f

artnet_host = '127.0.0.1'
pixels_per_universe = 128
x_size = 64
y_size = 32
pixel_count = x_size * y_size
channel_count = pixel_count * 3
num_universes = pixel_count / pixels_per_universe
if pixel_count % pixels_per_universe != 0:
    raise Exception('non-integer number of universes')

print('#GLEDIATOR Patch File')
print('Patch_Matrix_Size_X=%d' % x_size)
print('Patch_Matrix_Size_Y=%d' % y_size)
print('Patch_Num_Unis=%d' % num_universes)

ip1, ip2, ip3, ip4 = str(artnet_host).split('.')

uni_counter = 0
uni_id = 0

for y in range(0, y_size):
    for x in range(0, x_size):
        if uni_counter == pixels_per_universe:
            uni_counter = 0
            uni_id = uni_id + 1

        if uni_counter == 0:
            print('Patch_Uni_ID_%d_IP1=%s' % (uni_id, ip1))
            print('Patch_Uni_ID_%d_IP2=%s' % (uni_id, ip2))
            print('Patch_Uni_ID_%d_IP3=%s' % (uni_id, ip3))
            print('Patch_Uni_ID_%d_IP4=%s' % (uni_id, ip4))
            print('Patch_Uni_ID_%d_Net_Nr=0' % uni_id)
            print('Patch_Uni_ID_%d_Sub_Net_Nr=0' % uni_id)
            print('Patch_Uni_ID_%d_Uni_Nr=%d' % (uni_id, uni_id+1))
            print('Patch_Uni_ID_%d_Num_Ch=%d' % (uni_id, pixels_per_universe*3))

        print('Patch_Pixel_X_%d_Y_%d_Ch_R = %d' % (x, y, uni_counter*3))
        print('Patch_Pixel_X_%d_Y_%d_Ch_G = %d' % (x, y, uni_counter*3+1))
        print('Patch_Pixel_X_%d_Y_%d_Ch_B = %d' % (x, y, uni_counter*3+2))
        print('Patch_Pixel_X_%d_Y_%d_Uni_ID = %d' % (x, y, uni_id))
        uni_counter = uni_counter + 1
        # print('Counter: %d  Universe Counter: %d' % (counter, uni_counter))

f.close()