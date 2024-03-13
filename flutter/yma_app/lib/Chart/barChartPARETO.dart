// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MyBarChartPareto extends StatelessWidget {
  const MyBarChartPareto({
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
          data[1] as int,
          data[2] as int,
          data[3] as double,
        ),
      );
    }
    return chartDataList;
  }

  @override
  Widget build(BuildContext context) {
    final TrackballBehavior trackballBehavior = TrackballBehavior(
      enable: true,
      tooltipSettings: InteractiveTooltip(
        textStyle: GoogleFonts.nunito(
          fontSize: 10
        )
      ),
      tooltipAlignment: ChartAlignment.near,
      tooltipDisplayMode: TrackballDisplayMode.groupAllPoints
    );
    return SfCartesianChart(
      backgroundColor: Colors.transparent,
      title: ChartTitle(
        text: paretoTitle,
        textStyle: GoogleFonts.nunito(
          color: const Color.fromARGB(255, 0, 0, 0), 
          fontWeight: FontWeight.bold,
          fontSize: 10
        )
      ),
      primaryXAxis: CategoryAxis(
        labelRotation: 0,
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
      legend: const Legend(
        isVisible: false,
      ),
      series: <CartesianSeries>[
        StackedColumnSeries<ChartData, String>(
            dataSource: generateData(),
            xValueMapper: (ChartData data, _) => data.x,
            yValueMapper: (ChartData data, _) => data.y1,
            color: const Color.fromARGB(255, 0, 255, 8),
            name: 'PASS'),
        StackedColumnSeries<ChartData, String>(
            dataSource: generateData(),
            xValueMapper: (ChartData data, _) => data.x,
            yValueMapper: (ChartData data, _) => data.y2,
            color: const Color.fromARGB(255, 255, 17, 0),
            name: 'FAIL'),
        LineSeries<ChartData, String>(
          dataSource: generateData(),
          xValueMapper: (ChartData data, _) => data.x,
          yValueMapper: (ChartData data, _) => data.lineValue,
          color: Colors.blue,
          yAxisName: '% FAIL', // Second axis has been set code above
          name: '% FAIL',
          markerSettings: const MarkerSettings(isVisible: true),
        )
      ],
      axes: const <ChartAxis>[
        NumericAxis(
          opposedPosition: true,
          name: '% FAIL', // Second axis has been set code above
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