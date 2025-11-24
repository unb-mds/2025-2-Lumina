import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/landing_page.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mockito/mockito.dart';

class MockSharedPreferences extends Mock implements SharedPreferences {}



void main() {
  // Configuração para simular as preferências compartilhadas antes de cada teste
  // É necessário simular o SharedPreferences porque ele usa métodos estáticos.
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
}