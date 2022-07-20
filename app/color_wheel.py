import numpy as np
import matplotlib.pylab as plt

'''
Layer1 is the most inner one where 4 is the most outer ring
'''
layer1=[(208,107,54),(247,229,78),(182,200,81),(85,162,82),(75,160,154),(78,171,218),(46,106,176),(77,63,139),(119,60,139),(155,46,94),(207,51,109),(198,54,48)]
layer2=[(224,151,90),(248,235,118),(206,216,108),(141,186,102),(123,187,187),(137,194,230),(70,136,191),(120,106,164),(151,110,165),(190,94,135),(218,107,148),(213,96,69)]
layer3=[(230,200,158),(250,245,175),(227,230,160),(185,211,159),(179,215,208),(184,219,240),(146,176,211),(169,159,197),(189,165,198),(215,157,183),(234,170,192),(227,158,127)]
layer4=[(249,238,221),(248,246,224),(248,246,220),(226,236,216),(223,236,243),(210,233,247),(211,223,240),(213,211,227),(227,215,232),(240,216,226),(244,220,231),(248,214,198)]
wheel=[layer1,layer2,layer3,layer4]


def color_pick_COM(index):
	return [index-6]


def color_pick_ANA(index):
	if index>=11:
		return [10, 0, index]
	if index<=0:
		return [11, 1, index]
	else:
		return [index-1, index+1, index]


def color_pick_TRI(index):
	return [index-4, index-8]


def color_pick_CD(index):
	return [index-5, index-7]


def color_pick_QUA(index):
	return [index, index-3, index-6, index-9]


def color_pick_TET(index):
	return [index, index-2, index-6, index-8]


def stylist_choose(style, layer, index, result_num):
	if style=='COM':
		if result_num==1:
			return wheel[layer][color_pick_COM(index)[0]]
		if result_num==2:
			return [wheel[layer][color_pick_COM(index)[0]], wheel[layer-1][color_pick_COM(index)[0]]]
		if result_num==3:
			return [wheel[layer][color_pick_COM(index)[0]], wheel[layer-1][color_pick_COM(index)[0]], wheel[layer-2][color_pick_COM(index)[0]]]
	if style=='ANA':
		if result_num==1:
			return [wheel[layer][color_pick_ANA(index)[0]]]
		if result_num==2:
			return [wheel[layer][color_pick_ANA(index)[0]],wheel[layer][color_pick_ANA(index)[1]]]
		if result_num==3:
			print(color_pick_ANA(index))
			return [wheel[layer][color_pick_ANA(index)[0]],wheel[layer][color_pick_ANA(index)[1]],wheel[layer][color_pick_ANA(index)[2]]]
	if style=='TRI':
		colors_index=color_pick_TRI(index)
		return [wheel[layer][colors_index[0]], wheel[layer][colors_index[1]]]
	if style=='CD':
		colors_index=color_pick_CD(index)
		return [wheel[layer][colors_index[0]], wheel[layer][colors_index[1]]]
	if style=='QUA':
		colors_index=color_pick_QUA(index)
		return [wheel[layer][colors_index[0]], wheel[layer][colors_index[1]], wheel[layer][colors_index[2]], wheel[layer][colors_index[3]]]
	if style=='TET':
		colors_index=color_pick_TET(index)
		return [wheel[layer][colors_index[0]], wheel[layer][colors_index[1]], wheel[layer][colors_index[2]], wheel[layer][colors_index[3]]]
	else:
		return None


def color_rec(color, style, result_num):
	x = np.array([[color]])
	y = np.array(wheel)
	res=np.linalg.norm(x-y, axis=-1)
	result = np.where(res == np.amin(res))
	listOfCordinates = list(zip(result[0], result[1]))[0]
	layer=listOfCordinates[0]
	index=listOfCordinates[1]
	return stylist_choose(style, layer, index, result_num)


def check_wheel(color, style, result_num):
	RGB=color_output(color, style, result_num)
	return plt.imshow([RGB])


#color_list is a list contains multiple colors, use 3->1 or 2->1
def color_locate(color_list):
	if len(color_list)==2:
		t=tuple(map(sum, zip(color_list[0], color_list[1])))
		color_ready=tuple(int(ti/2) for ti in t)
	if len(color_list)==3:
		t=tuple(map(sum, zip(color_list[0], color_list[1])))
		t2=tuple(map(sum, zip(t, color_list[2])))
		color_ready=tuple(int(ti/3) for ti in t2) 
	if len(color_list)==1:
		color_ready=color_list[0]
	return color_ready


def color_check_COM(color_list, result_num):
	input_size=len(color_list)
	if input_size>1 and result_num==1:
		return [color_rec(color_locate(color_list), 'COM', result_num)]
	if input_size==2 and result_num==2:
		return [color_rec(color_list[0], 'COM', result_num-1),color_rec(color_list[1], 'COM', result_num-1)]
	if input_size==1 and result_num==1:
		return [color_rec(color_list, 'COM', result_num)]
	if input_size==1:
		return color_rec(color_list, 'COM', result_num)
	
	
def color_check_ANA(color_list, result_num):
	return color_rec(color_locate(color_list), 'ANA', result_num)


# This is the main function, color list should be a list contains tuples where each one is a RGB tuple.
# Output is also a list of tuples, each tuple is a recommended color
def color_output(color_list, style, result_num):
	if style=='COM':
		return color_check_COM(color_list, result_num)
	if style=='ANA':
		return color_check_ANA(color_list, result_num)


def convert(RGB):
	return tuple(i for i in list(RGB))

