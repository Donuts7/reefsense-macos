
COLORS = {
    'primary': '#1568AB',
    'black': '#000000',
    'primary_dark': '#1976D2',
    'primary_darker': '#1565C0',
    'background': '#F5F7FA',
    'white': '#FFFFFF',
    'text': '#2C3E50',
    'text_secondary': '#718096',
    'text_light': '#A0AEC0',      # Added this
    'disabled': '#CBD5E0',
    'border': '#E2E8F0',
    'status_bg': '#EBF8FF',
    'select_mode_unselected': '#E2E8F0',
    'select_mode_selected': '#2196F3',
    'light_grey': '#A0AEC0',
    'table_header': '#EBF8FF',    # Added this
    'error': '#E53E3E',
    'success': '#38A169',
    'summary_text': '#2196F3',  # Same as primary for consistency
    'table_row_alternate': '#F8FAFC',  # Light background for alternate rows
    
}

DIMENSIONS = {
    'border_radius': '6px',
    'padding': '16px',
    'button_padding': '12px 24px',
    'margin': '12px',
    'spacing': '16px'
}

TYPOGRAPHY = {
    'default_size': '14px',
    'title_size': '28px',
    'small_size': '12px',
    'font_family': '"Segoe UI", system-ui, -apple-system, sans-serif'
}

MAIN_STYLESHEET = f"""
QMainWindow, QDialog {{
    background-color: {COLORS['background']};
}}

QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
    border: none;
    padding: {DIMENSIONS['button_padding']};
    border-radius: {DIMENSIONS['border_radius']};
    font-size: {TYPOGRAPHY['default_size']};
    font-weight: bold;
    font-family: {TYPOGRAPHY['font_family']};
    min-width: 100px;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_darker']};
}}

QPushButton:disabled {{
    background-color: {COLORS['disabled']};
    color: {COLORS['text_secondary']};
}}

QLabel {{
    color: {COLORS['text']};
    font-size: {TYPOGRAPHY['default_size']};
    font-family: {TYPOGRAPHY['font_family']};
}}

QGroupBox {{
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']};
    padding-top: 24px;
    padding: {DIMENSIONS['padding']};
    margin-top: {DIMENSIONS['margin']};
    font-family: {TYPOGRAPHY['font_family']};
}}

QGroupBox::title {{
    color: {COLORS['black']};
    subcontrol-origin: margin;
    left: 8px;
    top: 8px;
    padding: 0 8px;
    
}}

QSpinBox {{
    color: {COLORS['text']};
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']};
    padding: 2px 4px;
    min-width: 80px;
    min-height: 20px;
}}



QSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 16px;
    height: 10px;
    border-left: 1px solid {COLORS['border']};
    image: url('_internal/src/gui/styles/up_arrow.png');
    
}}

QSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 16px;
    height: 10px;
    border-left: 1px solid {COLORS['border']};
    border-top: 1px solid {COLORS['border']};
    image: url('_internal/src/gui/styles/down_arrow.png');
    
}}

QSpinBox, QDoubleSpinBox {{ 
    color: {COLORS['text']};
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']};
    padding: 2px 4px;
    min-width: 80px;
    min-height: 20px;
   
}}

QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 16px;
    height: 10px;
    border-left: 1px solid {COLORS['border']};
    image: url('_internal/src/gui/styles/up_arrow.png');
}}

QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 16px;
    height: 10px;
    border-left: 1px solid {COLORS['border']};
    border-top: 1px solid {COLORS['border']};
    image: url('_internal/src/gui/styles/down_arrow.png');
}}


QHeaderView::section {{
    background-color: {COLORS['white']};
    color: {COLORS['text']};
    padding: 8px;
    border: none;
    border-right: 1px solid {COLORS['border']};
    border-bottom: 1px solid {COLORS['border']};
    font-family: {TYPOGRAPHY['font_family']};
    font-weight: bold;
}}

QTableWidget {{
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']};
    gridline-color: {COLORS['border']};
}}

QTableWidget::item {{
    padding: 8px;
    color: {COLORS['text']};
    background-color: {COLORS['white']};
}}

QCheckBox {{
    color: {COLORS['text']};
    font-family: {TYPOGRAPHY['font_family']};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 14px;
    height: 14px;
    border-radius: 4px;
    border: 2px solid {COLORS['primary']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['primary_darker']};
    border: 2px solid {COLORS['primary_darker']};
}}

QRadioButton {{
    color: {COLORS['text']};
    font-family: {TYPOGRAPHY['font_family']};
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 11px;
    border: 2px solid {COLORS['primary']};
    background-color: {COLORS['white']};
}}


QRadioButton::indicator:checked {{
    background-color: {COLORS['primary_darker']};
    border: 2px solid {COLORS['primary_darker']};
}}

QTabWidget {{
    background-color: {COLORS['background']};
}}

QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: {DIMENSIONS['border_radius']};
    background-color: {COLORS['white']};
    top: -1px;
}}

QTabBar::tab {{
    background-color: {COLORS['light_grey']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    border-top-left-radius: {DIMENSIONS['border_radius']};
    border-top-right-radius: {DIMENSIONS['border_radius']};
    padding: 8px 20px;
    margin-right: 2px;
    font-family: {TYPOGRAPHY['font_family']};
    min-width: 120px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['white']};
    color: {COLORS['text']};
}}

QTabBar::tab:!selected:hover {{
    background-color: {COLORS['light_grey']};
    color: {COLORS['text_secondary']};
}}

QLabel#pred_summary, QLabel#gt_summary {{
    color: {COLORS['text']};
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    margin-bottom: 10px;
}}

QTableView {{
    background-color: {COLORS['white']};
    alternate-background-color: {COLORS['background']};
    border: 1px solid {COLORS['border']};
    gridline-color: {COLORS['border']};
}}

QTableView::item {{
    padding: 8px;
    color: {COLORS['text']};
}}

QTableView::item:selected {{
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
}}

ResultsTable::item:alternate {{
    background-color: {COLORS['white']};
}}
"""

TITLE_LABEL_STYLE = f"""
    font-size: {TYPOGRAPHY['title_size']};
    
    color: {COLORS['black']};
    font-family: {TYPOGRAPHY['font_family']};
    padding: 16px 0;
"""

STATUS_LABEL_STYLE = f"""
    color: {COLORS['text']};
    font-weight: bold;
    padding: 12px 16px;
    background-color: {COLORS['status_bg']};
    border-radius: {DIMENSIONS['border_radius']};
    font-family: {TYPOGRAPHY['font_family']};
"""

