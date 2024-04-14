import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';
import 'dart:io';
import 'package:http_parser/http_parser.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:file_picker/file_picker.dart';
import 'work_ua.dart';
import 'djinni.dart';
import 'dou.dart';
import 'robota_ua.dart';
import 'dart:convert';

void main() {
  runApp(MyApp());
}

/// MyApp is the root widget of the application, it sets up the MaterialApp.
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Navigation Example',
      home: HomePage(),
    );
  }
}

final TextEditingController _searchController = TextEditingController();

/// HomePage displays the main interface of the application.
class HomePage extends StatelessWidget {

  final List<Map<String, dynamic>> options = [
    {'title': 'Work.ua', 'data': 'work.ua'},
    {'title': 'Robota.ua', 'data': 'robota.ua'},
    {'title': 'DOU', 'data': 'dou'},
    {'title': 'Djinni', 'data': 'djinni'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home'),
        actions: [
          IconButton(
            icon: Icon(Icons.description),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => PDFDownloader()),
              );
            },
          ),
        ],
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: options.length,
              itemBuilder: (context, index) {
                final option = options[index];
                return Card(
                  margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: ListTile(
                    title: Text(option['title']),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => OptionPage(
                            title: option['title'],
                            data: option['data'],
                            searchQuery: _searchController.text,
                          ),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}


/// OptionPage displays the list of vacancies based on the selected option.
class OptionPage extends StatefulWidget {
  final String title;
  final String data;
  final String searchQuery;

  OptionPage({
    required this.title,
    required this.data,
    required this.searchQuery,
  });

  @override
  _OptionPageState createState() => _OptionPageState();
}

class _OptionPageState extends State<OptionPage> {
  List<String> vacanciesData = [];

  void fetchData() async {
    final url = "http://0.0.0.0:8000/get_vacancies/?request=${widget.searchQuery}&source=${widget.data}";
    print(url);
    
    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      final rows = response.body.split('\n');
      setState(() {
        vacanciesData = rows.sublist(1);
      });
    } else {
      setState(() {
        vacanciesData = ["Помилка при отриманні CSV з API"];
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> cldrn;
    if (widget.data == 'djinni') {
      cldrn = vacanciesData.map((row) => VacancyDjinniItem(data: row)).toList();
    } else if (widget.data == 'dou') {
      cldrn = vacanciesData.map((row) => VacancyDOUItem(data: row)).toList();
    } else if (widget.data == 'robota.ua') {
      cldrn = vacanciesData.map((row) => VacancyRobotaUAItem(data: row)).toList();
    } else {
      cldrn = vacanciesData.map((row) => VacancyWorkUAItem(data: row)).toList();
    }
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: cldrn,
        ),
      ),
    );
  }
}


/// PDFDownloader allows users to pick a PDF file and send it to an API for analysis.
class PDFDownloader extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PDF Downloader'),
      ),
      body: Center(
        child: ElevatedButton(
            onPressed: () async {
              FilePickerResult? result = await FilePicker.platform.pickFiles(
                type: FileType.custom,
                allowedExtensions: ['pdf'],
              );
          
              if (result != null) {
                File file = File(result.files.single.path!);
                String fileName = result.files.single.name;
                // Виконати HTTP запит на ваш API для передачі файлу
                var request = http.MultipartRequest(
                  'POST',
                  Uri.parse('http://127.0.0.1:8000/analyze_resume/'),
                );
          
                request.files.add(
                  http.MultipartFile(
                    'file',
                    file.readAsBytes().asStream(),
                    file.lengthSync(),
                    filename: fileName,
                    contentType: MediaType('application', 'pdf'),
                  ),
                );
          
                var response = await http.Client().send(request);
          
                if (response.statusCode == 200) {
                  print('Файл успішно передано');
                  var responseBody = await response.stream.bytesToString();
                  var jsonResponse = jsonDecode(responseBody);
                  _searchController.text = jsonResponse['class'];
                  
                  Navigator.pop(context);
                  
                } else {
                  print('Помилка під час передачі файлу: ${response.reasonPhrase}');
                }
              }
            },
            style: ElevatedButton.styleFrom(
              shape: CircleBorder(),
              padding: EdgeInsets.all(20),
            ),
            child: Icon(
              Icons.add,
              size: 50,
              color: Colors.black, // Колір плюса
            ), // Великий плюс посередині
          ),
      ),
    );
  }
}
