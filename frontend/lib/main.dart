import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart'; // Importa flutter_dotenv

// Define a variável de URL de base da API, que será lida do .env
late final String kApiBaseUrl;

// --- Configuração da Aplicação Flutter ---

// A função main precisa ser assíncrona para carregar o arquivo .env
Future<void> main() async {
  // Garante que o Flutter Binding esteja inicializado antes de carregar o .env
  WidgetsFlutterBinding.ensureInitialized(); 

  // Carrega o arquivo .env do caminho especificado (.env)
  try {
    await dotenv.load(fileName: ".env");
    // Define a URL da API lendo a variável do .env
    kApiBaseUrl = dotenv.env['API_BASE_URL']!;
    debugPrint("URL da API carregada: $kApiBaseUrl");
  } catch (e) {
    // Caso haja um erro no carregamento ou a chave esteja faltando, usamos um fallback
    debugPrint("ERRO: Não foi possível carregar o arquivo .env ou a chave API_BASE_URL está faltando. Usando fallback.");
    kApiBaseUrl = "http://10.0.2.2:8000"; // Fallback para desenvolvimento
  }
  
  runApp(const ChatApp());
}

class ChatApp extends StatelessWidget {
  const ChatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gemini Chatbot',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
        // Configuração de cores para um visual moderno (similar ao WhatsApp/Telegram)
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blueGrey,
          primary: const Color.fromARGB(255, 93, 7, 173), // Cor principal do topo (roxo)
          secondary: const Color(0xFF128C7E), // Cor de destaque (Verde mais claro)
        ),
        useMaterial3: true,
      ),
      home: const ChatScreen(),
    );
  }
}

// --- Modelo de Dados e Tela Principal ---

/// Classe para representar uma única mensagem no chat.
class ChatMessage {
  final String text;
  final bool isUser; // true se for o usuário, false se for o robô
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  // Lista de mensagens exibidas no chat.
  final List<ChatMessage> _messages = <ChatMessage>[];
  // Controlador para o campo de texto.
  final TextEditingController _textController = TextEditingController();
  // Estado para controlar o loading da resposta da API.
  bool _isSending = false;

  @override
  void initState() {
    super.initState();
    // Mensagem de boas-vindas inicial
    _messages.add(
      ChatMessage(
        text: "Olá! Sou o seu chatbot. Pergunte algo!",
        isUser: false,
        timestamp: DateTime.now(),
      ),
    );
  }

  /// Constrói e envia a mensagem do usuário.
  void _handleSubmitted(String text) {
    if (text.trim().isEmpty || _isSending) return;

    // 1. Adiciona a mensagem do usuário na lista
    ChatMessage userMessage = ChatMessage(
      text: text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
    );

    setState(() {
      _messages.insert(0, userMessage);
      _textController.clear();
      _isSending = true; // Ativa o loading
    });

    // 2. Chama a função de comunicação com a API
    _fetchGeminiResponse(userMessage.text);
  }

  /// Faz a requisição HTTP GET para o endpoint FastAPI.
  Future<void> _fetchGeminiResponse(String prompt) async {
    // Codifica o prompt para que caracteres especiais sejam tratados corretamente na URL
    final encodedPrompt = Uri.encodeComponent(prompt);
    // Usa a variável global kApiBaseUrl, lida do .env
    final url = Uri.parse('$kApiBaseUrl/prompt/$encodedPrompt'); 

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        // Sucesso: Decodifica o JSON e extrai a resposta.
        final jsonResponse = json.decode(utf8.decode(response.bodyBytes));
        final String botResponseText = jsonResponse['response'] ?? "Erro: Resposta vazia.";

        // 3. Adiciona a resposta do robô na lista
        ChatMessage botMessage = ChatMessage(
          text: botResponseText,
          isUser: false,
          timestamp: DateTime.now(),
        );

        setState(() {
          _messages.insert(0, botMessage);
        });

      } else {
        // Falha na requisição
        _addErrorMessage('Erro na API: Status Code ${response.statusCode}');
      }
    } catch (e) {
      // Erro de rede ou parse
      _addErrorMessage('Erro de conexão: Verifique se o FastAPI está rodando em $kApiBaseUrl.');
    } finally {
      // 4. Desativa o loading
      setState(() {
        _isSending = false;
      });
    }
  }

  /// Função auxiliar para adicionar mensagens de erro (visíveis ao usuário).
  void _addErrorMessage(String message) {
     ChatMessage errorMessage = ChatMessage(
          text: message,
          isUser: false,
          timestamp: DateTime.now(),
     );
     setState(() {
          _messages.insert(0, errorMessage);
     });
  }


  // --- Widgets da Interface ---

  /// Constrói o balão de mensagem individual.
  Widget _buildMessage(ChatMessage message) {
    // Alinhamento (direita para usuário, esquerda para robô)
    final alignment =
        message.isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start;
    // Cor do balão
    final color = message.isUser
        ? const Color(0xFFDCF8C6) // Verde claro (Usuário)
        : Colors.white; // Branco (Robô)
    // Alinhamento do container
    final mainAlignment =
        message.isUser ? Alignment.centerRight : Alignment.centerLeft;

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 10.0),
      child: Column(
        crossAxisAlignment: alignment,
        children: <Widget>[
          // Balão da mensagem
          Align(
            alignment: mainAlignment,
            child: Container(
              constraints: BoxConstraints(
                maxWidth: MediaQuery.of(context).size.width * 0.75, // Máximo de 75% da tela
              ),
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(12.0),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha:0.1),
                    blurRadius: 2,
                    offset: const Offset(0, 1),
                  ),
                ],
              ),
              padding: const EdgeInsets.all(12.0),
              child: Text(
                message.text,
                style: const TextStyle(fontSize: 16.0),
              ),
            ),
          ),
          // Timestamp (Opcional, para dar um toque mais real)
          Padding(
            padding: const EdgeInsets.only(top: 4.0, right: 8.0, left: 8.0),
            child: Text(
              '${message.timestamp.hour}:${message.timestamp.minute.toString().padLeft(2, '0')}',
              style: TextStyle(
                fontSize: 12.0,
                color: Colors.grey[600],
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Constrói a barra de entrada de texto e o botão de envio.
  Widget _buildMessageComposer() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(top: BorderSide(color: Colors.grey.shade300)),
      ),
      child: Row(
        children: <Widget>[
          // Campo de texto
          Flexible(
            child: TextField(
              controller: _textController,
              onSubmitted: _handleSubmitted,
              enabled: !_isSending, // Desabilita enquanto espera a resposta
              decoration: InputDecoration.collapsed(
                hintText: _isSending
                    ? "Aguardando resposta..."
                    : "Enviar uma mensagem...",
              ),
            ),
          ),
          // Botão de envio
          Container(
            margin: const EdgeInsets.symmetric(horizontal: 4.0),
            child: _isSending
                ? const Padding(
                    padding: EdgeInsets.all(8.0),
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      color: Color.fromARGB(255, 93, 7, 173),
                    ),
                  )
                : IconButton(
                    icon: const Icon(Icons.send),
                    color: const Color.fromARGB(255, 93, 7, 173),
                    onPressed: () => _handleSubmitted(_textController.text),
                  ),
          ),
        ],
      ),
    );
  }

  // --- Layout Completo da Tela ---

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Lumina', style: TextStyle(color: Colors.white)),
        backgroundColor: Theme.of(context).colorScheme.primary, // Cor escura do topo
        centerTitle: false,
      ),
      body: Container(
        // Cor de fundo para simular a interface de chat
        color: const Color(0xFFECE5DD), // Bege claro
        child: Column(
          children: <Widget>[
            // Lista de mensagens (exibidas de forma reversa)
            Flexible(
              child: ListView.builder(
                padding: const EdgeInsets.all(8.0),
                reverse: true, // As novas mensagens aparecem no topo
                itemBuilder: (_, int index) => _buildMessage(_messages[index]),
                itemCount: _messages.length,
              ),
            ),
            // Linha divisória
            const Divider(height: 1.0),
            // Barra de entrada de mensagem
            _buildMessageComposer(),
          ],
        ),
      ),
    );
  }
}