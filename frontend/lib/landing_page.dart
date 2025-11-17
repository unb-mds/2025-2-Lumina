import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';


class LandingPage extends StatefulWidget {
  final String? initialUsername;
  final void Function(String)? onUsernameSet;
  const LandingPage({super.key,
    this.initialUsername,
    this.onUsernameSet,});

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage> {
  final TextEditingController _nomeController = TextEditingController();
 @override
  void initState() {
    super.initState();
    _nomeController.text = widget.initialUsername ?? ''; 
  }
  @override
  void dispose() {
    _nomeController.dispose();
    super.dispose();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color.fromARGB(255, 20, 0, 36),
              Color.fromARGB(255, 31, 0, 56),
              Color.fromARGB(255, 77, 0, 132),
            ],
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 50),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              
              Column(
                children: const [
                
                 // Inserir a logo .png

                  SizedBox(height: 10),
                  Text(
                    'LUMINA',
                    style: TextStyle(
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                      color: Colors.purpleAccent,
                      letterSpacing: 3,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 40),

            
              const Text(
                'Bem vindo ao Lumina',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 20),

            
              const Text(
                'Este aplicativo tem como objetivo combater a desinformação por meio do uso de Inteligência Artificial em um modelo de chat bot.\n\n'
                'A ferramenta compara o assunto da conversa com o banco de dados atualizado e reconhece se é uma fake news.',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.white70,
                  height: 1.5,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 40),

            
              const Text(
                'Para começar, digite seu nome:',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 12),

              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(30),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _nomeController,
                        style: const TextStyle(color: Colors.black),
                        decoration: const InputDecoration(
                          hintText: 'Nome de Usuário',
                          hintStyle: TextStyle(
                            fontStyle: FontStyle.italic,
                            color: Colors.grey,
                          ),
                          border: InputBorder.none,
                          contentPadding: EdgeInsets.symmetric(horizontal: 20),
                        ),
                      ),
                    ),
                    GestureDetector(
                      onTap: () async {
                        final nomeusuario = _nomeController.text.trim();
                        if (nomeusuario.isNotEmpty) {
                          widget.onUsernameSet?.call(nomeusuario);


                          final prefs = await SharedPreferences.getInstance();
                          await prefs.setBool('hasSeenLanding', true); 

                          
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Bem-vindo(a), $nomeusuario!'),
                              backgroundColor: Colors.purpleAccent,
                            ),
                          );
                          Navigator.pushReplacementNamed(
                            context, 
                            '/chat',
                            arguments: nomeusuario, 
                            
                          );
                    
                        }
                         else {
                           
                           ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Por favor, digite seu nome para continuar.'),
                              backgroundColor: Colors.redAccent,
                            ),
                          );
                        }
                      },
                      child: Container(
                        padding: const EdgeInsets.all(14),
                        decoration: const BoxDecoration(
                          color: Colors.purpleAccent,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.arrow_forward,
                          color: Color.fromRGBO(255, 255, 255, 1),
                        ),
                      ),
                    ),
                    const SizedBox(width: 5),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
