import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

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
      defaultColumnWidth: const FixedColumnWidth(90.0),
      border: TableBorder.all(color: const Color.fromARGB(255, 0, 0, 0)),
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
          style: GoogleFonts.nunito(
            fontSize: 12,
            color: const Color.fromARGB(255, 255, 255, 255),
            fontWeight: FontWeight.bold),
        ),
      ),
    )).toList();
  }

  List<TableRow> _buildTableRows() {
    return widget.dataTable.map((data) {
      return TableRow(
        children: data.asMap().entries.map((entry) {
          final columnIndex = entry.key;
          final cell = entry.value;
          return Center(
            child: Text(
              columnIndex == 3 && cell == 0 ? '' : '$cell',
              style: GoogleFonts.nunito(
                fontSize: 12,
                color: columnIndex == 3 ? Colors.red : Colors.black,
              ),
              textAlign: TextAlign.center,
            ),
          );
        }).toList(),
      );
    }).toList();
  }
}
