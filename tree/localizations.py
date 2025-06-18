TRANSLATIONS = {
    "en": {
        "menu.app": "App",
        "menu.edit": "Edit",
        "menu.open": "Open",
        "menu.save": "Save",
        "menu.save_as": "Save As",
        "menu.undo": "Undo",
        "menu.redo": "Redo",
        "menu.format": "Format",
        "menu.pain": "Pain"
    },
    "pt": {
        "menu.app": "Aplicativo",
        "menu.edit": "Editar",
        "menu.open": "Abrir",
        "menu.save": "Salvar",
        "menu.save_as": "Salvar Como",
        "menu.undo": "Desfazer",
        "menu.redo": "Refazer",
        "menu.format": "Formatar",
        "menu.pain": "Dor"
    },
}


def translate(key: str, lang: str = "en") -> str:
    return TRANSLATIONS.get(lang, {}).get(key, key)
