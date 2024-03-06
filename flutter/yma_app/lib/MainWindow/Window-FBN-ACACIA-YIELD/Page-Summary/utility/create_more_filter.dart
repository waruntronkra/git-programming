import 'package:flutter/material.dart';
import 'package:dropdown_button2/dropdown_button2.dart';
import 'dart:convert';
import 'package:cool_alert/cool_alert.dart';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;

typedef SendCMDFilter = void Function(String cmdFilter, int tagNumber);
class AddMoreFilter extends StatefulWidget {
  const AddMoreFilter({
    required this.levelSelected,
    required this.modelSelected,
    required this.startDate,
    required this.endDate,
    required this.sendCMDFilter,
    required this.number,
    Key? key
  }) : super(key: key);

  final String levelSelected;
  final String modelSelected;
  final String startDate;
  final String endDate;
  final SendCMDFilter sendCMDFilter;
  final int number;

  @override
  State<AddMoreFilter> createState() => _AddMoreFilterState();
}

class _AddMoreFilterState extends State<AddMoreFilter> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey = GlobalKey<RefreshIndicatorState>();   
  String defaultFilterString = '{No FIlter}';
  String filterSelected = '';
  List<String> itemFilter = [
    '{No FIlter}',
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
  List<String> filteredList = [];
  String cmdAddMoreFilter = '';
  List<bool> switchValues = [];

  bool checkBox = false;  
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
      child: Container(       
        margin: const EdgeInsets.all(8.0),
        padding: const EdgeInsets.all(8.0),
        width: 150,
        decoration: BoxDecoration(
          border: Border.all(color: Colors.black),
          borderRadius: BorderRadius.circular(8.0),
        ),
        child: Column(
          children: [
            // Filter ============================================
            Container(
              margin: const EdgeInsets.only(bottom: 5),
              width: 130,
              height: 30,
              child: DropdownButtonHideUnderline(
                child: DropdownButton2<String>(
                  isExpanded: true,
                  hint: Row(
                    children: [
                      Expanded(
                        child: Text(
                          defaultFilterString,
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
                  onChanged: (String? newVal) async {
                    setState(() {
                      defaultFilterString = newVal!;
                      if (defaultFilterString == itemFilter[0]) {
                        filterSelected = '{No FIlter}';
                      }
                      else if (defaultFilterString == itemFilter[1]) {
                        filterSelected = 'buildtype';
                      }
                      else if (defaultFilterString == itemFilter[2]) {
                        filterSelected = 'is_rework';
                      }
                      else if (defaultFilterString == itemFilter[3]) {
                        filterSelected = 'equip_id';
                      }
                      else if (defaultFilterString == itemFilter[4]) {
                        filterSelected = 'opn_des';
                      }
                      else if (defaultFilterString == itemFilter[5]) {
                        filterSelected = 'emp_no';
                      }
                      else if (defaultFilterString == itemFilter[6]) {
                        filterSelected = 'part_no';
                      }
                      else if (defaultFilterString == itemFilter[7]) {
                        filterSelected = 'runtype';
                      }
                      else if (defaultFilterString == itemFilter[8]) {
                        filterSelected = 'workorder';
                      }
                      else if (defaultFilterString == itemFilter[9]) {
                        filterSelected = 'pic_wf';
                      }
                      else if (defaultFilterString == itemFilter[10]) {
                        filterSelected = 'driver_lot';
                      }
                      else if (defaultFilterString == itemFilter[11]) {
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
                  ),
                )
              )
            ),
            // Show list queried from [Filter] =====================
            Container(
              width: 130,
              height: 100,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.black)
              ),
              child: SingleChildScrollView(
                child: Column(
                  children: [
                    const SizedBox(height: 2),
                    ...resultFilteredList(filteredList, switchValues)  
                  ],
                ),
              ),
            ),
            // Unselect list queried from [Filter] =====================
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Checkbox(
                    checkColor: Colors.white,
                    fillColor: MaterialStateProperty.resolveWith(colorCheckBox),
                    value: checkBox,
                    onChanged: (bool? val) {
                      setState(() {
                        if (val == true) {
                          checkBox = val!;
                          switchValues = [];
                          switchValues = List.filled(filteredList.length, false);
                        }
                        else {
                          checkBox = val!;
                          switchValues = [];
                          switchValues = List.filled(filteredList.length, true);
                        }
                      });
                    },
                  ),
                  const SizedBox(
                    height: 19,
                    child: Text(
                      'Unselect All', 
                      style: TextStyle(
                        fontSize: 12, 
                        fontWeight: FontWeight.bold
                      )
                    )
                  )
                ]
              )
            )
          ]
        )
      )
    );
  }

  List<Widget> resultFilteredList(List<String> data, List<bool> boolArray) {
    List<Widget> subList = [];
    for (var i = 0; i < data.length; i++) {
      subList.add(
        Container(
          decoration: BoxDecoration(
            border: Border.all(color: Colors.black)
          ),
          width: 115,
          height: 15,
          margin: const EdgeInsets.only(bottom: 2),
          child: RawMaterialButton(
            fillColor: switchValues[i] ? const Color.fromARGB(255, 3, 141, 93) : Colors.white,
            onPressed: () {
              setState(() {
                switchValues[i] = !switchValues[i];
                cmdAddMoreFilter = '';
                for (var idx = 0; idx < filteredList.length; idx++) {
                  if (boolArray[idx] == true) {
                    cmdAddMoreFilter += ",''${filteredList[idx]}''";
                  }
                }
                cmdAddMoreFilter = 'AND $filterSelected IN (${cmdAddMoreFilter.replaceFirst(RegExp(r','), '')})';
                widget.sendCMDFilter(cmdAddMoreFilter, widget.number);
              });
            },
            child: Text(
              data[i],
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 9,
                fontWeight: FontWeight.bold,
                color: switchValues[i] ? Colors.white : Colors.black,
              ),
            ),
          ),
        ),
      );
    }
    return subList;
  }

  // Query from Added Filter selected
  Future<void> queryByFilter() async {
    try {
      if (widget.levelSelected.isNotEmpty && widget.modelSelected.isNotEmpty && widget.startDate.isNotEmpty && widget.endDate.isNotEmpty) {
        if (filterSelected != '{No FIlter}') {
          Map<String, dynamic> stringEncryptedArray = await encryptData([
            widget.levelSelected,
            widget.modelSelected,
            widget.startDate,
            widget.endDate,
            filterSelected,
            'false',
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
              'Version' : stringEncryptedArray['data'][6]
            }                         
          );
          if (dataQueried[1] == 200) {
            String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

            final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
            final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

            String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
            List<Map<String, dynamic>> decodedDataAddedFilter = List<Map<String, dynamic>>.from(json.decode(decryptJson));
        
            setState(() {
              if (decodedDataAddedFilter.isNotEmpty) {
                filteredList = [];
                switchValues = [];
                cmdAddMoreFilter = '';
                for (var i in decodedDataAddedFilter) {
                  if (i[filterSelected] != null) {
                    filteredList.add(i[filterSelected]);
                    cmdAddMoreFilter += ",''${i[filterSelected]}''";
                  }
                }
                cmdAddMoreFilter = 'AND $filterSelected IN (${cmdAddMoreFilter.replaceFirst(RegExp(r','), '')})';
                widget.sendCMDFilter(cmdAddMoreFilter, widget.number);
                switchValues = List.filled(filteredList.length, true);
              }
            });
          }  
        }   
        else {
          setState(() {
            filteredList = [];
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

  @override
  void dispose() {
    super.dispose();
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