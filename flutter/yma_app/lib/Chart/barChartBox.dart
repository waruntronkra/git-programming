// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MyBarChartBox extends StatelessWidget {
  const MyBarChartBox({
    required this.dataBoxPlot,
    required this.minYRange,
    required this.maxYRange,
    Key? key,
  }) : super(key: key);

  final Map<String, dynamic> dataBoxPlot;
  final double? minYRange;
  final double? maxYRange;

  @override
  Widget build(BuildContext context) {
    final TrackballBehavior trackballBehavior = TrackballBehavior(
      enable: true,
      tooltipSettings: const InteractiveTooltip(enable: true),
      tooltipAlignment: ChartAlignment.center,
      tooltipDisplayMode: TrackballDisplayMode.groupAllPoints,
    );

    List<ChartData> chartDataList = [];
    dataBoxPlot.forEach((date, values) {
      if (values != null) {
        chartDataList.add(ChartData(date, values.cast<double>()));
      }
    });
    return SfCartesianChart(
      primaryXAxis: const CategoryAxis(),
      primaryYAxis: NumericAxis(minimum: minYRange, maximum: maxYRange),
      series: <CartesianSeries>[
        BoxAndWhiskerSeries<ChartData, String>(
          dataSource: chartDataList,
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.y,
          color: Colors.blue,
          borderColor: Colors.black,
          borderWidth: 1,
        ),
      ],
      trackballBehavior: trackballBehavior,
    );
  }
}

class ChartData {
  ChartData(this.x, this.y);
  final String x;
  final List<double> y;
}
