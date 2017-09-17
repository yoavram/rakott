import os
import matplotlib.pyplot as plt

def color_names(color_palette='Set1', names=('red','blue','green','purple','orange','yellow')):
    import seaborn as sns
    return {n:c for n, c in zip(
        names, 
        sns.color_palette(color_palette, len(names))
    )}     

def fig_xlabel(fig, label, xcoord=0.5, ycoord=0):
    return fig.text(xcoord, ycoord, label, horizontalalignment='center', verticalalignment='bottom')

def fig_ylabel(fig, label, xcoord=0, ycoord=0.5):
    return fig.text(xcoord, ycoord, label, rotation='vertical', horizontalalignment='right', verticalalignment='center')

def fig_panel_labels(axes, letters=None, uppercase=True, xcoord=-0.17, ycoord=0.92, panel_label_size=None):
    import string
    if panel_label_size is None:
        panel_label_size = plt.rcParams[ 'axes.titlesize']*1.3
    if letters is None:
        if uppercase:
            letters = string.ascii_uppercase
        else:
            letters = string.ascii_lowercase
    return [
        ax.annotate(
            letter, (xcoord, ycoord), 
            xycoords='axes fraction', 
            fontsize=panel_label_size)
        for ax, letter 
        in zip(axes.flat, letters)
    ]

def savefig_bbox(*text_elements):
    """Create kwargs for plt.savefig or fig.savefig for making sure extra text elements are not clipped.

    Example
    -------
    > plt.plot(range(10))
    > txt = plt.text(0, 0, 'hello')
    > plt.savefig('hello.png', **savefig_bbox(txt))
    """
    return dict(bbox_inches='tight', bbox_extra_artists=text_elements)

def greyscale_figure(input_filename, output_filename=None):
    """Convert image to greyscale and save it with '_gray', if output filename not give.
    """
    from PIL import Image
    if output_filename is None:
        fname, ext = os.path.splitext(input_filename)
        output_filename = "{}_gray{}".format(fname, ext)
    Image.open(input_filename).convert('L').save(output_filename)

def legend_out(ax, *args, **kwargs):
    """https://stackoverflow.com/a/4701285/1063612
    """
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    return ax.legend(*args, loc='center left', bbox_to_anchor=(1, 0.5), **kwargs)


if __name__ == '__main__':
    pass