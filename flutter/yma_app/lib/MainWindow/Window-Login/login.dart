import 'dart:async';
import 'package:flutter/material.dart';
import 'package:rounded_loading_button/rounded_loading_button.dart';
import 'package:cool_alert/cool_alert.dart';
import 'dart:convert';
// ignore: depend_on_referenced_packages
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'package:encrypt/encrypt.dart' as encrypt;
import 'package:yma_app/MainWindow/Window-Switching-Window/selection_view.dart';
// import 'package:device_imei/device_imei.dart';

class WindowLogin extends StatefulWidget {
  const WindowLogin({super.key});

  @override
  State<WindowLogin> createState() => _WindowLoginState();
}

class _WindowLoginState extends State<WindowLogin> {
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
  final RoundedLoadingButtonController _btnController = RoundedLoadingButtonController();
  String currentDate = '';
  String username = '';
  String password = '';
  bool statusQueried = false;
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
    super.initState();
  }

  void checkUsername() async {
    await queryUser();
    if (statusQueried == true) {
        _btnController.success();
        Timer(const Duration(seconds: 1), () {
          _btnController.reset();
          navigatorKey.currentState!.push(MaterialPageRoute(builder: (context) => const WindowSelectView()));
      });
    }
    else {
      _btnController.error();
      Timer(const Duration(seconds: 1), () {
        _btnController.reset();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: navigatorKey,
      debugShowCheckedModeBanner: false,
      home: Scaffold(
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
                  child: Image.asset('images/fabrinet_image.png')
                ),
              ),
              // Image Login
              Center(
                child: SizedBox(
                  width: 250,
                  height: 250,
                  child: Image.asset('images/login_image.png')
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
                child: const Text(
                  'Password',
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
                margin: const EdgeInsets.only(top: 20),
                width: MediaQuery.of(context).size.width * 0.5,
                child: RoundedLoadingButton(
                  successColor: const Color.fromARGB(255, 3, 141, 93),
                  color: const Color.fromARGB(255, 3, 141, 93),
                  controller: _btnController,
                  onPressed: () async {
                    // await queryUserAppInfo();
                    // await queryAppInfo();
                    // if (username.isNotEmpty) {
                    //   if (currentRevision != currentRevisionLastest) {
                    //     print('Please Update');
                    //     print('currentRevision : $currentRevision');
                    //     print('currentRevisionLastest : $currentRevisionLastest');
                    //   }
                    //   else {
                    //     print('This is last verion already');
                    //     print('currentRevision : $currentRevision');
                    //     print('currentRevisionLastest : $currentRevisionLastest');
                    //   }
                    // }
                    // checkUsername();
                    navigatorKey.currentState!.push(MaterialPageRoute(builder: (context) => const WindowSelectView()));
                    _btnController.reset();
                  },
                  child: const Text(
                    'Login', 
                    style: TextStyle(
                      color: Colors.white
                    )
                  ),
                ) 
              ), 
              Text(phonNo)
            ],
          ),
        ),
      ),
    );
  }

  // ****************************************** Query Zone ******************************************
  Future<void> queryUser() async {
    try {
      Map<String, dynamic> stringEncryptedArray = await encryptData([
        username,
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
            statusQueried = true;
          }
          else {
            statusQueried = false;
          }
        });
      }
      else {
        setState(() {
          statusQueried = false;
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
      if (username.isNotEmpty) {
        Map<String, dynamic> stringEncryptedArray = await encryptData([
          username
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