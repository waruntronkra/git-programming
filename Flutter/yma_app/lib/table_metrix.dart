import 'package:flutter/material.dart';
import 'package:flutter_table/table_sticky_headers.dart';

class MyMetrixTable extends StatelessWidget {
  const MyMetrixTable({
        required this.data, 
        required this.titleColumn, 
        required this.titleRow,
        Key? key
  }) : super(key: key);
  
  final List<List<String>> data;
  final List<String> titleColumn;
  final List<String> titleRow;

  @override
  Widget build(BuildContext context) {
    TextStyle contentCellStyle = const TextStyle(
      fontSize: 12,
      fontWeight: FontWeight.normal,
      color: Colors.black,
    );

    TextStyle headerCellStyle = const TextStyle(
      fontSize: 12,
      fontWeight: FontWeight.bold,
      color: Color.fromARGB(255, 0, 0, 0),
    );

    return Scaffold(
      body: StickyHeadersTable(
        columnsLength: titleColumn.length,
        rowsLength: titleRow.length,
        columnsTitleBuilder: (i) => TableCell.stickyRow(
          titleColumn[i],
          textStyle: headerCellStyle,
          rowIndex: 0,
          columnIndex: i,
          rowHeadText: titleColumn[i],
          colHeadText: '',
        ),
        rowsTitleBuilder: (i) => TableCell.stickyColumn(
          titleRow[i],
          textStyle: headerCellStyle,
          rowIndex: i,
          columnIndex: 0,
          rowHeadText: titleRow[i],
          colHeadText: '',
        ),
        contentCellBuilder: (i, j) => TableCell.content(
          data[j][i],
          textStyle: contentCellStyle,
          rowIndex: j,
          columnIndex: i,
          rowHeadText: titleRow[j],
          colHeadText: titleColumn[i],
        ),
        legendCell: TableCell.legend(
          'DATE\nPROCESS',
          textStyle: headerCellStyle,
          rowIndex: 0,
          columnIndex: 0,
          rowHeadText: '',
          colHeadText: '',
        ),
      ),
    );
  }
}

class TableCell extends StatefulWidget {
  // +++++++++++ body +++++++++++
  TableCell.content(
    this.text, {
    this.textStyle,
    this.cellDimensions = CellDimensions.base,
    this.colorBg = Colors.white,
    this.onTap,
    required this.rowIndex,
    required this.columnIndex,
    required this.rowHeadText,
    required this.colHeadText,
  })  : cellWidth = cellDimensions.contentCellWidth,
        cellHeight = cellDimensions.contentCellHeight,
        _colorHorizontalBorder = const Color.fromARGB(255, 15, 2, 2),
        _colorVerticalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _textAlign = TextAlign.left,
        _padding = EdgeInsets.zero;

  // +++++++++++ Column Header +++++++++++
  TableCell.stickyRow(
    this.text, {
    this.textStyle,
    this.cellDimensions = CellDimensions.base,
    this.colorBg = const Color.fromARGB(255, 165, 255, 180),
    this.onTap,
    required this.rowIndex,
    required this.columnIndex,
    required this.rowHeadText,
    required this.colHeadText,
  })  : cellWidth = cellDimensions.stickyLegendWidth,
        cellHeight = cellDimensions.stickyLegendHeight,
        _colorHorizontalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _colorVerticalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _textAlign = TextAlign.center,
        _padding = EdgeInsets.zero;
  
  // +++++++++++ top-left +++++++++++
  TableCell.legend(
    this.text, {
    this.textStyle,
    this.cellDimensions = CellDimensions.base,
    this.colorBg = const Color.fromARGB(255, 255, 136, 0),
    this.onTap,
    required this.rowIndex,
    required this.columnIndex,
    required this.rowHeadText,
    required this.colHeadText,
  })  : cellWidth = 120,
        cellHeight = cellDimensions.stickyLegendHeight,
        _colorHorizontalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _colorVerticalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _textAlign = TextAlign.center,
        _padding = EdgeInsets.zero;

  // +++++++++++ Row Header +++++++++++
  TableCell.stickyColumn(
    this.text, {
    this.textStyle,
    this.cellDimensions = CellDimensions.base,
    this.colorBg = const Color.fromARGB(255, 189, 191, 255),
    this.onTap,
    required this.rowIndex,
    required this.columnIndex,
    required this.rowHeadText,
    required this.colHeadText,
  })  : cellWidth = 120,
        cellHeight = cellDimensions.contentCellHeight,
        _colorHorizontalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _colorVerticalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _textAlign = TextAlign.left,
        _padding = EdgeInsets.zero;

  final CellDimensions cellDimensions;

  final String text;
  final Function()? onTap;

  final double? cellWidth;
  final double? cellHeight;
  
  final int rowIndex;
  final int columnIndex;
  final String rowHeadText;
  final String colHeadText;

  final Color colorBg;
  final Color _colorHorizontalBorder;
  final Color _colorVerticalBorder;

  final TextAlign _textAlign;
  final EdgeInsets _padding;

  final TextStyle? textStyle;

  final List<String> groupPareto = [];

  @override 
  _TableCellState createState() => _TableCellState();
}

class _TableCellState extends State<TableCell> {
  List<String> paretoSelected = [];
  double dialogHeight = 0;
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onDoubleTap: () { 
        
      },
      child: Container(
        width: widget.cellWidth,
        height: widget.cellHeight,
        padding: widget._padding,
        decoration: BoxDecoration(
          border: Border.all(
            color: widget._colorHorizontalBorder,
            width: 0.2
          ),
          color: widget.colorBg
        ),
        alignment: Alignment.centerLeft,
        child: Column(
          children: <Widget>[
            Expanded(
              child: Container(
                alignment: Alignment.center,
                padding: EdgeInsets.zero,
                child: Text(
                  widget.text,
                  style: widget.textStyle,
                  maxLines: 2,
                  textAlign: widget._textAlign,
                ),
              ),
            ),
            Container(
              width: double.infinity,
              height: 1,
              color: widget._colorVerticalBorder,
            ),
          ],
        ),
      ),
    );
  }
}