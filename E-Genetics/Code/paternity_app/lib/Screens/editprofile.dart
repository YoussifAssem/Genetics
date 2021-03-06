// ignore_for_file: use_key_in_widget_constructors

import 'package:flutter/material.dart';
import 'package:paternity_app/Models/user.dart';

class EditProfilePage extends StatefulWidget {
  @override
  _EditProfilePageState createState() => _EditProfilePageState();
}

class _EditProfilePageState extends State<EditProfilePage> {
  bool showPassword = false;

  final email = TextEditingController();
  final password = TextEditingController();
  final confirmPassword = TextEditingController();

  late String text;
  User user = User();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: const Color.fromARGB(255, 38, 54, 80),
        /*
        appBar: AppBar(
          automaticallyImplyLeading: false,
          backgroundColor: Colors.blue[900],
          title: const Text(
            'Edit Profile',
          ),
          actions: [
            Container(
              alignment: Alignment.centerRight,
              child: Text(
                user.Email,
                style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                    fontStyle: FontStyle.italic),
              ),
            )
          ],
        ),*/
        body: ListView(
          children: [
            Container(
              padding: const EdgeInsets.only(left: 40, top: 25, right: 40),
              child: GestureDetector(
                onTap: () {
                  FocusScope.of(context).unfocus();
                },
                child: Column(
                  children: [
                    const Center(
                      child: Text(
                        'Edit Profile',
                        style: TextStyle(
                            color: Colors.white,
                            fontStyle: FontStyle.normal,
                            fontWeight: FontWeight.bold,
                            fontSize: 30),
                      ),
                    ),
                    const SizedBox(
                      height: 15,
                    ),
                    const SizedBox(
                      height: 35,
                    ),
                    TextFormField(
                      style: const TextStyle(
                        fontSize: 18,
                        color: Colors.white,
                      ),
                      
                      autocorrect: true,
                      controller: email,
                      decoration: InputDecoration(
                          prefixIcon: const Icon(
                            Icons.email,
                            color: Colors.white,
                          ),
                          filled: true,
                          hintText: user.Email,
                          hintStyle: const TextStyle(
                            fontSize: 18,
                            color: Colors.white,
                          )),
                    ),
                    const SizedBox(height: 20, width: 20),
                    TextFormField(
                      style: const TextStyle(
                        fontSize: 18,
                        color: Colors.white,
                      ),
                      
                      autocorrect: true,
                      controller: password,
                      decoration: const InputDecoration(
                          prefixIcon: Icon(
                            Icons.password,
                            color: Colors.white,
                          ),
                          filled: true,
                          hintText: 'Old Or New Password',
                          hintStyle: TextStyle(
                            fontSize: 18,
                            color: Colors.white,
                          )),
                      obscureText: true,
                    ),
                    const SizedBox(height: 20, width: 20),
                    TextFormField(
                      style: const TextStyle(
                        fontSize: 18,
                        color: Colors.white,
                      ),
                      
                      autocorrect: true,
                      controller: confirmPassword,
                      decoration: const InputDecoration(
                          prefixIcon: Icon(
                            Icons.password,
                            color: Colors.white,
                          ),
                          filled: true,
                          hintText: 'Confirm Password',
                          hintStyle: TextStyle(
                            fontSize: 18,
                            color: Colors.white,
                          )),
                      obscureText: true,
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    SizedBox(
                      height: 50,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          ElevatedButton(
                            child: const Text(
                              "SAVE",
                              style: TextStyle(
                                  fontSize: 14,
                                  letterSpacing: 2.2,
                                  color: Colors.white),
                            ),
                            style: ButtonStyle(
                              backgroundColor: MaterialStateProperty.all(
                                  const Color.fromARGB(255, 25, 26, 25)),
                            ),
                            onPressed: () async {
                              if (email.text == '' ||
                                  password.text == '' ||
                                  confirmPassword.text == '') {
                                text = 'Error, Please Fill All Requirements';
                                showAlertDialog(context);
                              } else if (password.text.length <= 6) {
                                text = ' Weak Password !';
                                showAlertDialog(context);
                              } else if (password.text !=
                                  confirmPassword.text) {
                                text = "Password Doesn't Match !";
                                showAlertDialog(context);
                              } else {
                                if (await user.editProfile(
                                        email: email.text,
                                        password: password.text) ==
                                    'Error') {
                                  text = 'Error, Data Email Already Exist';
                                  showAlertDialog(context);
                                } else {
                                  text = 'Done, Data Updated successfully';
                                  showAlertDialog(context);
                                }
                              }
                            },
                          )
                        ],
                      ),
                    )
                  ],
                ),
              ),
            ),
          ],
        ));
  }

  showAlertDialog(
    BuildContext context,
  ) {
    // Create button
    Widget okButton = TextButton(
      child: const Text("OK"),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );

    // Create AlertDialog
    AlertDialog alert = AlertDialog(
      title: const Text("Alert"),
      content: Text(text),
      actions: [
        okButton,
      ],
    );

    // show the dialog
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return alert;
      },
    );
  }
}
