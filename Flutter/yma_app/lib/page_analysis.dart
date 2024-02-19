import 'dart:math';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:yma_app/barChartBox.dart';
import 'dart:convert';
import 'package:shimmer/shimmer.dart';
import 'barChartHistogram.dart';
import 'table_histogram.dart';
import 'package:dropdown_button2/dropdown_button2.dart';

class PageAnalysis extends StatefulWidget {
  const PageAnalysis({
    required this.processArr,
    required this.levelSelected,
    required this.modelSelected,
    required this.daySelected,
    required this.modeDay,
    Key? key
  }) : super(key: key);

  final List<String> processArr;
  final String levelSelected;
  final String modelSelected;
  final String daySelected;
  final String modeDay;

  @override
  State<PageAnalysis> createState() => _PageAnalysisState();
}

class _PageAnalysisState extends State<PageAnalysis> {
  List<String> stepName = [];
  List<String> itemsSpec = [];
  String defaultSpec = '';
  String processSelected = '';
  String stepNameSelected = '';
  String stepNameSelectedToVoid = '';
  List<int> dataBarChartHistogram = [];
  List<Map<String, dynamic>> storeDecodedData = [];
  List<double> randomDataHistogram = [];
  String histogramTitle = '';
  double bin = 0.0;
  double? minXRange;
  double? maxXRange;
  double? maxYRange;
  double? maxYRangeNew;

  List<List<int>> dataBarChartHistogramArr = []; 
  List<dynamic> dataTableHistogramArr = []; 
  List<List<double>> randomDataHistogramArr = [];
  List<double> binArr = [];
  List<double?> maxXRangeArr = [];
  List<double?> minXRangeArr = [];
  List<double?> maxYRangeArr = [];
  List<String> dateArray = [];

  Map<String, dynamic> dataBoxPlot = {};
  List<Map<String, dynamic>> dataBoxPlotArr = [];
  double? minYRangeBox;
  double? maxYRangeBox;

  List<Map<String, dynamic>> decodedDataHistogram = [];
  List<Map<String, dynamic>> decodedDataHistogramRawData = [];

  Map<String, dynamic> stringEncryptedArray = {};

  bool isLoading = false;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Stack(
        children: [
          // ================ [PROCESS] ================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 10),
            child: Wrap(
              spacing: 1,
              children: [..._buildListProcessForBarChart(widget.processArr)],
            ),
          ),
          // ================ [CONDITION] ================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 90),
            width: MediaQuery.of(context).size.width * 0.96,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(5),
              border: Border.all(color: Colors.black, width: 2)
            ),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [..._buildListStepName(stepName)],
              )
            )
          ),
          // ================ [SPEC] ================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 160),
            width: MediaQuery.of(context).size.width * 0.96,
            height: 30,
            child: DropdownButtonHideUnderline(
              child: DropdownButton2<String>(
                isExpanded: true,
                hint: Row(
                  children: [
                    Expanded(
                      child: Row(
                        children: [
                          const Icon(Icons.dataset_linked_outlined, color: Color.fromARGB(255, 3, 141, 93), size: 23),
                          const SizedBox(width: 5),
                          Text(
                            defaultSpec,
                            style: const TextStyle(
                              fontSize: 12,
                              color: Color.fromARGB(255, 3, 141, 93)
                            ),
                            overflow: TextOverflow.ellipsis,
                          )
                        ]
                      )
                    )
                  ],
                ),
                items: itemsSpec.map((String item) => DropdownMenuItem<String>(
                  value: item,
                  child: Row(
                    children: [
                      const Icon(Icons.confirmation_num_outlined, color: Color.fromARGB(255, 3, 141, 93), size: 23),
                      const SizedBox(width: 5),
                      Text(
                        item,
                        style: const TextStyle(
                          fontSize: 12,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                        overflow: TextOverflow.ellipsis,
                      )
                    ]
                  )
                )).toList(),
                onChanged: (String? newVal) {
                  setState(() {
                    defaultSpec = newVal!;
                    if (newVal != '') {
                      dataBarChartHistogramArr = []; 
                      randomDataHistogramArr = [];
                      binArr = [];
                      maxXRangeArr = [];
                      minXRangeArr = [];
                      maxYRangeArr = [];
                      fetchDataHistogram(newVal, stepNameSelected);
                    }
                  });
                },
                buttonStyleData: ButtonStyleData(
                  height: 50,
                  width: 160,
                  padding: const EdgeInsets.only(left: 14, right: 14),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(5),
                    border: Border.all(
                      color: Colors.transparent,
                    ),
                    color: const Color.fromARGB(255, 255, 255, 255),
                  ),
                  elevation: 2,
                ),
                dropdownStyleData: DropdownStyleData(
                  maxHeight: 200,
                  width: MediaQuery.of(context).size.width * 0.96,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(0),
                    color: const Color.fromARGB(255, 255, 255, 255),
                  ),
                  offset: const Offset(1, 0),
                  scrollbarTheme: ScrollbarThemeData(
                    radius: const Radius.circular(40),
                    thickness: MaterialStateProperty.all<double>(6),
                    thumbVisibility: MaterialStateProperty.all<bool>(true),
                  ),
                ),
                menuItemStyleData: const MenuItemStyleData(
                  height: 40,
                  padding: EdgeInsets.only(left: 14, right: 14),
                ),
              )
            )
          ),
          // ================ [Histogram] & [BoxPlot] ================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 200),     
            child: SingleChildScrollView(   
              scrollDirection: Axis.horizontal,
              child : Row(
                children: [
                  ..._createHistogramChart (
                    randomDataHistogramArr,
                    binArr,
                    maxXRangeArr,
                    minXRangeArr,
                    maxYRangeArr,
                    dataBoxPlotArr,
                    minYRangeBox
                  )
                ]
              )
            )
          ),
          Visibility(
            visible: isLoading,
            child: Shimmer.fromColors(
              baseColor: Colors.grey[300]!,
              highlightColor: Colors.grey[100]!,
              child: Container(
                margin: const EdgeInsets.only(left: 10, top: 200),     
                child: SingleChildScrollView(   
                  scrollDirection: Axis.horizontal,
                  child : Row(
                    children: [
                      ..._createHistogramChart (
                        [[85.0, 70.0, 74.0, 73.0, 81.0, 72.0, 80.0, 85.0, 68.0, 78.0, 86.0, 78.0, 70.0, 73.0, 85.0, 73.0]],
                        [1.7058823529411764],
                        [98.70588235294113],
                        [68.0],
                        [12.0],
                        [{'A': [85.0, 70.0, 74.0, 73.0, 81.0, 72.0, 80.0, 85.0, 68.0, 78.0, 86.0, 78.0, 70.0, 73.0, 85.0]}],
                        68.0
                      )
                    ]
                  )
                ),
              ),
            )
          ),
          Container(margin: const EdgeInsets.only(left: 10, top: 800), height: 200)
        ]
      )
    );
  }

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
            onPressed: () async{
              stringEncryptedArray = await encryptData([
                widget.levelSelected,
                widget.modelSelected,
                widget.daySelected,
                widget.modeDay,
                item,
              ]);

              var data = await getDataPOST(
                'https://localhost:44342/api/YMA/AnalysisGroup',
                {
                'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
                'Model': stringEncryptedArray['data'][1],
                'Day': stringEncryptedArray['data'][2],
                'ModeDay': stringEncryptedArray['data'][3],
                'Process': stringEncryptedArray['data'][4]
                } 
              );
              String jsonEncrypted = jsonDecode(jsonDecode(data[0]))['encryptedJson'];

              final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
              final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

              String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
              List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
              
              setState(() {
                storeDecodedData = decodedData;
              });
              dataSorting(decodedData, item);
            },
          ),    
        ));
      }
    }
    return subListProcessForBarChart;
  }

  Future<void> dataSorting(List<Map<String, dynamic>> data, String process) async {
    setState(() {
      processSelected = process;
      for (var i in data) {
        stepName.add(i['STEP NAME']);
      }
      stepName = stepName.toSet().toList();
    });
  } 
  List<Widget> _buildListStepName(List<String> stepName) {
    List<Widget> subListStepName = [];
    for (String item in stepName) {
      subListStepName.add(Container(
        padding: const EdgeInsets.all(7),
        child: ElevatedButton(
          onPressed: () async {
            itemsSpec = [];
            for (var i in storeDecodedData) {
              if (i['STEP NAME'] == item) {
                itemsSpec.add('${i['MODE'].toString()} | LSL : ${i['LSL'].toString()} | USL : ${i['USL'].toString()}');
              }
            }
            setState(() {
              isLoading = true;
              defaultSpec = itemsSpec[0];
              stepNameSelected = item;
              dataBarChartHistogramArr = []; 
              randomDataHistogramArr = [];
              binArr = [];
              maxXRangeArr = [];
              minXRangeArr = [];
              maxYRangeArr = [];
              fetchDataHistogram(defaultSpec, stepNameSelected);
            });         
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color.fromARGB(255, 255, 255, 255),
            side: const BorderSide(color: Colors.green, width: 2),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(0),
            ),
          ),
          child: Row(
            children: [
              const Icon(
                Icons.poll_outlined,
                color: Colors.black,
                size: 15,
              ),
              const SizedBox(width: 5),
              Text(
                item,
                style: const TextStyle(
                  color: Colors.black,
                  fontSize: 12,
                ),
              ),
            ],
          ),
        ),
      ));
    }   
    return subListStepName;
  }

  Future<void> fetchDataHistogram(String parameter, String stepName) async {
    if (parameter.isNotEmpty && stepName.isNotEmpty) {    
      stringEncryptedArray = await encryptData([
        widget.levelSelected,
        widget.modelSelected,
        widget.daySelected,
        widget.modeDay,
        processSelected,
        stepName,
        parameter.split('|')[1].split(' ')[3],
        parameter.split('|')[2].split(' ')[3],
        parameter.split('|')[0].split(' ')[0]
      ]);

      var data = await getDataPOST(
        'https://localhost:44342/api/YMA/HistogramData',
        {
        'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
        'Model': stringEncryptedArray['data'][1],
        'Day': stringEncryptedArray['data'][2],
        'ModeDay': stringEncryptedArray['data'][3],
        'Process': stringEncryptedArray['data'][4],
        'StepName': stringEncryptedArray['data'][5],
        'Lsl': stringEncryptedArray['data'][6],
        'Usl': stringEncryptedArray['data'][7],
        'Mode': stringEncryptedArray['data'][8]
        } 
      );
      String jsonEncrypted = jsonDecode(jsonDecode(data[0]))['encryptedJson'];

      final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
      final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

      String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
      decodedDataHistogram = List<Map<String, dynamic>>.from(json.decode(decryptJson));
      
      stepNameSelectedToVoid = stepName;
      fetchRawDataHistogram(parameter, stepName);
    }
  }

  Future<void> fetchRawDataHistogram (String parameter, String stepName) async {
    if (parameter.isNotEmpty && stepName.isNotEmpty) {
      stringEncryptedArray = await encryptData([
        widget.levelSelected,
        widget.modelSelected,
        widget.daySelected,
        widget.modeDay,
        processSelected,
        stepName,
        parameter.split('|')[1].split(' ')[3],
        parameter.split('|')[2].split(' ')[3],
        parameter.split('|')[0].split(' ')[0]
      ]);

      dataBoxPlot = {};
      var data = await getDataPOST(
        'https://localhost:44342/api/YMA/HistogramRawData',
        {
        'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
        'Model': stringEncryptedArray['data'][1],
        'Day': stringEncryptedArray['data'][2],
        'ModeDay': stringEncryptedArray['data'][3],
        'Process': stringEncryptedArray['data'][4],
        'StepName': stringEncryptedArray['data'][5],
        'Lsl': stringEncryptedArray['data'][6],
        'Usl': stringEncryptedArray['data'][7],
        'Mode': stringEncryptedArray['data'][8]
        }  
      );
      String jsonEncrypted = jsonDecode(jsonDecode(data[0]))['encryptedJson'];

      final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
      final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

      String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
      decodedDataHistogramRawData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

      Map<String, dynamic> deictForDataBoxPlot = {};
      for (var i in decodedDataHistogramRawData) {
        if (!deictForDataBoxPlot.containsKey(i['GROUP'])) {
          deictForDataBoxPlot[i['GROUP']] = [];
        }
        deictForDataBoxPlot[i['GROUP']].add(i['DATA']);
      }
      dataBoxPlot = deictForDataBoxPlot;
      isLoading = false;
      sortDataHistogram();
    }
  }

  Future<void> sortDataHistogram() async {
    setState(() {
      
      dataBarChartHistogramArr = []; 
      dataTableHistogramArr = []; 
      randomDataHistogramArr = [];
      binArr = [];
      maxXRangeArr = [];
      minXRangeArr = [];
      maxYRangeArr = [];
      dataBoxPlotArr = [];
      minYRangeBox = 0;

      if (decodedDataHistogram.isNotEmpty) {
        minYRangeBox = decodedDataHistogram[0]['MIN'];
        maxYRangeBox = decodedDataHistogram[0]['MAX'];
        histogramTitle = stepNameSelectedToVoid;
        dateArray = [];
        for (var element in decodedDataHistogram) {
          if (element['GROUP'].isNotEmpty) { 
            dateArray.add(element['GROUP']);
          }
        }
        
        for (var dt in dateArray) {
          Map<String, List<int>> histogramGroupDate = {};
          Map<String, List<String>> tableHistogramGroupDate = {};
          for (var i in decodedDataHistogram) {
            if (i['GROUP'] == dt) {
              tableHistogramGroupDate[i['GROUP']] = [
                'N : ${i['N'].toString()}',
                'MAX : ${i['MAX'].toStringAsFixed(2)}',
                'Q3 : ${i['Q3'].toStringAsFixed(2)}',
                'MEAN : ${i['MEAN'].toStringAsFixed(2)}',
                'MEDIAN : ${i['MEDIAN'].toStringAsFixed(2)}',
                'Q1 : ${i['Q1'].toStringAsFixed(2)}',
                'MIN : ${i['MIN'].toStringAsFixed(2)}',
                'STDEV : ${i['STDEV'].toStringAsFixed(2)}',
                'VARIANCE : ${i['VARIANCE'].toStringAsFixed(2)}'
              ];
              histogramGroupDate[i['GROUP']] = [
                i['F1'],
                i['F2'],
                i['F3'],
                i['F4'],
                i['F5'],
                i['F6'],
                i['F7'],
                i['F8'],
                i['F9'],
                i['F10'],
                i['F11'],
                i['F12'],
                i['F13'],
                i['F14'],
                i['F15'],
                i['F16'],
                i['F17']
              ];
            }
          }

          dataBarChartHistogram = histogramGroupDate[dt] ?? [];
          bin = double.parse((decodedDataHistogram[0]['RANGE'] / decodedDataHistogram[0]['BINS']).toString());
          double min = 0;
          minXRange = 0;
          for (var i in decodedDataHistogram) {
            if (i['GROUP'] == dt) {
              min = i['MIN'];
              minXRange = i['MIN'];
            }
          }

          List<double> binGroup = [];
          for (var j = 0; j < 19; j++) {
            binGroup.add(min);
            min = min + bin;
          }

          List<double> randomNumber = [];
          // Amount of each bar
          for (int j = 0; j < dataBarChartHistogram.length; j++) {
            if (dataBarChartHistogram[j] > 0) {
              // run random number per amount of bar
              for (int i = 0; i < dataBarChartHistogram[j]; i++) {
                randomNumber.add((binGroup[j] + binGroup[j + 1]) / 2);
              }
            }
          }
          // randomDataHistogram = randomNumber;
          randomDataHistogram = [];
          for (var i in dataBoxPlot[dt]) {
            randomDataHistogram.add((i));
          }

          maxXRange = binGroup.isNotEmpty ? binGroup.reduce((value, element) => max(value, element)) : 0.0;
          maxYRange = (dataBarChartHistogram.isNotEmpty? dataBarChartHistogram.reduce((value, element) => max(value, element)) + 1 : 0.0).toDouble();
          if (minXRange == 0.0 && maxXRange == 0.0 && maxYRange == 0.0) {
            minXRange = null;
            maxXRange = null;
            maxYRange = null;
          }

          Map<String, dynamic> boxDict = {};
          boxDict[dt] = dataBoxPlot[dt];
          
          dataBarChartHistogramArr.add(dataBarChartHistogram);
          dataTableHistogramArr.add(tableHistogramGroupDate);
          randomDataHistogramArr.add(randomDataHistogram);
          binArr.add(bin);
          minXRangeArr.add(minXRange);
          maxXRangeArr.add(maxXRange);
          maxYRangeArr.add(maxYRange);
          dataBoxPlotArr.add(boxDict);
        }
   
        maxYRangeNew = maxYRangeArr.isNotEmpty
          ? maxYRangeArr.fold<double>(
              double.negativeInfinity,
              (maxValue, element) => element != null ? max(maxValue, element) : maxValue,
            )
          : double.nan;
      }
      else {
        dataBarChartHistogram = [];
      }
      
    });
      
  }

  List<Widget> _createHistogramChart(
    List<List<double>> randomDataHistogramArr,
    List<double> binArr,
    List<double?> maxXRangeArr,
    List<double?> minXRangeArr,
    List<double?> maxYRangeArr,
    List<Map<String, dynamic>> dataBoxPlotArr,
    double? minYRangeBox
  ) 
  {
    List<Widget> subHistogramChart = [];
    
    for (var i = 0; i < randomDataHistogramArr.length; i++) {
      subHistogramChart.add(Column(
        children: [
          // Histogram Plot =======================================
          SizedBox(
            height: 200,
            width: 200,
            child: MyBarChartHistogram(
              randomDataHistogram: randomDataHistogramArr[i],
              bin: binArr[i],
              maxXRange: maxXRangeArr[i],
              minXRange: minXRangeArr[i],
              maxYRange: maxYRangeNew,
            ),
          ),
          // Box Plot =======================================
          SizedBox(
            height: 300,
            width: 200,
            child: MyBarChartBox(
              dataBoxPlot: dataBoxPlotArr[i],
              minYRange: minYRangeBox,
              maxYRange: maxYRangeBox
            ),
          ),
          // Table =======================================
          Container(
            width: 125,
            margin: const EdgeInsets.only(left: 0),
            child: dataTableHistogramArr.isNotEmpty
                ? TableHistogram(
                    tableData: dataTableHistogramArr[i],
                  )
                : const SizedBox()
          )
        ]
      ));
    }
    return subHistogramChart;
  }

  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! [Encrypt] Data !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Future<Map<String, dynamic>> encryptData(List<dynamic> data) async {
    String keyValue = 'yieldeachproduct'; // *** important, same as flutter sent ***
    var iv = encrypt.IV.fromLength(16);

    final keyBytesTest = encrypt.Key.fromUtf8(keyValue);
    final encrypterTest = encrypt.Encrypter(encrypt.AES(keyBytesTest, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));
    
    List<dynamic> encryptedData = [];
    for (var value in data) {
      encryptedData.add(encrypterTest.encrypt(value, iv: iv));
    }

    List<String> stringEncryptedData = [];
    for (var value in encryptedData) {
      stringEncryptedData.add(base64Encode(value.bytes));
    }

    return {
      'key' : keyValue,
      'iv' : iv,
      'data' : stringEncryptedData
    };
  }
}

Future<dynamic> getDataPOST(String url, Map<String, String> body) async {
  http.Response response = await http.post(
    Uri.parse(url),
    body: body,
  );
  if (response.statusCode == 200) {
    return [response.body, response.statusCode];
  }
  else {
    return [response.body, response.statusCode];
  }
}