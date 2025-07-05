from enum import Enum

class ButtonStyle(Enum):
    MAIN_WINDOW = "main_window"
    DIALOG = "dialog"
    NAVIGATION = "navigation"

class TextStyle(Enum):
    TITLE = 'title'
    SUBTITLE = 'subtitle'
    LABEL = 'label'
    FOOTER = 'footer'

class StyleConfig:
    BUTTON_STYLES = {
        ButtonStyle.MAIN_WINDOW: {
            'width': 150,
            'height': 30,
            'margins': (0, 10, 0, 20),
        },
        ButtonStyle.DIALOG: {
            'width': 150,
            'height': 30,
            'margins': (0, 10, 0, 20),
        },
        ButtonStyle.NAVIGATION: {
            'width': 30,
            'height': 20,
            'margins': (0, 10, 0, 20),
        },
    }

    TEXT_STYLES = {
        TextStyle.TITLE: {
            'font_size': 16,
            'font_weight': 'bold',
            'font_family': 'Consolas'
        },
        TextStyle.SUBTITLE: {
            'font_size': 14,
            'font_weight': 'normal',
            'font_family': 'Consolas'
        },
        TextStyle.LABEL: {
            'font_size': 8,
            'font_weight': 'normal',
            'font_family': 'Consolas'
        },
        TextStyle.FOOTER: {
            'font_size': 10,
            'font_weight': 'normal',
            'font_family': 'Arial'
        }
    }

def apply_button_style(button, style: ButtonStyle):
    config = StyleConfig.BUTTON_STYLES[style]
    
    button.setFixedSize(config['width'], config['height'])
    button.setContentsMargins(*config['margins'])

def apply_text_style(label, style: TextStyle):
    config = StyleConfig.TEXT_STYLES[style]
    
    font = label.font()
    font.setPointSize(config['font_size'])
    font.setBold(config['font_weight'] == 'bold')
    font.setFamily(config['font_family'])
    label.setFont(font)
