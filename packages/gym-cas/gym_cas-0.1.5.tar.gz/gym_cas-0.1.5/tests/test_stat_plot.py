from gym_cas import *
from gym_cas.stat_plot import BoxplotSeries, BarplotSeries
from spb.series import Line2DBaseSeries


def only_small_errors(a: list, b: list, e=1e-14):
    for i in range(len(a)):
        if abs(a[i] - b[i]) > e:
            return False
    return True


def test_boxplot():
    p = boxplot([[1, 2, 3, 8], [1, 2, 3, 10]], labels=["test1", "test2"], show=False)
    s = p.series
    assert isinstance(p, MB)
    assert len(s) == 1
    assert isinstance(s[0], BoxplotSeries)
    assert s[0].get_data()[0]["whislo"] == 1


def test_plot_bars():
    p = plot_bars([1, 2, 3, 3], labels=["hejsa"], show=False)
    s = p.series
    assert isinstance(p, MB)
    assert len(s) == 1
    assert isinstance(s[0], BarplotSeries)
    assert s[0].get_data() == ([1, 2, 3], [25, 25, 50])

    p = plot_bars([[1, 2, 3, 10, 10], [1, 2, 2, 3, 6, 8]], labels=["hejsa", "davs der"], show=False)
    s = p.series
    assert isinstance(p, MB)
    assert len(s) == 2
    assert isinstance(s[0], BarplotSeries)
    assert s[0].get_data()[1] == [100 / 5, 100 / 5, 100 / 5, 200 / 5]


def test_plot_sum():
    p = plot_sum([1, 2, 3, 3], labels=["hejsa"], show=False)
    assert isinstance(p, MB)
    s = p.series
    assert len(s) == 1
    assert isinstance(s[0], Line2DBaseSeries)

    p = plot_sum(
        [[1, 2, 3, 10, 10], [1, 2, 2, 3, 6]], groups=[0, 10, 20, 30, 40, 50], labels=["hejsa", "davs der"], show=False
    )
    assert isinstance(p, MB)
    s = p.series
    assert len(s) == 2
    assert isinstance(s[0], Line2DBaseSeries)


def test_plot_hist():
    p = plot_hist([1, 2, 3, 3], groups=[1, 3, 5, 7, 9], show=False)
    assert isinstance(p, MB)
    s = p.series
    assert len(s) == 1
    assert isinstance(s[0], BarplotSeries)
    assert s[0].get_data()[0] == [2, 4, 6, 8]
    assert only_small_errors(s[0].get_data()[1], [100 / 9 / 2, 200 / 9 / 2, 300 / 9 / 2, 300 / 9 / 2])
