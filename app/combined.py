from color_select import get_color
from color_wheel import color_output

# test = {'url':['https://closettest.s3.us-west-1.amazonaws.com/trousers.jpg',
#               'https://closettest.s3.us-west-1.amazonaws.com/beret.jpg'],
#        'num_recommendation':2,
#        'pattern': True}


def cloth_rec(dictionary):
    if dictionary['pattern']:
        style = 'ANA'
    else:
        style = 'COM'
    color = get_color(dictionary['urls'])
    res = color_output(color,style,dictionary['num_recommendation'])
    return res

# res = cloth_rec(test)
# print(res)