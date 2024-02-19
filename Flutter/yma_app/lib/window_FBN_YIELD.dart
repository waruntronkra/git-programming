// ignore_for_file: file_names
import 'package:flutter/material.dart';
// ignore: depend_on_referenced_packages
import 'package:intl/intl.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:cool_alert/cool_alert.dart';
import 'package:shimmer/shimmer.dart';
import 'mixChartYIELD_FBN.dart';
import 'table_fbn_yield.dart';

class WindowFBNYIELD extends StatefulWidget {
  const WindowFBNYIELD({
    required this.levelSelected,
    required this.modelSelected,
    Key? key
  }) : super(key: key);

  final String levelSelected;
  final String modelSelected;

  @override
  State<WindowFBNYIELD> createState() => _WindowFBNYIELDState();
}

class _WindowFBNYIELDState extends State<WindowFBNYIELD> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  late DateTime startDate;
  late DateTime endDate;

  String fromDATE = '';
  String toDATE = '';
  
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
  String stringFilterSelectedCode = '';
  
  List<Map<String, dynamic>> decodedData = [];
  List<List<dynamic>> dictDecodedDataByDate = [];
  List<double> dictDecodedDataPercentByDate = [];
  List<List<dynamic>> dataTable = [];
  String titleMixChart = '';
  bool mixChartVisible = false;

  Map<String, dynamic> stringEncryptedArray = {};

  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    updateDateRangeForToday();
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
  String textBoxLabel = 'Unselect All';

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        key: scaffoldKey,
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
        body: Column(
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
    );
  }

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
                        color: const Color.fromARGB(255, 3, 141, 93),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 215, 249, 237),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
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
                        color: const Color.fromARGB(255, 3, 141, 93),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 215, 249, 237),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
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
                        color: const Color.fromARGB(255, 3, 141, 93),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 215, 249, 237),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
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
                        color: const Color.fromARGB(255, 3, 141, 93),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
                          });
                        },
                      )
                    ),
                    Container(
                      width: 40,
                      height: 40,
                      margin: const EdgeInsets.only(top: 5, bottom: 5, left: 5),
                      decoration: BoxDecoration(
                        color: const Color.fromARGB(255, 215, 249, 237),
                        border: Border.all(color: Colors.black, width: 2)
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
                            queryByFilter();
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
                        border: Border.all(color: Colors.black)
                      ),
                      child: Text(
                        fromDATE,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                      )
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
                        border: Border.all(color: Colors.black)
                      ),
                      child: Text(
                        toDATE,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                      )
                    )
                  ]
                ),            
                // ----- Row Drop Dow [Group] & [Filter] -----
                Row(
                  children: [                 
                    // Label Group By ==================
                    Container(
                      height: 20,
                      padding: const EdgeInsets.only(top: 3),
                      alignment: Alignment.topLeft,
                      width: 60,
                      child: const Text(
                        'Group By', 
                        style: TextStyle(
                          fontSize: 12, 
                          fontWeight: FontWeight.bold
                        )
                      )
                    ),
                    // Group By ==================   
                    Container(
                      margin: const EdgeInsets.only(left: 3, top: 10, bottom: 5),
                      width: 140,
                      height: 30,
                      child: DropdownButtonHideUnderline(
                        child: DropdownButton2<String>(
                          isExpanded: true,
                          hint: Row(
                            children: [
                              Expanded(
                                child: Text(
                                  defaultGroupBy,
                                  style: const TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: Color.fromARGB(255, 3, 141, 93)
                                  ),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              )
                            ],
                          ),
                          items: itemGroupBy.map((String item) => DropdownMenuItem<String>(
                            value: item,
                            child: Text(
                              item,
                              style: const TextStyle(
                                fontSize: 11,
                                color: Color.fromARGB(255, 3, 141, 93)
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          )).toList(),
                          onChanged: (String? newVal) {
                            setState(() {
                              defaultGroupBy = newVal!;
                            });
                          },
                          buttonStyleData: ButtonStyleData(
                            height: 50,
                            width: 160,
                            padding: const EdgeInsets.only(left: 14, right: 14),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: Colors.transparent,
                              ),
                              color: const Color.fromARGB(255, 255, 255, 255),
                            ),
                            elevation: 2,
                          ),
                          dropdownStyleData: DropdownStyleData(
                            maxHeight: 200,
                            width: 138,
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
                    // Label Filter ==================
                    Container(
                      height: 20,
                      width: 35,
                      margin: const EdgeInsets.only(left: 10),
                      padding: const EdgeInsets.only(top: 3),
                      alignment: Alignment.topLeft,
                      child: const Text(
                        'Filter', 
                        style: TextStyle(
                          fontSize: 12, 
                          fontWeight: FontWeight.bold
                        )
                      )
                    ),
                    // Filter ==================   
                    Container(
                      margin: const EdgeInsets.only(left: 3, top: 10, bottom: 5),
                      width: 130,
                      height: 30,
                      child: DropdownButtonHideUnderline(
                        child: DropdownButton2<String>(
                          isExpanded: true,
                          hint: Row(
                            children: [
                              Expanded(
                                child: Text(
                                  defaultFilter,
                                  style: const TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: Color.fromARGB(255, 3, 141, 93)
                                  ),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              )
                            ],
                          ),
                          items: itemFilter.map((String item) => DropdownMenuItem<String>(
                            value: item,
                            child: Text(
                              item,
                              style: const TextStyle(
                                fontSize: 11,
                                color: Color.fromARGB(255, 3, 141, 93)
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          )).toList(),
                          onChanged: (String? newVal) {
                            setState(() {
                              defaultFilter = newVal!;
                              if (defaultFilter == itemFilter[0]) {
                                filterSelected = 'buildtype';
                              }
                              else if (defaultFilter == itemFilter[1]) {
                                filterSelected = 'is_rework';
                              }
                              else if (defaultFilter == itemFilter[2]) {
                                filterSelected = 'equip_id';
                              }
                              else if (defaultFilter == itemFilter[3]) {
                                filterSelected = 'opn_des';
                              }
                              else if (defaultFilter == itemFilter[4]) {
                                filterSelected = 'emp_no';
                              }
                              else if (defaultFilter == itemFilter[5]) {
                                filterSelected = 'part_no';
                              }
                              else if (defaultFilter == itemFilter[6]) {
                                filterSelected = 'runtype';
                              }
                              else if (defaultFilter == itemFilter[7]) {
                                filterSelected = 'workorder';
                              }
                              else if (defaultFilter == itemFilter[8]) {
                                filterSelected = 'pic_wf';
                              }
                              else if (defaultFilter == itemFilter[9]) {
                                filterSelected = 'driver_lot';
                              }
                              else if (defaultFilter == itemFilter[10]) {
                                filterSelected = 'tia_lot';
                              }
                              queryByFilter();
                            });
                          },
                          buttonStyleData: ButtonStyleData(
                            height: 50,
                            width: 160,
                            padding: const EdgeInsets.only(left: 14, right: 14),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(10),
                              border: Border.all(
                                color: Colors.transparent,
                              ),
                              color: const Color.fromARGB(255, 255, 255, 255),
                            ),
                            elevation: 2,
                          ),
                          dropdownStyleData: DropdownStyleData(
                            maxHeight: 200,
                            width: 128,
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
                    )
                  ]
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
    Color colorCheckBox(Set<MaterialState> states) {
      const Set<MaterialState> interactiveStates = <MaterialState>{
        MaterialState.pressed,
        MaterialState.hovered,
        MaterialState.focused,
      };
      if (states.any(interactiveStates.contains)) {
        return const Color.fromARGB(255, 3, 141, 93);
      }
      return const Color.fromARGB(255, 3, 141, 93);
    }
    return SingleChildScrollView(
      child: Column(
        children: [
          // Checkbox ========================================================================
          Row(
            children: [
              Container(
                alignment: Alignment.topLeft,
                margin: const EdgeInsets.only(left: 15),
                child: Checkbox(
                  checkColor: Colors.white,
                  fillColor: MaterialStateProperty.resolveWith(colorCheckBox),
                  value: checkBox,
                  onChanged: (bool? val) {
                    setState(() {
                      checkBox = val!;
                      if (val == true) {
                        isChecked = [];
                        for (var i = 0; i < listFilterSelected.length; i++) {
                          isChecked.add(false); 
                          isCheckedColor.add(const Color.fromARGB(255, 255, 255, 255)); 

                          isCheckedString = [];
                          for (var i = 0; i < listFilterSelected.length; i++) {
                            isCheckedString.add('');
                          }
                          stringFilterSelectedCode = '';
                          for (var i in isCheckedString) {
                            if (i.isNotEmpty) {
                              stringFilterSelectedCode += ",''$i''";
                            }
                          }
                          stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
                        }
                      }
                      else {
                        isChecked = [];
                        for (var i = 0; i < listFilterSelected.length; i++) {
                          isChecked.add(true); 
                          isCheckedColor.add(const Color.fromARGB(255, 3, 141, 93)); 
                        }

                        isCheckedString = [];
                        for (String val in listFilterSelected) {
                          isCheckedString.add(val);
                        }
                        stringFilterSelectedCode = '';
                        for (var i in isCheckedString) {
                          if (i.isNotEmpty) {
                            stringFilterSelectedCode += ",''$i''";
                          }
                        }
                        stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
                      }
                    });
                  },
                ),
              ),
              Container(
                height: 19,
                alignment: Alignment.topLeft,
                child: Text(
                  textBoxLabel, 
                  style: const TextStyle(
                    fontSize: 12, 
                    fontWeight: FontWeight.bold
                  )
                )
              ),
            ]
          ),
          // Filter Result Queried ==================
          Container(
            width: MediaQuery.of(context).size.width * 0.9,
            height: 100,
            decoration: BoxDecoration(
              border: Border.all(color: Colors.black)
            ),
            child: SingleChildScrollView(
              child: Container(
                margin: const EdgeInsets.only(top: 5, bottom: 3),
                child: Column(
                  children: [                  
                    ...listPerFiltered(listFilterSelected),    
                  ]
                ),
              )
            )
          ),
          // Button for click Query ==================
          Container(
            width: MediaQuery.of(context).size.width * 0.85,
            margin: const EdgeInsets.only(top: 5),
            height: 30,
            child : ElevatedButton(
              onPressed: () {
                setState(() { 
                  if (widget.levelSelected.isNotEmpty && widget.modelSelected.isNotEmpty) {
                    mixChartVisible = false;
                    queryDataForMixChart('Yield');
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
            visible: isLoading,
            child: Shimmer.fromColors(
              baseColor: Colors.grey[300]!,
              highlightColor: Colors.grey[100]!,
              child: Container(
                width: MediaQuery.of(context).size.width * 0.98,
                height: 300,
                margin: const EdgeInsets.only(top: 10),
                child: const MixChartFBNYield(
                  dataBarChart: [[' ', 2, 0], ['  ', 3, 0], ['   ', 1, 0], ['    ', 4, 0]],
                  dataLineChartMix: [3, 4, 2, 5],
                  chartTitle: '',
                ),
              )
            ),
          ),
          Visibility(
            visible: mixChartVisible,
            child: Container(
              width: MediaQuery.of(context).size.width * 0.98,
              height: 300,
              margin: const EdgeInsets.only(top: 10),
              child: MixChartFBNYield(
                dataBarChart: dictDecodedDataByDate,
                dataLineChartMix: dictDecodedDataPercentByDate,
                chartTitle: titleMixChart,
              ),
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
                        columnName: [defaultGroupBy, 'In', 'Out', 'Fail', 'Yield'],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          Visibility(
            visible: isLoading,
            child: Shimmer.fromColors(
              baseColor: Colors.grey[300]!,
              highlightColor: Colors.grey[100]!,
              child: SizedBox(
                width: MediaQuery.of(context).size.width * 0.95,
                height: 200,
                child: const SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: SingleChildScrollView(
                    child: Column(
                      children:  [
                        TableFBNYIELD(
                          dataTable: [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']],
                          columnName: ['', '', '', '', ''],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  } 

  Future<void> queryByFilter() async {
    checkBox = false;
    listFilterSelected = [];
    mixChartVisible = false;
    decodedData = [];

    stringEncryptedArray = await encryptData([
      widget.levelSelected,
      widget.modelSelected,
      startDate.toString(),
      endDate.toString(),
      filterSelected
    ]);

    var dataQueried = await getDataPOST(
      'https://localhost:44342/api/YMA/FbnYieldQueryFilter',
      {
        'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
        'Model': stringEncryptedArray['data'][1],
        'From': stringEncryptedArray['data'][2],
        'To': stringEncryptedArray['data'][3],
        'Filter': stringEncryptedArray['data'][4]
      }                         
    );
    if (dataQueried[1] == 200) {
      String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

      final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
      final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

      String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
      decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
      setState(() {
        if (decodedData.isNotEmpty) {
          listFilterSelected = [];
          for (var i in decodedData) {
            listFilterSelected.add(i['Param']);
          }
          isChecked = [];
          isCheckedColor = [];
          for (var i = 0; i < listFilterSelected.length; i++) {
            isChecked.add(true); 
            isCheckedColor.add(const Color.fromARGB(255, 3, 141, 93)); 
          }

          isCheckedString = [];
          for (String val in listFilterSelected) {
            isCheckedString.add(val);
          }
          stringFilterSelectedCode = '';
          for (var i in isCheckedString) {
            if (i.isNotEmpty) {
              stringFilterSelectedCode += ",''$i''";
            }
          }
          stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
        }
        else {
          listFilterSelected = [];
        }
      });
    }
    else {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Enable to connect Database !'
      );
    }
  }

  List<Widget> listPerFiltered(List<String> data) {
    List<Widget> subList = [];
    if (data.isNotEmpty) {
      for (var i = 0; i < data.length; i++) {
        subList.add(Container(
          width: MediaQuery.of(context).size.width * 0.85,
          margin: const EdgeInsets.only(bottom: 2),
          height: 20,
          child : ElevatedButton(
            onPressed: () {
              setState(() {
                if (isChecked[i] == true) {
                  isChecked[i] = false;
                  isCheckedString[i] = '';
                }
                else {
                  isChecked[i] = true;
                  isCheckedString[i] = data[i];
                }

                stringFilterSelectedCode = '';
                for (var i in isCheckedString) {
                  if (i.isNotEmpty) {
                    stringFilterSelectedCode += ",''$i''";
                  }
                }
                stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
              });
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: isChecked[i] == true ? isCheckedColor[i] : Colors.white,
              side: const BorderSide(color: Colors.black),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(0)
              )
            ),
            child: Text(
              data[i],
              style: TextStyle(
                color: isChecked[i] == true ? Colors.white : Colors.black,
                fontSize: 12
              ),
            ),
          )
        ));
      }
    }
    return subList;
  }

  Future<void> queryDataForMixChart(String drillOn) async {
    if (stringFilterSelectedCode.isNotEmpty) {
      isLoading = true;
      stringEncryptedArray = await encryptData([
        widget.levelSelected,
        widget.modelSelected,
        startDate.toString(),
        endDate.toString(),
        filterSelected,
        stringFilterSelectedCode,
        defaultGroupBy,
        drillOn
      ]);
      var dataQueried = await getDataPOST(
        'https://localhost:44342/api/YMA/FbnYieldQueryDetail',
        {
          'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
          'Model': stringEncryptedArray['data'][1],
          'From': stringEncryptedArray['data'][2],
          'To': stringEncryptedArray['data'][3],
          'Filter': stringEncryptedArray['data'][4],
          'FilterCode': stringEncryptedArray['data'][5],
          'Groupby': stringEncryptedArray['data'][6],
          'Drillon': stringEncryptedArray['data'][7]
        },
      );
  
      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
        setState(() {
          dictDecodedDataByDate = [];
          dataTable = [];
          dictDecodedDataPercentByDate = [];
          for (var item in decodedData) {
            dataTable.add([item[defaultGroupBy], item['In'], item['Out'], item['Fail'], item['Yield']]);
            if (item[defaultGroupBy] != 'All First Pass' && item[defaultGroupBy] != 'All In/Out') {
              dictDecodedDataByDate.add([item[defaultGroupBy], item['Out'], item['Fail']]);
              dictDecodedDataPercentByDate.add(double.parse(((item['Out'] / item['In']) * 100).toStringAsFixed(2)));
            }
          }
          titleMixChart = 'Yield By $defaultGroupBy';
          isLoading = false;
          mixChartVisible = true;
        });
      }
      else {
        CoolAlert.show(
          width: 1,
          context: scaffoldKey.currentContext!,
          type: CoolAlertType.error,
          text:'Enable to connect Database !'
        );
      }
    }
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

  // ****************************************** Tab [PARETO] ******************************************

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