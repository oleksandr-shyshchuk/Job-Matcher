import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';
import 'dart:io';
import 'package:url_launcher/url_launcher.dart';
import 'work_ua.dart';

class VacancyDOUItem extends StatelessWidget {
  final String data;

  VacancyDOUItem({required this.data});
  
  
  /// Constructs a VacancyDOUItem widget.
  ///
  /// The [data] parameter is required and should contain the CSV data
  /// representing the attributes of the vacancy.
  @override
  Widget build(BuildContext context) {
    final List<dynamic> attributes = parseCsvString(data);

    return Card(
      margin: EdgeInsets.all(8.0),
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ListTile(
              title: Text(
                attributes[0], // Назва вакансії
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
            Divider(),
            ListTile(
              title: Row(
                children: [
                  Text(
                    '${attributes[1]}', // Назва компанії
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
                  Spacer(),
                  Text(
                    '${attributes[2]}', // Зарплата
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.green,
                    ),
                  ),
                ],
              ),
            ),
            ListTile(
              title: Text(
                'Description:',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              subtitle: Text(
                attributes[4].toString(), // Опис
                style: TextStyle(fontSize: 16),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: ListTile(
                    title: Text(
                      '',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    launch(attributes[5]); // Відкриття посилання у браузері
                  },
                  style: ElevatedButton.styleFrom(
                    side: BorderSide(color: Colors.black, width: 0.5), // Контур чорним коліром шириною 2 пікселя
                  ),
                  child: Text('Open Link'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
