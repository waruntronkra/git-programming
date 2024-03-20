// ignore_for_file: file_names
import 'package:dropdown_button2/dropdown_button2.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cool_alert/cool_alert.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:YMM/MainWindow/Window-FBN-ACACIA-YIELD/Page-Summary/utility/create_more_filter.dart';

typedef SendMergedFilterCode = void Function(String text, String groupBySelected);
class WidgetsMoreFilter extends StatefulWidget {
  const WidgetsMoreFilter({
    required this.levelSelected,
    required this.modelSelected,
    required this.startDate,
    required this.endDate,
    required this.isChecked,
    required this.isCheckedColor,
    required this.isCheckedString,
    required this.sendMergedFilterCode,
    Key? key
  }) : super(key: key);

  final String levelSelected;
  final String modelSelected;
  final String startDate;
  final String endDate;
  final List<bool> isChecked;
  final List<Color> isCheckedColor;
  final List<String> isCheckedString;
  final SendMergedFilterCode sendMergedFilterCode;

  @override
  State<WidgetsMoreFilter> createState() => _WidgetsMoreFilterState();
}

class _WidgetsMoreFilterState extends State<WidgetsMoreFilter> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey = GlobalKey<RefreshIndicatorState>();   

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

  bool checkBox = false;
  List<bool> isCheckedFrom = [];
  List<Color> isCheckedColorFrom = [];
  List<String> isCheckedStringFrom = [];
  String stringFilterSelectedCode = '';

  List<String> listFilterSelectedFrom = [];

  int numberMoreFilterAdded = 0;
  String defaultAdMoreFilterString = '{No FIlter}';
  String addedFilterSelected = '';
  Map<int, dynamic> objectCMDFilter = {};
  String allCMDFilter = '';
  
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

  @override
  void initState() {
    isCheckedFrom = widget.isChecked;
    isCheckedColorFrom = widget.isCheckedColor;
    isCheckedStringFrom = widget.isCheckedString;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      key: _refreshIndicatorKey,
      displacement: 60,
      color: Colors.white,
      backgroundColor: const Color.fromARGB(255, 3, 141, 93),
      onRefresh: () async {
        await queryByFilter();
      },
      child: SingleChildScrollView(
        child: Column(
          children: [
            Center(
              child:SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Container(
                  margin: const EdgeInsets.only(left: 10),
                  child: Column(
                    children: [
                      Row(
                        children: [                 
                          // Label Group By ==================
                          Container(
                            height: 20,
                            padding: const EdgeInsets.only(top: 3),
                            alignment: Alignment.topLeft,
                            width: 75,
                            child: Text(
                              'Group By :', 
                              style: GoogleFonts.nunito(
                                fontSize: 12, 
                                fontWeight: FontWeight.bold
                              )
                            )
                          ),
                          // Group By ==================   
                          Container(
                            margin: const EdgeInsets.only(top: 10, bottom: 5),
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
                                        style: GoogleFonts.nunito(
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                          color: const Color.fromARGB(255, 3, 141, 93)
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
                                    style: GoogleFonts.nunito(
                                      fontSize: 11,
                                      color: const Color.fromARGB(255, 3, 141, 93)
                                    ),
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                )).toList(),
                                onChanged: (String? newVal) {
                                  setState(() {
                                    defaultGroupBy = newVal!;
                                    widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
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
                                )
                              )
                            )
                          )
                        ]
                      ),
                      Row(
                        children: [  
                          // Label Filter ==================
                          Container(
                            height: 20,
                            width: 50,
                            padding: const EdgeInsets.only(top: 3),
                            alignment: Alignment.topRight,
                            child: Text(
                              'Filter :', 
                              style: GoogleFonts.nunito(
                                fontSize: 12, 
                                fontWeight: FontWeight.bold
                              )
                            )
                          ),
                          // Filter ==================   
                          Container(
                            margin: const EdgeInsets.only(left: 7, top: 10, bottom: 5),
                            width: 140,
                            height: 30,
                            child: DropdownButtonHideUnderline(
                              child: DropdownButton2<String>(
                                isExpanded: true,
                                hint: Row(
                                  children: [
                                    Expanded(
                                      child: Text(
                                        defaultFilter,
                                        style: GoogleFonts.nunito(
                                          fontSize: 11,
                                          fontWeight: FontWeight.bold,
                                          color: const Color.fromARGB(255, 3, 141, 93)
                                        ),
                                        overflow: TextOverflow.ellipsis,
                                      )
                                    )
                                  ],
                                ),
                                items: itemFilter.map((String item) => DropdownMenuItem<String>(
                                  value: item,
                                  child: Text(
                                    item,
                                    style: GoogleFonts.nunito(
                                      fontSize: 11,
                                      color: const Color.fromARGB(255, 3, 141, 93)
                                    ),
                                    overflow: TextOverflow.ellipsis,
                                  )
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
                                    _refreshIndicatorKey.currentState?.show();
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
                                )
                              )
                            )
                          )
                        ]
                      )
                    ]
                  )
                )
              )
            ),
            SingleChildScrollView(
              child: Column(
                children: [
                  // Checkbox ========================================================================
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        Container(
                          margin: const EdgeInsets.only(left: 15),
                          child: Checkbox(
                            checkColor: Colors.white,
                            fillColor: MaterialStateProperty.resolveWith(colorCheckBox),
                            value: checkBox,
                            onChanged: (bool? val) {
                              setState(() {
                                checkBox = val!;
                                if (val == true) {
                                  isCheckedFrom = [];
                                  for (var i = 0; i < listFilterSelectedFrom.length; i++) {
                                    isCheckedFrom.add(false); 
                                    isCheckedColorFrom.add(const Color.fromARGB(255, 255, 255, 255)); 

                                    isCheckedStringFrom = [];
                                    for (var i = 0; i < listFilterSelectedFrom.length; i++) {
                                      isCheckedStringFrom.add('');
                                    }
                                    stringFilterSelectedCode = '';
                                    for (var i in isCheckedStringFrom) {
                                      if (i.isNotEmpty) {
                                        stringFilterSelectedCode += ",''$i''";
                                      }
                                    }
                                    stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
                                    widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
                                  }
                                }
                                else {
                                  isCheckedFrom = [];
                                  for (var i = 0; i < listFilterSelectedFrom.length; i++) {
                                    isCheckedFrom.add(true); 
                                    isCheckedColorFrom.add(const Color.fromARGB(255, 3, 141, 93)); 
                                  }

                                  isCheckedStringFrom = [];
                                  for (String val in listFilterSelectedFrom) {
                                    isCheckedStringFrom.add(val);
                                  }
                                  stringFilterSelectedCode = '';
                                  for (var i in isCheckedStringFrom) {
                                    if (i.isNotEmpty) {
                                      stringFilterSelectedCode += ",''$i''";
                                    }
                                  }
                                  stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
                                  widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
                                }
                              });
                            },
                          ),
                        ),
                        SizedBox(
                          height: 19,
                          child: Text(
                            'Unselect All', 
                            style: GoogleFonts.nunito(
                              fontSize: 12, 
                              fontWeight: FontWeight.bold
                            )
                          )
                        ),
                      ]
                    ),
                  ),
                  // Filter Result Queried ==================
                  Container(
                    width: MediaQuery.of(context).size.width * 0.88,
                    height: 100,
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.grey),
                      borderRadius: BorderRadius.circular(10)
                    ),
                    child: SingleChildScrollView(
                      child: Container(
                        margin: const EdgeInsets.only(top: 5, bottom: 3),
                        child: Column(
                          children: [                  
                            ...listPerFiltered(listFilterSelectedFrom),    
                          ]
                        ),
                      )
                    )
                  ),
                ],
              ),
            ),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Increase more filter ==========================
                  IconButton(
                    color: const Color.fromARGB(255, 3, 141, 93),
                    icon: const Icon(Icons.add_circle_rounded),
                    onPressed: () {
                      setState(() {
                        if (numberMoreFilterAdded <= 0) {
                          numberMoreFilterAdded = 0;
                        }
                        numberMoreFilterAdded++;
                      });
                    }
                  ),
                  const Text('Add more Filter'),
                  // Decrease more filter ==========================
                  IconButton(
                    color: const Color.fromARGB(255, 3, 141, 93),
                    icon: const Icon(Icons.delete_forever_rounded),
                    onPressed: () {
                      setState(() {
                        numberMoreFilterAdded--;
                        objectCMDFilter.remove(numberMoreFilterAdded);
                        allCMDFilter = '';
                        for (var item in objectCMDFilter.entries) {
                          allCMDFilter += '$allCMDFilter ${item.value}';
                        }
                        widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
                      });
                    }
                  ),
                  const Text('Delete Filter added'),
                ]
              )
            ),
            Container(
              margin: const EdgeInsets.only(left: 10),
              alignment: Alignment.center,
              child: Wrap(
                spacing: 1,
                children: addMoreFilter(numberMoreFilterAdded)
              )
            )
          ]
        )
      )
    );
  }

  List<Widget> listPerFiltered(List<String> data) {
    List<Widget> subList = [];
    if (data.isNotEmpty) {
      for (var i = 0; i < data.length; i++) {
        subList.add(Container(
          width: MediaQuery.of(context).size.width * 0.85,
          margin: const EdgeInsets.only(bottom: 3),
          height: 20,
          child : ElevatedButton(
            onPressed: () {
              setState(() {
                if (isCheckedFrom[i] == true) {
                  isCheckedFrom[i] = false;
                  isCheckedStringFrom[i] = '';
                }
                else {
                  isCheckedFrom[i] = true;
                  isCheckedStringFrom[i] = data[i];
                }

                stringFilterSelectedCode = '';
                for (var i in isCheckedStringFrom) {
                  if (i.isNotEmpty) {
                    stringFilterSelectedCode += ",''$i''";
                  }
                }
                stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
                widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
              });
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: isCheckedFrom[i] == true ? isCheckedColorFrom[i] : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(5)
              )
            ),
            child: Text(
              data[i],
              style: GoogleFonts.nunito(
                color: isCheckedFrom[i] == true ? Colors.white : Colors.black,
                fontSize: 11
              ),
            ),
          )
        ));
      }
    }
    return subList;
  }

  List<Widget> addMoreFilter(int quantity) {
    List<Widget> subList = [];
    for (int i = 0; i < quantity; i++) {
      subList.add(AddMoreFilter(
        levelSelected: widget.levelSelected,
        modelSelected: widget.modelSelected,
        startDate: widget.startDate,
        endDate: widget.endDate,
        sendCMDFilter: receiveCMDFilter,
        number: i,
      ));
    }
    return subList;
  }

  
  void receiveCMDFilter(String cmdFilter, int tagNumber) {
    if (!objectCMDFilter.containsKey(tagNumber)) {
      objectCMDFilter[tagNumber] = [];
    }
    objectCMDFilter[tagNumber] = cmdFilter;

    allCMDFilter = '';
    for (var item in objectCMDFilter.entries) {
      allCMDFilter += '$allCMDFilter ${item.value}';
    }
    widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
  }
  
  // Query from Filter selected
  Future<void> queryByFilter() async {
    try {
      setState(() {
        listFilterSelectedFrom = [];
      });
      if (widget.levelSelected.isNotEmpty && widget.modelSelected.isNotEmpty) {
        listFilterSelectedFrom = [];

        Map<String, dynamic> stringEncryptedArray = await encryptData([
          widget.levelSelected,
          widget.modelSelected,
          widget.startDate,
          widget.endDate,
          filterSelected,
          'true',
          '71'
        ]);
        
        var dataQueried = await getDataPOST(
          'https://supply-api.fabrinet.co.th/api/YMA/FbnYieldQueryFilter',
          {
            'Level': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
            'Model': stringEncryptedArray['data'][1],
            'From': stringEncryptedArray['data'][2],
            'To': stringEncryptedArray['data'][3],
            'Filter': stringEncryptedArray['data'][4],
            'IsFirstFilter' : stringEncryptedArray['data'][5],
            'Version': stringEncryptedArray['data'][6], 
          }                         
        );
        if (dataQueried[1] == 200) {
          String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

          final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
          final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

          String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
          List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
          
          listFilterSelectedFrom = [];
          for (var i in decodedData) {
            listFilterSelectedFrom.add(i['param']);
          }
          isCheckedFrom = [];
          isCheckedColorFrom = [];
          for (var i = 0; i < listFilterSelectedFrom.length; i++) {
            isCheckedFrom.add(true); 
            isCheckedColorFrom.add(const Color.fromARGB(255, 3, 141, 93)); 
          }

          isCheckedStringFrom = [];
          for (String val in listFilterSelectedFrom) {
            isCheckedStringFrom.add(val);
          }
          stringFilterSelectedCode = '';
          for (var i in isCheckedStringFrom) {
            if (i.isNotEmpty) {
              stringFilterSelectedCode += ",''$i''";
            }
          }
          setState(() {
            if (decodedData.isNotEmpty) {
              stringFilterSelectedCode = stringFilterSelectedCode.replaceFirst(RegExp(r','), '');
              widget.sendMergedFilterCode('AND $filterSelected IN ($stringFilterSelectedCode)$allCMDFilter', defaultGroupBy);
              listFilterSelectedFrom = listFilterSelectedFrom;
            }
            else {
              listFilterSelectedFrom = [];
            }
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