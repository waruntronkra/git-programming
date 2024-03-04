// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MixChartFBNYieldMultiLine extends StatelessWidget {
  const MixChartFBNYieldMultiLine({
    required this.dataBarChart,
    required this.dataMultiLineChart,
    required this.chartTitle,
    required this.xAxis,
    Key? key
  }) : super(key: key);

  final List<dynamic> dataBarChart;
  final Map<String, dynamic> dataMultiLineChart;
  final String chartTitle;
  final List<String> xAxis;

  List<StackBarChartData> generateDataStackBar() {
    List<StackBarChartData> data = [];
    for (var i = 0; i < dataBarChart.length; i++) {
      data.add(StackBarChartData(
        xAxis[i], // x-axis name
        dataBarChart[i][0], // 1st stack
        dataBarChart[i][1] // 2nd stack
      ));
    }
    return data;
  }

  List<MultipleLineChartData> generateDataMultipleLine(String key) {
    List<MultipleLineChartData> data = [];
    for (var i = 0; i < xAxis.length; i++) {
      data.add(MultipleLineChartData(xAxis[i], dataMultiLineChart[key][i]));
    }
    return data;
  }

  @override
  Widget build(BuildContext context) {
    final TrackballBehavior trackballBehavior = TrackballBehavior(
      enable: true,
      tooltipSettings: const InteractiveTooltip(enable: true),
      tooltipAlignment: ChartAlignment.near,
      tooltipDisplayMode: TrackballDisplayMode.groupAllPoints
    );
    List<LineSeries<MultipleLineChartData, String>> seriesList = dataMultiLineChart.keys.toList().asMap().entries.map((entry) {
      String key = entry.value;
      return LineSeries<MultipleLineChartData, String>(
        dataSource: generateDataMultipleLine(key),
        xValueMapper: (MultipleLineChartData data, _) => data.dt,
        yValueMapper: (MultipleLineChartData data, _) => data.value,
        name: key,
        yAxisName: '% YIELD',
        markerSettings: const MarkerSettings(isVisible: true),
      );
    }).toList();
    
    return SfCartesianChart(
      title: ChartTitle(
        text: chartTitle,
        textStyle: const TextStyle(
          color: Color.fromARGB(255, 0, 0, 0), 
          fontWeight: FontWeight.bold,
          fontSize: 13
        )
      ),
      legend: const Legend(
        isVisible: true,
        position: LegendPosition.top
      ),
      primaryXAxis: const CategoryAxis(labelRotation: 90, labelStyle: TextStyle(fontSize: 10)),
      series: <CartesianSeries>[
        StackedColumnSeries<StackBarChartData, String>(
          dataSource: generateDataStackBar(),
          xValueMapper: (StackBarChartData data, _) => data.x,
          yValueMapper: (StackBarChartData data, _) => data.y1,
          color: const Color.fromARGB(255, 0, 255, 8),
          name: 'PASS'
        ),
        StackedColumnSeries<StackBarChartData, String>(
          dataSource: generateDataStackBar(),
          xValueMapper: (StackBarChartData data, _) => data.x,
          yValueMapper: (StackBarChartData data, _) => data.y2,
          color: const Color.fromARGB(255, 255, 17, 0),
          name: 'FAIL'
        ),
        ...seriesList,
      ],
      axes: const <ChartAxis>[
        NumericAxis(
          opposedPosition: true,
          name: '% YIELD', // Second axis has been set code above
        ),
      ],
      trackballBehavior: trackballBehavior,
    );
  }
}

class StackBarChartData{
  StackBarChartData(this.x, this.y1, this.y2);

  final String x;
  final int y1;
  final int y2;
}

class MultipleLineChartData{
  MultipleLineChartData(this.dt, this.value);

  final String dt;
  final dynamic value;
}