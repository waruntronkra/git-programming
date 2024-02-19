import 'package:flutter/material.dart';
import 'dart:convert';
// ignore: depend_on_referenced_packages
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
// import 'table_yield.dart';
import 'widget_DATE.dart';
import 'widget_CHART.dart';
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:motion_tab_bar_v2/motion-tab-bar.dart';
import 'package:motion_tab_bar_v2/motion-tab-controller.dart';
import 'tab_pareto.dart';
import 'barChartPARETO.dart';
import 'barChartPARETObyDATE.dart';
import 'page_analysis.dart';
import 'window_FBN_YIELD.dart';

class SecondPage extends StatefulWidget {
  static final activePage = GlobalKey<_SecondPageState>();
  const SecondPage({Key? key}) : super(key: key);

  @override
  State<SecondPage> createState() => _SecondPageState();
}

class _SecondPageState extends State<SecondPage> with SingleTickerProviderStateMixin{
  String selectedOption = '';
  var tableProductName = [];

  double _startValue = 0;
  double _endValue = 0;
  String fromDATE = '';
  String toDATE = '';

  Map<String, dynamic> sortedJsonYield = {};

  Map<String, dynamic> dataLevelObject = {};
  List<String> dataModelArr = [];
  List<String> dataProcessArr = [];
  List<String> dataColArr = [];

  String levelSelected = '';
  String modelSelected = '';
  String daySelected = '';

  String modeDay = '';
  
  dynamic dataColumnName;
  List<String> sortedDates = [];

  List<List<String>> tableData = [];
  List<String> colMetrixTable = [];
  List<String> rowMetrixTable = [];

  bool isChecked = false;

  Map<String, dynamic> dataLineChart = {};
  Map<String, dynamic> dataQtyLineChart = {};
  List<String> xAxis = [];
  Map<String, List<double?>> dataForLineChart = {};
  Map<String, List<int?>> dataForQtyLineChart = {};
  List<String> arrProcessForMixChart = [];

  List<List<dynamic>> dataBarChart = [];
  List<double> dataLineChartMix = [];
  bool mixChartVisible = false;
  bool isLoadingLineChart = false;
  String buttonProcessClicked = '';

  List<String> failuresPareto = [];
  List<Map<String, dynamic>> decodedDataPareto = [];
  List<List<dynamic>> mergedDataPareto = [];
  Map<String, List<List<String>>> dataPareto = {};
  String dataParetoCallBack = '';
  String paretoTitle = '';
  bool paretoChartVisible = false;

  List<List<dynamic>> dataBarChartByDate = [];
  bool paretoByDateChartVisible = false;
  bool sliderVisible = false;
  bool swithTopFive = false;
  String paretoByDateTitle = '';

  bool switchToPageATS = false;
  bool switchToPageFBN = false;

  Map<String, dynamic> stringEncryptedArray = {};
  
  late MotionTabBarController _tabController;
  int currentTabIndex = 0;
  @override
  void initState() {
    super.initState();
    fetchDataLevel(); 
    _tabController = MotionTabBarController(length: 4, vsync: this); // Create for click to switch page
  }
  @override 
  void dispose() { 
    _tabController.dispose(); 
    super.dispose(); 
  }
 
  String textText = '';
  void updatePareto(String value) { 
    if (value.isNotEmpty) {
      setState(() {
        dataParetoCallBack = value; // process
      });
    }
  }

  // Main Second Page
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        appBar: AppBar(
          title: Text(
            "$levelSelected : $modelSelected ($daySelected)",
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold
            ),
          ),
          actions:  <Widget> [
            IconButton(
              icon: const Icon(Icons.swap_horizontal_circle_rounded),
              onPressed: () => showDialog<String>(
                context: context,
                builder: (BuildContext context) => Dialog(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text('Choose YIELD Showing'),
                        const SizedBox(height: 15),
                        Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(5),
                            boxShadow: const [
                              BoxShadow(
                                color: Colors.grey,
                                offset: Offset(2, 2),
                                blurRadius: 4
                              )
                            ],
                            border: Border.all(color: Colors.black),
                          ),
                          width: 190,
                          child: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color.fromARGB(255, 3, 141, 93),
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(5)
                              )
                            ),
                            onPressed: () {
                              setState(() {
                                switchToPageATS = false;
                                switchToPageFBN = true;
                              });
                              Navigator.pop(context);
                            },
                            child: const Text("[ATS] Yield Summary"),
                          ),
                        ),
                        Container(
                          margin: const EdgeInsets.only(top: 10),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(5),
                            boxShadow: const [
                              BoxShadow(
                                color: Colors.grey,
                                offset: Offset(2, 2),
                                blurRadius: 4
                              )
                            ],
                            border: Border.all(color: Colors.black),
                          ),
                          width: 190,
                          child: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color.fromARGB(255, 3, 141, 93),
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(5)
                              )
                            ),
                            onPressed: () {
                              setState(() {
                                switchToPageATS = true;
                                switchToPageFBN = false;
                              });
                              Navigator.pop(context);
                            },
                            child: const Text("[FBN] Yield Summary"),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              )
            )
          ],
        ),
        bottomNavigationBar: MotionTabBar(
          controller: _tabController,
          initialSelectedTab: "SUMMARY",
          useSafeArea: true,
          labels: const ["SUMMARY", "ANALYSIS", "RAW DATA", "TRANSACTION"],
          icons: const [Icons.dashboard, Icons.analytics, Icons.list, Icons.data_array],
          tabSize: 50,
          tabBarHeight: 53,
          tabBarColor: const Color.fromARGB(255, 3, 141, 93),
          textStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
          onTabItemSelected: (int value) {
            setState(() {
              _tabController.index = value;
            });
          },
        ),
        drawer: Drawer(
          child: ListView(
            padding: EdgeInsets.zero,
            children: [
              Container(
                color: const Color.fromARGB(255, 3, 141, 93),
                height: 85,
                child: const DrawerHeader(
                  child: Text(
                    'PRODUCT',
                    style: TextStyle(
                      color: Color.fromARGB(255, 0, 0, 0),
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
              ..._buildSubListLevel(dataLevelObject),
            ],
          ),
        ),
        body: TabBarView(
          controller: _tabController,
          children: [
            switchToPageATS == false ? _buildTabSummary() 
            : WindowFBNYIELD(
              modelSelected: modelSelected,
              levelSelected: levelSelected,
            ),
            _buildTabAnalysis(),
            _buildTabRawData('RAW DATA'),
            _buildTabTransaction('TRANSACTION')
          ],
        ),
      )
    );
  }

  final MaterialStateProperty<Icon?> thumbIcon =
      MaterialStateProperty.resolveWith<Icon?>(
    (Set<MaterialState> states) {
      if (states.contains(MaterialState.selected)) {
        return const Icon(Icons.check);
      }
      return const Icon(Icons.close);
    },
  );

  // +++++++++++++++++++++++++++++++++++++++ This is Tab [SUMMARY] +++++++++++++++++++++++++++++++++++++++
  Widget _buildTabSummary() {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
          appBar: PreferredSize(
            preferredSize: const Size.fromHeight(50),
            child: AppBar(
            automaticallyImplyLeading: false,
            bottom: const TabBar(
              labelColor: Color.fromARGB(255, 3, 141, 93),
              indicatorColor: Color.fromARGB(255, 3, 141, 93),
              tabs: <Widget>[
                Tab(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.widgets),
                      Text('  CHART')
                    ],
                  )
                ),
                Tab(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.bar_chart_rounded),
                      Text('  PARETO')
                    ],
                  )
                )
              ],
              labelStyle: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold
              ),
            )
          )
        ),
        body: Column(
          children: [
            // DATE dropdown =================================
            SizedBox(
              width: MediaQuery.of(context).size.width * 0.97,
              height: 55,
              child: WidgetDate(
                fetchData: fetchYIELD,
                levelSelected: levelSelected,
                modelSelected: modelSelected,
              ),
            ),
            Expanded(
              child: TabBarView(
                children: <Widget>[
                  // Line and Mix chart =================================
                  WidgetChart(
                    dataLineChart: dataLineChart,
                    dataQtyLineChart: dataQtyLineChart,
                    xAxis: xAxis,
                    arrProcessForMixChart: arrProcessForMixChart,
                    sortedJsonYield: sortedJsonYield,
                    dataLineChartMix: dataLineChartMix,
                    dataBarChart: dataBarChart,
                    mixChartVisible: mixChartVisible,
                    updateChart: updateMixChart,
                    processSelected: buttonProcessClicked,
                    isLoadingLineChart: isLoadingLineChart,
                  ),
                  // Pareto List =================================
                  SingleChildScrollView(
                    child: Stack(
                      children: [
                        // Pareto List =================================
                        PagePareto(
                          levelSelected: levelSelected,
                          modelSelected: modelSelected,
                          daySelected: daySelected,
                          failures: failuresPareto,
                          plotPareto: plotPareto,
                        ),
                        // Pareto Chart =================================
                        Visibility(
                          visible: paretoChartVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 150),
                            height: 300,
                            child: MyBarChartPareto(
                              dataBarChart: mergedDataPareto,
                              paretoTitle: paretoTitle,
                            )
                          )
                        ),
                        // QTY label =================================
                        Visibility(
                          visible: paretoChartVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 450, left: 10),
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
                        // % FAIL label =================================
                        Visibility(
                          visible: paretoChartVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 450),
                            width: MediaQuery.of(context).size.width * 1,
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
                        // Slider =================================
                        Visibility(
                          visible: sliderVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 480),
                            child: RangeSlider(
                              values: RangeValues(_startValue, _endValue),
                              min: 0,
                              max: sortedDates.isNotEmpty ? sortedDates.length.toDouble() - 1 : 1,
                              activeColor: const Color.fromARGB(255, 3, 141, 93),
                              onChanged: (RangeValues values) {
                                setState(() {
                                  paretoByDateChartVisible = true;
                                  _startValue = values.start;
                                  _endValue = values.end;
                                  plotParetoByDATE(_startValue.toInt(), _endValue.toInt());
                                  fromDATE = sortedDates.isNotEmpty ? sortedDates.reversed.toList()[_startValue.toInt()] : '';
                                  toDATE = sortedDates.isNotEmpty ? sortedDates.reversed.toList()[_endValue.toInt()] : '';
                                });
                              },                       
                            )
                          )
                        ),
                        // From : label =================================
                        Visibility(
                          visible: sliderVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 520, left: 10),
                            child: Text('From : $fromDATE'),
                          )
                        ),
                        // To : label =================================
                        Visibility(
                          visible: sliderVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 520),
                            alignment: Alignment.topRight,
                            width: MediaQuery.of(context).size.width * 0.98,
                            child: Text('To : $toDATE'),
                          )
                        ),
                        // Chart by DATE =================================
                        Visibility(
                          visible: paretoByDateChartVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 580),
                            height: 500,
                            child: MyBarChartParetoByDate(
                              dataBarChart: dataBarChartByDate,
                              paretoTitle: paretoByDateTitle,
                            )
                          )
                        ),
                        // Switch Top 5 =================================
                        Visibility(
                          visible: sliderVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 545, left: 10),
                            alignment: Alignment.topLeft,
                            child: Switch(
                              thumbIcon: thumbIcon,
                              value: swithTopFive,
                              activeColor: const Color.fromARGB(255, 3, 141, 93),
                              onChanged: (bool value) {
                                setState(() {
                                  swithTopFive = value;
                                  if (swithTopFive == true) {
                                    if (dataBarChartByDate.length >= 5) {
                                      dataBarChartByDate = dataBarChartByDate.sublist(0, 5);
                                    }
                                  }
                                  else {
                                    plotParetoByDATE(_startValue.toInt(), _endValue.toInt());
                                  }
                                });
                              },
                            ),
                          )
                        ),
                        // Top 5 Label =================================
                        Visibility(
                          visible: sliderVisible,
                          child: Container(
                            margin: const EdgeInsets.only(top: 561, left: 75),
                            child: const Text(
                              'Top 5',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: Color.fromARGB(255, 3, 141, 93)
                              ),
                            )
                          )
                        ),
                        // Empty area =================================
                        Container(
                          margin: const EdgeInsets.only(top: 1000),
                          width: MediaQuery.of(context).size.width * 0.97,
                          height: 50,
                        )
                      ]
                    )
                  )
                ]
              )
            )
          ]
        ),
      ),
    );
  }

  // ============== Function Query YIELD [Prepare data for Line Chart] ==============
  Future<void> fetchYIELD(String day) async {
    if (day.split(' ')[1] == 'Day' || day.split(' ')[1] == 'Days') {
      modeDay = 'DATE';
    }
    else if (day.split(' ')[1] == 'Week' || day.split(' ')[1] == 'Weeks') {
      modeDay = 'WEEK';
    }
    else if (day.split(' ')[1] == 'Month' || day.split(' ')[1] == 'Months') {
      modeDay = 'MONTH';
    }
    else if (day.split(' ')[1] == 'Quarter' || day.split(' ')[1] == 'Quarters') {
      modeDay = 'QUARTER';
    }

    setState(() {
      isLoadingLineChart = true;
      mixChartVisible = false;
      arrProcessForMixChart = [];
    });

    stringEncryptedArray = await encryptData([
      levelSelected,
      modelSelected,
      (int.parse(day.split(' ')[0])-1).toString(),
      modeDay.toString()
    ]);
    var dataYIELD = await getDataPOST(
                                  'https://localhost:44342/api/YMA/QueryYield',
                                  {
                                  'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
                                  'Model': stringEncryptedArray['data'][1],
                                  'Day': stringEncryptedArray['data'][2],
                                  'ModeDay': stringEncryptedArray['data'][3]
                                  } 
                                );
    String jsonEncrypted = jsonDecode(jsonDecode(dataYIELD[0]))['encryptedJson'];

    final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
    final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

    String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
    List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

    List<String> dtJSON = [];
    for (var item in decodedData) {
      dtJSON.add(item[modeDay]);
    }
    List<String> prJSON = [];
    for (var item in decodedData) {
      prJSON.add(item['Process']);
    }
    Set<String> uniqueDates = Set<String>.from(dtJSON);
    dtJSON = uniqueDates.toList();
    Set<String> uniquePr = Set<String>.from(prJSON);
    prJSON = uniquePr.toList();
    if (decodedData.isNotEmpty) {
      // ================================== Sort DATE ==================================
      sortedDates = [];
      if (modeDay == 'DATE') {
        String getMonthAbbreviation(int month) {
          final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
          return months[month - 1];
        }
        DateTime customParse(String dateString) {
          final months = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
          };
          final parts = dateString.split(' ');
          final day = int.parse(parts[0]);
          final month = months[parts[1]]!;
          final year = int.parse(parts[2]);

          return DateTime(year, month, day);
        }

        List<DateTime> dateTimes = dtJSON.map(customParse).toList();
        dateTimes.sort((a, b) => b.compareTo(a));
        sortedDates = dateTimes.map((dateTime) {
          final day = dateTime.day.toString().padLeft(2, '0');
          final month = getMonthAbbreviation(dateTime.month);
          final year = dateTime.year.toString();
          return '$day $month $year';
        }).toList();
      }
      // ================================== Sort WEEK ==================================
      if (modeDay == 'WEEK') {
        sortedDates = dtJSON.toList()..sort((a, b) {
          // Extract the week and year from the strings
          int weekA = int.parse(a.substring(3, a.indexOf(' ')));
          int yearA = int.parse(a.substring(a.lastIndexOf('\'') + 1));

          int weekB = int.parse(b.substring(3, b.indexOf(' ')));
          int yearB = int.parse(b.substring(b.lastIndexOf('\'') + 1));

          int yearComparison = yearB.compareTo(yearA);
          if (yearComparison != 0) {
            return yearComparison;
          }
          return weekB.compareTo(weekA);
        });
      }
      // ================================== Sort MONTH ==================================
      if (modeDay == 'MONTH') {
        List<String> sortDatesDescending(List<String> dateStrings) {
          List<DateTime> dates = dateStrings.map((dateString) {
            return DateFormat('MMM yyyy').parse(dateString);
          }).toList();

          dates.sort((a, b) => b.compareTo(a));

          List<String> sortedDates = dates.map((date) {
            return DateFormat('MMM yyyy').format(date);
          }).toList();

          return sortedDates;
        }
        sortedDates = sortDatesDescending(dtJSON);
      }
      // ================================== Sort QUARTER ==================================
      if (modeDay == 'QUARTER') {
        List<String> sortQuarterYearsDescending(List<String> quarterYears) {
          List<DateTime> dates = quarterYears.map((quarterYear) {
            int quarter = int.parse(quarterYear.substring(1, 2));
            int year = int.parse(quarterYear.substring(3));
            return DateTime(year, (quarter - 1) * 3 + 1);
          }).toList();

          dates.sort((a, b) => b.compareTo(a));

          List<String> sortedQuarterYears = dates.map((date) {
            int quarter = (date.month - 1) ~/ 3 + 1;
            int year = date.year;
            return 'Q$quarter-$year';
          }).toList();

          return sortedQuarterYears;
        }
        sortedDates = sortQuarterYearsDescending(dtJSON);
      }
      // ==================================================================================    
     
      // Group fro YIELD
      Map<String, dynamic> groupProcessFromJSON = {};
      for (var item in decodedData) {
        if (!groupProcessFromJSON.containsKey(item['Process'])) {
          groupProcessFromJSON[item['Process']] = [];
        }
        groupProcessFromJSON[item['Process']].add([
          item[modeDay],
          item['QTY'],
          item['FPY'],
          item['RTY'],
          item['IN'],
          item['Pass'],
          item['IN'] - item['OUT']
        ]);
      }
      
      Map<String, dynamic> groupProcessDTFromJSON = {};
      for (var entry in groupProcessFromJSON.entries) {
        String key = entry.key;
        List<dynamic> value = entry.value;

        Set<String> uniqueSet = {};
        List<List<dynamic>> resultList = [];

        for (var subList in value) {
          String subListString = subList.toString();
          if (uniqueSet.add(subListString)) {
            resultList.add(subList);
          }
        }
        value = resultList;
        List<String> subDT = [];
        for (var dt in value) {
          subDT.add(dt[0]);
        } 
        subDT = subDT.toSet().toList();
        
        for (var j in sortedDates) { 
          if (subDT.contains(j)) {
            if (!groupProcessDTFromJSON.containsKey(key)) {
              groupProcessDTFromJSON[key] = [];
            }
            groupProcessDTFromJSON[key].add(value[subDT.indexOf(j)]);
          }
          else {
            if (!groupProcessDTFromJSON.containsKey(key)) {
              groupProcessDTFromJSON[key] = [];
            }
            groupProcessDTFromJSON[key].add(['', '', '', '', '', '', '']);
          }
        }
      }
      sortedJsonYield = groupProcessDTFromJSON;
      colMetrixTable = sortedDates;
      rowMetrixTable = prJSON;

      setState(() {   
        paretoChartVisible = false;
        isLoadingLineChart = false;
        _startValue = 0;
        _endValue = (sortedDates.length).toDouble() - 1;
        fromDATE = sortedDates[sortedDates.length - 1];
        toDATE = sortedDates[0];

        mixChartVisible = false;
        daySelected = day;

        tableData = [];
        dataLineChart = {};
        dataQtyLineChart = {};
        xAxis = [];
        dataForLineChart = {};
        dataForQtyLineChart = {};
        dataPareto = {};

        arrProcessForMixChart = [];
        for (var entry in sortedJsonYield.entries) {
          var key = entry.key;
          var subArray = entry.value;
          for (var arr in subArray) {
            if (!dataForLineChart.containsKey(key)) {
              dataForLineChart[key] = [];
            }
            if (!dataForQtyLineChart.containsKey(key)) {
              dataForQtyLineChart[key] = [];
            }

            if (arr[2] != '') {
              dataForLineChart[key]?.add(arr[2]);
              dataForQtyLineChart[key]?.add(arr[1]);
            }
            else {
              dataForLineChart[key]?.add(null);
              dataForQtyLineChart[key]?.add(null);
            }
          }
          arrProcessForMixChart.add(key);
        }
        // ++++++++++++++++++++ Prepare data to Line ++++++++++++++++++++
        dataForLineChart.forEach((key, value) {
          dataLineChart[key] = value.reversed.toList();
        });
        dataForQtyLineChart.forEach((key, value) {
          dataQtyLineChart[key] = value.reversed.toList();
        });
        for (var val in colMetrixTable.reversed.toList()) {
          xAxis.add(val);
        } 
      });
      fetchPARETO(levelSelected, modelSelected, daySelected);
    }
    else {
      setState(() {
        isLoadingLineChart = false;
        sortedDates = [];
        arrProcessForMixChart = [];
        sortedJsonYield = {};
        dataLineChart = {};
        _startValue = 0;
        _endValue = 1;
        fromDATE = '';
        toDATE = '';
      });
    }
  }

  // ============== Function Query PARETO ==============
  Future<void> fetchPARETO(String level, String model, String day) async {
    if (level.isNotEmpty && model.isNotEmpty && day.isNotEmpty) {
      stringEncryptedArray = await encryptData([
        level,
        model,
        (int.parse(day.split(' ')[0])-1).toString(),
        modeDay.toString()
      ]);
      var dataPARETO = await getDataPOST(
                                    'https://localhost:44342/api/YMA/QueryPareto',
                                    {
                                    'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
                                    'Model': stringEncryptedArray['data'][1],
                                    'Day': stringEncryptedArray['data'][2],
                                    'ModeDay': stringEncryptedArray['data'][3]
                                    } 
                                  );

      String jsonEncrypted = jsonDecode(jsonDecode(dataPARETO[0]))['encryptedJson'];

      dynamic keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
      dynamic encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

      String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
      List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
      
      if (decodedData.isNotEmpty) {
        setState(() {
          failuresPareto = [];
          decodedDataPareto = [];
          for (var i in decodedData) {
            failuresPareto.add(i['Result']);
          }
          failuresPareto = failuresPareto.toSet().toList();
          if (failuresPareto.isNotEmpty) {
            failuresPareto.removeAt(0);
            if (failuresPareto.isEmpty) {
              paretoChartVisible = false;
              paretoByDateChartVisible = false;
              sliderVisible = false;
              mergedDataPareto = [];
            }
            else {
              sliderVisible = true;
            }
          }
          else {
            paretoChartVisible = false;
            paretoByDateChartVisible = false;
            mergedDataPareto = [];
          }
          decodedDataPareto = decodedData;
        });
      }
    }
  }

  // ========================================== Plot Pareto Chart ==========================================
  Future<void> plotPareto(String failureSelected) async {
    setState(() {
      paretoTitle = failureSelected;
      paretoChartVisible = true;
      List<dynamic> groupParetoPASS = [];
      for (var i in decodedDataPareto) {
        if (i['Result'] == 'PASS') {
          groupParetoPASS.add(i);
        }
      }
      List<dynamic> groupParetoFAIL = [];
      for (var i in decodedDataPareto) {
        if (i['Result'] != 'PASS') {
          groupParetoFAIL.add(i);
        }
      }

      Map<String, dynamic> dictGroupParetoPASS = {};
      for (var i in sortedDates) {
        if (!dictGroupParetoPASS.containsKey(i)) {
          dictGroupParetoPASS[i] = [];
        }
        for (var val in groupParetoPASS) {
          if (val[modeDay] == i && val['Result'] == 'PASS') {
            dictGroupParetoPASS[i].add(val['QTY']);
          }
          else if (val[modeDay] != i && val['Result'] == 'PASS') {
            dictGroupParetoPASS[i].add(0);
          }
        }
      }
      Map<String, dynamic> dictGroupParetoFAIL = {};
      for (var i in sortedDates) {
        if (!dictGroupParetoFAIL.containsKey(i)) {
          dictGroupParetoFAIL[i] = [];
        }
        for (var val in groupParetoFAIL) {
          if (val[modeDay] == i && val['Result'] == failureSelected) {
            dictGroupParetoFAIL[i].add(val['QTY']);
          }
          else if (val[modeDay] != i && val['Result'] == failureSelected) {
            dictGroupParetoFAIL[i].add(0);
          }
        }
      }

      Map<String, int> sumParetoPASS = {};
      dictGroupParetoPASS.forEach((key, value) {
        if (value.isNotEmpty) {
          int sum = value.reduce((a, b) => a + b);
          sumParetoPASS[key] = sum;
        } else {
          sumParetoPASS[key] = 0;
        }
      });
      Map<String, int> sumParetoFAIL = {};
      dictGroupParetoFAIL.forEach((key, value) {
        int sum = value.reduce((a, b) => a + b);
        sumParetoFAIL[key] = sum;
      });

      Map<String, double> paretoPercentFail = {};
      sumParetoFAIL.forEach((key, value) {
        if (sumParetoPASS.containsKey(key) && sumParetoPASS[key] != 0) {
          double divisionResult = (value / sumParetoPASS[key]!) * 100;
          paretoPercentFail[key] = double.parse(divisionResult.toStringAsFixed(2));
        } 
        else {
          if (value > 0) {
            paretoPercentFail[key] = 100;
          }
          else {
            paretoPercentFail[key] = 0;
          }
        }
      });

      mergedDataPareto = [];
      sumParetoPASS.forEach((key, value1) {
        if (sumParetoFAIL.containsKey(key) && paretoPercentFail.containsKey(key)) {
          mergedDataPareto.add([key, value1, sumParetoFAIL[key]!, paretoPercentFail[key]!]);
        }
      });
      mergedDataPareto = mergedDataPareto.reversed.toList();
    });
  }

  // +++++++++++++++++++++++++++++++ sort data for plot chart by DATE +++++++++++++++++++++++++++++++
  Future<void> plotParetoByDATE(int fromNum, int toNum) async { 
    List<String> dateSlider = sortedDates.reversed.toList().sublist(fromNum, toNum + 1);
    
    List<dynamic> groupParetoFAIL = [];
    for (var i in decodedDataPareto) {
      if (i['Result'] != 'PASS' && dateSlider.contains(i[modeDay])) {
        groupParetoFAIL.add(i);
      }
    }
    dataBarChartByDate = [];
    if (groupParetoFAIL.isNotEmpty) {
      paretoByDateTitle = '${dateSlider[0]} - ${dateSlider[dateSlider.length - 1]}' ;
      for (var val in groupParetoFAIL) {
          dataBarChartByDate.add([val['Result'], val['QTY']]);
      }
      paretoByDateChartVisible = true;
    }
    else {
      paretoByDateChartVisible = false;
    }
    
    Map<String, int> resultMap = {};
    for (var sublist in dataBarChartByDate) {
      String key = sublist[0];
      int value = sublist[1];
      resultMap.update(key, (existingValue) => existingValue + value, ifAbsent: () => value);
    }

    dataBarChartByDate = resultMap.entries.map((entry) => [entry.key, entry.value]).toList();
    dataBarChartByDate = dataBarChartByDate.toList()..sort((a, b) => b[1].compareTo(a[1]));

    if (swithTopFive == true) {
      if (dataBarChartByDate.length >= 5) {
        dataBarChartByDate = dataBarChartByDate.sublist(0, 5);
      }
    }
  }

  // ============== [Prepare data for Mix Chart] ==============
  Future<void> updateMixChart(String pr) async {
    setState(() {
      buttonProcessClicked = pr;
      dataBarChart = [];
      
      for (var entry in sortedJsonYield.entries) {

        if (entry.key == pr) {
          dataBarChart.add(entry.value);
        }
      }
      // Prepare data to Bar Chart
      List<List<dynamic>> dataBarChartSort = [];
      for (var i in dataBarChart[0]) {
        if (i[0] != '') {
          dataBarChartSort.add([i[0], int.parse(i[5].toString()), int.parse(i[6].toString())]);
        }
      }
      List<double> dataLineInBarChartSort = [];
      for (var i in dataBarChart[0]) {
        if (i[0] != '') {
          dataLineInBarChartSort.add(i[2]);
        }
      }
      dataLineChartMix = dataLineInBarChartSort.reversed.toList();
      dataBarChart = dataBarChartSort.reversed.toList();

      mixChartVisible = true;
    });
  }
  
  // oooooooooooooooooooooooooooooooooo This is Tab [ANALYSIS] oooooooooooooooooooooooooooooooooo
  Widget _buildTabAnalysis() {
    return PageAnalysis(
      processArr: arrProcessForMixChart,
      levelSelected: levelSelected,
      modelSelected: modelSelected,
      daySelected: daySelected == '' ? '1 Day' : (int.parse(daySelected.split(' ')[0])-1).toString(),
      modeDay: modeDay
    );
  }

  // oooooooooooooooooooooooooooooooooo This is Tab [RAW DATA] oooooooooooooooooooooooooooooooooo
  Widget _buildTabRawData(String tabTitle) {
    return SingleChildScrollView(
      child: Column(
        children: [
          Container(
            margin: const EdgeInsets.only(left: 36, top: 16),
            width: 90,
            height: 50,
            child: const Text('sadsd')
          )
        ],
      )
    );
  }

  // oooooooooooooooooooooooooooooooooo This is Tab [TRANSACTION] oooooooooooooooooooooooooooooooooo
  Widget _buildTabTransaction(String tabTitle) {
    return SingleChildScrollView(
      child: Column(
        children: [
          Container(
            margin: const EdgeInsets.only(left: 36, top: 16),
            width: 90,
            height: 50,
            child: const Text('wrfaqw')
          )
        ],
      )
    );
  }

  // ========================= Create drop list by [LEVEL] =========================
  Future<void> fetchDataLevel() async {
    String keyValue = 'yieldeachproduct'; // *** important, same as flutter sent ***
    var iv = encrypt.IV.fromLength(16);

    var productName = await getDataPOST(
      'https://localhost:44342/api/YMA/ProductName',
      {
        'Value' : iv.base16
      } 
    );
    String jsonEncrypted = jsonDecode(jsonDecode(productName[0]))['encryptedJson'];

    final keyBytes = encrypt.Key.fromUtf8(keyValue);
    final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

    String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: iv);
    List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

    List<String> levelNameSorted = [];
    for (var element in decodedData) {
      if (!levelNameSorted.contains(element['Level'])) {
        levelNameSorted.add(element['Level']);
      }
    }

    Map<String, dynamic> modelNameSorted = {};
    for (var element in decodedData) {
      if (!modelNameSorted.containsKey(element['Level'])) {
        modelNameSorted[element['Level']] = [];
      }
      modelNameSorted[element['Level']].add(element['Model']);
    }

    setState(() {
      dataLevelObject = modelNameSorted; // Send this value to List
      tableProductName = levelNameSorted;
    });
  }

  List<Widget> _buildSubListLevel(Map<String, dynamic> dataLevel) {
    List<Widget> subListsLevel = [];
    if (dataLevel.isNotEmpty) {
      // =============== Create sub menu Level ===============
      for (var dict in dataLevel.entries) {
        subListsLevel.add(
          ExpansionTile(
            backgroundColor: const Color.fromARGB(255, 196, 255, 204),
            onExpansionChanged: (bool isExpanded) async {
              if (isExpanded) {
                for (var itemData in tableProductName) {
                  if (itemData == dict.key) {
                    dataModelArr = List<String>.from(dict.value);
                  }
                }
                setState(() {
                  levelSelected = dict.key;
                });
                await fetchDataModel(dict.value.cast<String>());
              }
            },
            title: Row(
              children: [
                const Icon(Icons.data_object), // Replace 'your_icon_here' with the desired icon
                const SizedBox(width: 8), // Add some space between icon and text
                Text(dict.key),
              ],
            ),
            children: [..._buildSubListModel(dataModelArr)],
          ),
        );
      }
    }
    return subListsLevel;
  }

  // ========================= Create drop list by [MODEL] =========================
  Future<void> fetchDataModel(List<String> model) async {
    // Case array input
    setState(() {
      dataModelArr = model;
    });
  }
  List<Widget> _buildSubListModel(List<String>? dataModel) {
    List<Widget> subListsModel = [];
    // =============== Create sub menu Model ===============
    if (dataModel != null) {
      for (String item in dataModel) {
        subListsModel.add(
          ExpansionTile(
            backgroundColor:const Color.fromARGB(255, 151, 255, 250),
            onExpansionChanged: (bool isExpanded) async {
              if (isExpanded) {
                setState(() {
                  modelSelected = item;
                  mixChartVisible = false;
                  dataLineChart = {};
                  arrProcessForMixChart = [];
                  paretoChartVisible = false;
                  failuresPareto = [];
                });
              }
            },
            title: Row(
              children: [
                const Icon(Icons.list_alt),
                const SizedBox(width: 8),
                Text(item),
              ],
            ),
          ),
        );
      }
    }
    return subListsModel;
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

// ============================== API ==============================
// https://supply-api.fabrinet.co.th/api
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