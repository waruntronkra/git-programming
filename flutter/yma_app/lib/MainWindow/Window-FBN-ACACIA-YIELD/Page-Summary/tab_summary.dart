import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_user_guildance/flutter_user_guildance.dart';
// ignore: depend_on_referenced_packages
import 'package:intl/intl.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:flutter_sliding_up_panel/flutter_sliding_up_panel.dart';
// import 'package:flutter/foundation.dart';
// import 'package:flutter_speed_dial/flutter_speed_dial.dart';
import 'package:cool_alert/cool_alert.dart';
import 'package:YMs/MainWindow/Window-FBN-ACACIA-YIELD/Page-Summary/utility/show_more_filter.dart';
import 'package:YMs/MainWindow/Window-FBN-ACACIA-YIELD/Page-Summary/utility/multiLineChart.dart';
import 'package:YMs/MainWindow/Window-FBN-ACACIA-YIELD/Page-Summary/utility/table.dart';
import 'package:YMs/MainWindow/Window-FBN-ACACIA-YIELD/Page-Summary/utility/barchart.dart';

class WindowFBNYIELD extends StatefulWidget {
  const WindowFBNYIELD({super.key});

  @override
  State<WindowFBNYIELD> createState() => _WindowFBNYIELDStateNew();
}

class _WindowFBNYIELDStateNew extends State<WindowFBNYIELD> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey = GlobalKey<RefreshIndicatorState>(); 
  UserGuidanceController userGuidanceController = UserGuidanceController();

  late ScrollController scrollController;
  SlidingUpPanelController panelController = SlidingUpPanelController();

  late DateTime startDate;
  late DateTime endDate;

  var tableProductName = [];
  Map<String, dynamic> dataLevelObject = {};
  List<String> dataModelArr = [];

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

  String filterSelected = 'buildtype';
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
  List<List<dynamic>> dictDecodedDataByDate = [];
  List<double> dictDecodedDataPercentByDate = [];
  List<List<dynamic>> dataTable = [];
  String titleMixChart = '';
  bool mixChartVisible = false;

  Map<String, dynamic> stringEncryptedArray = {};

  bool expandMoreFilter = false;

  Map<String, dynamic> dataLineChart = {};
  List<String> xAxis = [];
  Map<String, dynamic> dataQtyLineChart = {};

  List<dynamic> groupDataToBarChart = [];
  List<List<dynamic>> groupDataToTablePareto = [];

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
            primary: Color.fromARGB(255, 3, 141, 93), // Header background color
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
        startDate = selectedDate;
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
            primary: Color.fromARGB(255, 3, 141, 93), // Header background color
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
        endDate = selectedDate;
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

    WidgetsBinding.instance.addPostFrameCallback((_) => _openEndDrawer());
    super.initState();
  }

  void _openEndDrawer() {
    if (scaffoldKey.currentState != null) {
      scaffoldKey.currentState!.openEndDrawer();
    }
  }

  void _closeEndDrawer() {
    if (scaffoldKey.currentState != null) {
      scaffoldKey.currentState!.closeEndDrawer();
    }
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

  int _selectedIndex = -1;
  void _onItemTapped(int index) {
    setState(() {
      if (_selectedIndex == index) {
        _selectedIndex = -1; // Collapse the selected item
      } else {
        _selectedIndex = index; // Expand the selected item
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return UserGuidance(
      controller: userGuidanceController,
      opacity: 0.5,
      child: DefaultTabController(
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
                    style: GoogleFonts.nunito(
                      fontSize: 13,
                      fontWeight: FontWeight.bold
                    ),
                  ),
                  actions: [
                    IconButton(
                      onPressed: () {
                        userGuidanceController.show();
                      },
                      icon: const Icon(Icons.help),
                    ),
                    IconButton(
                      onPressed: () {
                        _openEndDrawer();
                      },
                      icon: const Icon(Icons.menu),
                    ),
                  ],
                  bottom: TabBar(
                    labelColor:const Color.fromARGB(255, 3, 141, 93),
                    indicatorColor:const Color.fromARGB(255, 3, 141, 93),
                    tabs: const <Widget>[
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
                    labelStyle: GoogleFonts.nunito(
                      fontSize: 11,
                      fontWeight: FontWeight.bold
                    ),
                  ),         
                ),
              ),
              // floatingActionButton: Builder(
              //   builder: (context) => FloatingActionButton(
              //     backgroundColor: const Color.fromARGB(255, 3, 141, 93),
              //     onPressed: () {
              //       Scaffold.of(context).openEndDrawer();
              //     },
              //     child: const Icon(Icons.menu, color: Colors.white),
              //   )
              // ),
              endDrawer: Drawer(
                width: 220,
                child: ListView.builder(
                  padding: EdgeInsets.zero,
                  itemCount: dataLevelObject.keys.toList().length,
                  itemBuilder: (context, index) {
                    if (index == 0) {
                      return UserAccountsDrawerHeader(
                        decoration: const BoxDecoration(
                        gradient: LinearGradient(
                            begin: Alignment.topRight,
                            end: Alignment.bottomLeft,
                            colors: [
                              Color.fromARGB(255, 42, 221, 159),
                              Color.fromARGB(255, 3, 141, 93)
                            ],
                          ),
                        ),
                        accountName: const Text(''),
                        accountEmail: Text(
                          'waruntronk.fabrinet.co.th',
                          style: GoogleFonts.nunito(
                            fontWeight: FontWeight.bold,
                            color: const Color.fromARGB(255, 255, 255, 255),
                            fontSize: 14,
                          ),
                        ),
                        currentAccountPicture: const CircleAvatar(
                          backgroundImage: NetworkImage("https://companiesmarketcap.com/img/company-logos/256/FN.png"),
                        ),
                        currentAccountPictureSize: const Size(100, 100),
                      );
                    }
                    return Column(
                      children: [
                        Container (
                          width: 200,
                          height: 25,
                          margin: const EdgeInsets.all(5),
                          child: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: _selectedIndex == index ? const Color.fromARGB(255, 3, 141, 93) : const Color.fromARGB(255, 220, 239, 233),
                              foregroundColor: Colors.black,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(5)
                              )
                            ),
                            onPressed: () async {
                              _onItemTapped(index);
                              setState(() {
                                levelSelected = dataLevelObject.keys.toList()[index];
                              });
                            },
                            child: Text(
                              dataLevelObject.keys.toList()[index],
                              style: GoogleFonts.nunito(
                                fontSize: 11.0,
                                fontWeight: FontWeight.bold,
                                color: _selectedIndex == index ? Colors.white : Colors.black
                              )
                            )
                          )
                        ),
                        AnimatedContainer(
                          duration: const Duration(milliseconds: 500),
                          padding: const EdgeInsets.all(5),
                          curve: Curves.easeInOut,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(5),
                            boxShadow: const [
                              BoxShadow(
                                color: Color.fromARGB(255, 193, 193, 193),
                                offset: Offset(1, 1),
                                blurRadius: 5
                              )
                            ]
                          ),
                          height: _selectedIndex == index ? dataLevelObject[levelSelected].length * 30.0 : 0.0,
                          width: _selectedIndex == index ? 200.0 : 0.0,
                          child: SingleChildScrollView(
                            child: _selectedIndex == index ? 
                            Column(
                              children: [
                                ...createListWidgetModel(dataLevelObject[levelSelected])
                              ],
                            )
                            : null,
                          ),
                        ),
                      ]
                    );
                  }
                ),
              ),
              body: RefreshIndicator(
                key: _refreshIndicatorKey,
                displacement: 50,
                color: Colors.white,
                backgroundColor: const Color.fromARGB(255, 3, 141, 93),
                onRefresh: () async {
                  await queryDataForParetoChart('Pareto');
                  await queryDataForYieldChart('Yield');
                },
                child: Container(
                  color: const Color.fromARGB(172, 239, 245, 250),
                  child: Column(
                    children: [
                      Container(
                        child: fixAllPage()
                      ),
                      Expanded(
                        child: TabBarView(
                          children: <Widget>[
                            _pageAverall(),
                            _pagePareto(),
                          ]
                        )
                      )
                    ]
                  )
                )
              ),
              // floatingActionButtonLocation: FloatingActionButtonLocation.startFloat,
              // floatingActionButton: SpeedDial(
              //   backgroundColor: const Color.fromARGB(255, 3, 141, 93),
              //   activeBackgroundColor: Colors.red,
              //   foregroundColor: Colors.white,
              //   childrenButtonSize: const Size(20, 30),
              //   buttonSize: const Size(35, 35),
              //   childMargin: const EdgeInsets.only(left: 5),
              //   icon: Icons.menu,
              //   activeIcon: Icons.close,
              //   spaceBetweenChildren: 1,
              //   switchLabelPosition: true,
              //   closeManually: true,
              //   children: [
              //     ..._buildSubListLevel(dataLevelObject),
              //   ],
              // ),
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
            //   enableOnTap: false,
            //   child: Container(
            //     margin: const EdgeInsets.symmetric(horizontal: 15.0),
            //     decoration: const ShapeDecoration(
            //       color: Color.fromARGB(255, 3, 141, 93),
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
            //           child: UserGuildanceAnchor(
            //             step: 1,
            //             tag: "Step 1: Choose product",
            //             child: Row(
            //               mainAxisAlignment: MainAxisAlignment.center,
            //               children: [
            //                 const Icon(
            //                   Icons.menu,
            //                   size: 28,
            //                   color: Colors.white,
            //                 ),
            //                 const Padding(
            //                   padding: EdgeInsets.only(
            //                     left: 8.0,
            //                   ),
            //                 ),
            //                 Text(
            //                   'Choose Product to View',
            //                   style: GoogleFonts.nunito(
            //                     color: Colors.white,
            //                     fontWeight: FontWeight.bold,
            //                     fontSize: 14
            //                   ),
            //                 )
            //               ],
            //             )
            //           )
            //         ),
            //         Container(
            //           margin: const EdgeInsets.all(10),
            //           padding: const EdgeInsets.only(top: 5),
            //           decoration: BoxDecoration(
            //             color: Colors.white,
            //             borderRadius: BorderRadius.circular(5)
            //           ),
            //           height: MediaQuery.of(context).size.height * 0.83,
            //           child: SingleChildScrollView(
            //             child: Column(
            //               children: _buildSubListLevel(dataLevelObject),
            //             )
            //           )
            //         )
            //       ]
            //     )
            //   )
            // )
          ]
        )
      )
    );
  }

  List<Widget> createListWidgetModel(List<dynamic> data) {
    List<Widget> subLists = [];
    if (data.isNotEmpty) {
      // =============== Create sub menu Level ===============
      for (var i in data) {
        subLists.add(Container(
          width: 180,
          height: 20,
          margin: const EdgeInsets.only(bottom: 5),
          child: ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: Colors.black,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(5)
              )
            ),
            onPressed: () {
              setState(() {
                modelSelected = i;
                _closeEndDrawer();
              });
            },
            child: Text(
              i,
              style: GoogleFonts.nunito(
                fontSize: 11.0,
                fontWeight: FontWeight.bold,
              )
            ),
          ),
        ));
      } 
    }
    return subLists;
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
                UserGuildanceAnchor(
                  step: 2,
                  tag: "Step 2: Select by Day/Week/Month/Quarter",
                  child: Row(
                    children: [
                      // Day roll back ==================
                      Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 3, 141, 93),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10)
                        ),
                        child: UserGuildanceAnchor(
                          step: 3,
                          tag: 'Last Day',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                                Text('D', style: GoogleFonts.nunito(color: Colors.white))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForYesterday();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                      Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 215, 249, 237),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: UserGuildanceAnchor(
                          step: 4,
                          tag: 'This Day',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_downward_rounded, size: 15),
                                Text('D', style: GoogleFonts.nunito(color: Colors.black))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForToday();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                      // Week roll back ==================
                      Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 15),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 3, 141, 93),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: UserGuildanceAnchor(
                          step: 5,
                          tag: 'Last Week',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                                Text('W', style: GoogleFonts.nunito(color: Colors.white))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForLastWeek();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                      Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 215, 249, 237),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: UserGuildanceAnchor(
                          step: 6,
                          tag: 'This Week',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_downward_rounded, size: 15),
                                Text('W', style: GoogleFonts.nunito(color: Colors.black))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForThisWeek();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                      // Month roll back ==================
                      Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 15),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 3, 141, 93),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: UserGuildanceAnchor(
                          step: 7,
                          tag: 'Last Month',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                                Text('M', style: GoogleFonts.nunito(color: Colors.white))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForLastMonth();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                      Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 215, 249, 237),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: UserGuildanceAnchor(
                          step: 8,
                          tag: 'This Month',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_downward_rounded, size: 15),
                                Text('M', style: GoogleFonts.nunito(color: Colors.black))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForThisMonth();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                      // Quarter roll back ==================
                     Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 15),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 3, 141, 93),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child:  UserGuildanceAnchor(
                          step: 9,
                          tag: 'Last Quarter',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_back_rounded, size: 15, color: Colors.white),
                                Text('Q', style: GoogleFonts.nunito(color: Colors.white))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForLastQuarter();
                                setDateRange();
                              });
                            }
                          )
                        )
                      ),
                     Container(
                        width: 40,
                        height: 40,
                        margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 215, 249, 237),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey,
                            )
                          ],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child:  UserGuildanceAnchor(
                          step: 10,
                          tag: 'This Quarter',
                          child: RawMaterialButton(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Icon(Icons.arrow_downward_rounded, size: 15),
                                Text('Q', style: GoogleFonts.nunito(color: Colors.black))
                              ],
                            ),
                            onPressed: () {
                              setState(() {
                                updateDateRangeForThisQuarter();
                                setDateRange();
                              });
                            }
                          )
                        ) 
                      )             
                    ]
                  )
                ),
                // ----- Row DATE Showing -----
                Container(
                  margin: const EdgeInsets.only(top: 8),
                  child: Row(
                    children: [
                      // Label From ==================
                      Container(
                        height: 20,
                        alignment: Alignment.topLeft,
                        width: 35,
                        child: Text(
                          'From', 
                          style: GoogleFonts.nunito(
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
                          style: GoogleFonts.nunito(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color:const Color.fromARGB(255, 3, 141, 93)
                          ),
                        )
                      ),
                      UserGuildanceAnchor(
                        step: 11,
                        tag: "[From] Date",
                        child: IconButton(
                          icon: const Icon(Icons.calendar_month_outlined),
                          onPressed: () => _selectDateFrom(context)
                        )
                      ),
                      // Label To ==================
                      Container(
                        height: 20,
                        alignment: Alignment.topRight,
                        width: 35,
                        child: Text(
                          'To', 
                          style: GoogleFonts.nunito(
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
                          style: GoogleFonts.nunito(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            color: const Color.fromARGB(255, 3, 141, 93)
                          ),
                        )
                      ),
                      UserGuildanceAnchor(
                        step: 12,
                        tag: "[To] Date",
                          child: IconButton(
                          icon: const Icon(Icons.calendar_month_outlined),
                          onPressed: () => _selectDateTo(context)
                        )
                      )
                    ]
                  )            
                ),            
                // Button to see filter page
                Container(
                  margin: const EdgeInsets.only(top: 5, bottom: 5),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    boxShadow: const [
                      BoxShadow(
                        blurRadius: 5,
                        offset: Offset(1, 1),
                        color: Colors.grey,
                      )
                    ]
                  ),
                  child: UserGuildanceAnchor(
                    step: 13,
                    tag: "Step 3: Click to see filter",
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        foregroundColor: Colors.white,
                        backgroundColor: const Color.fromARGB(255, 3, 141, 93),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(15)
                        )
                      ),
                      onPressed: () {
                        setState(() {
                          expandMoreFilter = !expandMoreFilter;
                        });
                      },
                      child: Text(
                        'See More Filter',
                        style: GoogleFonts.nunito(
                          color: Colors.white,
                          fontWeight: FontWeight.bold
                        ),
                      ),
                    )
                  )
                ),
                // More filter ==================
                AnimatedContainer(
                  duration: const Duration(milliseconds: 500),
                  margin: const EdgeInsets.only(top: 5),
                  width: expandMoreFilter ? MediaQuery.of(context).size.width * 0.95 : 0,
                  height: expandMoreFilter ? MediaQuery.of(context).size.height * 0.3 : 0,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Colors.white,
                    boxShadow: const [
                      BoxShadow(
                        blurRadius: 5,
                        offset: Offset(1, 1),
                        color: Colors.grey
                      )
                    ]
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
                backgroundColor: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(5),
                  side: const BorderSide(color: Colors.grey)
                )
              ),
              child: Text(
                'QUERY',
                style: GoogleFonts.nunito(
                  color: Colors.black,
                  fontSize: 13,
                  fontWeight: FontWeight.bold
                ),
              ),
            )
          ),
          // Chart YIELD ==================
          Visibility(
            visible: mixChartVisible,
            child: Container(
              width: MediaQuery.of(context).size.width * 0.93,
              height: MediaQuery.of(context).size.height * 0.35,
              margin: const EdgeInsets.only(top: 10, bottom: 10),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(5),
                boxShadow: const [
                  BoxShadow(
                    blurRadius: 5,
                    offset: Offset(1, 1),
                    color: Colors.grey
                  )
                ]
              ),
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
                    ]
                  )
                )
              )
            )
          ),
          const SizedBox(height: 100)   
        ]
      )
    );
  } 

  // *************** [Page Pareto] ***************
  Widget _pagePareto() {
    return SingleChildScrollView(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 5),
            width: MediaQuery.of(context).size.width * 0.93,
            height: MediaQuery.of(context).size.height * 0.5,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(10),
              boxShadow: const [
                BoxShadow(
                  color: Color.fromARGB(255, 219, 219, 219),
                  offset: Offset(1, 1),
                  blurRadius: 5
                )
              ]
            ),
            child: BarChart(
              paretoTitle: 'Top (%) Fail Defect',
              dataBarChart: groupDataToBarChart
            )
          ),
          Visibility(
            visible: mixChartVisible,
            child: Container(
              alignment: Alignment.center,
              margin: const EdgeInsets.only(top: 10),
              width: MediaQuery.of(context).size.width * 0.95,
              height: MediaQuery.of(context).size.height * 0.25,
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      TableFBNYIELD(
                        dataTable: groupDataToTablePareto,
                        columnName: const ['Defect', 'Fail', '% Fail'],
                      )
                    ]
                  )
                )
              )
            )
          ),
          const SizedBox(height: 50)  
        ],
      )
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

  void getMergedFilterCode(String text, String groupBySelected) {
    setState(() {
      stringFilterSelectedCode = text;
      defaultGroupBy = groupBySelected;
    });
  }

  Future<void> queryDataForYieldChart(String drillOn) async {
    try {
      if (stringFilterSelectedCode.isNotEmpty) {
        stringEncryptedArray = await encryptData([
          levelSelected,
          modelSelected,
          startDate.toString(),
          endDate.toString(),
          stringFilterSelectedCode.split(' ')[1],
          stringFilterSelectedCode,
          defaultGroupBy,
          drillOn,
          '71'
        ]);
        var dataQueried = await getDataPOST(
          'https://supply-api.fabrinet.co.th/api/YMA/FbnYieldQueryDetail',
          {
            'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
            'Model': stringEncryptedArray['data'][1],
            'From': stringEncryptedArray['data'][2],
            'To': stringEncryptedArray['data'][3],
            'FilterSelected': stringEncryptedArray['data'][4],
            'FilterCode': stringEncryptedArray['data'][5],
            'Groupby': stringEncryptedArray['data'][6],
            'Drillon': stringEncryptedArray['data'][7],
            'Version': stringEncryptedArray['data'][8]
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
            if (item[defaultGroupBy] != 'OVERALL Cummulative' && item[defaultGroupBy] != 'OVERALL In/Out') {
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
              if (item[defaultGroupBy] != 'OVERALL Cummulative' && item[defaultGroupBy] != 'OVERALL In/Out') {
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

  Future<void> queryDataForParetoChart(String drillOn) async {
    try {
      if (stringFilterSelectedCode.isNotEmpty) {
        stringEncryptedArray = await encryptData([
          levelSelected,
          modelSelected,
          startDate.toString(),
          endDate.toString(),
          stringFilterSelectedCode.split(' ')[1],
          stringFilterSelectedCode,
          defaultGroupBy,
          drillOn,
          '71'
        ]);
        var dataQueried = await getDataPOST(
          'https://supply-api.fabrinet.co.th/api/YMA/FbnYieldQueryDetail',
          {
            'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
            'Model': stringEncryptedArray['data'][1],
            'From': stringEncryptedArray['data'][2],
            'To': stringEncryptedArray['data'][3],
            'FilterSelected': stringEncryptedArray['data'][4],
            'FilterCode': stringEncryptedArray['data'][5],
            'Groupby': stringEncryptedArray['data'][6],
            'Drillon': stringEncryptedArray['data'][7],
            'Version': stringEncryptedArray['data'][8]
          },
        );
      
        if (dataQueried[1] == 200) {
          String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

          final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
          final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

          String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
          List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

          groupDataToBarChart = [];
          for (var data in decodedData) {
            groupDataToBarChart.add([data['defect'], double.parse(((data['fail'] / data['count']) * 100).toStringAsFixed(2))]);
          } 

          groupDataToTablePareto = [];
          for (var data in decodedData) {
            groupDataToTablePareto.add([data['defect'], data['fail'], ((data['fail'] / data['count']) * 100).toStringAsFixed(2)]);
          }
          
          setState(() {
            groupDataToBarChart = groupDataToBarChart;
            groupDataToTablePareto = groupDataToTablePareto;
          });
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

  // ========================================= Query [LEVEL] =========================================
  Future<void> fetchDataLevel() async {
    try {
      stringEncryptedArray = await encryptData([
        '71'
      ]);

      var productName = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/ProductName',
        {
          'Version' : '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
        } 
      );
      String jsonEncrypted = jsonDecode(jsonDecode(productName[0]))['encryptedJson'];

      final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
      final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

      String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
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
  List<Widget> _buildSubListLevel(Map<String, dynamic> dataLevel) {
    List<Widget> subListsLevel = [];
    if (dataLevel.isNotEmpty) {
      // =============== Create sub menu Level ===============
      for (var dict in dataLevel.entries) {
        subListsLevel.add(
          ExpansionTile(
            textColor: Colors.black,
            iconColor: Colors.black,
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
                const Icon(Icons.folder_copy, color: Colors.black),
                const SizedBox(width: 8),
                Text(
                  dict.key, 
                  style: GoogleFonts.nunito(
                    color: Colors.black,
                    fontSize: 13
                  )
                )
              ]
            ),
            children: [..._buildSubListModel(dataModelArr)],
          ),
          
          // SpeedDialChild(
          //   child: const Icon(Icons.check, size: 12),
          //   backgroundColor: const Color.fromARGB(255, 3, 141, 93),
          //   foregroundColor: Colors.white,
          //   label: dict.key,
          //   labelStyle: GoogleFonts.nunito(
          //     fontSize: 10
          //   ),
          //   shape: const StadiumBorder(),
          //   onTap: () {
          //     setState(() {
          //       _left = 50;
          //     });
          //   }
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
            backgroundColor:const Color.fromARGB(255, 151, 255, 250),
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
                Text(
                  item, 
                  style: GoogleFonts.nunito(
                    color: Colors.black,
                    fontSize: 13
                  )
                )
              ]
            )
          )
        );
      }
    }
    return subListsModel;
  }

  @override
  void dispose() {
    userGuidanceController.dispose();
    super.dispose();
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