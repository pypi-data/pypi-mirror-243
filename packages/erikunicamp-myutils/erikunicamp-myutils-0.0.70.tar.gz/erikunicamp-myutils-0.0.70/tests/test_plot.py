from myutils import plot

def test_export_all_axis():
# def test_export_all_axis(ax, fig, labels, outdir, pad=0.3, prefix='', fmt='pdf'):
    pass

def test_hex2rgb():
    rgb1 = plot.hex2rgb([], normalize=False, alpha=None)
    assert len(rgb1) == 0

    hexcolours = ['#000000', '#ffffff', '#f26b7f']
    rgb1 = plot.hex2rgb(hexcolours, normalize=False, alpha=None)
    assert all([a == b for a, b in zip(rgb1[0], [0, 0, 0])])
    assert all([a == b for a, b in zip(rgb1[1], [255, 255, 255])])
    assert all([a == b for a, b in zip(rgb1[2], [242, 107, 127])])

    hexcolours = ['#000000', '#ffffff', '#f26b7f']
    rgb1 = plot.hex2rgb(hexcolours, normalize=True, alpha=None)
    assert all([a == b for a, b in zip(rgb1[0], [0, 0, 0])])
    assert all([a == b for a, b in zip(rgb1[1], [1, 1, 1])])
    assert all([a == b for a, b in zip(rgb1[2], [242/255, 107/255, 127/255])])

    hexcolours = ['#000000', '#ffffff', '#f26b7f']
    rgb1 = plot.hex2rgb(hexcolours, normalize=True, alpha=.5)
    assert all([a == b for a, b in zip(rgb1[0], [0, 0, 0, .5])])
    assert all([a == b for a, b in zip(rgb1[1], [1, 1, 1, .5])])
    assert all([a == b for a, b in zip(rgb1[2], [242/255, 107/255, 127/255, .5])])
