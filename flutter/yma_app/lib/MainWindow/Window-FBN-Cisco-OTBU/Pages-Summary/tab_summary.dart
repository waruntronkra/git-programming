// ignore_for_file: file_names, depend_on_referenced_packages
import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:cool_alert/cool_alert.dart';
import 'package:YMs/Widget/widget_DATE.dart';
import 'package:intl/intl.dart';
import 'package:YMs/Chart/mixChartYIELDMultiLine.dart';

class WindowCiscoOTBUYIELD extends StatefulWidget {
  const WindowCiscoOTBUYIELD({super.key});

  @override
  State<WindowCiscoOTBUYIELD> createState() => _WindowCiscoOTBUYIELDState();
}

class _WindowCiscoOTBUYIELDState extends State<WindowCiscoOTBUYIELD> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey = GlobalKey<RefreshIndicatorState>();   
  Map<String, dynamic> stringEncryptedArray = {};

  String tagQuery = '';

  late DateTime previousTS;
  String selectedTS = '';

  String firstExpandeString = '';
  String secondExpandeString = '';
  String dateString = '';

  bool iconSMTChange = false;
  bool iconAchange = false;
  bool iconBchange = false;
  bool iconCchange = false;
  bool iconDchange = false;
  bool iconEchange = false;

  List<String> dataDetailFromList = [];
  String parameterSelected = '';

  List<String> xAxis = [];
  List<dynamic> stackBarChartPerDT = [];
  Map<String, dynamic> mapMultiLineChartPerOP = {};
  bool visibleChart = false;

  void updateDateRange(String dayInput) {
    int dayNum = int.parse(dayInput.split(' ')[0]);
    String mode = dayInput.split(' ')[1];
    DateTime now = DateTime.now();

    if (mode.contains('Day')) {
      DateTime dayBack = now.subtract(Duration(days: dayNum - 1));
      previousTS = DateTime(dayBack.year, dayBack.month, dayBack.day, 0, 0);
    }
    else if (mode.contains('Week')) {
      DateTime weekBack = now.subtract(Duration(days: now.weekday + ((dayNum - 1) * 7)));
      previousTS = DateTime(weekBack.year, weekBack.month, weekBack.day, 0, 0);
    }
    else if (mode.contains('Month')) {
      previousTS = DateTime(now.year, now.month - dayNum, 1, 0, 0);
    }
    else if (mode.contains('Quarter')) {
      int currentQuarter = ((now.month - 1) / 3).ceil();
      int lastQuarter = currentQuarter - 1 <= 0 ? 4 : currentQuarter - 1;
      previousTS = DateTime(now.year - 1, (lastQuarter - (dayNum - 1)) * 3 + 1, 1, 0, 0);
    }
    setState(() {
      visibleChart = false;
      selectedTS = dayInput;
      tagQuery = 'listDetail';
      _refreshIndicatorKey.currentState?.show();
    });
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        key: scaffoldKey,
        appBar: AppBar(
          title: Text(
            '$firstExpandeString : $secondExpandeString ($selectedTS)',
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.bold
            ),
          ),
          bottom: const TabBar(
            labelColor: Colors.blue,
            indicatorColor: Colors.blue,
            tabs: [
              Tab(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.ssid_chart_rounded),
                    Text(' YIELD')
                  ],
                ),
              ),
              Tab(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.bar_chart_rounded),
                    Text(' PARETO')
                  ],
                ),
              )
            ],
          ),
        ),
        endDrawer: Drawer(
          child: ListView(
            children: [
              const UserAccountsDrawerHeader(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topRight,
                    end: Alignment.bottomLeft,
                    colors: [
                      Colors.blue,
                      Colors.purple
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
              ...buildExpansionTile(
                ['SMT', 'Module', 'Sub-Assy', 'Optic', 'DF', 'RCFA']
              )
            ]
          )
        ),
        body: RefreshIndicator(
          key: _refreshIndicatorKey,
          displacement: 60,
          color: Colors.white,
          backgroundColor: Colors.blue,
          onRefresh: () async {
            if (tagQuery == 'listDetail') {
              await listDetail();
            }
            else if (tagQuery == 'queryYield') {
              await queryYield();
            }
          },
          child: Column(
            children: [
              Container(
                alignment: Alignment.center,
                width: MediaQuery.of(context).size.width * 0.97,
                height: 50,
                child: WidgetDate(
                  fetchData: updateDateRange,
                  levelSelected: firstExpandeString,
                  modelSelected: secondExpandeString,
                  colorBase: Colors.blue,
                ),
              ),
              Expanded(
                child: TabBarView(
                  children: <Widget>[
                    // LazyLoadingTreeView(),
                    pageSummary(),
                    const Text('s'),
                  ]
                )
              )
            ]
          )
        )
      ),
    );
  }

  List<Widget> buildExpansionTile(List<String> title) {
    List<Widget> subListWidget = [];
    for (var i = 0; i < title.length; i++) {
      subListWidget.add(ExpansionTile(
        backgroundColor: Colors.blue,
        iconColor: Colors.white,
        textColor: Colors.white,
        trailing: const Icon(Icons.arrow_drop_down),
        leading: const Icon(Icons.folder_copy_rounded),
        title: Text(
          title[i],
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
        ),
        onExpansionChanged: (bool val) {
          setState(() {
            firstExpandeString = title[i];
            if (val == true) {
              iconSMTChange = true;
            }
            else {
              iconSMTChange = false;
            }
          });
        },
        children: [
          ExpansionTile(
            backgroundColor: const Color.fromARGB(255, 79, 176, 255),
            trailing: const Icon(Icons.arrow_drop_down, color: Colors.transparent),
            title: Stack(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 30),
                  child: iconAchange == false ?
                  const Icon(Icons.subject_rounded, color: Colors.white)
                  :
                  const Icon(Icons.menu_open_sharp, color: Colors.white)
                ),
                Container(
                  margin: const EdgeInsets.only(left: 60),
                  child: const Text(
                    'Model', 
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.white
                    )
                  )
                )
              ]
            ),
            onExpansionChanged: (bool val) {
              setState(() {
                secondExpandeString = 'Model';
                if (val == true) {
                  iconAchange = true;
                }
                else {
                  iconAchange = false;
                }
              });
            },
          ),
          ExpansionTile(
            backgroundColor:const Color.fromARGB(255, 151, 208, 255),
            trailing: const Icon(Icons.arrow_drop_down, color: Colors.transparent),
            title: Stack(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 30),
                  child: iconBchange == false ?
                  const Icon(Icons.subject_rounded, color: Colors.white)
                  :
                  const Icon(Icons.menu_open_sharp, color: Colors.white)
                ),
                Container(
                  margin: const EdgeInsets.only(left: 60),
                  child: const Text(
                    'Part_No', 
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.white
                    )
                  )
                )
              ]
            ),
            onExpansionChanged: (bool val) {
              setState(() {
                secondExpandeString = 'Part_No';
                if (val == true) {
                  iconBchange = true;
                }
                else {
                  iconBchange = false;
                }
              });
            },
          ),
          ExpansionTile(
            backgroundColor: const Color.fromARGB(255, 151, 208, 255),
            trailing: const Icon(Icons.arrow_drop_down, color: Colors.transparent),
            title: Stack(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 30),
                  child: iconCchange == false ?
                  const Icon(Icons.subject_rounded, color: Colors.white)
                  :
                  const Icon(Icons.menu_open_sharp, color: Colors.white)
                ),
                Container(
                  margin: const EdgeInsets.only(left: 60),
                  child: const Text(
                    'Workorder', 
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.white
                    )
                  )
                )
              ]
            ),
            onExpansionChanged: (bool val) {
              setState(() {
                secondExpandeString = 'Workorder';
                if (val == true) {
                  iconCchange = true;
                }
                else {
                  iconCchange = false;
                }
              });
            },
          ),
          ExpansionTile(
            backgroundColor: const Color.fromARGB(255, 151, 208, 255),
            trailing: const Icon(Icons.arrow_drop_down, color: Colors.transparent),
            title: Stack(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 30),
                  child: iconDchange == false ?
                  const Icon(Icons.subject_rounded, color: Colors.white)
                  :
                  const Icon(Icons.menu_open_sharp, color: Colors.white)
                ),
                Container(
                  margin: const EdgeInsets.only(left: 60),
                  child: const Text(
                    'Product_Name', 
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.white
                    )
                  )
                )
              ]
            ),
            onExpansionChanged: (bool val) {
              setState(() {
                secondExpandeString = 'Product_Name';
                if (val == true) {
                  iconDchange = true;
                }
                else {
                  iconDchange = false;
                }
              });
            },
          ),
          ExpansionTile(
            backgroundColor: const Color.fromARGB(255, 151, 208, 255),
            trailing: const Icon(Icons.arrow_drop_down, color: Colors.transparent),
            title: Stack(
              children: [
                Container(
                  margin: const EdgeInsets.only(left: 30),
                  child: iconEchange == false ?
                  const Icon(Icons.subject_rounded, color: Colors.white)
                  :
                  const Icon(Icons.menu_open_sharp, color: Colors.white)
                ),
                Container(
                  margin: const EdgeInsets.only(left: 60),
                  child: const Text(
                    'Operation', 
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Colors.white
                    )
                  )
                )
              ]
            ),
            onExpansionChanged: (bool val) {
              setState(() {
                secondExpandeString = 'Operation';
                if (val == true) {
                  iconEchange = true;
                }
                else {
                  iconEchange = false;
                }
              });
            },
          )
        ],
      ));
    }
    return subListWidget;
  }

  Widget pageSummary() {
    return SingleChildScrollView(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          dataDetailFromList.isNotEmpty ?
            Container(
              margin: const EdgeInsets.only(top: 10),
              padding: const EdgeInsets.only(top: 5),
              height: 100,
              width: MediaQuery.of(context).size.width * 0.9,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.black)
              ),
              child: SingleChildScrollView(
                child: Column(
                  children: listWidgetDetail(dataDetailFromList)
                ),
              ),
            )
            :
            Center(
              child: SizedBox(
                width: 350,
                height: 350,
                child: Image.asset('images/FBN_CISCO_1.png')
              )
            ),
          // Chart YIELD ==================
          Visibility(
            visible: visibleChart,
            child: Container(
              margin: const EdgeInsets.only(left: 5, top: 5),
              padding: const EdgeInsets.all(5),
              width: MediaQuery.of(context).size.width * 0.975,
              height: MediaQuery.of(context).size.height * 0.4,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(5),
                boxShadow: const [
                  BoxShadow(
                    blurRadius: 10,
                    offset: Offset(1, 1),
                    color: Color.fromARGB(255, 219, 219, 219)
                  )
                ]
              ),
              child: Container(
                  decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(5),
                  color: Colors.white
                ),
                child: MixChartFBNYieldMultiLine(
                  dataBarChart: stackBarChartPerDT,
                  dataMultiLineChart: mapMultiLineChartPerOP,
                  xAxis: xAxis,
                  chartTitle: '$firstExpandeString : $secondExpandeString',
                )
              )
            )
          )
        ],
      )
    );
  }

  List<Widget> listWidgetDetail(List<String> data)  {
    List<Widget> subWidget = [];
    for (String val in data) {
      subWidget.add(Container(
        height: 20,
        width: MediaQuery.of(context).size.width * 0.88,
        margin: const EdgeInsets.only(bottom: 2),
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(0)
            )
          ),
          onPressed: () {
            setState(() {
              parameterSelected = val;
              tagQuery = 'queryYield';
              _refreshIndicatorKey.currentState?.show();
            });
          },
          child: Text(
            val,
            style: const TextStyle(
              fontSize: 12
            ),
          ),
        ),
      ));
    }
     return subWidget;
  } 

  // +++++++++++++++++++++++++++++++++++++++++++++++++ [Zone Query] +++++++++++++++++++++++++++++++++++++++++++++++++
  
  Future<void> listDetail() async {
    try {
      stringEncryptedArray = await encryptData([
        firstExpandeString, 
        secondExpandeString, 
        previousTS.toString()
      ]);

      var dataQueried = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/QueryListDetailCiscoOTBU',
        {
          'Parameter': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
          'Level': stringEncryptedArray['data'][1],
          'Date': stringEncryptedArray['data'][2],
        } 
      );

      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
        setState(() {
          if (decodedData.isNotEmpty) {
            dataDetailFromList = [];
            for (var i in decodedData) {
              dataDetailFromList.add(i[secondExpandeString]);
            }
          } 
          else {
            dataDetailFromList = [];
          }
        });
      }
      else {
        dataDetailFromList = [];
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

  Future<void> queryYield() async {
    try {
      stringEncryptedArray = await encryptData([
        (int.parse(selectedTS.split(' ')[0]) - 1).toString(), 
        selectedTS.split(' ')[1][0], 
        firstExpandeString,
        secondExpandeString,
        parameterSelected
      ]);

      var dataQueried = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/QueryYieldCiscoOTBU',
        {
          'Day': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
          'DayMode': stringEncryptedArray['data'][1],
          'Level': stringEncryptedArray['data'][2],
          'StepName': stringEncryptedArray['data'][3],
          'Parameter': stringEncryptedArray['data'][4],
        } 
      );

      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

        String modeDT = '';
        if (selectedTS.split(' ')[1][0] == 'D') {
          modeDT = 'DATE';
        }
        else if (selectedTS.split(' ')[1][0] == 'W') {
          modeDT = 'WEEK';
        }
        else if (selectedTS.split(' ')[1][0] == 'M') {
          modeDT = 'MONTH';
        }
        else if (selectedTS.split(' ')[1][0] == 'Q') {
          modeDT = 'QUARTER';
        }

        xAxis = [];
        stackBarChartPerDT = [];
        mapMultiLineChartPerOP = {};
        if (decodedData.isNotEmpty) {
          setState(() {
            List<String> dtJSON = [];
            for (var i in decodedData) {
              dtJSON.add(i[modeDT]);
            }
            Set<String> uniqueDates = Set<String>.from(dtJSON);
            dtJSON = uniqueDates.toList();
            // ================================== Sort DATE ==================================
            if (modeDT == 'DATE') {
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
              xAxis = dateTimes.map((dateTime) {
                final day = dateTime.day.toString().padLeft(2, '0');
                final month = getMonthAbbreviation(dateTime.month);
                final year = dateTime.year.toString();
                return '$day $month $year';
              }).toList();
            }
            // ================================== Sort WEEK ==================================
            if (modeDT == 'WEEK') {
              xAxis = dtJSON.toList()..sort((a, b) {
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
            if (modeDT == 'MONTH') {
              List<String> sortDatesDescending(List<String> dateStrings) {
                List<DateTime> dates = dateStrings.map((dateString) {
                  return DateFormat('MMM yyyy').parse(dateString);
                }).toList();

                dates.sort((a, b) => b.compareTo(a));

                List<String> xAxis = dates.map((date) {
                  return DateFormat('MMM yyyy').format(date);
                }).toList();

                return xAxis;
              }
              xAxis = sortDatesDescending(dtJSON);
            }
            // ================================== Sort QUARTER ==================================
            if (modeDT == 'QUARTER') {
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
              xAxis = sortQuarterYearsDescending(dtJSON);
            }
            xAxis = xAxis.reversed.toList();
            // ==================================================================================
            
            // =========================== Prepare data for stack Bar Chart ===========================
            Map<String, dynamic> groupStackBarChartPerDT = {};
            for (var i in decodedData) {
              if (!groupStackBarChartPerDT.containsKey(i[modeDT])) {
                groupStackBarChartPerDT[i[modeDT]] = [];
              }
              groupStackBarChartPerDT[i[modeDT]].add([i['Pass'], i['Fail']]);
            }
            
            Map<String, dynamic> sumStackBarChartPerDT = {};
            for (var item in groupStackBarChartPerDT.entries) {
              int sumPass = 0;
              int sumFail = 0;
              for (var value in item.value) {
                sumPass = sumPass + value[0] as int;
                sumFail = sumFail + value[1] as int;
              }
              sumStackBarChartPerDT[item.key] = [sumPass, sumFail];
            } 

            Map<String, dynamic> mapStackBarChartPerDT = {};
            for (var dt in xAxis) {
              mapStackBarChartPerDT[dt] = sumStackBarChartPerDT[dt];
            }
            stackBarChartPerDT = mapStackBarChartPerDT.values.toList();

            // =========================== Prepare data for Multiple Line Chart ===========================
            Map<String, dynamic> groupMultiLineChartPerOP = {};
            for (var i in decodedData) {
              if (!groupMultiLineChartPerOP.containsKey(i['Operation'])) {
                groupMultiLineChartPerOP[i['Operation']] = [];
              }
              groupMultiLineChartPerOP[i['Operation']].add([i[modeDT], i['FPY']]);
            }

            for (var item in groupMultiLineChartPerOP.entries) {
              List<String> subDT = [];
              for (var i in item.value) {
                subDT.add(i[0]);
              }

              List<double?> arr = [];
              for (var val in item.value) {
                for (var dt in xAxis) {
                  if (subDT.contains(dt)) {
                    arr.add(val[1]);
                  }
                  else {
                    arr.add(null);
                  }
                }
                break;
              }
              mapMultiLineChartPerOP[item.key] = arr;
            }
            visibleChart = true;
          });
        }
      }
      else {
        dataDetailFromList = [];
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