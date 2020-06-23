"""Utils to create a matplotlib plot for a benchmark    """
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from files.list_files import get_file


def display_data(meas, t):
    """ displays the measured data in the plot"""
    nr_of_meas = len(meas) - 1
    fig, axes = plt.subplots(nr_of_meas, 1, figsize=(7, nr_of_meas * 3))
    ax_ind = 0
    for _, item in meas.items():
        if isinstance(item, dict):
            mean_name = ('mean {:2.2f}{unit}, median {:2.2f}{unit}, std: {:2.2f}{unit}').format(
                item.get('mean', float('nan')), item.get('median', float('nan')),
                item.get('std', float('nan')), unit=item.get('unit'))
            ylabel = ('{} [{}]').format(item['ylabel'], item['unit'])

            t_meas = item['t']
            add_info = "missing data"

            if len(t_meas) != 0:
                add_info = ''
                if item.get('notime', False):
                    axes[ax_ind].plot(item['measurement'], 'o')
                    axes[ax_ind].plot([item['mean']] * len(item['measurement']))
                    axes[ax_ind].plot([item['min']] * len(item['measurement']), ':')
                    axes[ax_ind].plot([item['max']] * len(item['measurement']), ':')
                    axes[ax_ind].legend(['measured', mean_name])
                else:
                    t_ind_min = (np.abs(t - t_meas[0])).argmin()
                    t_ind_max = (np.abs(t - t_meas[-1])).argmin()

                    axes[ax_ind].plot(t_meas,
                                      item['measurement'],
                                      'o',
                                      t[t_ind_min:t_ind_max],
                                      item['measurement_ip'][t_ind_min:t_ind_max],
                                      t,
                                      [item['mean']] * len(t),
                                      t,
                                      [item['min']] * len(t),
                                      ':',
                                      t,
                                      [item['max']] * len(t),
                                      ':')
                    axes[ax_ind].legend(['measured', 'interpolated', mean_name])

            axes[ax_ind].set_title(item['name'] + " " + item['info'] + " " + add_info)
            axes[ax_ind].set_ylabel(ylabel)
            axes[ax_ind].set_ylim(item.get('ylim'))

            ax_ind += 1
    #fig.suptitle('Diagnostics', fontsize=16)
    fig.tight_layout(pad=3.0)
    return fig


def render_image(uuid):
    """ renders an image and prepares it to be sent via a request
    Args:
        uuid (uuid): uuid of bm

    Returns:
        [type]: image ready to be sent from the API
    """
    meas = get_file('meas/' + uuid + '.json')
    t = np.array(meas['measurements']['time'])
    m = meas['measurements']

    fig = display_data(m, t)
    canvas = FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)

    return png_output.getvalue()
