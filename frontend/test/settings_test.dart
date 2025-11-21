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
}