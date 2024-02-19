// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'lineChartYIELD.dart';
import 'barChartYIELD.dart';
import 'package:shimmer/shimmer.dart';

typedef UpdateMixChart = void Function(String process);
class WidgetChart extends StatefulWidget {
  const WidgetChart({
    required this.dataLineChart,
    required this.dataQtyLineChart,
    required this.xAxis,
    required this.arrProcessForMixChart,
    required this.sortedJsonYield,
    required this.dataLineChartMix,
    required this.dataBarChart,
    required this.mixChartVisible,
    required this.updateChart,
    required this.processSelected,
    required this.isLoadingLineChart,
    Key? key
    }) : super(key: key);

  final Map<String, dynamic> dataLineChart;
  final Map<String, dynamic> dataQtyLineChart;
  final List<String> xAxis;
  final List<String> arrProcessForMixChart;
  final Map<String, dynamic> sortedJsonYield;
  final List<double> dataLineChartMix;
  final List<List<dynamic>> dataBarChart;
  final bool mixChartVisible;
  final UpdateMixChart updateChart;
  final String processSelected;
  final bool isLoadingLineChart;

  @override
  State<WidgetChart> createState() => _WidgetChartState();
}

class _WidgetChartState extends State<WidgetChart> {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Stack(
        children: [
          // Line Chart [Loading...] =================================
          Visibility(
            visible: widget.isLoadingLineChart,
            child: Shimmer.fromColors(
              baseColor: Colors.grey[300]!,
              highlightColor: Colors.grey[100]!,
              child: Container(
                margin: const EdgeInsets.only(left: 10),
                padding: const EdgeInsets.only(left: 0, top: 0, bottom: 10),
                width: MediaQuery.of(context).size.width * 0.94,
                height: 290,
                child: const MyLineChart(
                  dataLineChart: {'.' : [3, 4, 2, 5], '..': [4, 1, 5, 3]},
                  dataQtyLineChart: {'.' : [0, 0, 0, 0], '..' : [0, 0, 0, 0],},
                  xAxis: ['', ' ', '   ', '    '],
                )
              ),
            ),
          ),
          // Line Chart =================================
          Visibility(
            visible: widget.isLoadingLineChart == true ? false : true,
            child: Container(
              margin: const EdgeInsets.only(left: 10),
              padding: const EdgeInsets.only(left: 0, top: 0, bottom: 10),
              width: MediaQuery.of(context).size.width * 0.94,
              height: 290,
              child: MyLineChart(
                dataLineChart: widget.dataLineChart,
                dataQtyLineChart: widget.dataQtyLineChart,
                xAxis: widget.xAxis,
              )
            ),
          ),
          // Row Process =================================
          Visibility(
            visible: widget.arrProcessForMixChart.isEmpty ? false : true,
            child: Container(
              margin: const EdgeInsets.only(left: 10, top: 275),
              child: Wrap(
                spacing: 1,
                children: [..._buildListProcessForBarChart(widget.arrProcessForMixChart)],
              ),
            )
          ),
          // Mix Chart =================================
          Visibility(
            visible: widget.mixChartVisible,
            child: Container(
              margin: const EdgeInsets.only(left: 0, top: 330),
              width: MediaQuery.of(context).size.width * 0.97,
              height: 290,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: MyBarChart(
                  dataBarChart: widget.dataBarChart,
                  dataLineChartMix: widget.dataLineChartMix,
                  chartTitle: widget.processSelected,
                )
              )
            )
          ),
          Visibility(
            visible: widget.mixChartVisible,
            child: Container(
              margin: const EdgeInsets.only(top: 630, left: 8),
              child: Transform.rotate(
                angle: 1.6,
                child: const Text(
                  'QTY',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                )
              )
            )
          ),
          Visibility(
            visible: widget.mixChartVisible,
              child: Container(
              margin: const EdgeInsets.only(top: 630),
              width: MediaQuery.of(context).size.width * 0.98,
              alignment: Alignment.topRight,
              child: Transform.rotate(
                angle: 1.6,
                child: const Text(
                  '% FAIL',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                )
              )
            )
          ),
          Container(
            margin: const EdgeInsets.only(top: 650),
            width: MediaQuery.of(context).size.width * 0.97,
            height: 50,
          )
        ],
      ),
    );
  }
  
  // ========================= Create Process Button for Mix Chart =========================
  List<Widget> _buildListProcessForBarChart(List<String>? processIn) {
    List<Widget> subListProcessForBarChart = [];
    if (processIn != null) {
      for (String item in processIn) {
        subListProcessForBarChart.add(Container(
          height: 25,
          margin: const EdgeInsets.only(left: 5, top: 5),
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color.fromARGB(255, 3, 141, 93),
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(5),
              )
            ),
            child: Text(item),
            onPressed: () {
              widget.updateChart(item);
            },
          ),    
        ));
      }
    }
    return subListProcessForBarChart;
  }
}