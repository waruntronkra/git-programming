import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MyLineChart extends StatelessWidget {
  const MyLineChart({
    required this.dataLineChart,
    required this.xAxis,
    Key? key
  }) : super(key : key);

  final Map<String, dynamic> dataLineChart;
  final List<String> xAxis;

  List<PackData> generateData(String key) {
    List<PackData> data = [];
    for (var i = 0; i < xAxis.length; i++) {
      data.add(PackData(xAxis[i],dataLineChart[key][i]));
    }
    return data;
  }

  // int calculateLabelRotationAngle(int labelCount) {
  //   const int rotationThreshold = 8;
  //   print(labelCount);
  //   // If there are too many labels, rotate them for better visibility
  //   if (labelCount > rotationThreshold) {
  //     // Calculate the rotation angle dynamically based on the label count
  //     return ((45 / rotationThreshold) * (labelCount - rotationThreshold)).toInt();
  //   } 
  //   else {
  //     // No rotation needed if the label count is within the threshold
  //     return 0;
  //   }
  // }

  @override
  Widget build(BuildContext context) {
    final TrackballBehavior trackballBehavior = TrackballBehavior(
        enable: true,
        tooltipSettings: const InteractiveTooltip(enable: true),
        tooltipAlignment: ChartAlignment.near,
        tooltipDisplayMode: TrackballDisplayMode.groupAllPoints
    );

    // int xAxisLabelCount = xAxis.length;
    // int rotationAngle = calculateLabelRotationAngle(xAxisLabelCount);

    return SfCartesianChart(
      title: const ChartTitle(
        text: '% YIELD',
        textStyle: TextStyle(
          color: Color.fromARGB(255, 0, 0, 0), 
          fontWeight: FontWeight.bold,
          fontSize: 13
        )
      ),
      primaryXAxis: const CategoryAxis(
        labelRotation: 0,
      ),
      legend: const Legend(isVisible: true),
      trackballBehavior: trackballBehavior,
      series: <CartesianSeries<PackData, String>>[
        ...dataLineChart.keys.map((key) => LineSeries<PackData, String>(
          dataSource: generateData(key),
          xValueMapper: (PackData val, _) => val.dt,
          yValueMapper: (PackData val, _) => val.value,
          name: key,
          markerSettings: const MarkerSettings(isVisible: true),
        )).toList()
      ]
    );
  }
}

class PackData {
  PackData(this.dt, this.value);

  final String dt;
  final dynamic value;
}