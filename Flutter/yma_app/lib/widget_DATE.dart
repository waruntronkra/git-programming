// ignore_for_file: file_names

import 'package:flutter/material.dart';
import 'package:dropdown_button2/dropdown_button2.dart';

typedef FetchData = void Function(String selectedValue);
class WidgetDate extends StatefulWidget {
  const WidgetDate ({
    required this.fetchData, 
    required this.levelSelected,
    required this.modelSelected,
    Key? key
  }) : super(key: key);

  final FetchData fetchData;
  final String levelSelected;
  final String modelSelected;

  @override
  State<WidgetDate> createState() => _WidgetDateState();
}

class _WidgetDateState extends State<WidgetDate> {
  var itemsDay = [
    '2 Days',
    '3 Days',
    '4 Days',
    '5 Days',
    '6 Days',
    '7 Days',
    '10 Days',
    '15 Days',
    '20 Days',
    '30 Days',
  ];
  var itemsWeek = [
    '1 Week',
    '2 Weeks',
    '3 Weeks',
    '4 Weeks',
    '6 Weeks',
    '8 Weeks',
    '12 Weeks',
    '13 Weeks',
    '15 Weeks',
    '20 Weeks',
  ];
  var itemsMonth = [
    '1 Month',
    '2 Months',
    '3 Months',
    '4 Months',
    '5 Months',
    '6 Months',
    '8 Months',
    '10 Months',
    '12 Months',
    '18 Months',
  ];
  var itemsQuarter = [
    '1 Quarter',
    '2 Quarters',
    '3 Quarters',
    '4 Quarters',
    '6 Quarters',
    '8 Quarters',
  ];

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Day DropDown =================================
          Container(
            margin: const EdgeInsets.only(left: 13, top: 10),
            width: 80,
            height: 40,
            child: DropdownButtonHideUnderline(
              child: DropdownButton2<String>(
                isExpanded: true,
                hint: const Row(
                  children: [
                    Expanded(
                      child: Text(
                        'DAY',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    )
                  ],
                ),
                items: itemsDay.map((String item) => DropdownMenuItem<String>(
                  value: item,
                  child: Text(
                    item,
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color.fromARGB(255, 3, 141, 93)
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                )).toList(),
                onChanged: (String? newVal) {
                  setState(() {
                    if (widget.levelSelected != '' && widget.modelSelected != '') {
                      widget.fetchData(newVal.toString());
                    }
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
                  width: 78,
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
          // Week DropDown =================================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 10),
            width: 90,
            height: 40,
            child: DropdownButtonHideUnderline(
              child: DropdownButton2<String>(
                isExpanded: true,
                hint: const Row(
                  children: [
                    Expanded(
                      child: Text(
                        'WEEK',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    )
                  ],
                ),
                items: itemsWeek.map((String item) => DropdownMenuItem<String>(
                  value: item,
                  child: Text(
                    item,
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color.fromARGB(255, 3, 141, 93)
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                )).toList(),
                onChanged: (String? newVal) {
                  setState(() {
                    if (widget.levelSelected != '' && widget.modelSelected != '') {
                      widget.fetchData(newVal.toString());
                    }
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
                  width: 88,
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
              ),
            ),
          ),
          // Month DropDown =================================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 10),
            width: 105,
            height: 40,
            child: DropdownButtonHideUnderline(
              child: DropdownButton2<String>(
                isExpanded: true,
                hint: const Row(
                  children: [
                    Expanded(
                      child: Text(
                        'MONTH',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    )
                  ],
                ),
                items: itemsMonth.map((String item) => DropdownMenuItem<String>(
                  value: item,
                  child: Text(
                    item,
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color.fromARGB(255, 3, 141, 93)
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                )).toList(),
                onChanged: (String? newVal) {
                  setState(() {
                    if (widget.levelSelected != '' && widget.modelSelected != '') {
                      widget.fetchData(newVal.toString());
                    }
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
                  width: 103,
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
              ),
            ),
          ),
          // Quarter DropDown =================================
          Container(
            margin: const EdgeInsets.only(left: 10, top: 10),
            width: 110,
            height: 40,
            child: DropdownButtonHideUnderline(
              child: DropdownButton2<String>(
                isExpanded: true,
                hint: const Row(
                  children: [
                    Expanded(
                      child: Text(
                        'QUARTER',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Color.fromARGB(255, 3, 141, 93)
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    )
                  ],
                ),
                items: itemsQuarter.map((String item) => DropdownMenuItem<String>(
                  value: item,
                  child: Text(
                    item,
                    style: const TextStyle(
                      fontSize: 13,
                      color: Color.fromARGB(255, 3, 141, 93)
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                )).toList(),
                onChanged: (String? newVal) {
                  setState(() {
                    if (widget.levelSelected != '' && widget.modelSelected != '') {
                      widget.fetchData(newVal.toString());
                    }
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
                  width: 108,
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
    );
  }
}