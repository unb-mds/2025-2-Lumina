import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/main.dart';
import 'package:frontend/chat_screen.dart';
import 'package:frontend/landing_page.dart';
import 'package:frontend/Settings.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';


void main() {
  late Directory tempDir;

  setUpAll(() async {
    // 1. Configurações globais
    try {
      apiBaseUrl = "http://teste-api.com";
    } catch (e) {
      // Ignora se já estiver definida
    }
    
    // 2. Cria diretório temporário
    tempDir = await Directory.systemTemp.createTemp('hive_main_test_dir');
    
    // 3. Configura Mock do PathProvider para o Hive (necessário para Hive.initFlutter)
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      const MethodChannel('plugins.flutter.io/path_provider'),
      (MethodCall methodCall) async {
        return tempDir.path;
      },
    );

    // 4. Inicializa o Hive e Prepara o Box
    await Hive.initFlutter();
    if (!Hive.isBoxOpen('chat_history')) {
       await Hive.openBox('chat_history');
    }
  });

  setUp(() {
    // 1. Limpa SharedPreferences antes de cada teste
    SharedPreferences.setMockInitialValues({});

    // 2. REINICIA O MOCK DO PATH PROVIDER ANTES DE CADA TESTE
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      const MethodChannel('plugins.flutter.io/path_provider'),
      (MethodCall methodCall) async {
        return tempDir.path;
      },
    );
  });

  

  // FUNÇÃO AUXILIAR CORRIGIDA: Sequência de pumps manual para concluir Futures
  Future<void> waitForChatScreenLoad(WidgetTester tester) async {
    // 1. Primeiro pump: Inicia o ChatScreen, chama initState() e mostra o loading.
    await tester.pump(); 
    
    // 2. Processa a fila de microtasks (onde as Futures mockadas terminam e o setState é chamado).
    await tester.pump(Duration.zero); 
    
    // 3. Terceiro pump: Reconstroi a tela após o setState.
    // O CircularProgressIndicator deve desaparecer e a UI real aparecer.
    await tester.pump(const Duration(milliseconds: 100)); 
  }

  group('ChatApp - Roteamento Inicial', () {
    testWidgets('Deve iniciar na LandingPage se showLanding for true', (WidgetTester tester) async {
      await tester.pumpWidget(const ChatApp(showLanding: true));
      await tester.pumpAndSettle();

      expect(find.byType(LandingPage), findsOneWidget);
      expect(find.byType(ChatScreen), findsNothing);
    });

   
  });

// -----------------------------------------------------------------------------

  group('ChatApp - Gerenciamento de Estado e Preferências', () {
    
    testWidgets('Deve carregar configurações salvas (Tema Dark e Fonte Grande)', (WidgetTester tester) async {
      SharedPreferences.setMockInitialValues({
        'theme_mode': ThemeMode.dark.index,
        'font_size_scale': 1.2,
        'username': 'Tester Main',
      });

      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester); // Aguarda o carregamento inicial

      final materialApp = tester.widget<MaterialApp>(find.byType(MaterialApp));
      expect(materialApp.themeMode, ThemeMode.dark);

      final context = tester.element(find.byType(ChatScreen));
      final mediaQuery = MediaQuery.of(context);
      expect(mediaQuery.textScaler, const TextScaler.linear(1.2));
      
      final chatScreen = tester.widget<ChatScreen>(find.byType(ChatScreen));
      expect(chatScreen.username, 'Tester Main');
    });

    testWidgets('Deve atualizar o Tema e salvar no SharedPreferences via rota de Configurações', (WidgetTester tester) async {
      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester);

      final BuildContext context = tester.element(find.byType(ChatScreen));
      Navigator.of(context).pushNamed('/settings');
      await tester.pumpAndSettle();

      expect(find.byType(ConfiguracoesPage), findsOneWidget);

      final settingsPage = tester.widget<ConfiguracoesPage>(find.byType(ConfiguracoesPage));
      
      settingsPage.onThemeModeChanged!(ThemeMode.light);
      await tester.pumpAndSettle();

      final materialApp = tester.widget<MaterialApp>(find.byType(MaterialApp));
      expect(materialApp.themeMode, ThemeMode.light);

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getInt('theme_mode'), ThemeMode.light.index);
    });

    testWidgets('Deve atualizar a Escala de Fonte e salvar no SharedPreferences', (WidgetTester tester) async {
      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester);

      final BuildContext context = tester.element(find.byType(ChatScreen));
      Navigator.of(context).pushNamed('/settings');
      await tester.pumpAndSettle();

      final settingsPage = tester.widget<ConfiguracoesPage>(find.byType(ConfiguracoesPage));
      settingsPage.onFontSizeScaleChanged!(1.4);
      await tester.pumpAndSettle();

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getDouble('font_size_scale'), 1.4);

      final newContext = tester.element(find.byType(ConfiguracoesPage));
      expect(MediaQuery.of(newContext).textScaler, const TextScaler.linear(1.4));
    });
    testWidgets('Deve atualizar o Nome de Usuário e salvar no SharedPreferences', (WidgetTester tester) async {
      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester);

      // 1. Navega para a tela de configurações
      final BuildContext context = tester.element(find.byType(ChatScreen));
      Navigator.of(context).pushNamed('/settings');
      await tester.pumpAndSettle();

      // 2. Chama o callback de atualização do username
      const String novoUsername = 'Novo Usuário Teste';
      final settingsPage = tester.widget<ConfiguracoesPage>(find.byType(ConfiguracoesPage));
      
      // Assumindo que ConfiguracoesPage tem um onUsernameChanged
      settingsPage.onUsernameChanged!(novoUsername); 
      await tester.pumpAndSettle();

      // 3. Verifica a persistência no SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('username'), novoUsername);

      // 4. Verifica se o estado do ChatApp foi atualizado (volta e verifica a ChatScreen)
      Navigator.of(context).pop(); // Volta para a ChatScreen
      await tester.pumpAndSettle();

      final chatScreen = tester.widget<ChatScreen>(find.byType(ChatScreen));
      expect(chatScreen.username, novoUsername);
    });
    testWidgets('Deve atualizar o Idioma e salvar no SharedPreferences', (WidgetTester tester) async {
      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester);

      // 1. Navega para a tela de configurações
      final BuildContext context = tester.element(find.byType(ChatScreen));
      Navigator.of(context).pushNamed('/settings');
      await tester.pumpAndSettle();

      // 2. Chama o callback de atualização do idioma
      const String novoIdioma = 'espanhol';
      final settingsPage = tester.widget<ConfiguracoesPage>(find.byType(ConfiguracoesPage));
      
      // Assumindo que ConfiguracoesPage tem um onLanguageChanged
      settingsPage.onLanguageChanged!(novoIdioma); 
      await tester.pumpAndSettle();

      // 3. Verifica a persistência no SharedPreferences
      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('language_string'), novoIdioma);

      // 4. Verifica se o estado do ChatApp foi atualizado (volta e verifica, se o idioma for exposto)
      // Se a main.dart atualiza algum estado global ou específico (como 'language_string' no seu código), 
      // essa verificação seria aqui. Por exemplo, se a ChatScreen tivesse uma propriedade 'currentLanguage'.
      // Como não temos essa propriedade no seu teste, focamos na persistência por enquanto.

      // Exemplo de verificação de estado atualizado (se o ChatApp expuser o idioma):
      // final chatApp = tester.widget<ChatApp>(find.byType(ChatApp));
      // expect(chatApp.currentLanguage, novoIdioma);
    });

    testWidgets('Deve resetar configurações para o padrão ao chamar _resetSelectSettings', (WidgetTester tester) async {
      SharedPreferences.setMockInitialValues({
        'theme_mode': ThemeMode.dark.index,
        'font_size_scale': 0.8,
        'language_string': 'ingles',
      });

      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester);

      var materialApp = tester.widget<MaterialApp>(find.byType(MaterialApp));
      expect(materialApp.themeMode, ThemeMode.dark);

      final BuildContext context = tester.element(find.byType(ChatScreen));
      Navigator.of(context).pushNamed('/settings');
      await tester.pumpAndSettle();

      final settingsPage = tester.widget<ConfiguracoesPage>(find.byType(ConfiguracoesPage));
      settingsPage.onResetSettings!(); 
      await tester.pumpAndSettle();

      final prefs = await SharedPreferences.getInstance();
      
      expect(prefs.get('theme_mode'), isNull);
      expect(prefs.get('font_size_scale'), isNull);
      expect(prefs.get('language_string'), isNull);

      materialApp = tester.widget<MaterialApp>(find.byType(MaterialApp));
      expect(materialApp.themeMode, ThemeMode.system); 
      
      final newContext = tester.element(find.byType(ConfiguracoesPage));
      expect(MediaQuery.of(newContext).textScaler, const TextScaler.linear(1.0));
    });
  });

// -----------------------------------------------------------------------------

  group('ChatApp - Reset de Tutoriais', () {
    testWidgets('Deve resetar as flags de tutorial no SharedPreferences', (WidgetTester tester) async {
      SharedPreferences.setMockInitialValues({
        'hasSeenChatTutorial': true,
        'hasSeenMenuTutorial': true,
      });

      await tester.pumpWidget(const ChatApp(showLanding: false));
      await waitForChatScreenLoad(tester);

      final BuildContext context = tester.element(find.byType(ChatScreen));
      Navigator.of(context).pushNamed('/settings');
      await tester.pumpAndSettle();

      final settingsPage = tester.widget<ConfiguracoesPage>(find.byType(ConfiguracoesPage));
      settingsPage.onResetTutorials!();
      await tester.pumpAndSettle();

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getBool('hasSeenChatTutorial'), false);
      expect(prefs.getBool('hasSeenMenuTutorial'), false);
    });
  });
}