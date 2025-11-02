import 'package:flutter/material.dart';

class ConfiguracoesPage extends StatelessWidget {
  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onThemeModeChanged;
  final int languageValue;
  final void Function(int)? onLanguageChanged;

  const ConfiguracoesPage({
    super.key,
    this.currentThemeMode = ThemeMode.light,
    this.onThemeModeChanged,
    this.languageValue = 0,
    this.onLanguageChanged,
  });

  String getLanguageLabel(int v) => v == 0 ? 'Português (Brasil)' : 'English';

  void _openLanguageDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return _buildLanguageDialog(context);
      },
    );
  }

  void _openThemeDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) {
        return _buildThemeDialog(context);
      },
    );
  }

  Widget _buildLanguageDialog(BuildContext context) {
    final theme = Theme.of(context);
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      backgroundColor: theme.colorScheme.surface,
      titlePadding: EdgeInsets.zero,
      title: Container(
        decoration: BoxDecoration(
          color: theme.colorScheme.primary.withAlpha(46),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
        ),
        padding: const EdgeInsets.symmetric(vertical: 12),
        child: Center(
          child: Text(
            'Select the language',
            style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
        ),
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          RadioListTile<int>(
            title: const Text('Português (Brasil)'),
            value: 0,
            groupValue: languageValue,
            activeColor: theme.colorScheme.primary,
            onChanged: (v) {
              if (v != null) {
                onLanguageChanged?.call(v);
                Navigator.pop(context);
              }
            },
          ),
          RadioListTile<int>(
            title: const Text('English'),
            value: 1,
            groupValue: languageValue,
            activeColor: theme.colorScheme.primary,
            onChanged: (v) {
              if (v != null) {
                onLanguageChanged?.call(v);
                Navigator.pop(context);
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildThemeDialog(BuildContext context) {
    final theme = Theme.of(context);
    final current = currentThemeMode;
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      backgroundColor: theme.colorScheme.surface,
      titlePadding: EdgeInsets.zero,
      title: Container(
        decoration: BoxDecoration(
          color: theme.colorScheme.primary.withAlpha(46),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
        ),
        padding: const EdgeInsets.symmetric(vertical: 12),
        child: Center(
          child: Text(
            'Escolha a aparência',
            style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
        ),
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          RadioListTile<ThemeMode>(
            title: const Text('Modo claro'),
            value: ThemeMode.light,
            groupValue: current,
            activeColor: theme.colorScheme.primary,
            onChanged: (m) {
              if (m != null) {
                onThemeModeChanged?.call(m);
                Navigator.pop(context);
              }
            },
          ),
          RadioListTile<ThemeMode>(
            title: const Text('Modo escuro'),
            value: ThemeMode.dark,
            groupValue: current,
            activeColor: theme.colorScheme.primary,
            onChanged: (m) {
              if (m != null) {
                onThemeModeChanged?.call(m);
                Navigator.pop(context);
              }
            },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    final tileColor = theme.colorScheme.surface;
    final scaffoldBg = theme.scaffoldBackgroundColor;

    return Scaffold(
      backgroundColor: scaffoldBg,
      appBar: AppBar(
        backgroundColor: scaffoldBg,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: theme.colorScheme.primary),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'Configurações',
          style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
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
                color: tileColor,
                borderRadius: BorderRadius.circular(12),
                boxShadow: [
                  BoxShadow(
                    color: isDark ? Colors.black.withAlpha(77) : Colors.grey.withAlpha(38),
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('Usuário', style: theme.textTheme.bodyLarge),
                  Row(
                    children: [
                      Text('Editar', style: theme.textTheme.bodyMedium),
                      const SizedBox(width: 6),
                      Icon(Icons.arrow_forward_ios, color: theme.colorScheme.primary, size: 16),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 2),
            Text(
              'Configurações do aplicativo',
              style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            _configTile(
              context: context,
              icon: Icons.language,
              color: theme.colorScheme.primary,
              title: 'Idioma (${getLanguageLabel(languageValue)})',
              tileColor: tileColor,
              onTap: () => _openLanguageDialog(context),
            ),
            _configTile(
              context: context,
              icon: Icons.nightlight_round,
              color: Colors.yellow.shade700,
              title: 'Aparência',
              tileColor: tileColor,
              onTap: () => _openThemeDialog(context),
            ),
            _configTile(
              context: context,
              icon: Icons.text_fields,
              color: theme.colorScheme.primary,
              title: 'Tamanho da fonte',
              tileColor: tileColor,
              onTap: null,
            ),
            const SizedBox(height: 30),
            Text(
              'Sobre',
              style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            _configTile(
              context: context,
              icon: Icons.info,
              color: theme.colorScheme.onSurface,
              title: 'Saiba mais',
              tileColor: tileColor,
            ),
            _configTile(
              context: context,
              icon: Icons.menu_book,
              color: theme.colorScheme.onSurface,
              title: 'Tutorial',
              tileColor: tileColor,
            ),
            _configTile(
              context: context,
              icon: Icons.description_outlined,
              color: Colors.blue,
              title: 'Termos de Serviço',
              tileColor: tileColor,
            ),
          ],
        ),
      ),
    );
  }

  Widget _configTile({
    required BuildContext context,
    required IconData icon,
    required Color color,
    required String title,
    required Color tileColor,
    VoidCallback? onTap,
  }) {
    final theme = Theme.of(context);

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: tileColor,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 26),
                const SizedBox(width: 12),
                Text(title, style: theme.textTheme.bodyLarge),
              ],
            ),
            Icon(Icons.arrow_forward_ios, color: theme.colorScheme.primary, size: 18),
          ],
        ),
      ),
    );
  }
}