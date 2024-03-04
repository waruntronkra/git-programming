import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class BarChart extends StatelessWidget {
  const BarChart({
    required this.dataBarChart,
    required this.paretoTitle,

    Key? key
  }) : super(key: key);

  final List<dynamic> dataBarChart;
  final String paretoTitle;

  List<ChartData> generateData() {
    List<ChartData> chartDataList = [];
    for (var data in dataBarChart) {
      chartDataList.add(
        ChartData(
          data[0].toString(),
          data[1] as double
        ),
      );
    }
    return chartDataList;
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
          text: paretoTitle,
          textStyle: const TextStyle(
              color: Color.fromARGB(255, 0, 0, 0),
              fontWeight: FontWeight.bold,
              fontSize: 13)),
      primaryXAxis: const CategoryAxis(labelRotation: 90, labelStyle: TextStyle(fontSize: 10)),
      series: <CartesianSeries>[
        StackedColumnSeries<ChartData, String>(
          dataSource: generateData(),
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.y1,
          color: const Color.fromARGB(255, 255, 0, 0),
          name: '% Fail',
          dataLabelSettings: const DataLabelSettings(
            alignment: ChartAlignment.near,
            isVisible: true, angle: -90, 
            textStyle: TextStyle(color: Colors.black)
          ),
        ),
      ],
      trackballBehavior: trackballBehavior,
    );
  }
}

class ChartData{
  ChartData(this.x, this.y1);
  final String x;
  final double y1;
}