// ignore_for_file: file_names, prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';
import 'package:google_fonts/google_fonts.dart';

class MyLineChart extends StatelessWidget {
  const MyLineChart({
    required this.dataLineChart,
    required this.dataQtyLineChart,
    required this.xAxis,
    Key? key
  }) : super(key : key);

  final Map<String, dynamic> dataLineChart;
  final Map<String, dynamic> dataQtyLineChart;
  final List<String> xAxis;

  List<PackData> generateData(String key) {
    List<PackData> data = [];
    for (var i = 0; i < xAxis.length; i++) {
      data.add(PackData(xAxis[i], dataLineChart[key][i], dataQtyLineChart[key][i]));
    }
    return data;
  }
  
  @override
  Widget build(BuildContext context) {
    final List<Color> seriesColors = [
      Colors.red,
      const Color.fromARGB(255, 0, 8, 255),
      const Color.fromARGB(255, 255, 230, 0),
      Colors.orange,
      Colors.green,
      const Color.fromARGB(255, 255, 113, 160),
      Colors.purple,
      Colors.black,
      Colors.grey,
      const Color.fromARGB(255, 0, 221, 255),
    ];
    List<String> legend = [];
    for (var item in dataLineChart.entries) {
      legend.add(item.key);
    }

    final TrackballBehavior trackballBehavior = TrackballBehavior(
      enable: true,
      tooltipAlignment: ChartAlignment.near,
      tooltipSettings: InteractiveTooltip(
        format: 'series.name : point.y %',
        textStyle: GoogleFonts.nunito(
          fontSize: 10
        )
      ),
      tooltipDisplayMode: TrackballDisplayMode.groupAllPoints,
    );

    List<LineSeries<PackData, String>> seriesList = dataLineChart.keys.toList().asMap().entries.map((entry) {
      int index = entry.key;
      String key = entry.value;
      return LineSeries<PackData, String>(
        dataSource: generateData(key),
        xValueMapper: (PackData val, _) => val.dt,
        yValueMapper: (PackData val, _) => val.value,
        name: key,
        markerSettings: const MarkerSettings(isVisible: true),
        color: seriesColors[index]
      );
    }).toList();

    return SfCartesianChart(
      backgroundColor: Colors.transparent,
      title: ChartTitle(
        text: '% YIELD',
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
      legend: Legend(
        isVisible: true,
        position: LegendPosition.right,
        textStyle: GoogleFonts.nunito(
          fontSize: 10
        )
      ),
      trackballBehavior: trackballBehavior,
      series: seriesList,
    );
  }
}

class PackData {
  PackData(this.dt, this.value, this.qty);

  final String dt;
  final dynamic value;
  final dynamic qty;
}