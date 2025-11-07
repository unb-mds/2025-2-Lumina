import 'package:flutter/material.dart';


const Map<String, List<String>> _translations = {
  
  'config_title': ['Configurações', 'Settings'],
  'section_account': ['Conta', 'Account'],
  'section_general': ['Geral', 'General'],
  'section_help': ['Ajuda e Legal', 'Help and Legal'],
  
  'tile_user': ['Usuário', 'User'],
  'tile_theme': ['Tema', 'Theme'],
  'tile_language': ['Idioma', 'Language'],
  'tile_font_size': ['Tamanho da Fonte', 'Font Size'],
  'tile_tutorial': ['Tutorial', 'Tutorial'],
  'tile_terms': ['Termos de Serviço', 'Terms of Service'],
  'tile_reset_defaults': ['Restaurar Configurações', 'Reset Settings'], 
  
  
  'subtitle_light': ['Claro', 'Light'],
  'subtitle_dark': ['Escuro', 'Dark'],
  'subtitle_system': ['Sistema', 'System'],
  'subtitle_small': ['Pequena', 'Small'],
  'subtitle_normal': ['Normal', 'Normal'],
  'subtitle_large': ['Grande', 'Large'],
  'subtitle_extralarge': ['Extra Grande', 'Extra Large'],
  'button_edit': ['EDITAR', 'EDIT'],
  'button_reset': ['RESTAURAR', 'RESET'],
 
  'dialog_user_title': ['Alterar Usuário', 'Change User'],
  'dialog_user_hint': ['Novo nome de usuário', 'New username'],
  'dialog_font_title': ['Tamanho da Fonte', 'Font Size'],
  'dialog_theme_title': ['Selecione o Tema', 'Select Theme'],
  'dialog_language_title': ['Selecione o Idioma', 'Select Language'],
  'dialog_reset_title': ['Confirmar Restauração', 'Confirm Reset'],
  'dialog_reset_message': [
      'Tem certeza de que deseja restaurar Tema, Idioma e Tamanho da Fonte para os valores de fábrica? O nome de usuário será mantido.', 
      'Are you sure you want to reset Theme, Language, and Font Size to factory defaults? The username will be preserved.'
  ],
  
  'button_cancel': ['CANCELAR', 'CANCEL'],
  'button_save': ['SALVAR', 'SAVE'],
  'button_apply': ['APLICAR', 'APPLY'],
};


String _t(String key, String lang) {
  final langIndex = lang == 'portugues' ? 0 : 1; 
  final texts = _translations[key] ?? [key, key];
  return texts[langIndex.clamp(0, 1)]; 
}


class ConfiguracoesPage extends StatefulWidget {
  final ThemeMode currentThemeMode;
  final void Function(ThemeMode)? onThemeModeChanged;
  
  final String currentLanguage;
  final void Function(String)? onLanguageChanged; 
  
  final double currentFontSizeScale;
  final void Function(double)? onFontSizeScaleChanged;
  
  final String currentUsername;
  final void Function(String)? onUsernameChanged;

  final VoidCallback? onResetSettings;

  const ConfiguracoesPage({
    super.key,
    required this.currentThemeMode, 
    this.onThemeModeChanged,
    required this.currentLanguage, 
    this.onLanguageChanged,
    this.currentFontSizeScale = 1.0,
    this.onFontSizeScaleChanged,
    required this.currentUsername,
    this.onUsernameChanged,
    this.onResetSettings,
  });

  @override
  State<ConfiguracoesPage> createState() => _ConfiguracoesPageState();
}


class _ConfiguracoesPageState extends State<ConfiguracoesPage> {
  late String _localUsername; 
  
 @override
  void initState() {
    super.initState();
    
    _localUsername = widget.currentUsername; 
  }
  String _getFontSizeLabel(double scale) {
    final lang = widget.currentLanguage; 
    if (scale <= 0.8) return _t('subtitle_small', lang);
    if (scale <= 1.0) return _t('subtitle_normal', lang);
    if (scale <= 1.2) return _t('subtitle_large', lang);
    return _t('subtitle_extralarge', lang);
  }

  void _openResetConfirmationDialog(BuildContext context) {
    final lang = widget.currentLanguage;
    final theme = Theme.of(context);
    
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          backgroundColor: theme.colorScheme.surface,
          title: Text(_t('dialog_reset_title', lang), textAlign: TextAlign.center), 
          content: Text(
            _t('dialog_reset_message', lang),
            textAlign: TextAlign.center,
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(_t('button_cancel', lang)),
            ),
            TextButton(
              onPressed: () {
                
                widget.onResetSettings?.call();
                
                
                Navigator.pop(context);
                
                
                ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                          lang == 'portugues' 
                          ? 'Tema, Idioma e Fonte restaurados para o padrão.'
                          : 'Theme, Language, and Font restored to default.'
                      ),
                      backgroundColor: Colors.purple,
                      duration: const Duration(seconds: 3),
                    ),
                );
              },
              child: Text(_t('button_reset', lang), style: TextStyle(color: Colors.red)),
            ),
          ],
        );
      },
    );
}

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

  void _openFontSizeDialog(BuildContext context) {
    double tempScale = widget.currentFontSizeScale;
    final lang = widget.currentLanguage;
    showDialog(
      context: context,
      builder: (context) {
        final theme = Theme.of(context);
        return StatefulBuilder(
          builder: (context, setStateSB) {
            return AlertDialog(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              backgroundColor: theme.colorScheme.surface,
              title: Text(_t('dialog_font_title', lang), textAlign: TextAlign.center), 
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '${_t('subtitle_normal', lang)}: ${_getFontSizeLabel(tempScale)}',
                    textScaler: TextScaler.linear(tempScale),
                    style: theme.textTheme.bodyLarge,
                  ),
                  const SizedBox(height: 20),
                  Slider(
                    value: tempScale,
                    min: 0.8,
                    max: 1.4,
                    divisions: 6,
                    label: _getFontSizeLabel(tempScale),
                    onChanged: (double value) {
                      setStateSB(() {
                        tempScale = value;
                      });
                    },
                  ),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: Text(_t('button_cancel', lang)),
                ),
                TextButton(
                  onPressed: () {
                    widget.onFontSizeScaleChanged?.call(tempScale); 
                    Navigator.pop(context);
                  },
                  child: Text(_t('button_apply', lang)),
                ),
              ],
            );
          },
        );
      },
    );
  }

 
  void _openUsernameDialog(BuildContext context) {
    final TextEditingController usernameController = 
        TextEditingController(text: _localUsername);
    final lang = widget.currentLanguage;
        
    showDialog(
      context: context,
      builder: (context) {
        final theme = Theme.of(context);
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          backgroundColor: theme.colorScheme.surface,
          title: Text(_t('dialog_user_title', lang), textAlign: TextAlign.center),
          content: TextField(
            controller: usernameController,
            decoration: InputDecoration(
              hintText: _t('dialog_user_hint', lang),
            ),
            keyboardType: TextInputType.text,
            textCapitalization: TextCapitalization.words,
            onSubmitted: (value) {
              final newName = value.trim();
              if (newName.isNotEmpty) {
               
                widget.onUsernameChanged?.call(newName);
                Navigator.pop(context);
              }
            },
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(_t('button_cancel', lang)),
            ),
            TextButton(
              onPressed: () {
               final newName = usernameController.text.trim();
                if (newName.isNotEmpty) {
                  
                  widget.onUsernameChanged?.call(newName); 
                  setState(() {
                    _localUsername = newName;
                  }); 

                  Navigator.pop(context);
                }
              },
              child: Text(_t('button_save', lang)),
            ),
          ],
        );
      },
    );
  }


  Widget _buildLanguageDialog(BuildContext context) {
    final theme = Theme.of(context);
    final lang = widget.currentLanguage;

    const languageOptions = [
      {'label': 'Português (Brasil)', 'value': 'portugues'},
      {'label': 'English', 'value': 'ingles'},
    ];
    
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      backgroundColor: theme.colorScheme.surface,
      titlePadding: EdgeInsets.zero,
      title: Container(
        decoration: BoxDecoration(
          color: theme.colorScheme.primary.withValues(alpha: 0.1),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
        ),
        padding: const EdgeInsets.all(20),
        child: Text(
          _t('dialog_language_title', lang),
          style: theme.textTheme.titleLarge?.copyWith(color: theme.colorScheme.primary),
          textAlign: TextAlign.center,
        ),
      ),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: languageOptions.map((option) {
            final value = option['value'] as String;
            final label = option['label'] as String;

            return RadioListTile<String>(
              title: Text(label),
              value: value,
              groupValue: widget.currentLanguage, 
              onChanged: (String? newValue) {
                if (newValue != null) {
                  widget.onLanguageChanged?.call(newValue);
                  Navigator.of(context).pop();
                }
              },
              activeColor: theme.colorScheme.primary,
            );
          }).toList(),
        ),
      ),
    );
  }

  Widget _buildThemeDialog(BuildContext context) {
    final theme = Theme.of(context);
    final lang = widget.currentLanguage;
    
    final themeOptions = {
      ThemeMode.light: _t('subtitle_light', lang),
      ThemeMode.dark: _t('subtitle_dark', lang),
      ThemeMode.system: _t('subtitle_system', lang),
    };

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      backgroundColor: theme.colorScheme.surface,
      titlePadding: EdgeInsets.zero,
      title: Container(
        decoration: BoxDecoration(
          color: theme.colorScheme.primary.withValues(alpha: 0.1),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
        ),
        padding: const EdgeInsets.all(20),
        child: Text(
          _t('dialog_theme_title', lang),
          style: theme.textTheme.titleLarge?.copyWith(color: theme.colorScheme.primary),
          textAlign: TextAlign.center,
        ),
      ),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: themeOptions.entries.map((entry) {
            final mode = entry.key;
            final label = entry.value;

            return RadioListTile<ThemeMode>(
              title: Text(label),
              value: mode,
              groupValue: widget.currentThemeMode,
              onChanged: (ThemeMode? value) {
                if (value != null) {
                  widget.onThemeModeChanged?.call(value); 
                  Navigator.of(context).pop();
                }
              },
              activeColor: theme.colorScheme.primary,
            );
          }).toList(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final tileColor = theme.colorScheme.surface;
    final lang = widget.currentLanguage;

    String getThemeName(ThemeMode mode) {
      switch (mode) {
        case ThemeMode.light:
          return _t('subtitle_light', lang);
        case ThemeMode.dark:
          return _t('subtitle_dark', lang);
        case ThemeMode.system:

          return _t('subtitle_system', lang);
      }
    }
    
    String getLanguageName(String langKey) {
      return langKey == 'portugues' ? 'Português (Brasil)' : 'English';
    }


    return Scaffold(
      appBar: AppBar(
        title: Text(_t('config_title', lang)),
        backgroundColor: theme.colorScheme.primary,
        foregroundColor: theme.colorScheme.onPrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSectionHeader(context, _t('section_account', lang)),
            _configTile(
              context: context,
              icon: Icons.person_outline,
              color: Colors.blueAccent,
              title: _t('tile_user', lang),
              subtitle: _localUsername, 
              tileColor: tileColor,
              actionButton: TextButton(
                onPressed: () => _openUsernameDialog(context),
                child: Text(_t('button_edit', lang)),
              ),
            ),

            _buildSectionHeader(context, _t('section_general', lang)),
            _configTile(
              context: context,
              icon: Icons.palette_outlined,
              color: Colors.pink,
              title: _t('tile_theme', lang),
              subtitle: getThemeName(widget.currentThemeMode), 
              tileColor: tileColor,
              onTap: () => _openThemeDialog(context),
            ),
            _configTile(
              context: context,
              icon: Icons.translate_outlined,
              color: Colors.green,
              title: _t('tile_language', lang),
              subtitle: getLanguageName(widget.currentLanguage),
              tileColor: tileColor,
              onTap: () => _openLanguageDialog(context),
            ),
            
            _configTile(
              context: context,
              icon: Icons.text_fields_outlined,
              color: Colors.orange,
              title: _t('tile_font_size', lang),
              subtitle: _getFontSizeLabel(widget.currentFontSizeScale),
              tileColor: tileColor,
              onTap: () => _openFontSizeDialog(context), 
            ),
            _configTile(
              context: context,
              icon: Icons.refresh_outlined,
              color: Colors.red,
              title: _t('tile_reset_defaults', lang),
              tileColor: tileColor,
              onTap: () => _openResetConfirmationDialog(context), 
            ),

            _buildSectionHeader(context, _t('section_help', lang)),
            _configTile(
              context: context,
              icon: Icons.book,
              color: theme.colorScheme.onSurface,
              title: _t('tile_tutorial', lang),
              tileColor: tileColor,
            ),
            _configTile(
              context: context,
              icon: Icons.description_outlined,
              color: Colors.blue,
              title: _t('tile_terms', lang),
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
    String? subtitle, 
    required Color tileColor,
    VoidCallback? onTap,
    Widget? actionButton, 
  }) {
    final theme = Theme.of(context);

    return GestureDetector(
      onTap: actionButton == null ? onTap : null, 
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
                Column( 
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: theme.textTheme.bodyLarge),
                    if (subtitle != null) 
                      Text(
                        subtitle,
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: theme.colorScheme.onSurface.withValues(alpha: 0.6 ),
                        ),
                      ),
                  ],
                ),
              ],
            ),
            actionButton ?? Icon(
              Icons.arrow_forward_ios, 
              color: theme.colorScheme.onSurface.withValues(alpha:0.6), 
              size: 18
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(top: 16.0, bottom: 8.0),
      child: Text(
        title,
        style: theme.textTheme.titleMedium?.copyWith(
          color: theme.colorScheme.primary,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}