import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/chat_screen.dart'; // Sua ChatScreen
import 'package:shared_preferences/shared_preferences.dart';
import 'package:frontend/main.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'dart:convert';
void main() {
  // Inicializa a variável global apiBaseUrl antes de todos os testes
  setUpAll(() {
    // Como ela é 'late final' no main.dart, precisamos setar um valor mock
    // para evitar o erro "LateInitializationError"
    try {
      apiBaseUrl = "http://teste-api.com";
    } catch (e) {
      // Se já estiver inicializada, ignoramos
    }
  });
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
  group('Testes de Fluxo de Conversa (Chat)', () {
    
    testWidgets('Deve enviar mensagem, exibir loading e mostrar resposta de sucesso da API', (WidgetTester tester) async {
      // 1. ARRANGE (Preparação)
      const userMessage = "Olá Lumina";
      const botResponse = "Olá! Sou uma IA contra desinformação.";
      
      // Cria um MockClient que intercepta as chamadas HTTP
      final mockHttp = MockClient((request) async {
        // Verifica se a URL está correta (incluindo o encode)
        if (request.url.toString().contains(Uri.encodeComponent(userMessage))) {
          // Retorna sucesso (200) com o JSON esperado
          return http.Response(
            jsonEncode({'response': botResponse}), 
            200,
            headers: {'content-type': 'application/json; charset=utf-8'},
          );
        }
        return http.Response("Not Found", 404);
      });

      await tester.pumpWidget(MaterialApp(
        home: ChatScreen(
          username: "Tester",
          currentLanguage: 'portugues',
          httpClient: mockHttp, // Injeta o mock aqui!
        ),
      ));
      await tester.pumpAndSettle(); // Aguarda inicialização (initState)

      // 2. ACT (Ação do Usuário)
      
      // Digita a mensagem
      final textField = find.byType(TextField);
      await tester.enterText(textField, userMessage);
      
      // Clica em enviar
      final sendButton = find.byIcon(Icons.send);
      await tester.tap(sendButton);
      
      // 3. ASSERT (Verificação Imediata - Mensagem do Usuário e Loading)
      
      // O flutter precisa reconstruir a tela para mostrar a mensagem do usuário
      await tester.pump(); 

      // Verifica se a mensagem do usuário apareceu na lista
      expect(find.text(userMessage), findsOneWidget);
      
      // Verifica se o indicador de progresso está aparecendo (estado _isSending = true)
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      // O campo de texto deve estar desabilitado ou com hint diferente?
      // No seu código: hintText muda para "Aguardando resposta..."
      expect(find.text("Aguardando resposta..."), findsOneWidget);

      // 4. ASSERT (Verificação Final - Resposta do Bot)
      
      // Aguarda a resposta do Future (simulado pelo MockClient)
      await tester.pumpAndSettle();

      // Verifica se o loading sumiu
      expect(find.byType(CircularProgressIndicator), findsNothing);

      // Verifica se a resposta do Mock apareceu na tela
      expect(find.text(botResponse), findsOneWidget);
    });

    testWidgets('Deve exibir mensagem de erro quando a API retornar erro (ex: 500)', (WidgetTester tester) async {
      // 1. ARRANGE
      final mockHttp = MockClient((request) async {
        return http.Response('Internal Server Error', 500);
      });

      await tester.pumpWidget(MaterialApp(
        home: ChatScreen(
          username: "Tester",
          currentLanguage: 'portugues',
          httpClient: mockHttp,
        ),
      ));
      await tester.pumpAndSettle();

      // 2. ACT
      await tester.enterText(find.byType(TextField), "Teste Erro");
      await tester.tap(find.byIcon(Icons.send));
      await tester.pump(); // Atualiza UI (msg usuário)

      // Aguarda o processamento assíncrono
      await tester.pumpAndSettle();

      // 3. ASSERT
      // Verifica se a mensagem de erro específica do seu código apareceu
      expect(find.text('Erro na API: Status Code 500'), findsOneWidget);
    });

    testWidgets('Deve exibir mensagem de erro de conexão quando ocorrer exceção', (WidgetTester tester) async {
      // 1. ARRANGE
      final mockHttp = MockClient((request) async {
        throw Exception("Falha de conexão");
      });

      await tester.pumpWidget(MaterialApp(
        home: ChatScreen(
          username: "Tester",
          currentLanguage: 'portugues',
          httpClient: mockHttp,
        ),
      ));
      await tester.pumpAndSettle();

      // 2. ACT
      await tester.enterText(find.byType(TextField), "Teste Conexão");
      await tester.tap(find.byIcon(Icons.send));
      await tester.pumpAndSettle(); 

      // 3. ASSERT
      // Verifica a mensagem do bloco catch(e)
      // Nota: O texto contém a variável apiBaseUrl, então usamos find.textContaining ou construímos a string exata
      final expectedErrorText = 'Erro de conexão: Verifique se o FastAPI está rodando em $apiBaseUrl.';
      
      // Use find.text() com a string exata para maior precisão
      expect(find.text(expectedErrorText), findsOneWidget);
    });

  testWidgets('Não deve enviar mensagem se o campo estiver vazio ou apenas espaços', (WidgetTester tester) async {
      // 1. ARRANGE
      bool requestMade = false;
      final mockHttp = MockClient((r) async {
        requestMade = true;
        return http.Response('OK', 200);
      });

      await tester.pumpWidget(MaterialApp(
        home: ChatScreen(
          username: "Tester",
          currentLanguage: 'portugues',
          httpClient: mockHttp,
        ),
      ));
      await tester.pumpAndSettle();

      const String textSpaces = '   '; 

      // 2. ACT
      await tester.enterText(find.byType(TextField), textSpaces);
      await tester.tap(find.byIcon(Icons.send));
      await tester.pumpAndSettle();

      // 3. ASSERT
      
      // CORREÇÃO: Procuramos o texto APENAS dentro da ListView (onde ficam as mensagens)
      // Isso ignora o TextField que ainda contém os espaços.
      final messageInListFinder = find.descendant(
        of: find.byType(ListView),
        matching: find.text(textSpaces),
      );

      expect(messageInListFinder, findsNothing);
      
      // Verifica se a requisição HTTP NÃO foi feita
      expect(requestMade, isFalse);
    });
  });
}