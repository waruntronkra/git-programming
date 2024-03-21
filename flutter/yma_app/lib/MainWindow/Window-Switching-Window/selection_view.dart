// ignore_for_file: deprecated_member_use

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';
import 'package:provider/provider.dart';
import '../Window-ACACIA-YIELD/Pages-Summary/tab_summary.dart';
import '../Window-FBN-ACACIA-YIELD/Page-Summary/tab_summary.dart';
// import '../Window-FBN-Cisco-OTBU/Pages-Summary/tab_summary.dart';
// import '../Window-EP-YIELD/Pages-Summary/tab_summary.dart';

class WindowSelectView extends StatefulWidget {
  const WindowSelectView({super.key});

  @override
  State<WindowSelectView> createState() => _WindowSelectViewState();
}

class _WindowSelectViewState extends State<WindowSelectView> {
  @override
  Widget build(BuildContext context) {
    return WillPopScope( // This fuction use when don't want to go back to previous page
      onWillPop: () async {
        return false;
      },
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: const Size.fromHeight(0),
          child: AppBar(
            automaticallyImplyLeading: false, // Hide buttom go back previous page
            title: const Text('Selction Yield Dashboard'),
          )
        ),
        body: SingleChildScrollView(
          child: Stack(
            children: [
              // Image Dashboard
              Center(
                child: Container(
                  margin: const EdgeInsets.only(bottom: 10, top: 50),
                  width: 350,
                  height: 350,
                  child: Image.asset('assets/images/dashboard.png')
                )
              ),
              // Go to page ACACIA FBN Yield
             Container(
                margin: const EdgeInsets.only(top: 450, left: 50),
                alignment: Alignment.topLeft,
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      Container(
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 3, 141, 93),
                          borderRadius: BorderRadius.circular(10),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey
                            )
                          ]
                        ),
                        width: MediaQuery.of(context).size.width * 0.5,
                        height: 40,
                        child: MaterialButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              PageRouteBuilder(
                                pageBuilder: (context, animation, secondaryAnimation) => const WindowFBNYIELD(),
                                transitionDuration: const Duration(seconds: 1), // Set the duration here
                                transitionsBuilder: (context, animation, secondaryAnimation, child) {
                                  var begin = const Offset(1.0, 0.0);
                                  var end = Offset.zero;
                                  var curve = Curves.ease;

                                  var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

                                  return SlideTransition(
                                    position: animation.drive(tween),
                                    child: child,
                                  );
                                },
                              ),
                            );
                          },
                          child: const Text(
                            '[ACACIA] FBN Yield',
                            style: TextStyle(
                              fontSize: 13,
                              color: Colors.white
                            ),
                          )
                        )
                      ),
                    ]
                  )
                )
              ),
              // Go to page Cisco OTBU Yield
              // Container(
              //   margin: const EdgeInsets.only(top: 445, left: 50),
              //   alignment: Alignment.topLeft,
              //   child: SingleChildScrollView(
              //     scrollDirection: Axis.horizontal,
              //     child: Row(
              //       children: [
              //         SizedBox(
              //           width: MediaQuery.of(context).size.width * 0.5,
              //           height: 40,
              //           child: ElevatedButton(
              //             style: ElevatedButton.styleFrom(
              //               backgroundColor: const Color.fromARGB(255, 3, 141, 93),
              //               side: const BorderSide(
              //                 color: Colors.black,
              //               ),
              //               shape: RoundedRectangleBorder(
              //                 borderRadius: BorderRadius.circular(5),
              //               ),
              //             ),
              //             onPressed: () {
              //               Navigator.push(
              //                 context,
              //                 MaterialPageRoute(builder: (context) => const WindowCiscoOTBUYIELD())
              //               );
              //             },
              //             child: const Text(
              //               '[Cisco OTBU] Yield',
              //               style: TextStyle(
              //                 fontSize: 13,
              //                 color: Colors.white
              //               )
              //             )
              //           )   
              //         ),
              //         Container(
              //           margin: const EdgeInsets.only(left: 10),
              //           width: 50,
              //           height: 50,
              //           child: Image.asset('assets/images/cisco.png')
              //         )
              //       ]
              //     )
              //   )
              // ),
              // Go to page EFFECT PHOTONIC Yield
              // Container(
              //   margin: const EdgeInsets.only(top: 475, left: 50),
              //   alignment: Alignment.topLeft,
              //   child: SingleChildScrollView(
              //     scrollDirection: Axis.horizontal,
              //     child: Row(
              //       children: [
              //         SizedBox(
              //           width: MediaQuery.of(context).size.width * 0.5,
              //           height: 40,
              //           child: ElevatedButton(
              //             style: ElevatedButton.styleFrom(
              //               backgroundColor: const Color.fromARGB(255, 3, 141, 93),
              //               side: const BorderSide(
              //                 color: Colors.black,
              //               ),
              //               shape: RoundedRectangleBorder(
              //                 borderRadius: BorderRadius.circular(5),
              //               ),
              //             ),
              //             onPressed: () {
              //               Navigator.push(
              //                 context,
              //                 MaterialPageRoute(builder: (context) => const WindowEPYIELD())
              //               );
              //             },
              //             child: const Text(
              //               '[EFFECT PHOTONIC] Yield',
              //               style: TextStyle(
              //                 fontSize: 13,
              //                 color: Colors.white
              //               )
              //             )
              //           )   
              //         ),
              //         Container(
              //           margin: const EdgeInsets.only(left: 10),
              //           width: 90,
              //           height: 90,
              //           child: Image.asset('assets/images/effect-photonic.png')
              //         )
              //       ]
              //     )
              //   )
              // ),
              // Go to page ACACIA Yield
              Container(
                margin: const EdgeInsets.only(top: 490, left: 50),
                alignment: Alignment.topLeft,
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      Container(
                        decoration: BoxDecoration(
                          color: const Color.fromARGB(255, 3, 141, 93),
                          borderRadius: BorderRadius.circular(10),
                          boxShadow: const [
                            BoxShadow(
                              blurRadius: 5,
                              offset: Offset(1, 1),
                              color: Colors.grey
                            )
                          ]
                        ),
                        width: MediaQuery.of(context).size.width * 0.5,
                        height: 40,
                        child: MaterialButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              PageRouteBuilder(
                                pageBuilder: (context, animation, secondaryAnimation) => const WindowATSYield(),
                                transitionDuration: const Duration(seconds: 1), // Set the duration here
                                transitionsBuilder: (context, animation, secondaryAnimation, child) {
                                  var begin = const Offset(1.0, 0.0);
                                  var end = Offset.zero;
                                  var curve = Curves.ease;

                                  var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

                                  return SlideTransition(
                                    position: animation.drive(tween),
                                    child: child,
                                  );
                                },
                              ),
                            );
                          },
                          child: const Text(
                            '[ACACIA] Yield',
                            style: TextStyle(
                              fontSize: 13,
                              color: Colors.white
                            ),
                          )
                        )
                      ),
                      Container(
                        margin: const EdgeInsets.only(left: 10),
                        width: 90,
                        height: 90,
                        child: Image.asset('assets/images/acacia.png')
                      )
                    ]
                  )
                )
              ),
              // Hero(
              //   tag: 'tag-2',
              //   child: SizedBox(
              //     width: 50,
              //     height: 50,
              //     child: MaterialButton(
              //       color: Colors.red,
              //       onPressed: () {
              //         Navigator.push(
              //           context,
              //           PageRouteBuilder(
              //             pageBuilder: (context, animation, secondaryAnimation) => const HeroPage(),
              //             transitionDuration: const Duration(seconds: 1), // Set the duration here
              //             transitionsBuilder: (context, animation, secondaryAnimation, child) {
              //               var begin = const Offset(1.0, 0.0);
              //               var end = Offset.zero;
              //               var curve = Curves.ease;

              //               var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

              //               return SlideTransition(
              //                 position: animation.drive(tween),
              //                 child: child,
              //               );
              //             },
              //           ),
              //         );
              //       }
              //     )
              //   )
              // )
            ],
          ),
        ),
      )
    );
  }
}

class HeroPage extends StatelessWidget {
  const HeroPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          
        ),
        body: Hero(
          tag: "tag-2",
          child: Container(
          
            color: Colors.red,
          ),
        ),
    );
  }
}