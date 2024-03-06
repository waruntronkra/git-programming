import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'dart:convert';
import 'package:cool_alert/cool_alert.dart';
import 'package:dropdown_button2/dropdown_button2.dart';
import '../Page-Result-Test/Metrix-Table/metrix_table.dart';
import '../Page-Result-Test/Metrix-Table/row_head_metrix_table.dart';
import 'package:YMs/Widget/widget_DATE.dart';

class TabResultTest extends StatefulWidget {
  const TabResultTest({super.key});

  @override
  State<TabResultTest> createState() => _TabResultTestState();
}

class _TabResultTestState extends State<TabResultTest> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey = GlobalKey<RefreshIndicatorState>();   

  List<List<dynamic>> dataToTable = [];
  List<String> columnNameDate = [];
  List<String> rowNameSlot = [];

  List<List<List<dynamic>>> dataToTableArr = [];
  List<List<String>> columnNameDateArr = [];
  List<String> slotArray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'];
  List<String> stationArray = [
    'ATE_400ZR_242',
    'ATE_400ZR_243',
    'ATE_400ZR_249',
    'ATE_400ZR_267',
    'ATE_400ZR_271',
    'ATE_400ZR_273',
    'ATE_400ZR_293',
    'ATE_400ZR_294',
    'ATE_400ZR_297',
    'ATE_400ZR_298',
    'ATE_400ZR_302',
    'ATE_400ZR_304',
    'ATE_400ZR_319',
  ];
  List<String> processArry = ['FCAL', 'OPM', 'OPMP', 'OPMT', 'EXP', 'EXS'];
  String defaultProduct = 'Product';
  List<String> levelNameSorted = [];

  Map<String, dynamic> stringEncryptedArray = {};
  int selectedRadio = 0;

  @override
  void initState() {
    fetchDataLevel();
    super.initState();
  }

  @override 
  Widget build(BuildContext context) {
    return RefreshIndicator(
      key: _refreshIndicatorKey,
      displacement: 60,
      color: Colors.white,
      backgroundColor: Colors.orange,
      onRefresh: () async {
        await queryResultTest();
      },
      child: SingleChildScrollView(
        child: Column(
          children: [
            // DATE dropdown =================================
            Container(
              alignment: Alignment.center,
              width: MediaQuery.of(context).size.width * 0.97,
              height: 55,
              child: WidgetDate(
                fetchData: updateDaySlected,
                levelSelected: '.',
                modelSelected: '.',
                colorBase: Colors.orange,
              ),
            ),
            // Product dropdown =================================
            Center(
              child: Container(
                margin: const EdgeInsets.only(left: 13, top: 10, bottom: 5),
                width: 200,
                height: 40,
                child: DropdownButtonHideUnderline(
                  child: DropdownButton2<String>(
                    isExpanded: true,
                    hint: Row(
                      children: [
                        Expanded(
                          child: Text(
                            defaultProduct,
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: Colors.orange
                            ),
                            overflow: TextOverflow.ellipsis,
                          ),
                        )
                      ],
                    ),
                    items: levelNameSorted.map((String item) => DropdownMenuItem<String>(
                      value: item,
                      child: Text(
                        item,
                        style: const TextStyle(
                          fontSize: 13,
                          color: Colors.orange
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    )).toList(),
                    onChanged: (String? newVal) {
                      setState(() {
                        defaultProduct = newVal!;
                        // Do something...
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
                      openInterval: const Interval(.25, 1),
                      maxHeight: 200,
                      width: 198,
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
            ),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _refreshIndicatorKey.currentState?.show();
                });
              },
              child: const Text('REFRESH'),
            ),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Radio(
                    value: 0,
                    activeColor: Colors.orange,
                    groupValue: selectedRadio,
                    onChanged: (value) {
                      setState(() {
                        selectedRadio = value!;
                        dataToTableArr = [];
                        columnNameDateArr= [];
                        stationArray = [
                          'ATE_400ZR_242',
                          'ATE_400ZR_247',
                          'ATE_400ZR_251',
                          'ATE_400ZR_267',
                          'ATE_400ZR_272',
                          'ATE_400ZR_278'
                        ];
                        _refreshIndicatorKey.currentState?.show();
                      });
                    },
                  ),
                  const Text('FCAL'),

                  Radio(
                    value: 1,
                    activeColor: Colors.orange,
                    groupValue: selectedRadio,
                    onChanged: (value) {
                      setState(() {
                        selectedRadio = value!;
                        dataToTableArr = [];
                        columnNameDateArr= [];
                        stationArray = [
                          'ATE_400ZR_242',
                          'ATE_400ZR_243',
                          'ATE_400ZR_249',
                          'ATE_400ZR_267',
                          'ATE_400ZR_271',
                          'ATE_400ZR_273',
                          'ATE_400ZR_293',
                          'ATE_400ZR_294',
                          'ATE_400ZR_297',
                          'ATE_400ZR_298',
                          'ATE_400ZR_302',
                          'ATE_400ZR_304',
                          'ATE_400ZR_319'
                        ];
                        _refreshIndicatorKey.currentState?.show();
                      });
                    },
                  ),
                  const Text('OPM'),

                  Radio(
                    value: 2,
                    activeColor: Colors.orange,
                    groupValue: selectedRadio,
                    onChanged: (value) {
                      setState(() {
                        selectedRadio = value!;
                        dataToTableArr = [];
                        columnNameDateArr= [];
                        stationArray = [
                          'ATE_400ZR_242',
                          'ATE_400ZR_243',
                          'ATE_400ZR_249',
                          'ATE_400ZR_267',
                          'ATE_400ZR_271',
                          'ATE_400ZR_273',
                          'ATE_400ZR_293',
                          'ATE_400ZR_294',
                          'ATE_400ZR_297',
                          'ATE_400ZR_298',
                          'ATE_400ZR_302',
                          'ATE_400ZR_304',
                          'ATE_400ZR_319'
                        ];
                        _refreshIndicatorKey.currentState?.show();
                      });
                    },
                  ),
                  const Text('OPMP'),

                  Radio(
                    value: 3,
                    activeColor: Colors.orange,
                    groupValue: selectedRadio,
                    onChanged: (value) {
                      setState(() {
                        selectedRadio = value!;
                        dataToTableArr = [];
                        columnNameDateArr= [];
                        stationArray = [
                          'ATE_400ZR_242',
                          'ATE_400ZR_243',
                          'ATE_400ZR_249',
                          'ATE_400ZR_267',
                          'ATE_400ZR_271',
                          'ATE_400ZR_273',
                          'ATE_400ZR_293',
                          'ATE_400ZR_294',
                          'ATE_400ZR_297',
                          'ATE_400ZR_298',
                          'ATE_400ZR_302',
                          'ATE_400ZR_304',
                          'ATE_400ZR_319'
                        ];
                        _refreshIndicatorKey.currentState?.show();
                      });
                    },
                  ),
                  const Text('OPMT'),

                  Radio(
                    value: 4,
                    activeColor: Colors.orange,
                    groupValue: selectedRadio,
                    onChanged: (value) {
                      setState(() {
                        selectedRadio = value!;
                        dataToTableArr = [];
                        columnNameDateArr= [];
                        stationArray = [
                          'ATE_400ZR_262',
                          'ATE_400ZR_280',
                          'ATE_400ZR_305',
                          'ATE_400ZR_306',
                          'ATE_400ZR_316',
                          'ATE_400ZR_330'
                        ];
                        _refreshIndicatorKey.currentState?.show();
                      });
                    },
                  ),
                  const Text('EXP'),

                  Radio(
                    value: 5,
                    activeColor: Colors.orange,
                    groupValue: selectedRadio,
                    onChanged: (value) {
                      setState(() {
                        selectedRadio = value!;
                        dataToTableArr = [];
                        columnNameDateArr= [];
                        stationArray = [
                          'ATE_400ZR_262',
                          'ATE_400ZR_280',
                          'ATE_400ZR_305',
                          'ATE_400ZR_306',
                          'ATE_400ZR_316',
                          'ATE_400ZR_330'
                        ];
                        _refreshIndicatorKey.currentState?.show();
                      });
                    },
                  ),
                  const Text('EXS'),
                ]
              )   
            ),      
            ...createListTable(dataToTableArr, columnNameDateArr),
            const SizedBox(height: 50)
          ],
        )
      )
    );
  }

  void updateDaySlected(String day) {
    print(day);
    queryProcessStation();
  }

  List<Widget> listProcessProduct (List<String> processArray) {
    List<Widget> subWidget = [];
    for (var i = 0; i < processArry.length; i++) {
      subWidget.add(Row(
        children: [
          Radio(
            value: 0,
            activeColor: Colors.orange,
            groupValue: selectedRadio,
            onChanged: (value) {
              setState(() {
                selectedRadio = value!;
                dataToTableArr = [];
                columnNameDateArr= [];
                stationArray = [
                  'ATE_400ZR_242',
                  'ATE_400ZR_247',
                  'ATE_400ZR_251',
                  'ATE_400ZR_267',
                  'ATE_400ZR_272',
                  'ATE_400ZR_278'
                ];
                // _refreshIndicatorKey.currentState?.show();
              });
            },
          ),
          Text(processArry[i]),
        ]
      ));
    }
    return subWidget;
  }

  // ================================ Query Result Test ================================
  Future<void> queryResultTest() async {
    try {
      for (String station in stationArray) {
        stringEncryptedArray = await encryptData(['2', station, processArry[selectedRadio]]);
        var result = await getDataPOST(
          'https://supply-api.fabrinet.co.th/api/YMA/QueryResultTest',
          {
          'Day': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
          'Station': stringEncryptedArray['data'][1],
          'Process': stringEncryptedArray['data'][2],
          } 
        );
        String jsonEncrypted = jsonDecode(jsonDecode(result[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

        // Group by SLOT =========================
        Map<String, dynamic> groupResultTestBySlot = {};
        columnNameDate = [];
        for (var item in decodedData) {
          if (!groupResultTestBySlot.containsKey(item['TEST_SOCKET_INDEX'].toString())) {
            groupResultTestBySlot[item['TEST_SOCKET_INDEX'].toString()] = [];
          }
          groupResultTestBySlot[item['TEST_SOCKET_INDEX'].toString()].add([
            item['LOCAL_START_DATE_TIME'],
            item['FAIL_MODE'],
          ]);
          columnNameDate.add(item['LOCAL_START_DATE_TIME'].substring(0, item['LOCAL_START_DATE_TIME'].length - 4));
        }
        columnNameDate = columnNameDate.toSet().toList();

        // Group by DATE =========================
        Map<String, dynamic> groupResultTestByDate = {};
        for (var item in groupResultTestBySlot.entries) {
          List<String> subDt = [];
          for (var i in item.value) {
            subDt.add(i[0].substring(0, i[0].length - 4));
          }
          List<String> subValue = [];
          for (var i in item.value) {
            subValue.add(i[1]);
          }
          for (var j = 0; j < columnNameDate.length; j++) {
            if (subDt.contains(columnNameDate[j])) {
              if (!groupResultTestByDate.containsKey(item.key)) {
                groupResultTestByDate[item.key] = [];
              }
              groupResultTestByDate[item.key].add(subValue[subDt.indexOf(columnNameDate[j])]);
            }
            else {
              if (!groupResultTestByDate.containsKey(item.key)) {
                groupResultTestByDate[item.key] = [];
              }
              groupResultTestByDate[item.key].add('');
            }
          }
        }

        // Group follow by SLOT quantity =========================
        Map<String, dynamic> groupResultCompletely = {};
        
        rowNameSlot = [];
        for (var i in slotArray) {
          rowNameSlot.add('SLOT $i');
        }

        for (var i in slotArray) {
          if (!groupResultCompletely.containsKey(i)) {
            groupResultCompletely[i.toString()] = [];
          }

          List<String> subSlots = [];
          for (var item in groupResultTestByDate.entries) {
            subSlots.add(item.key);
          }
          List<dynamic> subValues = [];
          for (var item in groupResultTestByDate.entries) {
            subValues.add(item.value);
          }

          // ignore: unused_local_variable
          for (var item in groupResultTestByDate.entries) {
            if (subSlots.contains(i)) {
              groupResultCompletely[i.toString()] = subValues[subSlots.indexOf(i)];
            }
            else {
              List<String> emptyArray = [];
              for (var x = 0; x < columnNameDate.length; x++) {
                emptyArray.add('');
              }
              groupResultCompletely[i.toString()] = emptyArray;
            }
            break;
          }
        }

        // Prepare to Table =========================
        dataToTable = [];
        for (var item in groupResultCompletely.entries) {
          dataToTable.add(item.value);
        }
        dataToTableArr.add(dataToTable);
        columnNameDateArr.add(columnNameDate);

        await Future.delayed(const Duration(milliseconds: 500));
      }

      setState(() {
        dataToTableArr = dataToTableArr;
        columnNameDateArr = columnNameDateArr;
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

  Future<void> queryProcessStation() async {
    try {
      stringEncryptedArray = await encryptData([
        '10', 
        '400ZR'
      ]);
      var result = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/QueryProssStation',
        {
        'Day': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
        'Product': stringEncryptedArray['data'][1],
        } 
      );
      String jsonEncrypted = jsonDecode(jsonDecode(result[0]))['encryptedJson'];

      final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
      final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

      String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
      List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
      print(decodedData);
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

  List<Widget> createListTable(List<List<List<dynamic>>> dataToTableArr, List<List<String>> columnNameArr) {
    List<Widget> subWidget = [];
    if (dataToTableArr.isNotEmpty) {
      for (var i = 0; i < dataToTableArr.length; i++) {
        subWidget.add(Stack(
          children: [
            Container(
              alignment: Alignment.topLeft,
              margin: const EdgeInsets.only(left: 10),
              child: Text(
                stationArray[i],
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold
                ),
              ),
            ),
            Container(
              width: MediaQuery.of(context).size.width * 0.95,
              margin: const EdgeInsets.only(left: 10, top: 10),
              child: Row(
                children: [
                  RowHeadMetrixTable(
                    dataTable: rowNameSlot, 
                    columnName: const ['DATA\nPROCESS'],
                    dataColor: const Color.fromARGB(137, 239, 205, 132),
                    colHeadColor: Colors.white,
                  ),
                  SizedBox(
                    width: MediaQuery.of(context).size.width * 0.8,
                    height: 250,
                    child: SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          columnNameArr[i].isNotEmpty ? 
                          MetrixTable(
                            dataTable: dataToTableArr[i],
                            columnName: columnNameArr[i],
                            customizeFontColor: true,
                            colHeadColor: const Color.fromARGB(255, 172, 223, 255),
                          ) : const SizedBox(width: 10)
                        ]
                      )
                    )
                  )
                ]
              )
            )
          ]
        ));
      }
    }
    return subWidget;
  }

  // ========================= Query [LEVEL] =========================
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

      levelNameSorted = [];
      if (productName[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(productName[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

        for (var element in decodedData) {
          if (!levelNameSorted.contains(element['Level'])) {
            levelNameSorted.add(element['Level']);
          }
        }
      }

      setState(() {
        levelNameSorted = levelNameSorted;
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