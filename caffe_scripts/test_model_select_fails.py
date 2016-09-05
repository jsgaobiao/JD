# usage: python test_model_select_fails.py [model_def] [model_weights] [bgr_mean.npy] [test_file_list] [target_dir] [image_size]
# eg : python test_model_select_fail.py deploy.prototxt iter_16000.caffemodel bgr_mean.npy val.txt our_fail 227

import pdb
import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < 7 :
	print '---------------Wrong Parameter Number-----------------------'
	print '[Usage]: python test_model_select_fails.py [model_def] [model_weights] [bgr_mean.npy] [test_file_list] [target_dir] [image_size] (optional)[result.txt]'
	print '[eg] : python test_model_select_fail.py deploy.prototxt iter_16000.caffemodel bgr_mean.npy val.txt our_fail 227 result.txt'
	sys.exit()

#set display defaults
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'

# Load caffe
caffe_root = '/opt/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe

# Set caffe to CPU mode and load the net from disk
caffe.set_mode_cpu()
#model_def = '../bvlc_reference_caffenet/deploy.prototxt'
model_def = sys.argv[1]
#model_weights = '../model_store/tt_iter_16000.caffemodel'
model_weights = sys.argv[2]

#pdb.set_trace()

net = caffe.Net(model_def,	# defines the structure of the model
		model_weights,	# contains the trained weights
		caffe.TEST)

# load the mean ImageNet image
#mu = np.load('bgr_mean.npy')
mu = np.load(sys.argv[3])
mu = mu[0].mean(1).mean(1)
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)	    # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# Classification

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(1,        # batch size
                          3,         # 3-channel (BGR) images
                          int(sys.argv[6]), int(sys.argv[6]))  # image size is argv[6]*argv[6]

import os
import datetime
fin = open(sys.argv[4])
cnt = 0		# total number of images
corr = 0	# correct prediction number

# generate result txt
if len(sys.argv) == 8 :
    fout = open(sys.argv[7], "w")
        

for images in fin :

#	pdb.set_trace()

	image_arr = images.rstrip('\n')
	image_arr = image_arr.split(' ')
	if len(sys.argv) == 8 :
		fout.write(image_arr[0] + '\t')
		fout.write(image_arr[1] + '\t')
	image = caffe.io.load_image(image_arr[0])
	transformed_image = transformer.preprocess('data', image)
    
	print datetime.datetime.now()

	# copy the image data into the memory allocated for the net
	net.blobs['data'].data[...] = transformed_image

	# perform classification
	output = net.forward()

	output_prob = output['prob'][0] 
	# print 'predicted class is:', output_prob.argmax()
#	pdb.set_trace()
	if len(sys.argv) == 8 :
		fout.write(str(output_prob[0]) + '\t')
		fout.write(str(output_prob[1]) + '\t')
		fout.write(str(output_prob[2]) + '\n')
	cnt += 1
	if output_prob.argmax() == int(image_arr[1]) :
		corr += 1
	else :
		os.system('cp ' + image_arr[0] + ' '+ sys.argv[5] +'/'+ str(image_arr[1]) + '_' + str(output_prob.argmax()) + '_' + str(output_prob[output_prob.argmax()]) + '.jpg')
	
	print datetime.datetime.now()
	print 'Accuracy : ', float(corr) / float(cnt), 'Cnt : ', cnt

print float(corr) / float(cnt)
fin.close()
if len(sys.argv) == 8 :
	fout.close()

