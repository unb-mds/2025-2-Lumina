import 'package:flutter/material.dart';

// Definição da tela de Configurações (Temporária)
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Configurações"),
        backgroundColor: Color.fromARGB(255, 93, 7, 173),
      ),
      body: const Center(
        child: Text(
          "Página de configurações",
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}