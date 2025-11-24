import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:frontend/main.dart';
import 'package:shared_preferences/shared_preferences.dart';

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
  
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  
  bool _isSending = false;

  bool _showChatTutorial = false;
  bool _showMenuTutorial = false;


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
    _checkTutorialStatus();
  }


Future<void> _checkTutorialStatus() async {
  final prefs = await SharedPreferences.getInstance();
  final seenChatTutorial = prefs.getBool('hasSeenChatTutorial') ?? false;
  final seenMenuTutorial = prefs.getBool('hasSeenMenuTutorial') ?? false;

  if (!seenChatTutorial) {
    setState(() => _showChatTutorial = true);
  }

  if (seenChatTutorial && !seenMenuTutorial) {
    setState(() => _showMenuTutorial = true);
  }
}


Future<void> _closeChatTutorial() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool('hasSeenChatTutorial', true);
  setState(() {
    _showChatTutorial = false;
  });
}

Future<void> _closeMenuTutorial() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool('hasSeenMenuTutorial', true);
  setState(() {
    _showMenuTutorial = false;
  });
}




@override
  void didUpdateWidget(covariant ChatScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    
    if (widget.username != oldWidget.username) {
      setState(() {
        _currentDisplayedUsername = widget.username ?? "Visitante";
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
      ? theme.colorScheme.primary 
      : theme.colorScheme.surfaceContainerHigh;
      final Color textColor = isUser
      ? theme.colorScheme.onPrimary 
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
                color: bubbleColor, 
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
    return widget.currentLanguage == 'portugues' ? pt : en;
  }



Widget _buildBalloonWithArrow(String text, {ArrowDirection direction = ArrowDirection.down}) {
  final theme = Theme.of(context);
  final bool isDarkMode = theme.brightness == Brightness.dark;

  final Color balloonColor = isDarkMode
      ? theme.colorScheme.surfaceContainerHighest 
      : theme.colorScheme.surface;               

  final Color textColor = isDarkMode
      ? theme.colorScheme.onSurface
      : Colors.black87;

  return CustomPaint(
    painter: BalloonArrowPainter(direction, color: balloonColor),
    child: Container(
      margin: const EdgeInsets.all(8),
      padding: const EdgeInsets.all(14),
      constraints: const BoxConstraints(maxWidth: 280),
      decoration: BoxDecoration(
        color: balloonColor,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.2),
            blurRadius: 6,
            offset: const Offset(2, 2),
          )
        ],
      ),
      child: Text(
        text,
        style: TextStyle(color: textColor, fontSize: 15),
      ),
    ),
  );
}





  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      key: _scaffoldKey,
  onDrawerChanged: (isOpened) async {
    if (isOpened) {
      final prefs = await SharedPreferences.getInstance();
      final seenChat = prefs.getBool('hasSeenChatTutorial') ?? false;
      final seenMenu = prefs.getBool('hasSeenMenuTutorial') ?? false;

      if (seenChat && !seenMenu) {
        setState(() => _showMenuTutorial = true);
      }
    }
  },
      appBar: AppBar(
        title: const Text('LUMINA'),
        backgroundColor: theme.colorScheme.primary, 
        foregroundColor: theme.colorScheme.onPrimary,
        iconTheme: IconThemeData(color: theme.colorScheme.onPrimary),
      ),
      body: Stack(
        children: [
          SafeArea(
        child: Column(
          children: <Widget>[
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

       
      if (_showChatTutorial)
      GestureDetector(
        onTap: _closeChatTutorial,
        child: Container(
          color: Colors.black.withValues(alpha: 0.6),
          child: Stack(
            children: [
              Positioned(
                top: 20,
                left: 10,
                child: _buildBalloonWithArrow(
                  _t("Clique aqui para abrir o menu","Tap here to open the menu"),
                   direction: ArrowDirection.up,
                  ),
              ),
              Positioned(
                bottom: 75,
                left: 20,
                child: _buildBalloonWithArrow(
                    _t("Digite aqui a notícia que você quer verificar","Type the news you want to check here"),
                     direction: ArrowDirection.down,
                    ),
              ),
            ],
          ),
        ),
      ),

      ],
    ),

      drawer: Stack(
        children:[ 
          Drawer(
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


      if (_showMenuTutorial)
      GestureDetector(
        onTap: _closeMenuTutorial,
        child: Container(
          color: Colors.black.withValues(alpha: 0.6),
          child: Stack(
            children: [
              Positioned(
                bottom: 65,
                left: 15,
                child: _buildBalloonWithArrow(
                  _t("Clique aqui para abrir as configurações","Tap here to open settings"),
                   direction: ArrowDirection.down,
                  ),
              ),
              Positioned(
                top: 200,
                left: 100,
                child: _buildBalloonWithArrow(
                    _t("Aqui ficam salvas as suas conversas anteriores","Your previous conversations are saved here"),
                     direction: ArrowDirection.left,
                    ),
              ),
            ],
          ),
        ),
      ),
  ],
),

    );
  }
}

enum ArrowDirection { up, down, left, right }

class BalloonArrowPainter extends CustomPainter {
  final ArrowDirection direction;
  final Color color;

  BalloonArrowPainter(this.direction, {this.color = Colors.white});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = color;
    final path = Path();

    const arrowSize = 15.0;
    const arrowWidth = 16.0;

    switch (direction) {
      case ArrowDirection.up:
         path.moveTo(20, -arrowSize); 
         path.lineTo(20 - arrowWidth / 2, 0); 
         path.lineTo(20 + arrowWidth / 2, 0); 
         path.close();
        break;

      case ArrowDirection.down:
        path.moveTo(20, size.height + arrowSize);
        path.lineTo(20 - arrowWidth / 2, size.height);
        path.lineTo(20 + arrowWidth / 2, size.height);
        path.close();
        break;

      case ArrowDirection.left:
        path.moveTo(0, 20);
        path.lineTo(-arrowSize, 20 - arrowWidth / 2);
        path.lineTo(-arrowSize, 20 + arrowWidth / 2);
        path.close();
        break;

      case ArrowDirection.right:
        path.moveTo(size.width + arrowSize, 20);
        path.lineTo(size.width, 20 - arrowWidth / 2);
        path.lineTo(size.width, 20 + arrowWidth / 2);
        path.close();
        break;
    }

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => false;
}
