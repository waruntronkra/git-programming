import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:cool_alert/cool_alert.dart';
import 'page_summary.dart';
import 'package:encrypt/encrypt.dart' as encrypt;
// import 'package:device_imei/device_imei.dart';

class ResultMessage {
  bool status;
  String messenger;
  List<DataObject> dataObj;

  ResultMessage({
    required this.status,
    required this.messenger,
    required this.dataObj,
  });

  factory ResultMessage.fromJson(Map<String, dynamic> json) {
    var data = json['DataObj'] as List;
    List<DataObject> dataObjList =
        data.map((item) => DataObject.fromJson(item)).toList();

    return ResultMessage(
      status: json['Status'],
      messenger: json['Messenger'],
      dataObj: dataObjList,
    );
  }
}

class DataObject {
  String username;
  String email;

  DataObject({
    required this.username,
    required this.email,
  });

  factory DataObject.fromJson(Map<String, dynamic> json) {
    return DataObject(
      username: json['Username'],
      email: json['Email'],
    );
  }
}

class MyApp extends StatefulWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
  final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

  String url = '';
  Map<String, String> object = {};
  String queryText = '';
  String twoFactor = '';
  Color usernameBorderColor = const Color.fromRGBO(0, 31, 255, 1);
  Color factorBorderColor = Colors.red;
  String factorInput = '';
  bool activeInputFactor = false;
  bool goToMainPage = false;
  String textBT = 'Get Activation Number';
  var iv;
  String keyValue = 'yieldeachproduct'; // *** important, same as flutter sent ***

  // @override
  // void initState()  {
  //   super.initState();
  //   var imei = DeviceImei();
  //   print(imei);
  // }
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      navigatorKey: navigatorKey,
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        key: scaffoldKey,
        appBar:
            AppBar(backgroundColor: const Color.fromARGB(255, 213, 255, 212)),
        body: Stack(
          children: [
            // ==================== Mini Wallpaper ====================
            Container(
                width: MediaQuery.of(context).size.width,
                height: 135,
                color: const Color.fromARGB(255, 213, 255, 212)),
            // ==================== Logo ====================
            Positioned(
                top: -7,
                left: (MediaQuery.of(context).size.width - 330) / 2,
                child: Center(
                    child: SizedBox(
                        // Focus on [SIZE]
                        width: 330,
                        height: 130,
                        child: Image.asset('images/logo.png')))),
            // ==================== Text box for input Username ====================
            Container(
                margin: const EdgeInsets.all(16),
                child: Padding(
                  padding: const EdgeInsets.only(top: 140),
                  child: TextFormField(
                    onChanged: (value) {
                      setState(() {
                        iv = encrypt.IV.fromLength(16);

                        final keyBytesTest = encrypt.Key.fromUtf8(keyValue);
                        final encrypterTest = encrypt.Encrypter(encrypt.AES(keyBytesTest, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));
                        
                        final encryptedUsername = encrypterTest.encrypt(value.toString(), iv: iv);

                        String stringEncryptedLevel = base64Encode(encryptedUsername.bytes);

                        url = 'https://localhost:44342/api/YMA/UserInfo';
                        object = {'Username' : stringEncryptedLevel};
                      });
                    },
                    decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        filled: true,
                        fillColor: Color.fromARGB(255, 226, 226, 226),
                        labelText: 'Enter the [Username]',
                        prefixIcon: Icon(Icons.person)),
                  ),
                )),
            // ==================== Text box for input Second Factor ====================
            Visibility(
              visible: activeInputFactor,
              child: Container(
                  margin: const EdgeInsets.all(16),
                  child: Padding(
                    padding: const EdgeInsets.only(top: 215),
                    child: TextFormField(
                      onChanged: (val) {
                        factorInput = val.toString();
                      },
                      decoration: InputDecoration(
                          filled: true,
                          fillColor: const Color.fromARGB(255, 226, 226, 226),
                          border: const OutlineInputBorder(),
                          focusedBorder: OutlineInputBorder(
                              borderSide: BorderSide(
                                  color: usernameBorderColor, width: 1)),
                          enabledBorder: const OutlineInputBorder(
                              borderSide:
                                  BorderSide(color: Colors.black, width: 1)),
                          labelText: 'Enter [Second Factor Number]',
                          prefixIcon: const Icon(Icons.numbers)),
                    ),
                  )),
            ),
            // ==================== Button submit ====================
            Container(
                margin: const EdgeInsets.only(top: 100),
                child: Align(
                    alignment: Alignment.center,
                      child: SizedBox(
                          height: 50,
                          child: ElevatedButton.icon(
                            onPressed: () async {
                              if (activeInputFactor == false) { // I am debuging, if done, change false to [true] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                setState(() {
                                  // I am debuging, turn it back !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                  // usernameBorderColor = queryText == 'fail'
                                  //     ? Colors.red
                                  //     : const Color.fromARGB(
                                  //         255, 129, 136, 189);

                                  // activeInputFactor =
                                  //     factorInput == twoFactor
                                  //         ? true
                                  //         : false;
                                  // goToMainPage = factorInput == twoFactor
                                  //     ? true
                                  //     : false;

                                  if (goToMainPage == false) { // I am debuging, if done, change false to [true] !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                    navigatorKey.currentState!.push(MaterialPageRoute(builder: (context) =>const SecondPage()));
                                  } 
                                  // I am debuging, turn it back !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                  // else {
                                  //   CoolAlert.show(
                                  //       width: 1,
                                  //       context: scaffoldKey.currentContext!,
                                  //       type: CoolAlertType.error,
                                  //       text:
                                  //           'Invalid Second Factor Number!');
                                  // }
                                });
                              } 
                              else {
                                var data = await getDataPOST(url, object);
                                String jsonEncrypted = jsonDecode(jsonDecode(data[0]))['encryptedJson'];

                                final keyBytes = encrypt.Key.fromUtf8(keyValue);
                                final encrypter = encrypt.Encrypter(encrypt.AES(keyBytes, mode: encrypt.AESMode.cbc, padding: 'PKCS7'));

                                String decryptJson = encrypter.decrypt64(jsonEncrypted, iv: iv);
                                List<Map<String, dynamic>> decodedData = List<Map<String, dynamic>>.from(json.decode(decryptJson));
                                setState(() {
                                  if (decodedData.isNotEmpty) {
                                    queryText = 'true';
                                    // String username = decodedData[0]['Username'];
                                  }
                                  else {
                                    queryText = 'fail';
                                  }
                                  
                                  // twoFactor = decodedData[0]['random_number'];

                                  usernameBorderColor = queryText == 'fail'
                                      ? Colors.red
                                      : const Color.fromRGBO(0, 31, 255, 1);

                                  activeInputFactor =
                                      queryText != 'fail' ? true : false;

                                  if (queryText == 'fail') {
                                    textBT = 'Get Activation Number';
                                    CoolAlert.show(
                                        width: 1,
                                        context: scaffoldKey.currentContext!,
                                        type: CoolAlertType.error,
                                        text: 'Invalid Username!');
                                  } else {
                                    textBT = 'Login';
                                    CoolAlert.show(
                                        width: 1,
                                        context: scaffoldKey.currentContext!,
                                        type: CoolAlertType.success,
                                        text:
                                            '[Second Factor Number]\n - has been sent to your EMAIL -');
                                  }
                                });
                              }
                            },
                            style: ElevatedButton.styleFrom(
                                backgroundColor:
                                    const Color.fromARGB(255, 108, 238, 255),
                                foregroundColor: Colors.black,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10),
                                )),
                            icon: const Icon(Icons.login),
                            label: Text(textBT),
                          ))))
          ],
        ),
      ),
    );
  }
}