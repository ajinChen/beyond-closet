from color_select import get_color
from color_wheel import color_output


def cloth_rec(dictionary):
    if dictionary['pattern']:
        style = 'ANA'
    else:
        style = 'COM'
    color = get_color(dictionary['urls'])
    res = color_output(color,style,dictionary['num_recommendation'])
    return res