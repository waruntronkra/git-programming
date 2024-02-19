import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_charts/charts.dart';

class MyBarChart extends StatelessWidget {
  const MyBarChart({
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
        dataBarChart[i][0], 
        dataBarChart[i][1], 
        dataBarChart[i][2], 
        dataLineChartMix[i]
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

    return Scaffold(
      body: Column( 
        children: [ 
          Padding(
            padding: const EdgeInsets.all(20),
            child: SizedBox(
              width: MediaQuery.of(context).size.width * 0.97, // Set the desired width
              height: 280, 
              child: SfCartesianChart(
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
              )
            )
          )
        ]   
      )
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