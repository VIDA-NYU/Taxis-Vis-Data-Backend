import pandas as pd
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from typing import Any, Union, List, Tuple

from core.data_analysis.taxis_vis_analyser import TaxisVisAnalyser
from core.utils.csv_reader import read_csv_file, validate_required_columns
from core.utils.build_plots import (
    build_histogram,
    build_bar_chart,
    build_box_plot,
    build_pie_chart,
    build_scatter_plot,
    build_line_chart
)


def load_and_analyse(
        csv_file: Any,
        analysis_function: Any,
        required_columns: List[str],
        return_data: bool = False,
        **kwargs
) -> Union[Any, Tuple[Any, pd.DataFrame]]:
    df = read_csv_file(csv_file)
    validate_required_columns(df, required_columns)
    analyser = TaxisVisAnalyser(file_input=df)
    result = analysis_function(analyser, **kwargs)
    if return_data:
        return result, df
    return result


DEFAULT_REQUIRE_COLUMNS = [
    'tpep_pickup_datetime',
    'tpep_dropoff_datetime',
    'pickup',
    'dropoff',
    'trip_distance',
    'fare_amount',
    'passenger_count',
    'payment_type',
    'tip_amount'
]


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def trip_duration_histogram_view(request):
    try:
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        trip_durations = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.get_trip_durations(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        chart = build_histogram(
            x=trip_durations.tolist(),
            title='Distribution of Trip Durations (Minutes)',
            xaxis_title='Trip Duration (Minutes)',
            yaxis_title='Frequency',
            name='Trip Durations',
            nbinsx=50,
            color='rgba(100, 149, 237, 0.7)'
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def peak_hours_bar_view(request):
    try:
        csv_file = request.FILES.get('file')
        threshold = request.data.get('threshold', None)

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        peak_hours, df = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser, thres: analyser.identify_peak_hours(threshold=thres),
            required_columns=DEFAULT_REQUIRE_COLUMNS,
            thres=threshold,
            return_data=True
        )

        analyser = TaxisVisAnalyser(file_input=df)
        all_hours = analyser.df.groupby('pickup_hour').size().reset_index(name='trip_count')
        all_hours = all_hours.merge(peak_hours, on='pickup_hour', how='left', suffixes=('', '_peak'))
        all_hours['is_peak'] = all_hours['trip_count_peak'].notnull()

        colors = [
            'rgba(255, 99, 71, 0.6)' if is_peak else 'rgba(100, 149, 237, 0.6)'
            for is_peak in all_hours['is_peak']
        ]

        chart = build_bar_chart(
            x=all_hours['pickup_hour'].tolist(),
            y=all_hours['trip_count'].tolist(),
            title='Number of Trips per Pickup Hour',
            xaxis_title='Pickup Hour',
            yaxis_title='Number of Trips',
            name='Number of Trips',
            colors=colors
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def fare_distribution_box_view(request):
    try:
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        fare_amounts = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.get_fare_amounts(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        chart = build_box_plot(
            y=fare_amounts.tolist(),
            title='Fare Amount Distribution',
            yaxis_title='Fare Amount ($)',
            name='Fare Amounts',
            color='rgba(255, 165, 0, 0.6)'
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def passenger_count_pie_view(request):
    try:
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        passenger_count = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.analyse_passenger_count(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        labels = passenger_count['passenger_count'].astype(str).tolist()
        values = passenger_count['count'].tolist()

        chart = build_pie_chart(
            labels=labels,
            values=values,
            title='Passenger Count Distribution',
            name='Passenger Count Distribution',
            colors=[
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)'
            ]
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def payment_type_pie_view(request):
    try:
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        payment_type = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.analyse_payment_type(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        labels = payment_type['payment_type'].astype(str).tolist()
        values = payment_type['count'].tolist()

        chart = build_pie_chart(
            labels=labels,
            values=values,
            title='Payment Type Distribution',
            name='Payment Type Distribution',
            colors=[
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)'
            ]
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def tip_amount_analysis_view(request):
    try:
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        tip_distribution = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.get_tip_amounts(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        chart = build_box_plot(
            y=tip_distribution.tolist(),
            title='Tip Amount Distribution',
            yaxis_title='Tip Amount ($)',
            name='Tip Amounts',
            color='rgba(255, 105, 180, 0.6)'
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def distance_fare_scatter_plot_view(request):
    try:
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        distance_fare = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.analyse_distance_fare_scatter(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        chart = build_scatter_plot(
            x=distance_fare['trip_distance'].tolist(),
            y=distance_fare['fare_amount'].tolist(),
            title='Trip Distance vs. Fare Amount',
            xaxis_title='Trip Distance (Miles)',
            yaxis_title='Fare Amount ($)',
            name='Trips',
            mode='markers',
            marker_size=5,
            marker_opacity=0.6,
            marker_color='rgba(0, 123, 255, 0.6)'
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def time_series_line_view(request):
    try:
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({'error': 'No CSV file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        time_series = load_and_analyse(
            csv_file=csv_file,
            analysis_function=lambda analyser: analyser.analyse_time_series_trips(),
            required_columns=DEFAULT_REQUIRE_COLUMNS
        )

        chart = build_line_chart(
            x=time_series['pickup_date'].astype(str).tolist(),
            y=time_series['trip_count'].tolist(),
            title='Time Series of Trips Over Days',
            xaxis_title='Date',
            yaxis_title='Number of Trips',
            name='Trips',
            line_color='rgba(255, 99, 71, 0.8)',
            line_width=2,
            marker_size=4
        )

        return Response({'chart': chart}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
