from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse


def chart_list(request):
    """数据统计"""

    return render(request, 'chart_list.html')


def chart_bar(request):
    """构造柱状图数据"""
    legend_list = ['吸螺', '骡子']
    series_list = [
        {
            "name": '吸螺',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20, 45]
        },
        {
            "name": '骡子',
            "type": 'bar',
            "data": [45, 50, 62, 17, 13, 25, 33]
        }
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
    result = {
        'status': True,
        'data_dict': {
            'legend_list': legend_list,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """构造饼状图数据"""
    db_data_list = [
        {"value": 1048, 'name': 'IT部门'},
        {"value": 1735, "name": '运营'},
        {"value": 580, "name": '新媒体'},
    ]
    result = {
        'status': True,
        "data": db_data_list
    }
    return JsonResponse(result)


def chart_line(request):
    legend = ["上海", "广西"]
    series_list = [
        {
            "name": '上海',
            "type": 'line',
            "stack": 'Total',
            "data": [15, 20, 36, 10, 10, 10]
        },
        {
            "name": '广西',
            "type": 'line',
            "stack": 'Total',
            "data": [45, 10, 66, 40, 20, 50]
        }
    ]
    x_axis = ['1月', '2月', '4月', '5月', '6月', '7月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):
    """highcharts实例"""
    return render(request, 'highcharts.html')