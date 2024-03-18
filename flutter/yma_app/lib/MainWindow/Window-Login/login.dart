import 'dart:async';
import 'package:flutter/material.dart';
import 'package:cool_alert/cool_alert.dart';
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

  @override
  void initState() {
    var now = DateTime.now();
    var formatter = DateFormat('MM/dd/yyyy hh:mm:ss a');
    currentDate = formatter.format(now);
    _getGitFiles();
    loadUsername();
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback((_) {
      showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Update Notification'),
            content: const Text('There is an update'),
            actions: <Widget>[
              TextButton(
                onPressed: () {
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
  List<String> files = [];
  Future<void> _getGitFiles() async {
    var apiUrl = 'https://api.github.com/repos/waruntronkra/git-programming/contents/APK';

    try {
      var response = await http.get(Uri.parse(apiUrl));
      if (response.statusCode == 200) {
        List<dynamic> fileList = jsonDecode(response.body);
          print(fileList[0]['name']);
      
      } else {
        print('Failed to load files: ${response.statusCode}');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  Future<void> loadUsername() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      savedUsername = prefs.getString('username') ?? '';
      usernameController.text = savedUsername;
    });
  }

  Future<void> saveUsername(String username) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('username', username);
    loadUsername();
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
        child: Column(
          children: [
            // Image Fabrinet
            Center(
              child: SizedBox(
                width: 100,
                height: 100,
                child: Image.asset('assets/images/fabrinet_image.png')
              ),
            ),
            // Image Login
            Center(
              child: SizedBox(
                width: 250,
                height: 250,
                child: Image.asset('assets/images/login_image.png')
              ),
            ),
            // Username Input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Container(
              alignment: Alignment.topLeft,
              width: MediaQuery.of(context).size.width * 0.9,
              child: const Text(
                'Username',
                style: TextStyle(
                  fontWeight: FontWeight.bold
                ),
              ),
            ),
            Center(
              child: Container(
                margin: const EdgeInsets.only(top: 5),
                width: MediaQuery.of(context).size.width * 0.9,
                child: TextField(
                  controller: usernameController,
                  onChanged: (String? value) {
                    setState(() {
                      username = value!;
                    });
                  },
                  cursorColor: const Color.fromARGB(255, 3, 141, 93),
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person),
                    prefixIconColor: Color.fromARGB(255, 3, 141, 93),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(
                        color: Color.fromARGB(255, 3, 141, 93),
                        width: 2
                      )
                    )
                  ),
                )
              )
            ),
            // Password Input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Container(
              alignment: Alignment.topLeft,
              width: MediaQuery.of(context).size.width * 0.9,
              margin: const EdgeInsets.only(top: 20),
              child: Text(
                'Two-Factor PIN',
                style: GoogleFonts.nunito(
                  fontWeight: FontWeight.bold
                ),
              ),
            ),
            Center(
              child: Container(
                margin: const EdgeInsets.only(top: 5),
                width: MediaQuery.of(context).size.width * 0.9,
                child: TextField(
                  onChanged: (String? val) {
                    setState(() {
                      password = val!;
                    });
                  },
                  cursorColor: const Color.fromARGB(255, 3, 141, 93),
                  obscureText: true,
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.lock),
                    prefixIconColor: Color.fromARGB(255, 3, 141, 93),
                    focusedBorder: OutlineInputBorder(
                      borderSide: BorderSide(
                        color: Color.fromARGB(255, 3, 141, 93),
                        width: 2
                      )
                    )
                  ),
                )
              )
            ),
            // Login Button >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Container(
              decoration:  BoxDecoration(
                color: const Color.fromARGB(255, 3, 141, 93),
                boxShadow: const [
                  BoxShadow(
                    blurRadius: 5,
                    offset: Offset(1, 1),
                    color: Colors.grey
                  )
                ],
                borderRadius: BorderRadius.circular(10)
              ),
              margin: const EdgeInsets.only(top: 20),
              width: MediaQuery.of(context).size.width * 0.5,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  saveUsername(usernameController.text);
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const WindowSelectView())
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.transparent,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10)
                  )
                ),
                child: const Text(
                  'Submit', 
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20
                  )
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
    final Uri url = Uri.parse('https://github.com/waruntronkra/git-programming/raw/main/app-release.apk');
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