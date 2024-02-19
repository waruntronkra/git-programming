import 'package:flutter/material.dart';
import 'package:flutter_table/table_sticky_headers.dart';

typedef void OnButtonClickedCallback(String arr);
class DecoratedTablePage extends StatelessWidget {
  const DecoratedTablePage({
        required this.data, 
        required this.titleColumn, 
        required this.titleRow,
        required this.dataPareto,
        required this.onButtonClicked,
        required this.levelSelected,
        required this.modelSelected,
        required this.daySelected,
        Key? key
  }) : super(key: key);

  final List<List<String>> data;
  final List<String> titleColumn;
  final List<String> titleRow;
  final Map<String, List<List<String>>> dataPareto;
  final OnButtonClickedCallback onButtonClicked;
  final String levelSelected;
  final String modelSelected;
  final String daySelected;

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
          dataPareto: const {},
          onButtonClicked:onButtonClicked,
          levelSelected: levelSelected,
          modelSelected: modelSelected,
          daySelected: daySelected
        ),
        rowsTitleBuilder: (i) => TableCell.stickyColumn(
          titleRow[i],
          textStyle: headerCellStyle,
          rowIndex: i,
          columnIndex: 0,
          rowHeadText: titleRow[i],
          colHeadText: '',
          dataPareto: const {},
          onButtonClicked:onButtonClicked,
          levelSelected: levelSelected,
          modelSelected: modelSelected,
          daySelected: daySelected
        ),
        contentCellBuilder: (i, j) => TableCell.content(
          data[j][i],
          textStyle: contentCellStyle,
          rowIndex: j,
          columnIndex: i,
          rowHeadText: titleRow[j],
          colHeadText: titleColumn[i],
          dataPareto: dataPareto,
          onButtonClicked:onButtonClicked,
          levelSelected: levelSelected,
          modelSelected: modelSelected,
          daySelected: daySelected
        ),
        legendCell: TableCell.legend(
          'DATE\nPROCESS',
          textStyle: headerCellStyle,
          rowIndex: 0,
          columnIndex: 0,
          rowHeadText: '',
          colHeadText: '',
          dataPareto: const {},
          onButtonClicked:onButtonClicked,
          levelSelected: levelSelected,
          modelSelected: modelSelected,
          daySelected: daySelected
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
    required this.dataPareto,
    required this.onButtonClicked,
    required this.levelSelected,
    required this.modelSelected,
    required this.daySelected
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
    required this.dataPareto,
    required this.onButtonClicked,
    required this.levelSelected,
    required this.modelSelected,
    required this.daySelected 
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
    required this.dataPareto,
    required this.onButtonClicked,
    required this.levelSelected,
    required this.modelSelected,
    required this.daySelected 
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
    required this.dataPareto,
    required this.onButtonClicked,
    required this.levelSelected,
    required this.modelSelected,
    required this.daySelected 
  })  : cellWidth = 120,
        cellHeight = cellDimensions.contentCellHeight,
        _colorHorizontalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _colorVerticalBorder = const Color.fromRGBO(116, 116, 116, 1),
        _textAlign = TextAlign.left,
        _padding = EdgeInsets.zero;

  final OnButtonClickedCallback onButtonClicked; 

  final CellDimensions cellDimensions;

  final String text;
  final Function()? onTap;

  final double? cellWidth;
  final double? cellHeight;
  
  final int rowIndex;
  final int columnIndex;
  final String rowHeadText;
  final String colHeadText;
  final Map<String, List<List<String>>> dataPareto;
  final String levelSelected;
  final String modelSelected;
  final String daySelected;

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
        // getPareto();
        // Navigator.push(
        //   context,
        //   MaterialPageRoute(
        //     builder: (context) => PagePareto(
        //       levelSelected: widget.levelSelected,
        //       modelSelected: widget.modelSelected,
        //       daySelected: widget.daySelected,
        //     )
        //   ),
        // );
        // navigatorKey.currentState!.push(
        //   MaterialPageRoute(builder: (context) =>
        //     const PagePareto(
        //       levelSelected: '',
        //       modelSelected: '',
        //       daySelected: '',
        //       processSelected: ''
        //     )
        //   )
        // );
        // widget.onButtonClicked(paretoSelected);
        // widget.onButtonClicked(widget.rowHeadText);
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

  Future<void> getPareto() async {
    List<String> arr = []; 
    if (widget.dataPareto[widget.rowHeadText]?[widget.columnIndex] != null) {
      for (var i in widget.dataPareto[widget.rowHeadText]![widget.columnIndex]) {
        arr.add(i);
      }
    }
    setState(() { 
      paretoSelected = arr; 
    });
  }
}