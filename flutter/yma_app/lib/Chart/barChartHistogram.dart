// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MyBarChartHistogram extends StatelessWidget {
   const MyBarChartHistogram({
    required this.randomDataHistogram,
    required this.bin,
    required this.minXRange,
    required this.maxXRange,
    required this.maxYRange,
    Key? key,
  }) : super(key: key);

  final List<double> randomDataHistogram;
  final double bin;
  final double? minXRange;
  final double? maxXRange;
  final double? maxYRange;

  List<ChartData> generateHistogramData() {
    final List<ChartData> histogramData = [];
 
    for (double value in randomDataHistogram) {
      histogramData.add(ChartData(value));
    }
    return histogramData;
  }

  @override
  Widget build(BuildContext context) {
    final TrackballBehavior trackballBehavior = TrackballBehavior(
      enable: true,
      tooltipSettings: const InteractiveTooltip(enable: true),
      tooltipAlignment: ChartAlignment.near,
      tooltipDisplayMode: TrackballDisplayMode.groupAllPoints,
    );
    final List<ChartData> histogramData = generateHistogramData();
    return SfCartesianChart(
      primaryXAxis: NumericAxis(minimum: minXRange, maximum: maxXRange),
      primaryYAxis: NumericAxis(maximum: maxYRange),
      series: <CartesianSeries>[
        HistogramSeries<ChartData, double>(
          dataSource: histogramData,
          showNormalDistributionCurve: true,
          curveColor: const Color.fromARGB(255, 255, 0, 0),
          yValueMapper: (ChartData data, _) => data.y,
          color: Colors.blue,
          borderColor: Colors.black,
          borderWidth: 0.5,
          binInterval: bin,
        ),
      ],
      trackballBehavior: trackballBehavior,
    );
  }
}

class ChartData{
  ChartData(this.y);
  final double y;
}
