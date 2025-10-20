import 'package:flutter/material.dart';

class ConfiguracoesPage extends StatelessWidget {
  const ConfiguracoesPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        backgroundColor: Colors.grey[100],
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.purple),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: const Text(
          'Configurações',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: ListView(
          children: [
          
            Container(
              padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
              margin: const EdgeInsets.only(bottom: 30),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: const [
                  Text(
                    'Usuário',
                    style: TextStyle(fontSize: 18),
                  ),
                  Row(
                    children: [
                      Text(
                        'Editar',
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 16,
                        ),
                      ),
                      SizedBox(width: 5),
                      Icon(Icons.arrow_forward_ios,
                          color: Colors .purple, size: 18),
                    ],
                  ),
                ],
              ),
            ),


            const Text(
              'Configurações do aplicativo',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),

            _configTile(
              icon: Icons.language,
              color: Colors.purple,
              title: 'Idioma',
            ),
            _configTile(
              icon: Icons.nightlight_round,
              color: Colors.yellow,
              title: 'Aparência',
            ),
            _configTile(
              icon: Icons.text_fields,
              color: Colors.purple,
              title: 'Tamanho da fonte',
            ),

            const SizedBox(height: 30),

     
            const Text(
              'Sobre',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),

            _configTile(
              icon: Icons.info,
              color: Colors.black,
              title: 'Saiba mais',
            ),
            _configTile(
              icon: Icons.menu_book,
              color: Colors.black,
              title: 'Tutorial',
            ),
            _configTile(
              icon: Icons.description_outlined,
              color: Colors.blue,
              title: 'Termos de Serviço',
            ),
          ],
        ),
      ),
    );
  }

  Widget _configTile({
    required IconData icon,
    required Color color,
    required String title,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 26),
              const SizedBox(width: 12),
              Text(
                title,
                style: const TextStyle(fontSize: 16),
              ),
            ],
          ),
          const Icon(Icons.arrow_forward_ios,
              color: Colors.purple, size: 18),
        ],
      ),
    );
  }
}