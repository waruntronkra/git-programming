// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

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
    List<Color> lineColors = const [
      Color.fromARGB(255, 0, 68, 255),
      Color.fromARGB(255, 255, 0, 21),
      Color.fromARGB(255, 255, 0, 234),
      Color.fromARGB(255, 255, 145, 0),
      Color.fromARGB(255, 0, 255, 26),
      Color.fromARGB(255, 0, 181, 197),
      Color.fromARGB(255, 88, 51, 0),
      Color.fromARGB(255, 0, 0, 0),
      Color.fromARGB(255, 95, 0, 87),
    ];

    List<String> legend = [];
    for (var item in dataLineChart.entries) {
      legend.add(item.key);
    }
    // List<Widget> tooltipArr = [];
    final TrackballBehavior trackballBehavior = TrackballBehavior(
      enable: true,
      // tooltipSettings: const InteractiveTooltip(enable: true, color: Colors.transparent, borderColor: Colors.transparent),
      tooltipSettings: const InteractiveTooltip(enable: true),
      tooltipAlignment: ChartAlignment.near,
      tooltipDisplayMode: TrackballDisplayMode.groupAllPoints,
      // builder: (context, trackballDetails) {
      //   List<String> dataAllIndex = [];
      //   for (var process in legend) {
      //     if (dataLineChart[process][trackballDetails.pointIndex] != null) {
      //       dataAllIndex.add((dataLineChart[process][trackballDetails.pointIndex]).toString());
      //     }
      //     else {
      //       dataAllIndex.add('');
      //     }
      //   }
      //   print(dataAllIndex);
      //   print(legend);
      //   tooltipArr = [];
      //   for (var i = 0; i < dataAllIndex.length; i++) {
      //     if (dataAllIndex[i].isNotEmpty) {
      //       print('${legend[i]} : ${dataAllIndex[i]}');
      //       tooltipArr.add(Row(
      //         mainAxisSize: MainAxisSize.min,
      //         children: [
      //           Icon(Icons.circle, size: 11, color: lineColors[i]),
      //           const SizedBox(width: 5),
      //           Text(
      //             '${legend[i]} : ${dataAllIndex[i]}',
      //             style: const TextStyle(
      //               fontSize: 11
      //             ),
      //           )
      //         ]
      //       ));
      //     }
      //   }
      //   return Container(
      //     decoration: BoxDecoration(
      //       color: const Color.fromARGB(255, 255, 255, 255),
      //       borderRadius: BorderRadius.circular(5),
      //       boxShadow: const[
      //         BoxShadow(
      //           color: Colors.grey,
      //           offset: Offset(0, 2),
      //           blurRadius: 4,
      //           spreadRadius: 1
      //         )
      //       ]
      //     ),
      //     padding: const EdgeInsets.all(10),
      //     child: Column(
      //       crossAxisAlignment: CrossAxisAlignment.start,
      //       mainAxisSize: MainAxisSize.min, 
      //       children: [
      //         Text(
      //           xAxis[trackballDetails.pointIndex!], 
      //           style: const TextStyle(
      //             fontSize: 12,
      //             fontWeight: FontWeight.bold
      //           ),
      //         ),
      //         ...tooltipArr
      //       ]
      //     ),
      //   );
      // },
    );

    List<LineSeries<PackData, String>> seriesList = dataLineChart.keys.toList().asMap().entries.map((entry) {
      int index = entry.key;
      String key = entry.value;
      return LineSeries<PackData, String>(
        dataSource: generateData(key),
        xValueMapper: (PackData val, _) => val.dt,
        yValueMapper: (PackData val, _) => val.value,
        name: key,
        color: lineColors[index], // Use the Color array
        markerSettings: const MarkerSettings(isVisible: true),
      );
    }).toList();

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
      series: seriesList
    );
  }
}

class PackData {
  PackData(this.dt, this.value, this.qty);

  final String dt;
  final dynamic value;
  final dynamic qty;
}