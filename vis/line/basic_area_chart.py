import pyecharts.options as opts
from pyecharts.charts import Line

x_data = ['Mon', 'The', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
y_data = [820, 932, 901, 934, 1290, 1330, 1320]

(
    Line()
    .add_xaxis(xaxis_data = x_data)
    .add_yaxis(
        series_name = 'value',
        y_axis = y_data,
        symbol = 'emptyCircle',
        is_symbol_show = True,
        label_opts = opts.LabelOpts(is_show = True),
        areastyle_opts = opts.AreaStyleOpts(opacity = 1, color = '#C67570'),
    )
    .set_global_opts(
        toolbox_opts = opts.TooltipOpts(is_show = True),
        yaxis_opts = opts.AxisOpts(
            type_ = 'value',
            axistick_opts = opts.AxisTickOpts(is_show = True),
            splitline_opts = opts.SplitLineOpts(is_show = True),
        ),
        xaxis_opts = opts.AxisOpts(type_ = 'category', boundary_gap = False),
    )
    .render('vis/line/basic_area_chart.html')
)