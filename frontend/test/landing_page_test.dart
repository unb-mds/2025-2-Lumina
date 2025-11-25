import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/landing_page.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mockito/mockito.dart';
import 'package:frontend/Settings.dart';
class MockSharedPreferences extends Mock implements SharedPreferences {}

class ChatScreenMock extends StatelessWidget {
  final String username;
  const ChatScreenMock({super.key, required this.username});

  @override
  Widget build(BuildContext context) {
    // Tela de Chat mínima com um botão de Configurações
    return Scaffold(
      key: const Key('chatScreen'), // Chave para encontrar a tela de chat
      appBar: AppBar(
        title: const Text('ChatScreenMock'),
        actions: [
          IconButton(
            key: const Key('settingsButton'), // Chave para encontrar o botão de Configurações
            icon: const Icon(Icons.settings),
            onPressed: () {
              // Simula a navegação para a rota de configurações definida no TestAppWrapper
              Navigator.pushNamed(context, '/settings'); 
            },
          ),
        ],
      ),
      body: Center(child: Text('Bem-vindo, $username')),
    );
  }
}

// Wrapper para simular a gestão de estado do nome de usuário (como em main.dart)
class TestAppWrapper extends StatefulWidget {
  const TestAppWrapper({super.key});

  @override
  State<TestAppWrapper> createState() => _TestAppWrapperState();
}

class _TestAppWrapperState extends State<TestAppWrapper> {
  String _username = '';

  // Função que simula o _setUsername em main.dart para atualizar o estado
  void _setUsername(String newUsername) {
    setState(() {
      _username = newUsername;
    });
  }

  @override
  Widget build(BuildContext context) {
    final currentUsername = _username.isEmpty ? 'Visitante' : _username;
    
    return MaterialApp(
      // É importante definir um tema, pois a ConfiguracoesPage usa Theme.of(context)
      theme: ThemeData.light(), 
      routes: {
        '/': (context) => LandingPage(
          initialUsername: _username,
          onUsernameSet: _setUsername, // Passa o callback de atualização
        ),
        '/chat': (context) {
          return ChatScreenMock(username: currentUsername); // Usa o nome de usuário atualizado
        },
      },
      onGenerateRoute: (settings) {
        if (settings.name == '/settings') {
          return MaterialPageRoute(
            builder: (context) {
              // Configura a ConfiguracoesPage real com o nome de usuário atualizado
              return ConfiguracoesPage(
                currentFontSizeScale: 1.0,
                onFontSizeScaleChanged: (_) {},
                currentUsername: currentUsername, // O NOME DE USUÁRIO É PASSADO AQUI!
                onUsernameChanged: _setUsername,
                currentThemeMode: ThemeMode.system,
                onThemeModeChanged: (_) {},
                currentLanguage: 'portugues', 
                onResetSettings: () async {},
                onResetTutorials: () async {},
              );
            },
          );
        }
        return null;
      },
    );
  }
}

void main() {
  // Configuração para simular as preferências compartilhadas antes de cada teste
  // É necessário simular o SharedPreferences porque ele usa métodos estáticos.
  // ignore: unused_local_variable
  late MockSharedPreferences mockPrefs;

  setUp(() {
    mockPrefs = MockSharedPreferences();
    // Simula o método getInstance para retornar nosso mock
    SharedPreferences.setMockInitialValues({});
  });


  testWidgets('LandingPage renderiza o título "LUMINA" e o campo de nome de usuário', (WidgetTester tester) async {
    // ARRANGE
    // O teste precisa de um MaterialApp como pai para contextos como Navigator
    await tester.pumpWidget(
      const MaterialApp(
        home: LandingPage(),
      ),
    );

    // ACT & ASSERT
    // 1. Verificar se o título "LUMINA" está na tela
    expect(find.text('LUMINA'), findsOneWidget);

    // 2. Verificar se o campo de texto (TextField) com a chave 'usernameField' está presente
    expect(find.byKey(const Key('usernameField')), findsOneWidget);

    // 3. Verificar se o botão de avançar (Icon) está presente
    expect(find.byIcon(Icons.arrow_forward), findsOneWidget);

    // 4. Verificar se a mensagem de boas-vindas está presente
    expect(find.text('Bem vindo ao Lumina'), findsOneWidget);
  });
  testWidgets('Aperta o botão sem nome e exibe SnackBar de erro', (WidgetTester tester) async {
    // ARRANGE
    await tester.pumpWidget(
      MaterialApp(
        // Adicionando rotas, pois o teste fará um Navigator.pushReplacementNamed
        routes: {
          '/chat': (context) => const Placeholder(), // Mock da tela de chat
        },
        home: const LandingPage(),
      ),
    );

    // ACT
    // O campo de texto começa vazio por padrão, então simulamos o tap no botão.
    
    // 1. Encontrar o ícone de avançar dentro do botão
    final forwardButtonFinder = find.byIcon(Icons.arrow_forward);
    
    // 2. Tocar no botão
    await tester.tap(forwardButtonFinder);
    
    // 3. Reconstruir os widgets para que o SnackBar seja exibido (o SnackBar é um Overlay)
    await tester.pump(); 

    // ASSERT
    // Verificar se o SnackBar de erro é exibido
    expect(find.text('Por favor, digite seu nome para continuar.'), findsOneWidget);
    
    // Verificar se a navegação não ocorreu
    // Se a navegação ocorresse, a tela /chat apareceria. Como não navegamos,
    // o widget de mock 'Placeholder' não deve ser encontrado.
    expect(find.byType(Placeholder), findsNothing);
  });
  testWidgets('Insere nome e clica no botão, deve navegar para a tela de chat', (WidgetTester tester) async {
  // ARRANGE
  const String testUsername = 'Alice';
  
  await tester.pumpWidget(
    MaterialApp(
      // É crucial definir a rota /chat
      routes: {
        '/chat': (context) => const Text('ChatScreenMock'), // Mock da tela de chat para verificação
      },
      home: const LandingPage(),
    ),
  );

  // ACT
  // 1. Encontrar o campo de texto
  final usernameFieldFinder = find.byKey(const Key('usernameField'));
  
  // 2. Digitar o nome de usuário no campo
  await tester.enterText(usernameFieldFinder, testUsername);
  
  // 3. Encontrar e tocar no botão de avançar
  final forwardButtonFinder = find.byIcon(Icons.arrow_forward);
  await tester.tap(forwardButtonFinder);
  
  // 4. Reconstruir os widgets para que a navegação ocorra
  // NOTA: Para uma navegação assíncrona (como um push replacement), 
  // pode ser necessário um pumpAndSettle para aguardar todas as animações
  // e frames de construção.
  await tester.pumpAndSettle(); 

  // ASSERT
  // 1. Verificar se o widget da tela de chat (o nosso mock 'ChatScreenMock') está na tela
  expect(find.text('ChatScreenMock'), findsOneWidget);

  // 2. Opcional: Verificar se a LandingPage não está mais na tela
  expect(find.byType(LandingPage), findsNothing);
  
  // 3. Opcional: Verificar se o nome foi salvo (se a lógica da LandingPage salvar o nome)
  // Como SharedPreferences.setMockInitialValues({}) foi usado no setUp, 
  // não podemos facilmente verificar o valor salvo aqui, mas o sucesso da navegação 
  // já indica que o método save/navigate foi chamado.
});

testWidgets('Aperta o botão com apenas espaços e exibe SnackBar de erro', (WidgetTester tester) async {
  // ARRANGE
  const String spaceOnlyUsername = '   '; // Três espaços
  
  await tester.pumpWidget(
    MaterialApp(
      routes: {
        '/chat': (context) => const Placeholder(),
      },
      home: const LandingPage(),
    ),
  );

  // ACT
  // 1. Digitar apenas espaços no campo de texto
  await tester.enterText(find.byKey(const Key('usernameField')), spaceOnlyUsername);
    
  // 2. Tocar no botão
  await tester.tap(find.byIcon(Icons.arrow_forward));
  
  // 3. Reconstruir os widgets para que o SnackBar seja exibido
  await tester.pump(); 

  // ASSERT
  // Verificar se o SnackBar de erro é exibido (a mesma mensagem de campo vazio)
  expect(find.text('Por favor, digite seu nome para continuar.'), findsOneWidget);
    
  // Verificar se a navegação não ocorreu
  expect(find.byType(Placeholder), findsNothing);
});
testWidgets('Username digitado na LandingPage é exibido corretamente na ConfiguracoesPage', (WidgetTester tester) async {
  // ARRANGE
  const String expectedUsername = 'TesteUser';
  
  // 1. Inicializa o Wrapper que simula o fluxo completo do app
  await tester.pumpWidget(const TestAppWrapper());
  
  // ACT (1) - Digitar o nome de usuário na LandingPage
  await tester.enterText(find.byKey(const Key('usernameField')), expectedUsername);
  await tester.pump(); 

  // ACT (2) - Tocar no botão de navegação para /chat
  await tester.tap(find.byIcon(Icons.arrow_forward));
  
  // Completa a transição do Navigator.pushReplacementNamed
  await tester.pumpAndSettle(); 

  // ASSERT (Navegação para Chat)
  expect(find.byType(LandingPage), findsNothing);
  expect(find.byType(ChatScreenMock), findsOneWidget);
  
  // ACT (3) - Tocar no botão de Configurações na ChatScreenMock para ir para /settings
  await tester.tap(find.byKey(const Key('settingsButton')));
  
  // Completa a transição de navegação
  await tester.pumpAndSettle();

  // ASSERT (Configurações)
  // 1. Verifica se a ConfiguracoesPage está na tela
  expect(find.byType(ConfiguracoesPage), findsOneWidget);
  
  // 2. Verifica se o nome de usuário digitado ('TesteUser') está sendo exibido na tela
  // O nome de usuário é o 'subtitle' do tile de Usuário.
  expect(find.text(expectedUsername), findsOneWidget); 
  
  // 3. Opcional: Verifica o título do tile para garantir o contexto.
  expect(find.text('Usuário'), findsOneWidget);
});
testWidgets('Campo de usuário deve exibir o initialUsername se fornecido', (WidgetTester tester) async {
  // ARRANGE
  const String existingUsername = 'PreenchidoAutomatico';
  
  // 1. Renderiza a LandingPage fornecendo um nome de usuário inicial.
  await tester.pumpWidget(
    MaterialApp(
      home: LandingPage(
        initialUsername: existingUsername,
        onUsernameSet: (_) {}, // Fornece um callback mock
      ),
    ),
  );

  // ACT & ASSERT
  // 2. Verifica se o campo de texto contém o nome de usuário esperado.
  // Procuramos por um TextField/TextFormField que contenha o texto.
  expect(find.text(existingUsername), findsOneWidget);
  
  // 3. Verifica se o controller do campo de texto tem o valor correto.
  final textField = tester.widget<TextField>(find.byKey(const Key('usernameField')));
  expect(textField.controller!.text, existingUsername);
});
testWidgets('Aperta o botão com campo vazio e exibe SnackBar de erro', (WidgetTester tester) async {
  // ARRANGE
  // Garante que o campo está vazio por padrão
  await tester.pumpWidget(
    MaterialApp(
      routes: {
        '/chat': (context) => const Placeholder(),
      },
      home: const LandingPage(),
    ),
  );

  // ACT
  // O campo já está vazio.
  
  // 1. Tocar no botão
  await tester.tap(find.byIcon(Icons.arrow_forward));
  
  // 2. Reconstruir para que o SnackBar seja exibido
  await tester.pump(); 

  // ASSERT
  // Verifica se a mensagem de erro correta é exibida
  expect(find.text('Por favor, digite seu nome para continuar.'), findsOneWidget);
  
  // 3. Verifica se a navegação não ocorreu
  expect(find.byType(Placeholder), findsNothing);
});
}