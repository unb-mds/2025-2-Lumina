import 'package:flutter/material.dart';
import 'package:frontend/chat_screen.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:frontend/landing_page.dart';
import 'package:frontend/settings.dart'; 
import 'package:shared_preferences/shared_preferences.dart';




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

class ChatApp extends StatefulWidget {
  const ChatApp({super.key});

  @override
  State<ChatApp> createState() => _ChatAppState();
}

class _ChatAppState extends State<ChatApp> {
  ThemeMode _currentThemeMode = ThemeMode.system;
  double _fontSizeScale = 1.0;
  String? _username;
  String _currentLanguage = "portugues";
  @override
  void initState() {
    super.initState();
    _loadSettings(); 
  }

  void _resetSelectSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    await prefs.remove('theme_mode');
    await prefs.remove('language_string');
    await prefs.remove('font_size_scale');
    
    _loadSettings(); 
    
    debugPrint("Configurações de Tema, Idioma e Fonte Restauradas para o Padrão.");
}

  void _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _fontSizeScale = prefs.getDouble('font_size_scale') ?? 1.0;
      _username = prefs.getString('username');

      final themeIndex = prefs.getInt('theme_mode');
      if (themeIndex != null && themeIndex >= 0 && themeIndex < ThemeMode.values.length) {
        _currentThemeMode = ThemeMode.values[themeIndex];
      } else {
        _currentThemeMode = ThemeMode.system; 
      }

      _currentLanguage = prefs.getString('language_string') ?? 'portugues';
      if (_currentLanguage != 'portugues' && _currentLanguage != 'ingles') {
          _currentLanguage = 'portugues'; 
      }
    });
  }
  void _setUsername(String newUsername) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('username', newUsername);
    setState(() {
      _username = newUsername;
    });
  }
  void _setLanguage(String newLanguage) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('language_string', newLanguage); 
    setState(() {
      _currentLanguage = newLanguage;
    });
  }
  void _setThemeMode(ThemeMode newMode) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('theme_mode', newMode.index); 
    setState(() {
      _currentThemeMode = newMode;
    });
  }

  void _setFontSizeScale(double newScale) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('font_size_scale', newScale);
    setState(() {
      _fontSizeScale = newScale;
    });
  }
 
  void _resetTutorials() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool('hasSeenChatTutorial', false);
  await prefs.setBool('hasSeenMenuTutorial', false);
  debugPrint("Tutoriais resetados.");
  }



  final _lightColorScheme = ColorScheme.fromSeed(
    seedColor: Colors.blueGrey,
    primary: const Color.fromARGB(255, 93, 7, 173),
    brightness: Brightness.light,
  );
  
  final _darkColorScheme = ColorScheme.fromSeed(
    seedColor: Colors.blueGrey,
    primary: const Color.fromARGB(255, 173, 93, 255), 
    brightness: Brightness.dark,
  );
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gemini Chatbot',
      debugShowCheckedModeBanner: false,
      themeMode: _currentThemeMode, 
      
      theme: ThemeData(
        colorScheme: _lightColorScheme,
        primarySwatch: Colors.deepPurple,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        useMaterial3: true,
      ),
      
      darkTheme: ThemeData(
        colorScheme: _darkColorScheme,
        primarySwatch: Colors.deepPurple,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        useMaterial3: true,
      ),
      builder: (context, child) {
        return MediaQuery(
          data: MediaQuery.of(context).copyWith(
            textScaler: TextScaler.linear(_fontSizeScale),
          ),
          child: child!,
        );
      },
       
    
      initialRoute: '/',
      routes: {
        '/': (context) => LandingPage(
         initialUsername: _username,
          onUsernameSet: _setUsername, 
        ),
        '/chat': (context) {
          
          return ChatScreen(username: _username, currentLanguage: _currentLanguage);
        },
      },
      onGenerateRoute: (settings) {
        if (settings.name == '/settings') {
          final currentUsername = _username ?? 'Visitante';
          return MaterialPageRoute(
            builder: (context) {
              return ConfiguracoesPage(
                currentFontSizeScale: _fontSizeScale,
                onFontSizeScaleChanged: _setFontSizeScale,
                currentUsername: currentUsername, 
                onUsernameChanged: _setUsername, 
                currentThemeMode: _currentThemeMode,
                onThemeModeChanged: _setThemeMode,
                currentLanguage: _currentLanguage,
                onLanguageChanged: _setLanguage,
                onResetSettings: _resetSelectSettings,
                onResetTutorials: _resetTutorials,
              );
            },
          );
        }
        return null; 
      },
    );
  }
}


