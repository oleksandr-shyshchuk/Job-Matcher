import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';
import 'dart:io';
import 'package:url_launcher/url_launcher.dart';
import 'work_ua.dart';


/// A widget to display a single vacancy item from Robota.ua website.
class VacancyRobotaUAItem extends StatelessWidget {
  final String data;

  VacancyRobotaUAItem({required this.data});

  /// Constructs a VacancyRobotaUAItem widget.
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
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Flexible(
                  flex: 4,
                  child: ListTile(
                    title: Text(
                      attributes[0], // Назва вакансії
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
                Flexible(
                  child: Align(
                    alignment: Alignment.bottomRight,
                    child: Text(
                      attributes[3], // Розташування компанії
                      style: TextStyle(fontSize: 12),
                    ),
                  ),
                ),
              ],
            ),
            Divider(),
            ListTile(
              title: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '${attributes[1]}', // Назва компанії
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                  ),
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
              subtitle: attributes[7] != null && attributes[7].isNotEmpty
                ? Text(
                    attributes[7].toString(), // Опис
                    style: TextStyle(fontSize: 16),
                  )
                : null,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: ListTile(
                    title: Text(
                      'Posted:',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      attributes[5].toString(), // Час
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    launch(attributes[6]); // Відкриття посилання у браузері
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
