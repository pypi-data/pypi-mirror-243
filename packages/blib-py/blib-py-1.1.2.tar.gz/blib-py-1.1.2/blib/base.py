import cycler
import matplotlib

#
# Some default parameters I'd like to use
#

def useTheme(theme='light'):
    props = {
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica', 'Arial', 'Lucida Grande', 'DejaVu Sans'],
        'figure.figsize': (8, 4),
        'figure.dpi': 108,
        'legend.frameon': False,
        'axes.linewidth': 0.5,
        'axes.labelsize': 10,
        'axes.labelpad': 4.0,
        'axes.labelweight': 'normal',
        'axes.titleweight': 'normal',
        'axes.titlesize': 12,
        'axes.titlepad': 6.0,
    }
    if theme == 'dark':
        props.update({
            'figure.facecolor': 'black',
            'axes.facecolor': (0, 0, 0, 0.9),
            'axes.edgecolor': 'white',
            'axes.labelcolor': 'white',
            'grid.color': 'white',
            'xtick.color': 'white',
            'ytick.color': 'white',
            'hatch.color': 'white',
            'text.color': 'white',
            'legend.facecolor': 'black',
            'legend.edgecolor': 'white',
            'lines.markeredgecolor': 'white',
            'lines.markerfacecolor': 'white'
        })
        mc = [
            'mediumturquoise',
            'gold',
            'hotpink',
            'yellowgreen',
            'dodgerblue',
            'darkorange',
            'mediumpurple',
            'crimson',
            'grey',
            'rosybrown'
        ]
    elif theme == 'light':
        props.update({
            'figure.facecolor': 'white',
            'axes.facecolor': (1, 1, 1, 0.9),
            'axes.edgecolor': 'black',
            'axes.labelcolor': 'black',
            'grid.color': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'hatch.color': 'black',
            'text.color': 'black',
            'legend.facecolor': 'white',
            'legend.edgecolor': 'black',
            'lines.markeredgecolor': 'black',
            'lines.markerfacecolor': 'black'
        })
        mc = [
            'steelblue',
            'darkorange',
            'forestgreen',
            'crimson',
            'blueviolet',
            'darkgoldenrod',
            'hotpink',
            'grey',
            'olive',
            'mediumturquoise'
        ]
    else:
        raise ValueError('Unknown theme: {}'.format(theme))
    for keys in props:
        matplotlib.rcParams[keys] = props[keys]

    dd = {k[0]:k[1] for k in matplotlib.colors.CSS4_COLORS.items()}
    cc = [dd[m] for m in mc]
    matplotlib.rcParams['axes.prop_cycle'] = cycler.cycler(color=cc)
