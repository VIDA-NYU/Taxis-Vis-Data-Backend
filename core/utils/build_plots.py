def build_histogram(x, title, xaxis_title, yaxis_title, name='Histogram', nbinsx=50, color='rgba(100, 149, 237, 0.7)'):
    plot_data = {
        'x': x,
        'type': 'histogram',
        'name': name,
        'nbinsx': nbinsx,
        'marker': {'color': color}
    }
    layout = {
        'title': title,
        'xaxis': {'title': xaxis_title},
        'yaxis': {'title': yaxis_title}
    }
    chart = {
        'data': [plot_data],
        'layout': layout
    }
    return chart


def build_bar_chart(x, y, title, xaxis_title, yaxis_title, name='Bar Chart', colors=None):
    if colors is None:
        colors = ['rgba(100, 149, 237, 0.6)'] * len(x)
    plot_data = {
        'x': x,
        'y': y,
        'type': 'bar',
        'name': name,
        'marker': {'color': colors}
    }
    layout = {
        'title': title,
        'xaxis': {'title': xaxis_title},
        'yaxis': {'title': yaxis_title},
        'legend': {'orientation': 'h'}
    }
    chart = {
        'data': [plot_data],
        'layout': layout
    }
    return chart


def build_box_plot(y, title, yaxis_title, name='Box Plot', color='rgba(255, 165, 0, 0.6)'):
    plot_data = {
        'y': y,
        'type': 'box',
        'name': name,
        'boxpoints': 'all',
        'jitter': 0.3,
        'pointpos': -1.8,
        'marker': {'color': color}
    }
    layout = {
        'title': title,
        'yaxis': {'title': yaxis_title},
        'xaxis': {'visible': False}
    }
    chart = {
        'data': [plot_data],
        'layout': layout
    }
    return chart


def build_pie_chart(labels, values, title, name='Pie Chart', colors=None):
    if colors is None:
        colors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)'
        ]
    plot_data = {
        'labels': labels,
        'values': values,
        'type': 'pie',
        'name': name,
        'hoverinfo': 'label+percent+value',
        'textinfo': 'percent',
        'marker': {'colors': colors}
    }
    layout = {
        'title': title
    }
    chart = {
        'data': [plot_data],
        'layout': layout
    }
    return chart


def build_scatter_plot(x, y, title, xaxis_title, yaxis_title, name='Scatter Plot', mode='markers',
                       marker_size=5, marker_opacity=0.6, marker_color='rgba(0, 123, 255, 0.6)'):
    plot_data = {
        'x': x,
        'y': y,
        'mode': mode,
        'type': 'scatter',
        'name': name,
        'marker': {
            'size': marker_size,
            'opacity': marker_opacity,
            'color': marker_color
        }
    }
    layout = {
        'title': title,
        'xaxis': {'title': xaxis_title},
        'yaxis': {'title': yaxis_title}
    }
    chart = {
        'data': [plot_data],
        'layout': layout
    }
    return chart


def build_line_chart(x, y, title, xaxis_title, yaxis_title, name='Line Chart',
                     line_color='rgba(255, 99, 71, 0.8)', line_width=2, marker_size=4):
    plot_data = {
        'x': x,
        'y': y,
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': name,
        'line': {'color': line_color, 'width': line_width},
        'marker': {'size': marker_size}
    }
    layout = {
        'title': title,
        'xaxis': {'title': xaxis_title},
        'yaxis': {'title': yaxis_title}
    }
    chart = {
        'data': [plot_data],
        'layout': layout
    }
    return chart
