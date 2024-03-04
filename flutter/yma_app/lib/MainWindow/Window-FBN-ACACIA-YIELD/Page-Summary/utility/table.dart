import 'package:flutter/material.dart';

class TableFBNYIELD extends StatefulWidget {
  const TableFBNYIELD({
    required this.dataTable,
    required this.columnName,
    Key? key,
  }) : super(key: key);

  final List<List<dynamic>> dataTable;
  final List<String> columnName;

  @override
  State<TableFBNYIELD> createState() => _TableFBNYIELDState();
}

class _TableFBNYIELDState extends State<TableFBNYIELD> {
  @override
  Widget build(BuildContext context) {
    return Table(
      defaultColumnWidth: const FixedColumnWidth(100.0),
      border: TableBorder.all(color: Colors.grey),
      defaultVerticalAlignment: TableCellVerticalAlignment.middle,
      children: [
        TableRow(
          decoration: const BoxDecoration(
            color: Color.fromARGB(255, 3, 141, 93)
          ),
          children: _buildTableColumns(),
        ),
        ..._buildTableRows(),
      ],
    );
  }

  List<Widget> _buildTableColumns() {
    return widget.columnName.map((col) => SizedBox(
      height: 25,
      child: Center(
        child: Text(
          col,
          style: const TextStyle(
            fontSize: 12,
            color: Color.fromARGB(255, 255, 255, 255),
            fontWeight: FontWeight.bold),
        ),
      ),
    )).toList();
  }

  List<TableRow> _buildTableRows() {
    return widget.dataTable.map((data) {
      return TableRow(
        children: data.asMap().entries.map((entry) {
          // final columnIndex = entry.key;
          final cell = entry.value;
          return Center(
            child: Container(
              padding: const EdgeInsets.only(left: 5, right: 5),
              child: Text(
                '$cell',
                style: const TextStyle(
                  fontSize: 11,
                  color: Colors.black,
                ),
                textAlign: TextAlign.center,
              )
            ),
          );
        }).toList(),
      );
    }).toList();
  }
}
