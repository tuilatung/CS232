#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import sys
import os

def main():


        if(len(sys.argv)!=5):
                print('inputBMPFileName outputJPEGFilename quality(from 1 to 100) DEBUGMODE(0 or 1)')
                print('example:')
                print('./lena.bmp ./output.jpg 80 0')
                return

        srcFileName = sys.argv[1]
        outputJPEGFileName = sys.argv[2]
        quality = float(sys.argv[3])
        DEBUG_MODE = int(sys.argv[4])


        B = 8 # blocksize 
        img1 = cv2.imread(srcFileName)
        h, w = np.array(img1.shape[:2])//B * B
        img1= img1[:h, :w]

        #Convert BGR to RGB
        img2=np.zeros(img1.shape,np.uint8)
        img2[:,:,0]=img1[:,:,2]
        img2[:,:,1]=img1[:,:,1]
        img2[:,:,2]=img1[:,:,0]

        size_of_original = os.path.getsize(srcFileName)

        if DEBUG_MODE:
                plt.title(f'Original with size={size_of_original}')
                plt.imshow(img2)

        QY=np.array([[16,11,10,16,24,40,51,61],
                                [12,12,14,19,26,48,60,55],
                                [14,13,16,24,40,57,69,56],
                                [14,17,22,29,51,87,80,62],
                                [18,22,37,56,68,109,103,77],
                                [24,35,55,64,81,104,113,92],
                                [49,64,78,87,103,121,120,101],
                                [72,92,95,98,112,100,103,99]])

        QC=np.array([[17,18,24,47,99,99,99,99],
                                [18,21,26,66,99,99,99,99],
                                [24,26,56,99,99,99,99,99],
                                [47,66,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99],
                                [99,99,99,99,99,99,99,99]])

        Y_d =cv2.cvtColor(img1, cv2.COLOR_BGR2YCrCb)

        SSV=2
        SSH=2
        crf=cv2.boxFilter(Y_d[:,:,1],ddepth=-1,ksize=(2,2))
        cbf=cv2.boxFilter(Y_d[:,:,2],ddepth=-1,ksize=(2,2))
        crsub=crf[::SSV,::SSH]
        cbsub=cbf[::SSV,::SSH]
        imSub=[Y_d[:,:,0], crsub, cbsub]


        QUANLITY_FACTOR = quality
        if QUANLITY_FACTOR < 50 and QUANLITY_FACTOR > 1:
                scale = np.floor(5000/QUANLITY_FACTOR)
        elif QUANLITY_FACTOR < 100:
                scale = 200-2*QUANLITY_FACTOR
        else:
                print("Quality Factor must be in the range [1..99]")
        scale = scale / 100.0
        Q=[QY*scale,QC*scale,QC*scale]


        scol =  B
        srow = B



        TransAll=[]
        TransAllQuant=[]
        ch=['Y','Cr','Cb']
        # plt.figure()
        for idx,channel in enumerate(imSub):
                # plt.subplot(1,3,idx+1)
                channelrows=channel.shape[0]
                channelcols=channel.shape[1]
                Trans = np.zeros((channelrows,channelcols), np.float32)
                TransQuant = np.zeros((channelrows,channelcols), np.float32)
                blocksV=channelrows // B
                blocksH=channelcols // B
                vis0 = np.zeros((channelrows,channelcols), np.float32)
                vis0[:channelrows, :channelcols] = channel
                vis0=vis0-128 # convert 0-255 to -127 to 127
                for row in range(blocksV):
                        for col in range(blocksH):
                                currentblock = cv2.dct(vis0[row*B:(row+1)*B,col*B:(col+1)*B])
                                Trans[row*B:(row+1)*B,col*B:(col+1)*B] = currentblock
                                TransQuant[row*B:(row+1)*B,col*B:(col+1)*B] = np.round(currentblock/Q[idx])
                TransAll.append(Trans)
                TransAllQuant.append(TransQuant)
                if idx==0:
                        selectedTrans=Trans[srow*B:(srow+1)*B,scol*B:(scol+1)*B]
                else:
                        sr=int(np.floor(srow/SSV))
                        sc=int(np.floor(scol/SSV))
                        selectedTrans=Trans[sr*B:(sr+1)*B,sc*B:(sc+1)*B]
                if DEBUG_MODE:
                        pass
                        # plt.imshow(selectedTrans,cmap=cm.jet,interpolation='nearest')
                        # plt.colorbar(shrink=0.5)
                        # plt.title('DCT of '+ch[idx])


        DecAll=np.zeros((h,w,3), np.uint8)
        for idx,channel in enumerate(TransAllQuant):
                channelrows=channel.shape[0]
                channelcols=channel.shape[1]
                blocksV=channelrows//B
                blocksH=channelcols//B
                back0 = np.zeros((channelrows,channelcols), np.uint8)
                for row in range(blocksV):
                        for col in range(blocksH):
                                dequantblock=channel[row*B:(row+1)*B,col*B:(col+1)*B]*Q[idx]
                                currentblock = np.round(cv2.idct(dequantblock))+128
                                currentblock[currentblock>255]=255
                                currentblock[currentblock<0]=0
                                back0[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
                back1=cv2.resize(back0,(w,h))
                DecAll[:,:,idx]=np.round(back1)


        reImg=cv2.cvtColor(DecAll, cv2.COLOR_YCrCb2RGB)
        # reImg = np.reshape(reImg, (reImg.shape[1], reImg.shape[0], reImg.shape[2]))
        # cv2.imwrite('BackTransformedQuant.jpg', reImg)
        plt.figure()
        img3=np.zeros(img1.shape,np.uint8)
        img3[:,:,0]=reImg[:,:,2]
        img3[:,:,1]=reImg[:,:,1]
        img3[:,:,2]=reImg[:,:,0]


        # normalization shape
        img3 = img3[:-8,:-8,:]
        cv2.imwrite(outputJPEGFileName, img3)
        size_of_compressed = os.path.getsize(outputJPEGFileName)
        if DEBUG_MODE:
                plt.imshow(img3[:,:,::-1])
                plt.title(f'Compressed with size={size_of_compressed}')
                plt.show()

        return (size_of_original, size_of_compressed)

if __name__ == "__main__":
        original_size, compressed_size =  main()
        print("Compressed ratio = %.2f" % (original_size / compressed_size))