import 'package:flutter_test/flutter_test.dart';
// Importe o arquivo que contém a função que você quer testar
import 'package:frontend/Settings.dart'; 

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

    
  });
}