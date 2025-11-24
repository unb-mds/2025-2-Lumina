import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/chat_screen.dart'; // Sua ChatScreen
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  // Configura o SharedPreferences para retornar que os tutoriais JÁ FORAM vistos
  setUp(() {
    SharedPreferences.setMockInitialValues({
      'hasSeenChatTutorial': true,
      'hasSeenMenuTutorial': true,
    });
  });

  Widget buildTestableWidget() {
    return const MaterialApp(
      home: ChatScreen(
        username: "TesteUser",
        currentLanguage: 'portugues',
      ),
    );
  }

  testWidgets('ChatScreen deve exibir a mensagem de boas-vindas inicial', (WidgetTester tester) async {
    // 1. Arrange (Preparação)
    const testUsername = "TesteUser";
    const initialMessagePart = "Olá $testUsername! Sou Lumina, sua agente de IA para o combate à desinformação, como posso te ajudar hoje?";

    // 2. Act (Ação)
    // Constrói o widget com o MaterialApp para fornecer o Theme e o Navigator.
    await tester.pumpWidget(
      const MaterialApp(
        home: ChatScreen(
          username: testUsername,
          currentLanguage: 'portugues',
        ),
      ),
    );

    // O método initState chama _checkTutorialStatus (async),
    // então precisamos de um pump para processar essa chamada e o setState.
    await tester.pumpAndSettle();

    // 3. Assert (Verificação)
    
    // Verifica se a AppBar com o título 'LUMINA' está presente.
    expect(find.text('LUMINA'), findsOneWidget);

    // Verifica se a mensagem de boas-vindas (que contém o username) está presente.
    expect(find.textContaining(initialMessagePart), findsOneWidget);

    // Verifica se o campo de texto para envio de mensagens está presente.
    expect(find.byType(TextField), findsOneWidget);
    
    // Verifica se o botão de envio está presente.
    expect(find.byIcon(Icons.send), findsOneWidget);
  });
 testWidgets('Tutorial de Chat deve ser exibido na primeira visita e fechar ao toque', (WidgetTester tester) async {
    // 1. Arrange: Configura o SharedPreferences
    SharedPreferences.setMockInitialValues({
      'hasSeenChatTutorial': false, 
      'hasSeenMenuTutorial': false,
    });

    // 2. Act: Renderiza o widget
    await tester.pumpWidget(buildTestableWidget());
    await tester.pumpAndSettle(); 
    
    // Localiza o tutorial usando a nova Key
    final chatTutorialFinder = find.byKey(const Key('chatTutorialOverlay')); 

    // 3. Assert (Verificação Inicial)
    expect(chatTutorialFinder, findsOneWidget, reason: 'O tutorial de chat deve ser encontrado.');
    expect(find.text("Clique aqui para abrir o menu"), findsOneWidget, reason: 'O balão do menu deve estar visível.');
    
    
    // 4. Act (Interação): Simula o toque no tutorial para fechá-lo
    await tester.tap(chatTutorialFinder);
    
    // ⚠️ CHAVE DA CORREÇÃO:
    // O método _closeChatTutorial é ASSÍNCRONO e chama setState.
    // É crucial chamar pumpAndSettle() após o tap para garantir que:
    // 1. A função _closeChatTutorial termine sua execução assíncrona (salvar no SharedPreferences).
    // 2. O setState (que define _showChatTutorial = false) seja processado e o widget seja reconstruído.
    await tester.pumpAndSettle(); 

    // 5. Assert (Verificação Após Interação)
    
    // Verifica se o tutorial de chat DESAPARECEU (findsNothing)
    expect(chatTutorialFinder, findsNothing, reason: 'O tutorial de chat deve ter desaparecido após o toque.');

    // Verifica se o estado foi SALVO no SharedPreferences
    final prefs = await SharedPreferences.getInstance();
    expect(prefs.getBool('hasSeenChatTutorial'), isTrue, reason: 'O estado "hasSeenChatTutorial" deve ser salvo como true.');

  });


  // --- Teste do Tutorial de Menu (Drawer) ---
  testWidgets('Tutorial de Menu deve ser exibido após o chat tutorial ser visto e ao abrir o Drawer', (WidgetTester tester) async {
    // 1. Arrange: Configura o SharedPreferences
    SharedPreferences.setMockInitialValues({
      'hasSeenChatTutorial': true, // SIMULA: Chat tutorial já visto
      'hasSeenMenuTutorial': false, // SIMULA: Menu tutorial NUNCA visto
    });

    // 2. Act: Renderiza o widget
    await tester.pumpWidget(buildTestableWidget());
    await tester.pumpAndSettle();
    
    // 3. Assert (Verificação Inicial)
    
    // O tutorial de menu NÃO deve estar visível (porque o Drawer está fechado)
    expect(find.text("Clique aqui para abrir as configurações"), findsNothing, reason: 'O tutorial de menu não deve aparecer com o drawer fechado.');

    // 4. Act (Ação): Abre o Drawer
    final menuButton = find.byIcon(Icons.menu);
    await tester.tap(menuButton);
    await tester.pumpAndSettle(); // Espera o Drawer abrir

    // 5. Assert (Verificação com o Drawer Aberto)
    
    // Verifica se o Drawer está aberto
    expect(find.byType(Drawer), findsOneWidget);
    
    // O tutorial de menu DEVE estar visível (é o GestureDetector dentro do Stack do Drawer)
    final menuTutorialFinder = find.text("Clique aqui para abrir as configurações");
    expect(menuTutorialFinder, findsOneWidget, reason: 'O tutorial de menu deve ser exibido quando o drawer é aberto.');
    
    // 6. Act (Interação): Simula o toque no tutorial de menu para fechá-lo
    // O tutorial está dentro do Drawer Stack, vamos tocar nele
    await tester.tap(find.byType(GestureDetector).last); 
    await tester.pumpAndSettle(); // Processa a chamada _closeMenuTutorial (async) e o setState

    // 7. Assert (Verificação Após Interação)
    
    // Verifica se o tutorial de menu DESAPARECEU
    expect(menuTutorialFinder, findsNothing, reason: 'O tutorial de menu deve ter desaparecido após o toque.');

    // Verifica se o estado foi SALVO no SharedPreferences
    final prefs = await SharedPreferences.getInstance();
    expect(prefs.getBool('hasSeenMenuTutorial'), isTrue, reason: 'O estado "hasSeenMenuTutorial" deve ser salvo como true.');

  });
}