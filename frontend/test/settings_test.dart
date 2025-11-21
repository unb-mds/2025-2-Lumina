import 'package:flutter_test/flutter_test.dart';
// Importe o arquivo que contém a função que você quer testar
import 'package:frontend/Settings.dart'; 
import 'package:flutter/material.dart';

void main() {
  
  // O group() é opcional, mas ajuda a organizar testes relacionados
  group('Testes de Tradução (tForTest)', () {
    
    // test() define um caso de teste individual
    test('Deve traduzir "config_title" para português', () {
      // 1. Prepara (Arrange)
      const key = 'config_title';
      const lang = 'portugues';
      
      // 2. Atua (Act)
      final result = tForTest(key, lang);
      
      // 3. Verifica (Assert)
      expect(result, 'Configurações');
    });

    test('Deve traduzir "config_title" para inglês', () {
      const key = 'config_title';
      const lang = 'ingles';
      
      final result = tForTest(key, lang);
      
      expect(result, 'Settings');
    });

    test('Deve retornar a chave se a tradução não existir', () {
      const key = 'chave_inexistente';
      const lang = 'portugues';
      
      final result = tForTest(key, lang);
      
      expect(result, 'chave_inexistente');
    });

    group('Teste de Interface: Tamanho da Fonte', () {
    
    testWidgets('Deve abrir o diálogo, alterar o Slider e salvar o novo valor', (WidgetTester tester) async {
      // 1. ARRANGE (Preparação)
      double? capturedScale; // Variável para capturar o valor que o widget vai devolver
      
      // Precisamos envolver a página em MaterialApp para ter tema e navegação
      await tester.pumpWidget(MaterialApp(
        home: ConfiguracoesPage(
          currentThemeMode: ThemeMode.system,
          currentLanguage: 'portugues',
          currentUsername: 'UsuarioTeste',
          // Define o valor inicial como 1.0
          currentFontSizeScale: 1.0, 
          // Aqui capturamos o valor quando o usuário clicar em SALVAR
          onFontSizeScaleChanged: (newScale) {
            capturedScale = newScale;
          },
        ),
      ));

      // 2. ACT (Ação)
      
      // Passo A: Encontrar e clicar na opção "Tamanho da Fonte"
      // Usamos o ícone para garantir que é o tile correto, já que o texto aparece no título e no tile
      
      // Se o finder acima for muito específico, podemos usar: find.text('Tamanho da Fonte').last;
      
      await tester.tap(find.text('Tamanho da Fonte'));
      await tester.pumpAndSettle(); // Aguarda a animação do Diálogo abrir

      // Verificação intermediária: O diálogo abriu?
      expect(find.byType(AlertDialog), findsOneWidget);
      expect(find.byType(Slider), findsOneWidget);

      // Passo B: Interagir com o Slider
      // O slider vai de 0.8 a 1.4. O inicial é 1.0.
      // Vamos arrastar o slider para a direita para aumentar a fonte.
      // Offset(x, y) -> Movemos 200 pixels para a direita.
      await tester.drag(find.byType(Slider), const Offset(200, 0));
      await tester.pump(); // Reconstrói para atualizar o valor visual do slider

      // Passo C: Clicar em "APLICAR"
      await tester.tap(find.text('APLICAR'));
      await tester.pumpAndSettle(); // Aguarda o diálogo fechar

      // 3. ASSERT (Verificação)
      
      // Verifica se o diálogo fechou
      expect(find.byType(AlertDialog), findsNothing);
      
      // Verifica se a função callback foi chamada
      expect(capturedScale, isNotNull);
      
      // Verifica se o valor capturado é MAIOR que o inicial (1.0), já que arrastamos para a direita
      expect(capturedScale, greaterThan(1.0));
    });

    testWidgets('Botão CANCELAR não deve alterar o valor', (WidgetTester tester) async {
      // 1. ARRANGE
      bool callbackChamado = false;

      await tester.pumpWidget(MaterialApp(
        home: ConfiguracoesPage(
          currentThemeMode: ThemeMode.system,
          currentLanguage: 'portugues',
          currentUsername: 'UsuarioTeste',
          currentFontSizeScale: 1.0,
          onFontSizeScaleChanged: (val) {
            callbackChamado = true; // Isso NÃO deve acontecer
          },
        ),
      ));

      // 2. ACT
      await tester.tap(find.text('Tamanho da Fonte'));
      await tester.pumpAndSettle();

      // Movemos o slider só para garantir que houve interação
      await tester.drag(find.byType(Slider), const Offset(200, 0));
      await tester.pump();

      // Clicamos em CANCELAR em vez de APLICAR
      await tester.tap(find.text('CANCELAR'));
      await tester.pumpAndSettle();

      // 3. ASSERT
      expect(find.byType(AlertDialog), findsNothing); // Diálogo fechou
      expect(callbackChamado, isFalse); // O valor não foi salvo
    });
  });
  group('Teste de Interface: Tema', () {
    testWidgets('Deve abrir diálogo e alterar o tema', (WidgetTester tester) async {
      // 1. ARRANGE
      ThemeMode? capturedMode; // Variável para capturar a escolha

      await tester.pumpWidget(MaterialApp(
        home: ConfiguracoesPage(
          // Começamos com o tema do Sistema
          currentThemeMode: ThemeMode.system, 
          currentLanguage: 'portugues',
          currentUsername: 'UsuarioTeste',
          currentFontSizeScale: 1.0,
          // Capturamos a mudança aqui
          onThemeModeChanged: (newMode) {
            capturedMode = newMode;
          },
        ),
      ));

      // 2. ACT (Mudar para Escuro)
      // Toca no tile "Tema"
      await tester.tap(find.text('Tema'));
      await tester.pumpAndSettle(); // Aguarda o diálogo abrir

     final botaoSistema = find.descendant(
        of: find.byType(AlertDialog), 
        matching: find.text('Sistema'),
      );
      
      final botaoEscuro = find.descendant(
        of: find.byType(AlertDialog), 
        matching: find.text('Escuro'),
      );
      
      final botaoClaro = find.descendant(
        of: find.byType(AlertDialog), 
        matching: find.text('Claro'),
      );

      // Verifica se as opções apareceram
      expect(botaoSistema, findsOneWidget);
      expect(botaoEscuro, findsOneWidget);
      expect(botaoClaro, findsOneWidget);

      // Toca na opção "Escuro"
      await tester.tap(find.text('Escuro'));
      await tester.pumpAndSettle(); // Aguarda o diálogo fechar

      // 3. ASSERT (Verifica Escuro)
      expect(capturedMode, ThemeMode.dark); // Callback foi chamado com Dark?
      expect(find.byType(AlertDialog), findsNothing); // Diálogo fechou?

      // 4. ACT (Mudar para Claro)
      // Reabrimos o diálogo para testar outra opção
      await tester.tap(find.text('Tema'));
      await tester.pumpAndSettle();

      // Toca na opção "Claro"
      await tester.tap(find.text('Claro'));
      await tester.pumpAndSettle();

      // 5. ASSERT (Verifica Claro)
      expect(capturedMode, ThemeMode.light);
    });
  });
  });
  group('Teste de Funcionalidade: Restaurar Configurações', () {
  testWidgets('Deve abrir o diálogo de confirmação e chamar onResetSettings ao confirmar', (WidgetTester tester) async {
    // 1. ARRANGE (Preparação)
    bool resetCalled = false;
    
    // Renderiza o widget em um MaterialApp
    await tester.pumpWidget(MaterialApp(
      home: ConfiguracoesPage(
        currentThemeMode: ThemeMode.dark, // Estado inicial não-padrão
        currentLanguage: 'ingles',         // Estado inicial não-padrão
        currentUsername: 'Teste User',
        currentFontSizeScale: 1.2,
        onResetSettings: () {
          resetCalled = true; // Define a flag para verificar se foi chamado
        },
      ),
    ));
    
    // 2. ACT (Ação)

    // Passo A: Encontrar o ListTile e clicar
    await tester.tap(find.text('Reset Settings'));
    await tester.pumpAndSettle(); // Aguarda o diálogo abrir

    // Verificação intermediária: O diálogo abriu?
    expect(find.text('Confirm Reset'), findsOneWidget);

    // Passo B: Encontrar e clicar no botão RESTAURAR
    await tester.tap(find.text('RESET'));
    // pumpAndSettle para fechar o diálogo e exibir a SnackBar
    await tester.pumpAndSettle(); 

    // 3. ASSERT (Verificação)

    // Verifica se o diálogo fechou
    expect(find.byType(AlertDialog), findsNothing);

    // Verifica se o callback foi chamado
    expect(resetCalled, isTrue);

    // Verifica se a SnackBar de sucesso apareceu (em português)
    expect(find.text('Theme, Language, and Font restored to default.'), findsOneWidget);
    
    // Opcional: Garante que a SnackBar desapareça (se o teste continuar)
    await tester.pumpAndSettle(const Duration(seconds: 4)); 
    expect(find.text('Theme, Language, and Font restored to default.'), findsNothing);
  });

  testWidgets('O botão CANCELAR deve fechar o diálogo e NÃO chamar onResetSettings', (WidgetTester tester) async {
    // 1. ARRANGE
    bool resetCalled = false;
    
    await tester.pumpWidget(MaterialApp(
      home: ConfiguracoesPage(
        currentThemeMode: ThemeMode.dark,
        currentLanguage: 'ingles',
        currentUsername: 'Teste User',
        currentFontSizeScale: 1.2,
        onResetSettings: () {
          resetCalled = true; // Se for chamado, o teste falha.
        },
      ),
    ));
    
    // 2. ACT
    // Passo A: Abrir o diálogo
    await tester.tap(find.text('Reset Settings'));
    await tester.pumpAndSettle();

    // Verificação intermediária: O diálogo abriu?
    expect(find.text('Confirm Reset'), findsOneWidget);

    // Passo B: Clicar no botão CANCELAR
    await tester.tap(find.text('CANCEL'));
    await tester.pumpAndSettle(); // Aguarda o diálogo fechar

    // 3. ASSERT
    
    // Verifica se o diálogo fechou
    expect(find.byType(AlertDialog), findsNothing);

    // Verifica se o callback NÃO foi chamado
    expect(resetCalled, isFalse);

    // Verifica se nenhuma SnackBar foi exibida (não há texto de SnackBar)
    expect(find.text('Theme, Language, and Font restored to default.'), findsNothing);
  });
});
  group('Teste de Interface: Nome de Usuário', () {
    testWidgets('Deve abrir o diálogo, alterar o nome de usuário e atualizar o estado', (WidgetTester tester) async {
      // 1. ARRANGE (Preparação)
      const initialUsername = 'Visitante';
      const newUsername = 'Lumina User';
      String? capturedUsername;

      await tester.pumpWidget(MaterialApp(
        home: ConfiguracoesPage(
          currentThemeMode: ThemeMode.system,
          currentLanguage: 'portugues',
          currentUsername: initialUsername,
          currentFontSizeScale: 1.0,
          onUsernameChanged: (name) {
            capturedUsername = name;
          },
        ),
      ));

      // 2. ACT (Ação)

      // Passo A: Encontrar o ListTile do Usuário e clicar no botão EDITAR
      // O botão EDITAR é um TextButton dentro do _configTile do Usuário
      await tester.tap(find.text('EDITAR'));
      await tester.pumpAndSettle(); // Aguarda a animação do Diálogo abrir

      // Verificação intermediária: O diálogo abriu?
      expect(find.byType(AlertDialog), findsOneWidget);
      expect(find.text('Alterar Usuário'), findsOneWidget);

      // Passo B: Encontrar o TextField e digitar o novo nome
      // O AlertDialog contém um TextField.
      await tester.enterText(find.byType(TextField), newUsername);
      await tester.pump(); // Reconstrói para atualizar o TextField

      // Passo C: Clicar em SALVAR
      await tester.tap(find.text('SALVAR'));
      // Precisamos do pumpAndSettle para que a chamada do setState dentro do AlertDialog
      // e o fechamento do diálogo ocorram
      await tester.pumpAndSettle();

      // 3. ASSERT (Verificação)

      // Verifica se o diálogo fechou
      expect(find.byType(AlertDialog), findsNothing);

      // Verifica se a função callback foi chamada com o novo nome
      expect(capturedUsername, newUsername);

      // Verifica se o subtítulo no ConfiguracoesPage (que mostra o nome atual) foi atualizado
      // O nome de usuário é o subtítulo do primeiro tile
      expect(find.text(newUsername), findsOneWidget);
      expect(find.text(initialUsername), findsNothing);
    });

    testWidgets('Botão CANCELAR não deve alterar o nome de usuário', (WidgetTester tester) async {
      // 1. ARRANGE
      const initialUsername = 'Visitante';
      const newUsername = 'Novo Nome Ignorado';
      bool callbackChamado = false;

      await tester.pumpWidget(MaterialApp(
        home: ConfiguracoesPage(
          currentThemeMode: ThemeMode.system,
          currentLanguage: 'portugues',
          currentUsername: initialUsername,
          currentFontSizeScale: 1.0,
          onUsernameChanged: (val) {
            callbackChamado = true; // Isso NÃO deve acontecer
          },
        ),
      ));

      // 2. ACT
      await tester.tap(find.text('EDITAR'));
      await tester.pumpAndSettle();

      // Digita o novo nome
      await tester.enterText(find.byType(TextField), newUsername);
      await tester.pump();

      // Clicamos em CANCELAR em vez de SALVAR
      await tester.tap(find.text('CANCELAR'));
      await tester.pumpAndSettle();

      // 3. ASSERT
      expect(find.byType(AlertDialog), findsNothing); // Diálogo fechou
      expect(callbackChamado, isFalse); // O valor não foi salvo
      expect(find.text(initialUsername), findsOneWidget); // O nome antigo continua sendo exibido
      expect(find.text(newUsername), findsNothing); // O novo nome não é exibido
    });
  });
}