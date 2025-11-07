import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:frontend/main.dart';
class ChatMessage {
  final String text;
  final bool isUser; 
  final DateTime timestamp;

  ChatMessage({
    required this.text,
    required this.isUser,
    required this.timestamp,
  });
}

class ChatScreen extends StatefulWidget {
  final String? username;
  final String currentLanguage;

  const ChatScreen({super.key, this.username,required this.currentLanguage});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}


class _ChatScreenState extends State<ChatScreen> {
  
  String? _currentDisplayedUsername;
  
  final List<ChatMessage> _messages = <ChatMessage>[];
  
  final TextEditingController _textController = TextEditingController();
  
  
  bool _isSending = false;

  @override
  void initState() {
    super.initState();
     _currentDisplayedUsername = widget.username ?? "Visitante";
    
    _messages.add(
      ChatMessage(
        text: "Olá $_currentDisplayedUsername! Sou Lumina, sua agente de IA para o combate à desinformação, como posso te ajudar hoje?",
        isUser: false,
        timestamp: DateTime.now(),
      ),
    );
  }
@override
  void didUpdateWidget(covariant ChatScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    
    // 1. Verifica se a propriedade 'username' do widget mudou
    if (widget.username != oldWidget.username) {
      // 2. Chama setState para atualizar qualquer parte da UI que use o nome.
      setState(() {
        _currentDisplayedUsername = widget.username ?? "Visitante";
        
        // **OPCIONAL:** Se você precisar atualizar a mensagem de saudação inicial, 
        // a forma mais simples (se ela for sempre a primeira) é substituí-la:
        // Se a lista de mensagens não estiver vazia, atualiza a primeira mensagem
        if (_messages.isNotEmpty && !_messages.first.isUser) {
             _messages[0] = ChatMessage(
                text: "Olá $_currentDisplayedUsername! Sou Lumina, sua agente de IA para o combate à desinformação, como posso te ajudar hoje?",
                isUser: false,
                timestamp: DateTime.now(),
            );
        }
        
      });
    }
  }
  
  void _handleSubmitted(String text) {
    if (text.trim().isEmpty || _isSending) return;

    
    ChatMessage userMessage = ChatMessage(
      text: text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
    );

    setState(() {
      _messages.insert(0, userMessage);
      _textController.clear();
      _isSending = true; 
    });

    
    _fetchGeminiResponse(userMessage.text);
  }

 
  Future<void> _fetchGeminiResponse(String prompt) async {
   
    final encodedPrompt = Uri.encodeComponent(prompt);
    
    final url = Uri.parse('$apiBaseUrl/prompt/$encodedPrompt'); 

    try {
      final response = await http.get(url);

      if (response.statusCode == 200) {
        
        final jsonResponse = json.decode(utf8.decode(response.bodyBytes));
        final String botResponseText = jsonResponse['response'] ?? "Erro: Resposta vazia.";

        
        ChatMessage botMessage = ChatMessage(
          text: botResponseText,
          isUser: false,
          timestamp: DateTime.now(),
        );

        setState(() {
          _messages.insert(0, botMessage);
        });

      } else {
        
        _addErrorMessage('Erro na API: Status Code ${response.statusCode}');
      }
    } catch (e) {
      
      _addErrorMessage('Erro de conexão: Verifique se o FastAPI está rodando em $apiBaseUrl.');
    } finally {
      
      setState(() {
        _isSending = false;
      });
    }
  }

  
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


  
  Widget _buildMessage(ChatMessage message) {
    final theme = Theme.of(context);
  final isUser = message.isUser;
    final alignment =
        message.isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start;
    final Color bubbleColor = isUser
      // Mensagem Enviada (Usuário): Use a cor primária ou container do tema
      ? theme.colorScheme.primary 
      // Mensagem Recebida (Lumina): Use uma cor de superfície sutil para contraste
      : theme.colorScheme.surfaceContainerHigh;
      final Color textColor = isUser
      // Texto da Mensagem Enviada: Use a cor 'onPrimary' (texto sobre a cor primária)
      ? theme.colorScheme.onPrimary 
      // Texto da Mensagem Recebida: Use a cor 'onSurfaceVariant' (texto sobre a surfaceVariant)
      : theme.colorScheme.onSurfaceVariant;
    
    
    final mainAlignment =
        message.isUser ? Alignment.centerRight : Alignment.centerLeft;

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 10.0),
      child: Column(
        crossAxisAlignment: alignment,
        children: <Widget>[
          
          Align(
            alignment: mainAlignment,
            child: Container(
              constraints: BoxConstraints(
                maxWidth: MediaQuery.of(context).size.width * 0.75, 
              ),
              decoration: BoxDecoration(
                color: bubbleColor, // <-- SUBSTITUA A COR FIXA (ex: Colors.green ou Colors.white)
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
                style: TextStyle(fontSize: 16.0,color: textColor,),
                
              ),
            ),
          ),
          
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

  
  Widget _buildMessageComposer() {
    final theme = Theme.of(context);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
      decoration: BoxDecoration(
        color: theme.colorScheme.surface,
        border: Border(top: BorderSide(color: Colors.grey.shade300)),
      ),
      child: Row(
        children: <Widget>[
          
          Flexible(
            child: TextField(
              controller: _textController,
              onSubmitted: _handleSubmitted,
              enabled: !_isSending, 
              decoration: InputDecoration.collapsed(
                hintText: _isSending
                    ? "Aguardando resposta..."
                    : "Enviar uma mensagem...",
              ),
            ),
          ),
         
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

 String _t(String pt, String en) {
    // Retorna 0 para Português, 1 para Inglês
    return widget.currentLanguage == 'portugues' ? pt : en;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('LUMINA'),
        // É bom garantir que o AppBar use a cor primária do tema.
        backgroundColor: theme.colorScheme.primary, 
        foregroundColor: theme.colorScheme.onPrimary,
        iconTheme: IconThemeData(color: theme.colorScheme.onPrimary),
      ),
      body: SafeArea(
        child: Column(
          children: <Widget>[
            // Lista de Mensagens
            Flexible(
              child: ListView.builder(
                padding: const EdgeInsets.all(8.0),
                reverse: true,
                itemBuilder: (_, int index) => _buildMessage(_messages[index]),
                itemCount: _messages.length,
              ),
            ),
            
            const Divider(height: 1.0),
           
            _buildMessageComposer(),
          ],
        ),
      ),
      drawer: Drawer(
        child: Column(
          children: <Widget>[
           
            const DrawerHeader(
              decoration: BoxDecoration(
                color: Color.fromARGB(255, 93, 7, 173),
              ),
              child: SizedBox(
                width: double.infinity,
                child: Text(
                  'LUMINA',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            
            
            const Expanded(child: SizedBox()),

            
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Align(
                alignment: Alignment.bottomLeft,
                child: ListTile(
                  leading: const Icon(Icons.more_horiz), 
                  title: Text(_t('Configurações', 'Settings'), style: const TextStyle(fontSize: 16)),
                  onTap: () {
                    
                    Navigator.pop(context); 
                   
                    Navigator.pushNamed(context, '/settings');
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
