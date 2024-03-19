import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class MetrixTable extends StatefulWidget {
  const MetrixTable({
    required this.dataTable,
    required this.columnName,
    required this.customizeFontColor,
    required this.colHeadColor,
    Key? key,
  }) : super(key: key);

  final List<List<dynamic>> dataTable;
  final List<String> columnName;
  final bool customizeFontColor;
  final Color colHeadColor;

  @override
  State<MetrixTable> createState() => _MetrixTableState();
}

class _MetrixTableState extends State<MetrixTable> {
  @override
  Widget build(BuildContext context) {
    return Table(
      defaultColumnWidth: const FixedColumnWidth(75.0),
      border: TableBorder.all(color: const Color.fromARGB(255, 0, 0, 0)),
      defaultVerticalAlignment: TableCellVerticalAlignment.middle,
      children: [
        TableRow(
          decoration: BoxDecoration(
            color: widget.colHeadColor,
          ),
          children: _buildTableColumns(),
        ),
        ..._buildTableRows(),
      ],
    );
  }

  List<Widget> _buildTableColumns() {
    return widget.columnName.map((col) => SizedBox(
      height: 40,
      child: Center(
        child: Text(
          col,
          textAlign: TextAlign.center,
          style: GoogleFonts.nunito(
            fontSize: 10.5,
            color: const Color.fromARGB(255, 0, 0, 0),
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    )).toList();
  }

  List<TableRow> _buildTableRows() {
    return widget.dataTable.map((data) {
      return TableRow(
        children: data.map((cell) {
          return GestureDetector(
            onLongPress: () {
              _showFullTextDialog(context, cell);
            },
            child: Center(
              child: Container(
                padding: const EdgeInsets.all(5),
                child: Text(
                  '$cell',
                  style: GoogleFonts.nunito(
                    fontSize: 11,
                    color: widget.customizeFontColor == true ?
                    cell == 'PASS' ? const Color.fromARGB(255, 3, 141, 93) : Colors.red
                    :
                    Colors.black
                  ),
                  textAlign: TextAlign.center,
                  softWrap: false, // Set softWrap to false
                )
              )
            ),
          );
        }).toList(),
      );
    }).toList();
  }

  void _showFullTextDialog(BuildContext context, String fullText) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.black)
                ),
                width: 200,
                padding: const EdgeInsets.all(5),
                margin: const EdgeInsets.only(top: 5),
                child: Text(
                  fullText,
                  textAlign: TextAlign.center,
                  style: GoogleFonts.nunito(
                    color: widget.customizeFontColor == true ?
                    fullText == 'PASS' ? const Color.fromARGB(255, 3, 141, 93) : Colors.red
                    :
                    Colors.black,
                    fontSize: 13,
                    fontWeight: FontWeight.bold
                  )
                )
              )
            ]
          )
        );
      },
    );
  }

}
