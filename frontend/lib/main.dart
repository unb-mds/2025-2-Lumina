import 'package:flutter/material.dart';
import 'package:frontend/ChatScreen.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:frontend/LandingPage.dart';
import 'package:frontend/Settings.dart'; 
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
  
// Verifica se o usuário já viu a landing page
  final prefs = await SharedPreferences.getInstance();
  final hasSeenLanding = prefs.getBool('hasSeenLanding') ?? false;

  runApp(ChatApp(showLanding: !hasSeenLanding,));
}

class ChatApp extends StatefulWidget {
  final bool showLanding;
  const ChatApp({super.key, required this.showLanding});

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
    _loadSettings(); // Carrega todas as configurações
  }

  void _resetSelectSettings() async {
    final prefs = await SharedPreferences.getInstance();
    
    // Remove apenas as chaves de Tema, Idioma e Tamanho da Fonte
    // O nome de usuário (chave 'username') é mantido.
    await prefs.remove('theme_mode');
    await prefs.remove('language_string');
    await prefs.remove('font_size_scale');
    
    // Recarrega as configurações. Como as chaves foram removidas, 
    // _loadSettings aplicará os valores padrão e chamará setState.
    _loadSettings(); 
    
    debugPrint("Configurações de Tema, Idioma e Fonte Restauradas para o Padrão.");
}

  // NOVO: Função para carregar todas as configurações
  void _loadSettings() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _fontSizeScale = prefs.getDouble('font_size_scale') ?? 1.0;
      // NOVO: Carrega o nome de usuário, se não encontrar, usa null
      _username = prefs.getString('username');

      final themeIndex = prefs.getInt('theme_mode');
      if (themeIndex != null && themeIndex >= 0 && themeIndex < ThemeMode.values.length) {
        _currentThemeMode = ThemeMode.values[themeIndex];
      } else {
        _currentThemeMode = ThemeMode.system; // Padrão
      }

      _currentLanguage = prefs.getString('language_string') ?? 'portugues';
      // Garante que o valor carregado seja válido
      if (_currentLanguage != 'portugues' && _currentLanguage != 'ingles') {
          _currentLanguage = 'portugues'; 
      }
    });
  }
  // FUNÇÃO DE ATUALIZAÇÃO CHAVE: Salva o novo nome e atualiza o estado
  void _setUsername(String newUsername) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('username', newUsername);
    setState(() {
      _username = newUsername;
    });
  }
  // CORREÇÃO: Recebe e salva o idioma como String
  void _setLanguage(String newLanguage) async {
    final prefs = await SharedPreferences.getInstance();
    // Usa uma nova chave para armazenar a String
    await prefs.setString('language_string', newLanguage); 
    setState(() {
      _currentLanguage = newLanguage;
    });
  }
  // NOVO: Função para atualizar e persistir o tema
  void _setThemeMode(ThemeMode newMode) async {
    final prefs = await SharedPreferences.getInstance();
    // Salva o índice (inteiro) do ThemeMode
    await prefs.setInt('theme_mode', newMode.index); 
    setState(() {
      _currentThemeMode = newMode;
    });
  }

  // Função de callback para ser passada para a página de Configurações
  void _setFontSizeScale(double newScale) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('font_size_scale', newScale);
    setState(() {
      _fontSizeScale = newScale;
    });
  }
 
  // Função para resetar os tutoriais
  void _resetTutorials() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool('hasSeenChatTutorial', false);
  await prefs.setBool('hasSeenMenuTutorial', false);
  debugPrint("Tutoriais resetados.");
  }



  // Definições de cores para os dois temas
  final _lightColorScheme = ColorScheme.fromSeed(
    seedColor: Colors.blueGrey,
    primary: const Color.fromARGB(255, 93, 7, 173),
    brightness: Brightness.light,
  );
  
  final _darkColorScheme = ColorScheme.fromSeed(
    seedColor: Colors.blueGrey,
    primary: const Color.fromARGB(255, 173, 93, 255), // Um primário mais claro para o modo escuro
    brightness: Brightness.dark,
  );
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gemini Chatbot',
      debugShowCheckedModeBanner: false,
      // NOVO: Usa o tema persistente
      themeMode: _currentThemeMode, 
      
      // NOVO: Define o Tema Claro (usado quando themeMode é light)
      theme: ThemeData(
        colorScheme: _lightColorScheme,
        primarySwatch: Colors.deepPurple,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        useMaterial3: true,
      ),
      
      // NOVO: Define o Tema Escuro (usado quando themeMode é dark)
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
       
    
      initialRoute: widget.showLanding ? '/' : '/chat',
      routes: {
        '/': (context) => LandingPage(
         initialUsername: _username,
          onUsernameSet: _setUsername, // Passa a função para salvar
        ),
        '/chat': (context) {
          
          return ChatScreen(username: _username, currentLanguage: _currentLanguage);
        },
      },
      // NOVO: Altera o mapeamento de rotas para passar a função de callback para SettingsPage
      onGenerateRoute: (settings) {
        if (settings.name == '/settings') {
          // Garante que o nome do usuário seja passado para a página de configurações
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
        return null; // Deixa o roteamento padrão cuidar de outras rotas
      },
    );
  }
}


