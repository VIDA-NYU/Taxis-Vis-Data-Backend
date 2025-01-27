from django.urls import path
from .visualisation_views import (
    trip_duration_histogram_view,
    peak_hours_bar_view,
    fare_distribution_box_view,
    passenger_count_pie_view,
    payment_type_pie_view,
    tip_amount_analysis_view,
    distance_fare_scatter_plot_view,
    time_series_line_view,
)

urlpatterns = [
    path('trip-duration-histogram/', trip_duration_histogram_view, name='trip-duration-histogram'),
    path('peak-hours-bar/', peak_hours_bar_view, name='peak-hours-bar'),
    path('fare-distribution-box/', fare_distribution_box_view, name='fare-distribution-box'),
    path('passenger-count-pie/', passenger_count_pie_view, name='passenger-count-pie'),
    path('payment-type-pie/', payment_type_pie_view, name='payment-type-pie'),
    path('tip-amount-box/', tip_amount_analysis_view, name='tip-amount-box'),
    path('distance-fare-scatter-plot/', distance_fare_scatter_plot_view, name='distance-fare-scatter-plot'),
    path('time-series-line/', time_series_line_view, name='time-series-line'),
]
