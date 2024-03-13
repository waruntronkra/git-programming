// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:google_fonts/google_fonts.dart';

class MyBarChartParetoByDate extends StatelessWidget {
  const MyBarChartParetoByDate({
    required this.dataBarChart,
    required this.paretoTitle,

    Key? key
  }) : super(key: key);

  final List<List<dynamic>> dataBarChart;
  final String paretoTitle;

  List<ChartData> generateData() {
    List<ChartData> chartDataList = [];
    for (var data in dataBarChart) {
      chartDataList.add(
        ChartData(
          data[0].toString(),
          data[1] as int
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
        textStyle: GoogleFonts.nunito(
          color: const Color.fromARGB(255, 0, 0, 0),
          fontWeight: FontWeight.bold,
          fontSize: 11
        )
      ),
      primaryXAxis: CategoryAxis(
        labelRotation: 90,
        labelStyle: GoogleFonts.nunito(
          fontSize: 10
        ),
      ),
      primaryYAxis: NumericAxis(
        labelRotation: 0,
        labelStyle: GoogleFonts.nunito(
          fontSize: 10
        ),
      ),
      series: <CartesianSeries>[
        StackedColumnSeries<ChartData, String>(
          dataSource: generateData(),
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.y1,
          color: const Color.fromARGB(255, 255, 0, 0),
          name: 'QTY',
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
  final int y1;
}