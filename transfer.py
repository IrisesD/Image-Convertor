from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from floyd_steinberg import floyd_steinberg_dither
from floyd_steinberg import apply_threshold
from floyd_steinberg import gaussian_filter
from round import transfer_round
from coegen import coe_genenrate
from math import fabs
from math import floor
import sys
def trans(input_path,output_path,Q = 1, k1 = 0.1):
    floyd_steinberg_dither(input_path,'f0.jpg')
    print("The first dithering finished.")
    imgf = Image.open(input_path)
    imgf_arr = np.array(imgf)
    print(imgf_arr)
    imgb = Image.open('f0.jpg')
    imgft = np.array(imgf)
    #gaussian_filter(imgf)
    #print(imgft)
    print("Initial image filtering finished.")
    imgbt = np.array(imgb)
    #gaussian_filter(imgb)
    print("Dithered image filtering finished.")
    imge = [[[0,0,0]for i in range(len(imgf_arr[0]))]for j in range(len(imgf_arr))]
    La = [[[0,0,0]for i in range(len(imgf_arr[0]))]for j in range(len(imgf_arr))]
    H = [[[0,0,0]for i in range(len(imgf_arr[0]))]for j in range(len(imgf_arr))]
    meaner = 0
    meaneg = 0
    meaneb = 0
    for i in range(len(imgf_arr)):
        for j in range(len(imgf_arr[0])):
            imge[i][j][0] = fabs(int(imgft[i][j][0]) - int(imgbt[i][j][0]))
            meaner += imge[i][j][0]
            imge[i][j][1] = fabs(int(imgft[i][j][1]) - int(imgbt[i][j][1]))
            meaneg += imge[i][j][1]
            imge[i][j][2] = fabs(int(imgft[i][j][2]) - int(imgbt[i][j][2]))
            meaneb += imge[i][j][2]
            if i != 0 and i != len(imgf_arr)-1 and j != 0 and j != len(imgf_arr[0])-1:
                La[i][j][0] = int(imgf_arr[i][j][0]) - (1/8) * (int(imgf_arr[i-1][j-1][0])+int(imgf_arr[i-1][j][0])+int(imgf_arr[i][j+1][0])+ \
                    int(imgf_arr[i][j-1][0])+int(imgf_arr[i][j+1][0])+int(imgf_arr[i+1][j-1][0])+int(imgf_arr[i+1][j][0])+int(imgf_arr[i+1][j+1][0]))
                La[i][j][1] = int(imgf_arr[i][j][1]) - (1/8) * (int(imgf_arr[i-1][j-1][1])+int(imgf_arr[i-1][j][1])+int(imgf_arr[i][j+1][1])+ \
                    int(imgf_arr[i][j-1][1])+int(imgf_arr[i][j+1][1])+int(imgf_arr[i+1][j-1][1])+int(imgf_arr[i+1][j][1])+int(imgf_arr[i+1][j+1][1]))
                La[i][j][2] = int(imgf_arr[i][j][2]) - (1/8) * (int(imgf_arr[i-1][j-1][2])+int(imgf_arr[i-1][j][2])+int(imgf_arr[i][j+1][2])+ \
                    int(imgf_arr[i][j-1][2])+int(imgf_arr[i][j+1][2])+int(imgf_arr[i+1][j-1][2])+int(imgf_arr[i+1][j][2])+int(imgf_arr[i+1][j+1][2]))
    print("La computing finished.")
    meaner /= (len(imgf_arr)*len(imgf_arr[0]))
    meaneg /= (len(imgf_arr)*len(imgf_arr[0]))
    meaneb /= (len(imgf_arr)*len(imgf_arr[0]))
    kr = k1 / meaner
    kg = k1 / meaneg
    kb = k1 / meaneb
    print(kr,kg,kb)
    for i in range(len(imgf_arr)):
        for j in range(len(imgf_arr[0])):
            if La[i][j][0] >= Q:
                H[i][j][0] = kr
            if La[i][j][0] < Q and La[i][j][0] >= -Q:
                H[i][j][0] = (kr / (Q**3)) * (La[i][j][0]**3)
            if La[i][j][0] < -Q:
                H[i][j][0] = -kr
            if La[i][j][1] >= Q:
                H[i][j][1] = kg
            if La[i][j][1] < Q and La[i][j][1] >= -Q:
                H[i][j][1] = (kg / (Q**3)) * (La[i][j][1]**3)
            if La[i][j][1] < -Q:
                H[i][j][1] = -kg
            if La[i][j][2] >= Q:
                H[i][j][2] = kb
            if La[i][j][2] < Q and La[i][j][2] >= -Q:
                H[i][j][2] = (kb / (Q**3)) * (La[i][j][2]**3)
            if La[i][j][2] < -Q:
                H[i][j][2] = -kb
    print("H computing finished.")
    for i in range(len(imgf_arr)):
        for j in range(len(imgf_arr[0])):
            imgf_arr[i][j][0] += floor(H[i][j][0]*imge[i][j][0])
            #print(round(H[i][j][0]*imge[i][j][0]))
            imgf_arr[i][j][1] += floor(H[i][j][1]*imge[i][j][1])
            imgf_arr[i][j][2] += floor(H[i][j][2]*imge[i][j][2])
    print("Image updating finished.")
    im = Image.fromarray(imgf_arr) 
    im.save('f1.jpg')
    floyd_steinberg_dither('f1.jpg',output_path)
    print("The second dithering finished.")
    print("OK.")
Q = float(sys.argv[3])
k1 = float(sys.argv[4])
input_path = sys.argv[1]
output_path = sys.argv[2]
trans(Q,k1,input_path,output_path)
