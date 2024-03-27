import 'dart:async';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:cool_alert/cool_alert.dart';
import 'package:flutter/widgets.dart';
import 'dart:convert';
// ignore: depend_on_referenced_packages
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:YMM/MainWindow/Window-Switching-Window/selection_view.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:google_fonts/google_fonts.dart';
// ignore: depend_on_referenced_packages
import 'package:shared_preferences/shared_preferences.dart';
// import 'package:device_imei/device_imei.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: WindowLogin(),
    );
  }
}

class WindowLogin extends StatefulWidget {
  const WindowLogin({super.key});

  @override
  State<WindowLogin> createState() => _WindowLoginState();
}

class _WindowLoginState extends State<WindowLogin> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
  final TextEditingController usernameController = TextEditingController();

  String appVersionFromGit = '';
  String textVersionShow = '';

  String savedUsername = '';

  String currentDate = '';
  String username = '';
  String password = '';
  bool statusLogin = false;
  String phonNo = '';

  String currentVersion = '';
  String currentRevision = '';
  String currentSubRevision = '';

  String currentVersionLastest = '';
  String currentRevisionLastest = '';
  String currentSubRevisionLastest = '';

  bool windowAuthen = false;

  @override
  void initState() {
    loadUsername(true);
    super.initState();
  }

  Future<void> loadUsername(bool checkUpdate) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      savedUsername = prefs.getString('username') ?? '';
      usernameController.text = savedUsername;
    });

    if (checkUpdate == true) {
      textVersionShow = 'Checking version update...';
      await queryAppInfo();
      await _getGitFiles();
    }
  }

  Future<void> _getGitFiles() async {
    var response = await http.get(Uri.parse('https://api.github.com/repos/waruntronkra/git-programming/contents/APK'));
    if (response.statusCode == 200) {
      setState(() {
        appVersionFromGit = (jsonDecode(response.body))[0]['name'];
        textVersionShow = 'Version : $currentVersionLastest.$currentRevisionLastest.$currentSubRevisionLastest';
      });
    } 
    if (appVersionFromGit.isNotEmpty) {
      if (appVersionFromGit.split('-')[1].split('.apk')[0] != 'v$currentVersionLastest.$currentRevisionLastest.$currentSubRevisionLastest') {
        WidgetsBinding.instance.addPostFrameCallback((_) {
          showDialog(
            context: context,
            builder: (BuildContext context) {
              return AlertDialog(
                title: const Text('Update Notification'),
                content: Text('There is new version => ${appVersionFromGit.split('-')[1].split('.apk')[0]}.'),
                actions: <Widget>[
                  TextButton(
                    onPressed: () {
                      insertVersionToDB();
                      _launchURL();
                      Navigator.of(context).pop();
                    },
                    child: const Text('Update'),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.of(context).pop();
                    },
                    child: const Text('Update Later'),
                  ),
                ],
              );
            },
          );
        });
      }
    }
  }

  Future<void> saveUsername(String username) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('username', username);
    loadUsername(false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: scaffoldKey,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(0),
        child: AppBar()
      ),
      body: SingleChildScrollView(
        child: Stack(
          children: [
            Container(
              margin: const EdgeInsets.only(top: 180),
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height,
              decoration: const BoxDecoration(
                color: Color.fromARGB(255, 3, 141, 93),
                borderRadius: BorderRadius.only(topLeft: Radius.circular(20), topRight: Radius.circular(20))
              ),
            ),
            // Image Fabrinet
            // Center(
            //   child: SizedBox(
            //     width: 100,
            //     height: 100,
            //     child: Image.asset('assets/images/fabrinet_image.png')
            //   ),
            // ),
            // Image Login
            // Center(
            //   child: SizedBox(
            //     width: 250,
            //     height: 250,
            //     child: Image.asset('assets/images/login_image.png')
            //   ),
            // ),
            // Label Username Input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Center(
              child: Container(
                margin: const EdgeInsets.only(top: 10),
                width: 200,
                child:  Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text(
                      'Fabri',
                      style:  TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 40,
                        color: Color.fromARGB(255, 71, 120, 73)
                      ),
                    ),
                    const Text(
                      'net',
                      style:  TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 40,
                        color: Color.fromARGB(255, 53, 53, 53)
                      ),
                    ),
                    Stack(
                      children: [
                        Container(
                          margin: const EdgeInsets.only(left: 2.5, top: 2.4),
                          child: const Icon(
                            Icons.r_mobiledata_rounded,
                            size: 18,
                          )
                        ),
                        Container(
                          margin: const EdgeInsets.only(bottom: 20),
                          child: const Icon(
                            Icons.circle_outlined,
                            size: 13,
                          )
                        )
                      ]
                    )
                  ]
                )
              )
            ),
            Container(
              margin: const EdgeInsets.only(top: 200, left: 30),
              alignment: Alignment.topLeft,
              width: MediaQuery.of(context).size.width * 0.9,
              child: Text(
                'Username',
                style: GoogleFonts.nunito(
                  fontWeight: FontWeight.bold,
                  color: Colors.white
                ),
              ),
            ),
            // Username Input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Container(
              margin: const EdgeInsets.only(top: 230, left: 30, right: 30),
              decoration: BoxDecoration(
                color: const Color.fromARGB(255, 217, 255, 219),
                borderRadius: BorderRadius.circular(15)
              ),
              width: MediaQuery.of(context).size.width * 0.9,
              child: TextField(
                controller: usernameController,
                onChanged: (String? value) {
                  setState(() {
                    username = value!;
                  });
                },
                cursorColor: const Color.fromARGB(255, 3, 141, 93),
                decoration:  InputDecoration(
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                    borderSide: const BorderSide(
                      color: Colors.transparent
                    )
                  ),
                  prefixIcon: const Icon(Icons.person),
                  prefixIconColor: const Color.fromARGB(255, 3, 141, 93),
                  focusedBorder: const OutlineInputBorder(
                    borderSide: BorderSide(
                      color: Colors.transparent,
                    )
                  )
                ),
              )
            ),
            // Label Password Input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Container(
              alignment: Alignment.topLeft,
              width: MediaQuery.of(context).size.width * 0.9,
              margin: const EdgeInsets.only(top: 300, left: 30),
              child: Text(
                'Password',
                style: GoogleFonts.nunito(
                  fontWeight: FontWeight.bold,
                  color: Colors.white
                ),
              ),
            ),
            // Password Input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Container(
              margin: const EdgeInsets.only(top: 330, left: 30, right: 30),
              decoration: BoxDecoration(
                color: const Color.fromARGB(255, 217, 255, 219),
                borderRadius: BorderRadius.circular(15)
              ),
              width: MediaQuery.of(context).size.width * 0.9,
              child: TextField(
                onChanged: (String? val) {
                  setState(() {
                    password = val!;
                  });
                },
                cursorColor: const Color.fromARGB(255, 3, 141, 93),
                obscureText: true,
                decoration: InputDecoration(
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(15),
                    borderSide: const BorderSide(
                      color: Colors.transparent
                    )
                  ),
                  prefixIcon: const Icon(Icons.lock),
                  prefixIconColor: const Color.fromARGB(255, 3, 141, 93),
                  focusedBorder: const OutlineInputBorder(
                    borderSide: BorderSide(
                      color: Colors.transparent,
                    )
                  )
                ),
              )
            ),
            // Login Button >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Center(
              child: Container(
                decoration:  BoxDecoration(
                  color: const Color.fromARGB(255, 67, 69, 69),
                  borderRadius: BorderRadius.circular(15)
                ),
                margin: const EdgeInsets.only(top: 420),
                width: MediaQuery.of(context).size.width * 0.5,
                height: 50,
                child: MaterialButton(
                  onPressed: () async {
                    saveUsername(usernameController.text);
                    await windowAuthenAPI();
                    if (windowAuthen == true) {
                      Navigator.push(
                        context,
                        PageRouteBuilder(
                          transitionDuration: const Duration(seconds: 1),
                          pageBuilder: (context, animation, secondaryAnimation) {
                            return const WindowSelectView();
                          },
                          transitionsBuilder: (context, animation, secondaryAnimation, child) {
                            var begin = const Offset(0.0, -1.0);
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
                    }
                    else {
                      CoolAlert.show(
                        width: 1,
                        context: scaffoldKey.currentContext!,
                        type: CoolAlertType.error,
                        text:'Invalid Username or Password!'
                      );
                    }
                  },
                  child: Text(
                    'GO', 
                    style: GoogleFonts.nunito(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold
                    )
                  )
                ) 
              )
            ),
            Center (
              child: Container(
                margin: const EdgeInsets.only(top: 500),
                height: MediaQuery.of(context).size.height * 0.1,
                width: 180,
                alignment: Alignment.center,
                child: Text(
                  textVersionShow,
                  style: GoogleFonts.nunito(
                    color: Colors.white
                  ),
                ),
              )
            ),

            // ElevatedButton(
            //   onPressed: _launchURL,
            //   child: const Text('Check for update'),
            // ),
          ],
        ),
      ),
    );
  }

  Future<void> windowAuthenAPI() async {
    try {
      Map<String, dynamic> stringEncryptedArray = await encryptData([
        usernameController.text,
        password
      ]);

      var dataQueried = await getDataPOST('https://localhost:44342/api/YMA/WindowAuthen',
        {
          'Username': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
          'Password': stringEncryptedArray['data'][1]
        },
      );
      
      if (jsonDecode(dataQueried[0]) == 'Found!') {
        windowAuthen = true;
      }
      else {
        windowAuthen = false;
      }
      setState(() {
        windowAuthen = windowAuthen;
      });
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }

  Future<void> insertVersionToDB() async {
    try {
      var now = DateTime.now();
      var formatter = DateFormat('MM/dd/yyyy hh:mm:ss a');
      currentDate = formatter.format(now);
      
      Map<String, dynamic> stringEncryptedArray = await encryptData([
        "'$currentDate'",
        "'${appVersionFromGit.split('v')[1].split('.')[0]}'", // Version
        "'${appVersionFromGit.split('v')[1].split('.')[1]}'", // Revision
        "'${appVersionFromGit.split('v')[1].split('.')[2]}'", // Sub revision
        "'Initialize'",
        'INSERT'
      ]);

      await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/UpdateAppInfo',
        {
          'UpdateDate': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
          'Version': stringEncryptedArray['data'][1],
          'Revision': stringEncryptedArray['data'][2],
          'SubRevision': stringEncryptedArray['data'][3],
          'Description': stringEncryptedArray['data'][4],
          'ModeSQL': stringEncryptedArray['data'][5]
        },
      );
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }


  void showFullTextDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return const AlertDialog(
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Please update')
            ]
          )
        );
      },
    );
  }

  void _launchURL() async {
    final Uri url = Uri.parse('https://github.com/waruntronkra/git-programming/raw/main/APK/$appVersionFromGit');
    if (!await launchUrl(url)) {
      throw Exception('Could not launch $url');
    }
  }

  // ****************************************** Query Zone ******************************************
  Future<void> queryUser() async {
    try {
      Map<String, dynamic> stringEncryptedArray = await encryptData([
        usernameController.text,
      ]);

      var dataQueried = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/UserInfo',
        {
          'Username': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}',
        },
      );

      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
        setState(() {
          if (decodedData.isNotEmpty) {
            statusLogin = true;
          }
          else {
            statusLogin = false;
          }
        });
      }
      else {
        setState(() {
          statusLogin = false;
        });
      }
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }

  Future<void> queryUserAppInfo() async {
    try {
      Map<String, dynamic> stringEncryptedArray = await encryptData([
        savedUsername
      ]);

      var dataQueried = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/QueryUserAppInfo',
        {
          'LoginName': '${stringEncryptedArray['iv'].base16}${stringEncryptedArray['data'][0]}'
        },
      );

      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(stringEncryptedArray['key']);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: stringEncryptedArray['iv']);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

        setState(() {
          if (decodedData.isNotEmpty) {
            currentVersion = decodedData[0]['CURRENT_VERSION'].toString();
            currentRevision = decodedData[0]['CURRENT_REVISION'].toString();
            currentSubRevision = decodedData[0]['CURRENT_SUB_REVISION'].toString();
          }
        });
      }
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }

  Future<void> queryAppInfo() async {
    try {
      String keyValue = 'yieldeachproduct'; // *** important, same as flutter sent ***
      var iv = encrypt.IV.fromLength(16);

      var dataQueried = await getDataPOST(
        'https://supply-api.fabrinet.co.th/api/YMA/QueryAppInfo',
        {
          'Value' : iv.base16
        },
      );

      if (dataQueried[1] == 200) {
        String jsonEncrypted = jsonDecode(jsonDecode(dataQueried[0]))['encryptedJson'];

        final keyBytes = encrypt.Key.fromUtf8(keyValue);
        final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

        String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: iv);
        List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));

        setState(() {
          if (decodedData.isNotEmpty) {
            currentVersionLastest = decodedData[0]['VERSION'].toString();
            currentRevisionLastest = decodedData[0]['REVISION'].toString();
            currentSubRevisionLastest = decodedData[0]['SUB_REVISION'].toString();
          }
        });
      }
    }
    catch (e) {
      CoolAlert.show(
        width: 1,
        context: scaffoldKey.currentContext!,
        type: CoolAlertType.error,
        text:'Error : $e'
      );
    }
  }

  // Future<void> downloadFile() async {
  //   try {
  //     var dataQueried = await getDataGET(
  //       'https://localhost:44342/api/YMA/FileAppDownload'
  //     );
  //     print(dataQueried);

  //     if (dataQueried[1] == 200) {
  //      print(dataQueried);

  //     }
  //   }
  //   catch (e) {
  //     CoolAlert.show(
  //       width: 1,
  //       context: scaffoldKey.currentContext!,
  //       type: CoolAlertType.error,
  //       text:'Error : $e'
  //     );
  //   }
  // }

  // <<<<<<<<<<<<<<<<<<<<<<<<< [Encrypt] Data >>>>>>>>>>>>>>>>>>>>>>>>>
  Future<Map<String, dynamic>> encryptData(List<dynamic> data) async {
    String keyValue = 'yieldeachproduct'; // *** important, same as flutter sent ***
    var iv = encrypt.IV.fromLength(16);

    final keyBytesTest = encrypt.Key.fromUtf8(keyValue);
    final encrypterTest = encrypt.Encrypter(encrypt.AES(keyBytesTest, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));
    
    List<dynamic> encryptedData = [];
    for (var value in data) {
      encryptedData.add(encrypterTest.encrypt(value, iv: iv));
    }

    List<String> stringEncryptedData = [];
    for (var value in encryptedData) {
      stringEncryptedData.add(base64Encode(value.bytes));
    }
    return {
      'key' : keyValue,
      'iv' : iv,
      'data' : stringEncryptedData
    };
  }
}

// ============================== API ==============================
// https://supply-api.fabrinet.co.th/api
Future<dynamic> getDataPOST(String url, Map<String, String> body) async {
  http.Response response = await http.post(
    Uri.parse(url),
    body: body,
  );
  if (response.statusCode == 200) {
    return [response.body, response.statusCode];
  }
  else {
    return [response.body, response.statusCode];
  }
}

Future<dynamic> getDataGET(String url) async {
  http.Response response = await http.get(
    Uri.parse(url)
  );
  if (response.statusCode == 200) {
    return [response.body, response.statusCode];
  }
  else {
    return [response.body, response.statusCode];
  }
}