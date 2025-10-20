import 'package:flutter/material.dart';
import 'package:frontend/ChatScreen.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:frontend/Settings.dart'; 


late final String apiBaseUrl;


Future<void> main() async {
  
  WidgetsFlutterBinding.ensureInitialized(); 

  
  try {
    await dotenv.load(fileName: ".env");
   
    apiBaseUrl = dotenv.env['API_BASE_URL']!;
    debugPrint("URL da API carregada: $apiBaseUrl");
  } catch (e) {
   
    debugPrint("ERRO: Não foi possível carregar o arquivo .env ou a chave API_BASE_URL está faltando. Usando fallback.");
    apiBaseUrl = "http://10.0.2.2:8000"; 
  }
  
  runApp(const ChatApp());
}

class ChatApp extends StatelessWidget {
  const ChatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gemini Chatbot',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blueGrey,
          primary: const Color.fromARGB(255, 93, 7, 173), 
        ),
        useMaterial3: true,
      ),
      home: const ChatScreen(),
      routes: {
        '/settings': (context) => const ConfiguracoesPage(),
      },
    );
  }
}


