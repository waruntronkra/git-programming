import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
// import 'table_pareto.dart';

class PagePareto extends StatefulWidget {
  const PagePareto({
    required this.levelSelected,
    required this.modelSelected,
    required this.daySelected,
    required this.failures,
    Key? key
  }) : super(key: key);

  final String levelSelected;
  final String modelSelected;
  final String daySelected;
  final List<String> failures;

  @override
  State<PagePareto> createState() => _PageParetoState();
}

class _PageParetoState extends State<PagePareto> {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(left: 10, right: 10, top: 20),
            width: MediaQuery.of(context).size.width * 0.97,
            height: 140,
            decoration: BoxDecoration(
              border: Border.all(
                color: const Color.fromARGB(255, 3, 141, 93), 
                width: 2
              )
            ),
            child: SingleChildScrollView(
              child: Column(
                children: [...listFailure()],
              ),
            ),
          )
        ]
      )
    );
  }
  
  List<Widget> listFailure() {
    List<Widget> failure = [];
    for (String item in widget.failures) {
      failure.add(Container(
        height: 20,
        width: MediaQuery.of(context).size.width * 0.9,
        margin: const EdgeInsets.only(top: 5),
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color.fromARGB(255, 255, 238, 0),
            foregroundColor: const Color.fromARGB(255, 255, 0, 0),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(0),
            )
          ),
          onPressed: () {
            // do something
          },
          child: Text(item, style: const TextStyle(fontSize: 12)),
        )
      )
      );
    }
    return failure;
  }
}

Future<String> query(String url) async {
  http.Response response = await http.get(Uri.parse(url));
  return response.body;
}