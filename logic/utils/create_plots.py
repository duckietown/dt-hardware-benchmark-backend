from flask import make_response
import matplotlib.pyplot as plt
import numpy as np
from s3.list_files import get_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO

def display_data(meas, t):
    """ displays the measured data in the plot"""  
    nr_of_meas = len(meas) - 1
    fig, axes= plt.subplots(nr_of_meas, 1, figsize=(7, nr_of_meas*3))
    ax_ind = 0
    for _, item in meas.items():
        if(type(item) == dict):
            mean_name = ('mean {:2.2f}{unit}, median {:2.2f}{unit}, std: {:2.2f}{unit}'
                        ).format(item.get('mean'), item.get('median'), item.get('std'), unit=item.get('unit'))
            ylabel = ('{} [{}]').format(item['ylabel'], item['unit'])
            
            t_meas = item['t']
            t_ind_min = (np.abs(t - t_meas[0])).argmin()
            t_ind_max = (np.abs(t - t_meas[-1])).argmin()
            
            axes[ax_ind].plot(t_meas, item['measurement'], 'o', 
                                t[t_ind_min:t_ind_max], item['measurement_ip'][t_ind_min:t_ind_max],
                                t, [item['mean']]*len(t), 
                                t, [item['min']]*len(t), ':' ,
                                t, [item['max']]*len(t), ':' )
            axes[ax_ind].legend(['measured', 'interpolated', mean_name])
            axes[ax_ind].set_title(item['name'] + " " + item['info'])
            axes[ax_ind].set_ylabel(ylabel)
            axes[ax_ind].set_ylim(item.get('ylim'))
            
            ax_ind += 1
    #fig.suptitle('Diagnostics', fontsize=16)
    fig.tight_layout(pad=3.0)
    return fig


def render_image(id):
    meas = get_file('meas/'+id+'.json')
    t = np.array(meas['measurements']['time'])
    m = meas['measurements']

    fig = display_data(m, t)
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)

    return png_output.getvalue()
    