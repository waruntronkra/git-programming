import 'package:flutter/material.dart';

class RowHeadMetrixTable extends StatefulWidget {
  const RowHeadMetrixTable({
    required this.dataTable,
    required this.columnName,
    required this.dataColor,
    required this.colHeadColor,
    Key? key,
  }) : super(key: key);

  final List<String> dataTable;
  final List<String> columnName;
  final Color dataColor;
  final Color colHeadColor;

  @override
  State<RowHeadMetrixTable> createState() => _RowHeadMetrixTableState();
}

class _RowHeadMetrixTableState extends State<RowHeadMetrixTable> {
  @override
  Widget build(BuildContext context) {
    return Table(
      defaultColumnWidth: const FixedColumnWidth(60.0),
      border: TableBorder.all(color: const Color.fromARGB(255, 0, 0, 0)),
      defaultVerticalAlignment: TableCellVerticalAlignment.middle,
      children: [
        TableRow(
          decoration: const BoxDecoration(
            color: Colors.transparent
          ),
          children: _buildTableColumns(),
        ),
        ..._buildTableRows(),
      ],
    );
  }

  List<Widget> _buildTableColumns() {
    return widget.columnName.map((col) => Container(
      color: widget.colHeadColor,
      height: 40,
      child: Center(
        child: Text(
          col,
          textAlign: TextAlign.center,
          style: const TextStyle(
            fontSize: 11,
            color: Color.fromARGB(255, 0, 0, 0),
            fontWeight: FontWeight.bold
          ),
        ),
      ),
    )).toList();
  }

  List<TableRow> _buildTableRows() {
    return widget.dataTable.map((data) {
      return TableRow(
        children: List.generate(widget.columnName.length, (index) {
          return Container(
            padding: const EdgeInsets.all(5),
            color: widget.dataColor,
            child: Text(
              data,
              style: const TextStyle(
                fontSize: 12,
                color: Colors.black,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
              ),
          );
        }),
      );
    }).toList();
  }
}
