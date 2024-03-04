// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MixChartFBNYield extends StatelessWidget {
  const MixChartFBNYield({
    required this.dataBarChart,
    required this.dataLineChartMix,
    required this.chartTitle,
    Key? key
  }) : super(key: key);

  final List<List<dynamic>> dataBarChart;
  final List<double> dataLineChartMix;
  final String chartTitle;

  List<ChartData> generateData() {
    List<ChartData> data = [];
    for (var i = 0; i < dataBarChart.length; i++) {
      data.add(ChartData(
        dataBarChart[i][0], // x-axis name
        dataBarChart[i][1], // 1st stack
        dataBarChart[i][2], // 2nd stack
        dataLineChartMix[i] // percent
      ));
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
    return SfCartesianChart(
      title: ChartTitle(
        text: chartTitle,
        textStyle: const TextStyle(
          color: Color.fromARGB(255, 0, 0, 0), 
          fontWeight: FontWeight.bold,
          fontSize: 13
        )
      ),
      primaryXAxis: const CategoryAxis(),
      series: <CartesianSeries>[
        StackedColumnSeries<ChartData, String>(
          dataSource: generateData(),
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.y1,
          color: const Color.fromARGB(255, 0, 255, 8),
          name: 'PASS'
        ),
        StackedColumnSeries<ChartData, String>(
          dataSource: generateData(),
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.y2,
          color: const Color.fromARGB(255, 255, 17, 0),
          name: 'FAIL'
        ),
        LineSeries<ChartData, String>(
          dataSource: generateData(),
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.lineValue,
          color: Colors.blue,
          yAxisName: '% YIELD', // Second axis has been set code above
          name: 'YIELD',
          markerSettings: const MarkerSettings(isVisible: true),
        )
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

class ChartData{
  ChartData(this.x, this.y1, this.y2, this.lineValue);
  final String x;
  final int y1;
  final int y2;
  final double lineValue;
}