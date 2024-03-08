// ignore_for_file: file_names
import 'package:flutter/material.dart';
// ignore: depend_on_referenced_packages
import 'package:intl/intl.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:flutter_sliding_up_panel/flutter_sliding_up_panel.dart';
import 'package:cool_alert/cool_alert.dart';
import 'package:YMs/MainWindow/Window-EP-YIELD/Pages-Summary/utility/multiLineChart.dart';
import 'package:YMs/MainWindow/Window-EP-YIELD/Pages-Summary/utility/table.dart';
import 'package:YMs/MainWindow/Window-EP-YIELD/Pages-Summary/utility/show_more_filter.dart';

class WindowEPYIELD extends StatefulWidget {
  const WindowEPYIELD({super.key});

  @override
  State<WindowEPYIELD> createState() => _WindowEPYIELDStateNew();
}

class _WindowEPYIELDStateNew extends State<WindowEPYIELD> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey = GlobalKey<RefreshIndicatorState>(); 

  late ScrollController scrollController;
  SlidingUpPanelController panelController = SlidingUpPanelController();

  late DateTime startDate;
  late DateTime endDate;

  List<String> dataModelArr = [];

  Map<String, dynamic> dataLineChart = {};
  List<String> xAxis = [];
  Map<String, dynamic> dataQtyLineChart = {};

  String fromDATE = '';
  String toDATE = '';

  String levelSelected = '';
  String modelSelected = '';
  
  String defaultGroupBy = '{No Grouping}';
  List<String> itemGroupBy = [
    '{No Grouping}',
    'Hour',
    'Shift',
    'Day',
    'Week',
    'Month',
    'Quarter',
    'Operation'
  ];

  String filterSelected = '';
  String oldFilterSelected = '';
  String defaultFilter = 'Build Type';
  List<String> itemFilter = [
    'Build Type',
    'Is Rework',
    'Equipment ID',
    'Operation',
    'Operation EN',
    'Part No',
    'Run Type',
    'Work Order',
    'PIC_WF',
    'Driver Lot',
    'TIA Lot'
  ];

  List<String> listFilterSelected = [];
  List<bool> isChecked = [];
  List<Color> isCheckedColor = [];
  List<String> isCheckedString = [];
  String stringFilterSelectedCode = ' .';
  
  List<Map<String, dynamic>> decodedData = [];
  List<Map<String, dynamic>> decodedDataProductName = [];
  List<String> listProductName = [];
  List<String> listProductModel = [];

  List<List<dynamic>> dictDecodedDataByDate = [];
  List<double> dictDecodedDataPercentByDate = [];
  List<List<dynamic>> dataTable = [];
  String titleMixChart = '';
  bool mixChartVisible = false;

  Map<String, dynamic> stringEncryptedArray = {};

  bool isLoading = false;
  bool expandMoreFilter = false;

  DateTime selectedDate = DateTime.now();
  Future<void> _selectDateFrom(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate,
      firstDate: DateTime(2000),
      lastDate: DateTime(2100),
      builder: (BuildContext context, Widget? child) {
      return Theme(
        data: ThemeData (
          colorScheme: const ColorScheme.light(
            primary: Colors.red, // Header background color
            onPrimary: Colors.white, // Header text color
            surface: Colors.white, // Dialog background color
            onSurface: Colors.black, // Dialog text color
          ),
        ),
        child: child!,
      );
    });
    if (picked != null && picked != selectedDate) {
      setState(() {
        selectedDate = picked;
        fromDATE = DateFormat('dd/MM/yyyy HH:mm').format(selectedDate);
      });
    }
  }

  Future<void> _selectDateTo(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate,
      firstDate: DateTime(2000),
      lastDate: DateTime(2100),
      builder: (BuildContext context, Widget? child) {
      return Theme(
        data: ThemeData (
          colorScheme: const ColorScheme.light(
            primary: Colors.red, // Header background color
            onPrimary: Colors.white, // Header text color
            surface: Colors.white, // Dialog background color
            onSurface: Colors.black, // Dialog text color
          ),
        ),
        child: child!,
      );
    });
    if (picked != null && picked != selectedDate) {
      setState(() {
        selectedDate = picked;
        toDATE = DateFormat('dd/MM/yyyy HH:mm').format(selectedDate);
      });
    }
  }

  @override
  void initState() {
    scrollController = ScrollController();
    scrollController.addListener(() {
      if (scrollController.offset >=
              scrollController.position.maxScrollExtent &&
          !scrollController.position.outOfRange) {
        panelController.expand();
      } else if (scrollController.offset <=
              scrollController.position.minScrollExtent &&
          !scrollController.position.outOfRange) {
        panelController.anchor();
      } else {}
    });
    updateDateRangeForToday();
    fetchDataLevel();

    super.initState();
  }

  // Clear memory
  @override 
  void dispose() { 
    super.dispose(); 
  }

  // DATE for [THIS]
  void updateDateRangeForToday() {
    DateTime now = DateTime.now();
    startDate = DateTime(now.year, now.month, now.day, 0, 0);
    endDate = DateTime(now.year, now.month, now.day + 1, 0, 0);
  }
  void updateDateRangeForThisWeek() {
    DateTime now = DateTime.now();
    DateTime sunday = now.subtract(Duration(days: now.weekday));
    startDate = DateTime(sunday.year, sunday.month, sunday.day, 0, 0);
    endDate = DateTime(sunday.year, sunday.month, sunday.day + 7, 0, 0);
  }
  void updateDateRangeForThisMonth() {
    DateTime now = DateTime.now();
    startDate = DateTime(now.year, now.month, 1, 0, 0);
    endDate = DateTime(now.year, now.month + 1, 1, 0, 0);
  }
  void updateDateRangeForThisQuarter() {
    DateTime now = DateTime.now();
    int currentQuarter = ((now.month) / 3).ceil();
    startDate = DateTime(now.year, (currentQuarter - 1) * 3 + 1, 1, 0, 0);
    endDate = DateTime(now.year, currentQuarter * 4, DateTime(now.year, currentQuarter * 3, 1).day, 0, 0);
  }

  // DATE for [LAST]
  void updateDateRangeForYesterday() {
    DateTime now = DateTime.now();
    DateTime yesterday = now.subtract(const Duration(days: 1));
    startDate = DateTime(yesterday.year, yesterday.month, yesterday.day, 0, 0);
    endDate = DateTime(now.year, now.month, now.day, 0, 0);
  }
  void updateDateRangeForLastWeek() {
    DateTime now = DateTime.now();
    DateTime lastSunday = now.subtract(Duration(days: now.weekday + 6));
    DateTime lastSaturday = lastSunday.add(const Duration(days: 6));
    startDate = DateTime(lastSunday.year, lastSunday.month, lastSunday.day - 1, 0, 0);
    endDate = DateTime(lastSaturday.year, lastSaturday.month, lastSaturday.day, 0, 0);
  }
  void updateDateRangeForLastMonth() {
    DateTime now = DateTime.now();
    DateTime firstDayOfLastMonth = DateTime(now.year, now.month - 1, 1, 0, 0);
    DateTime lastDayOfLastMonth = DateTime(now.year, now.month, 1, 0, 0);
    startDate = firstDayOfLastMonth;
    endDate = lastDayOfLastMonth;
  }
  void updateDateRangeForLastQuarter() {
    DateTime now = DateTime.now();
    int currentQuarter = ((now.month - 1) / 3).ceil();
    int lastQuarter = currentQuarter - 1 <= 0 ? 4 : currentQuarter - 1;
    startDate = DateTime(now.year - 1, (lastQuarter - 1) * 3 + 1, 1, 0, 0);
    endDate = DateTime(now.year - 1, lastQuarter * 3 + 1, 1, 0, 0);
  }

  void setDateRange() {
    fromDATE = DateFormat('dd/MM/yyyy HH:mm').format(startDate);
    toDATE = DateFormat('dd/MM/yyyy HH:mm').format(endDate);
  }
  
  bool checkBox = false;

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Stack(
        children: [
          Scaffold(
            key: scaffoldKey,
            appBar: PreferredSize(
              preferredSize: const Size.fromHeight(100),
              child: AppBar(
                title: Text(
                  "$levelSelected : $modelSelected",
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold
                  ),
                ),
                bottom: const TabBar(
                  labelColor: Colors.red,
                  indicatorColor: Colors.red,
                  tabs: <Widget>[
                    Tab(
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.data_thresholding_outlined),
                          Text('  OVERALL')
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
                ),         
              ),
            ),
            endDrawer: Drawer(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  const UserAccountsDrawerHeader(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topRight,
                        end: Alignment.bottomLeft,
                        colors: [
                          Colors.red,
                          Color.fromARGB(255, 255, 119, 119)
                        ]
                      )
                    ),
                    accountName: Text(''),
                    accountEmail: Text(
                      'waruntronk.fabrinet.co.th',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Color.fromARGB(255, 255, 255, 255),
                        fontSize: 15
                      ),
                    ),
                    currentAccountPicture: CircleAvatar(
                      backgroundImage: NetworkImage(
                        "https://fits/emp_pic/511997.jpg"
                      ),
                    ),
                    currentAccountPictureSize: Size(100, 100),
                  ),
                  ..._buildSubListLevel(listProductName),
                ],
              ),
            ),
            body: RefreshIndicator(
              key: _refreshIndicatorKey,
              displacement: 60,
              color: Colors.white,
              backgroundColor: Colors.red,
              onRefresh: () async {
                await queryDataForMixChart('Yield');
              },
              child: Column(
                children: [
                  Container(
                    child: fixAllPage()
                  ),
                  Expanded(
                    child: TabBarView(
                      children: <Widget>[
                        _pageAverall(),
                        const Text('PARETO'),
                      ]
                    )
                  )
                ]
              ),
            )
          ),
          // SlidingUpPanelWidget(
          //   panelController: panelController,
          //   controlHeight: 50.0,
          //   anchor: 0.4,
          //   onTap: () {
          //     if (SlidingUpPanelStatus.expanded == panelController.status) {
          //       panelController.collapse();
          //     } else {
          //       panelController.expand();
          //     }
          //   },
          //   enableOnTap: true,
          //   child: Container(
          //     margin: const EdgeInsets.symmetric(horizontal: 15.0),
          //     decoration: const ShapeDecoration(
          //       color: Colors.red,
          //       shadows: [
          //         BoxShadow(
          //           blurRadius: 5.0,
          //           spreadRadius: 2.0,
          //           color: Color(0x11000000)
          //         )
          //       ],
          //       shape: RoundedRectangleBorder(
          //         borderRadius: BorderRadius.only(
          //           topLeft: Radius.circular(10.0),
          //           topRight: Radius.circular(10.0),
          //         ),
          //       ),
          //     ),
          //     child: Column(
          //       mainAxisSize: MainAxisSize.min,
          //       children: <Widget>[
          //         Container(
          //           alignment: Alignment.center,
          //           height: 50.0,
          //           child: const  Row(
          //             mainAxisAlignment: MainAxisAlignment.center,
          //             children: [
          //               Icon(
          //                 Icons.menu,
          //                 size: 30,
          //                 color: Colors.white,
          //               ),
          //               Padding(
          //                 padding: EdgeInsets.only(
          //                   left: 8.0,
          //                 ),
          //               ),
          //               Text(
          //                 'Choose Product to View',
          //                 style: TextStyle(
          //                   color: Colors.white,
          //                   fontWeight: FontWeight.bold,
          //                   fontSize: 16
          //                 ),
          //               )
          //             ],
          //           ),
          //         ),
          //         Divider(
          //           height: 0.5,
          //           color: Colors.grey[300],
          //         ),
          //         Container(
          //           margin: const EdgeInsets.all(5),
          //           decoration: BoxDecoration(
          //             color: Colors.white,
          //             borderRadius: BorderRadius.circular(5)
          //           ),
          //           height: MediaQuery.of(context).size.height * 0.83,
          //           child: SingleChildScrollView(
          //             child: Column(
          //               children: _buildSubListLevel(listProductName),
          //             )
          //           )
          //         )
          //       ]
          //     )
          //   )
          // )
        ]
      )
    );
  }

  String defaultAdMoreFilterString = '{No FIlter}';
  String addedFilterSelected = '';
  // ****************************** Widget fix for all page ******************************
  Widget fixAllPage() {
    return SingleChildScrollView(
      child: Column(
        children: [
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Column(
              children: [
                // ----- Row DATE -----
                Row(
                  children: [
                    // Day roll back ==================
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                            Text('D', style: TextStyle(color: Colors.white))
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForYesterday();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 255, 200, 200),
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_downward_rounded, size: 15),
                            Text('D')
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForToday();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    // Week roll back ==================
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 15),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                            Text('W', style: TextStyle(color: Colors.white))
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForLastWeek();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 255, 200, 200),
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_downward_rounded, size: 15),
                            Text('W')
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForThisWeek();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    // Month roll back ==================
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 15),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                            Text('M', style: TextStyle(color: Colors.white))
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForLastMonth();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 255, 200, 200),
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_downward_rounded, size: 15),
                            Text('M')
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForThisMonth();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    // Quarter roll back ==================
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 15),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                            Text('Q', style: TextStyle(color: Colors.white))
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForLastQuarter();
                            setDateRange();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 255, 200, 200),
                        boxShadow: const [
                          BoxShadow(
                            blurRadius: 5,
                            offset: Offset(1, 1),
                            color: Colors.grey,
                          )
                        ],
                        borderRadius: BorderRadius.circular(10)
                      ),
                      child: RawMaterialButton(
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.arrow_downward_rounded, size: 15),
                            Text('Q')
                          ],
                        ),
                        onPressed: () {
                          setState(() {
                            updateDateRangeForThisQuarter();
                            setDateRange();
                          });
                        },
                      )
                    ),               
                  ]
                ),
                // ----- Row DATE Showing -----
                Row(
                  children: [
                    // Label From ==================
                    Container(
                      height: 20,
                      alignment: Alignment.topLeft,
                      width: 35,
                      child: const Text(
                        'From', 
                        style: TextStyle(
                          fontSize: 12, 
                        )
                      )
                    ),
                    Container(
                      height: 20,
                      width: 100,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.grey),
                        borderRadius: BorderRadius.circular(5),
                        color: Colors.white
                      ),
                      child: Text(
                        fromDATE,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Colors.red
                        ),
                      )
                    ),
                    IconButton(
                      icon: const Icon(Icons.calendar_month_outlined),
                      onPressed: () => _selectDateFrom(context)
                    ),
                    // Label To ==================
                    Container(
                      height: 20,
                      alignment: Alignment.topRight,
                      width: 35,
                      child: const Text(
                        'To', 
                        style: TextStyle(
                          fontSize: 12, 
                        )
                      )
                    ),
                    Container(
                      height: 20,
                      width: 100,
                      margin: const EdgeInsets.only(left: 5),
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.grey),
                        borderRadius: BorderRadius.circular(5),
                        color: Colors.white
                      ),
                      child: Text(
                        toDATE,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Colors.red
                        ),
                      )
                    ),
                    IconButton(
                      icon: const Icon(Icons.calendar_month_outlined),
                      onPressed: () => _selectDateTo(context)
                    ),
                  ]
                ),            
                // Button to see filter page
                Container(
                  margin: const EdgeInsets.only(top: 10),
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(5)
                  ),
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      foregroundColor: Colors.white,
                      backgroundColor: Colors.transparent,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(5)
                      )
                    ),
                    onPressed: () {
                      setState(() {
                        expandMoreFilter = !expandMoreFilter;
                      });
                    },
                    child: const Text('See More Filter'),
                  ),
                ),
                // More filter ==================
                AnimatedContainer(
                  duration: const Duration(milliseconds: 500),
                  margin: const EdgeInsets.only(top: 5),
                  width: expandMoreFilter ? MediaQuery.of(context).size.width * 0.95 : 0,
                  height: expandMoreFilter ? MediaQuery.of(context).size.height * 0.3 : 0,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.black),
                    borderRadius: BorderRadius.circular(5)
                  ),
                  child: filterBox(),
                )
              ]        
            )
          ),
        ]
      )
    );
  }
  
  // *************** [Page Overall] ***************
  Widget _pageAverall() {
    return SingleChildScrollView(
      child: Column(
        children: [
          // Button for click Query ==================
          Container(
            width: MediaQuery.of(context).size.width * 0.85,
            margin: const EdgeInsets.only(top: 10),
            height: 30,
            child : ElevatedButton(
              onPressed: () {
                setState(() { 
                  if (levelSelected.isNotEmpty && modelSelected.isNotEmpty) {
                    mixChartVisible = false;
                    _refreshIndicatorKey.currentState?.show();
                  }
                });
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color.fromARGB(255, 212, 210, 210),
                side: const BorderSide(color: Colors.black),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(0)
                )
              ),
              child: const Text(
                'QUERY',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 13,
                  fontWeight: FontWeight.bold
                ),
              ),
            )
          ),
          // Mix Chart ==================
          Visibility(
            visible: mixChartVisible,
            child: Container(
              width: MediaQuery.of(context).size.width * 0.98,
              height: 300,
              margin: const EdgeInsets.only(top: 10),
               child: MyLineChart(
                dataLineChart: dataLineChart,
                dataQtyLineChart: dataQtyLineChart,
                xAxis: xAxis,
              )
            )
          ),
          // Table FBN YIELD ==================
          Visibility(
            visible: mixChartVisible,
            child: SizedBox(
              width: MediaQuery.of(context).size.width * 0.95,
              height: 200,
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      TableFBNYIELD(
                        dataTable: dataTable,
                        columnName: [defaultGroupBy, stringFilterSelectedCode.split(' ')[1],'In', 'Out', 'Fail', 'Yield'],
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
          const SizedBox(height: 50)   
        ],
      ),
    );
  } 

  Widget filterBox() {
    return WidgetsMoreFilter(
      levelSelected: levelSelected,
      modelSelected: modelSelected,
      startDate: startDate.toString(),
      endDate: endDate.toString(),
      isChecked: isChecked,
      isCheckedColor: isCheckedColor,
      isCheckedString: isCheckedString,
      sendMergedFilterCode: getMergedFilterCode
    );
  }

  void getMergedFilterCode(String text, String groupBySelected, String filter, String oldFilter) {
    setState(() {
      stringFilterSelectedCode = text;
      defaultGroupBy = groupBySelected;
      filterSelected = filter;    
      oldFilterSelected = oldFilter;    
    });
  }

  Future<void> queryDataForMixChart(String drillOn) async {
    try {
      if (stringFilterSelectedCode.isNotEmpty) {
        isLoading = true;
        if (!stringFilterSelectedCode.contains("'' : ''")) {
          stringFilterSelectedCode = stringFilterSelectedCode.replaceAll("' : '", "'' : ''");
        }
        
        stringEncryptedArray = await encryptData([
          modelSelected,
          startDate.toString(),
          endDate.toString(),
          filterSelected.replaceAll("' : '", "'' : ''"),
          stringFilterSelectedCode,
          defaultGroupBy,
          drillOn,
          '01'
        ]);
        var dataQueried = await getDataPOST(
          'https://supply-api.fabrinet.co.th/api/YMA/EPYieldQueryDetail',
          {
            'Model': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
            'From': stringEncryptedArray['data'][1],
            'To': stringEncryptedArray['data'][2],
            'FilterSelected': stringEncryptedArray['data'][3],
            'FilterCode': stringEncryptedArray['data'][4],
            'Groupby': stringEncryptedArray['data'][5],
            'Drillon': stringEncryptedArray['data'][6],
            'Version': stringEncryptedArray['data'][7]
          },
        );
        
        if (dataQueried[1] == 200) {
          String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

          final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
          final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

          String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
          List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
          
          dictDecodedDataByDate = [];
          dataTable = [];
          dictDecodedDataPercentByDate = [];
          var categoryFilter = [];
          List<String> categoryGroupBy = [];
          for (var item in decodedData) {
            dataTable.add([item[defaultGroupBy], item['Param'], item['In'], item['Out'], item['Fail'], item['Yield']]);
            if (item[defaultGroupBy] != 'All First Pass' && item[defaultGroupBy] != 'All In/Out') {
              dictDecodedDataByDate.add([item[defaultGroupBy], item['Out'], item['Fail']]);
              dictDecodedDataPercentByDate.add(double.parse(((item['Out'] / item['In']) * 100).toStringAsFixed(2)));

              categoryGroupBy.add(item[defaultGroupBy]);
              categoryFilter.add(item['Param']);
            }
          }
          titleMixChart = 'Yield By $defaultGroupBy';
          mixChartVisible = true;

          categoryGroupBy = categoryGroupBy.toSet().toList();
          categoryFilter = categoryFilter.toSet().toList();
          Map<String, dynamic> objGroupBy = {};
          for (var cat in categoryFilter) {
            Map<String, dynamic> subObject = {};
            for (var item in decodedData) {
              if (item[defaultGroupBy] != 'All First Pass' && item[defaultGroupBy] != 'All In/Out') {
                if (!subObject.containsKey(cat)) {
                  subObject[cat] = [];
                }

                if (item['Param'] == cat) {
                  subObject[cat].add([item[defaultGroupBy], item['Yield'], item['In']]);
                }
                else {
                  subObject[cat].add([item[defaultGroupBy], '', '']);
                }
              }
            }

            List<dynamic> bigArrSorted = [];
            for (var obj in subObject.entries) {
              for (var valObj in obj.value) {
                if (valObj[1].toString().isNotEmpty) {
                  bigArrSorted.add(obj.value[obj.value.indexOf(valObj)]);
                }
              }
            }

            if (!objGroupBy.containsKey(cat)) {
              objGroupBy[cat] = bigArrSorted;
            }
          }

          Map<String, dynamic> dataToLineChart = {};
          Map<String, dynamic> dataQtyToLineChart = {};
          for (var obj in objGroupBy.entries) {
            List<String> listDT = [];
            for (var i in obj.value) {
              listDT.add(i[0]);
            }

            List<double> listNum = [];
            for (var i in obj.value) {
              listNum.add(i[1]);
            }

            List<int> listQty = [];
            for (var i in obj.value) {
              listQty.add(i[2]);
            }

            for (int i = 0; i < categoryGroupBy.length; i++) {
              if (!dataToLineChart.containsKey(obj.key)) {
                dataToLineChart[obj.key] = [];
              }
              if (!dataQtyToLineChart.containsKey(obj.key)) {
                dataQtyToLineChart[obj.key] = [];
              }

              if (listDT.contains(categoryGroupBy[i])) {
                dataToLineChart[obj.key].add(listNum[listDT.indexOf(categoryGroupBy[i])]);
                dataQtyToLineChart[obj.key].add(listQty[listDT.indexOf(categoryGroupBy[i])]);
              }
              else {
                dataToLineChart[obj.key].add(null);
                dataQtyToLineChart[obj.key].add(0);
              }
            }
          } 

          setState(() {
            dataLineChart = dataToLineChart;
            dataQtyLineChart = dataQtyToLineChart;
            xAxis = categoryGroupBy;
          });
        }
        else {
          CoolAlert.show(
            width: 1,
            context: scaffoldKey.currentContext!,
            type: CoolAlertType.error,
            text:'Enable to connect Database ! ${dataQueried[0]}'
          );
        }
      }
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }

  // ****************************************** Tab [PARETO] ******************************************
  // ************************************************************************************

  // ========================================= Query [LEVEL] =========================================
  Future<void> fetchDataLevel() async {
    try {
      String keyValue = 'yieldeachproduct'; // *** important, same as flutter sent ***
      var iv = encrypt.IV.fromLength(16);

      var dataQueried = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/ProductNameEP',
        {
          'Value' : iv.base16
        } 
      );

      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(keyValue);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: iv);
        decodedDataProductName = List<Map<String, dynamic>>.from(json.decode(decryptJson));
        
        setState(() {
          listProductName = [];
          if (decodedDataProductName.isNotEmpty) {
            for (var i in decodedDataProductName) {
              listProductName.add(i['model_type']);
            }
          } 
          else {
            listProductName = [];
          }

        });
      }
      else {
        CoolAlert.show(
          width: 1,
          context: scaffoldKey.currentContext!,
          type: CoolAlertType.error,
          text:'Enable to connect Database ! ${dataQueried[0]}'
        );
      }
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }

  // ========================= Create drop list by [LEVEL] =========================
  List<Widget> _buildSubListLevel(List<String> data) {
    List<Widget> subListsLevel = [];
    if (data.isNotEmpty) {
      // =============== Create sub menu Level ===============
      for (var val in data) {
        subListsLevel.add(
          ExpansionTile(
            textColor: Colors.white,
            iconColor: Colors.white,
            backgroundColor: const Color.fromARGB(255, 255, 125, 125),
            onExpansionChanged: (bool isExpanded) async {
              setState(() {
                if (isExpanded) {
                  levelSelected = val;
                }
                listProductModel= [];
                for (var i in decodedDataProductName) {
                  if (i['model_type'] == val) {
                    listProductModel.add(i['model']);
                  }
                }
                
              });
            },
            title: Row(
              children: [
                const Icon(Icons.folder_copy, color: Colors.black),
                const SizedBox(width: 8),
                Text(val, style: const TextStyle(color: Colors.black)),
              ],
            ),
            children: _buildSubListModel(listProductModel),
          ),
        );
      }
    }
    return subListsLevel;
  }

  // ========================= Query [MODEL] =========================
  Future<void> fetchDataModel(List<String> model) async {
    // Case array input
    setState(() {
      dataModelArr = model;
    });
  }
  // ========================= Create drop list by [MODEL] =========================
  List<Widget> _buildSubListModel(List<String>? dataModel) {
    List<Widget> subListsModel = [];
    // =============== Create sub menu Model ===============
    if (dataModel != null) {
      for (String item in dataModel) {
        subListsModel.add(
          ExpansionTile(
            textColor: Colors.black,
            iconColor: Colors.black,
            backgroundColor:const Color.fromARGB(255, 247, 166, 166),
            onExpansionChanged: (bool isExpanded) async {
              if (isExpanded) {
                setState(() {
                  modelSelected = item;
                });
              }
            },
            title: Row(
              children: [
                const SizedBox(width: 30),
                const Icon(Icons.snippet_folder, color: Colors.black),
                const SizedBox(width: 8),
                Text(item, style: const TextStyle(color: Colors.black)),
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