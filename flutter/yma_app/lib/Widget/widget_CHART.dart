// ignore_for_file: file_names

import 'package:flutter/material.dart';
import '../Chart/lineChartYIELD.dart';
import '../Chart/barChartYIELD.dart';
import 'package:google_fonts/google_fonts.dart';
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
      child: Column(
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
              margin: const EdgeInsets.only(left: 5, top: 5),
              padding: const EdgeInsets.all(5),
              width: MediaQuery.of(context).size.width * 0.975,
              height: MediaQuery.of(context).size.height * 0.3,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(15),
                boxShadow: const [
                  BoxShadow(
                    blurRadius: 5,
                    color: Color.fromARGB(255, 233, 233, 233)
                  )
                ]
              ),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white
                ),
                child: MyLineChart(
                  dataLineChart: widget.dataLineChart,
                  dataQtyLineChart: widget.dataQtyLineChart,
                  xAxis: widget.xAxis,
                )
              )
            )
          ),
          // Row Process =================================
          Visibility(
            visible: widget.arrProcessForMixChart.isEmpty ? false : true,
            child: Container(
              margin: const EdgeInsets.only(bottom: 5),
              width: MediaQuery.of(context).size.width,
              alignment: Alignment.center,
              child: Wrap(
                spacing: 1,
                children: [..._buildListProcessForBarChart(widget.arrProcessForMixChart)],
              )
            )
          ),
          Stack(
            children: [
              // Mix Chart =================================
                widget.mixChartVisible == true ?
                Container(
                  margin: const EdgeInsets.only(left: 5),
                  padding: const EdgeInsets.all(5),
                  width: MediaQuery.of(context).size.width * 0.975,
                  height: MediaQuery.of(context).size.height * 0.3,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    boxShadow: const [
                      BoxShadow(
                        blurRadius: 5,
                        color: Color.fromARGB(255, 233, 233, 233)
                      )
                    ]
                  ),
                  child: Container(
                    decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Colors.white
                    ),
                    child: MyBarChart(
                      dataBarChart: widget.dataBarChart,
                      dataLineChartMix: widget.dataLineChartMix,
                      chartTitle: widget.processSelected,
                    )
                  )
                )
                :
                Container (
                  margin: const EdgeInsets.only(left: 30, top: 20),
                  child: const Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          Text('Step 1: '),
                          Text('Choose the process you want to see.'),
                        ],
                      ),
                    ],
                  )
                )
            ]
          ),
          const SizedBox(height: 50)
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
          decoration: const BoxDecoration(
            boxShadow: [
              BoxShadow(
                blurRadius: 7,
                offset: Offset(1, 1),
                color: Color.fromARGB(255, 170, 170, 170)
              )
            ]
          ),
          height: 25,
          margin: const EdgeInsets.only(left: 5, top: 5),
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(5),
              ),
            ),
            child: Text(
              item,
              style: GoogleFonts.nunito(
                fontSize: 14,
                fontWeight: FontWeight.bold
              ),
            ),
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