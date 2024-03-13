import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class TableHistogram extends StatefulWidget {
  const TableHistogram({
    required this.tableData,
    Key? key,
  }) : super(key: key);

  final Map<String, dynamic> tableData;

  @override
  State<TableHistogram> createState() => _TableHistogramState();
}

class _TableHistogramState extends State<TableHistogram> {
  late List<String> arrayToTable;

  @override
  void initState() {
    super.initState();
    arrayToTable = widget.tableData.values.map((value) => value.toString()).toList();
  }

  @override
  Widget build(BuildContext context) {
    return DataTable(
      columns: _buildColumns(),
      rows: _buildRows(),
      border: TableBorder.all(color: const Color.fromARGB(255, 0, 0, 0)),
      // ignore: deprecated_member_use
      dataRowHeight: 20,
    );
  }

  List<DataColumn> _buildColumns() {
    return widget.tableData.keys.map<DataColumn>((String key) {
      return DataColumn(
        label: SizedBox(
          width: 85.0,
          child: Text(
            key,
            style: GoogleFonts.nunito(
              fontSize: 12,
              color: Color.fromARGB(255, 3, 141, 93),
            ),
          ),
        ),
      );
    }).toList();
  }

  List<DataRow> _buildRows() {
    List<DataRow> rows = [];
    int rowCount = widget.tableData.values.first.length;
    for (int i = 0; i < rowCount; i++) {
      List<DataCell> cells = widget.tableData.entries.map<DataCell>((entry) {
        return DataCell(
          Text(
            entry.value[i].toString(),
            style: GoogleFonts.nunito(
                fontSize: 12
            ),
          ),
        );
      }).toList();
      rows.add(DataRow(cells: cells));
    }
    return rows;
  }


}
