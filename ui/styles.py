GLOBAL_STYLE = """
    /* ── Base Window ─────────────────────────────────────────────── */
    QMainWindow {
        background-color: #09090b;
        color: #fafafa;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }

    QWidget {
        background-color: transparent;
        color: #fafafa;
    }

    /* ── Layout Containers ────────────────────────────────────────── */
    #SidebarPanel {
        background-color: #09090b;
        border-right: 1px solid #27272a;
    }

    #RightPanel {
        background-color: #09090b;
        border-left: 1px solid #27272a;
    }

    /* ── Top Bar ──────────────────────────────────────────────────── */
    #TopBar {
        background-color: #09090b;
        border-bottom: 1px solid #27272a;
        min-height: 48px;
    }

    #LogoLabel {
        color: #3b82f6;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 0.05em;
        padding-left: 16px;
        text-transform: uppercase;
    }

    /* ── AI Prompt Bar ────────────────────────────────────────────── */
    QLineEdit#AIPrompt {
        background-color: #18181b;
        color: #fafafa;
        border: 1px solid #27272a;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 12px;
        font-family: 'JetBrains Mono', 'Consolas', monospace;
    }

    QLineEdit#AIPrompt:focus {
        border: 1px solid #3b82f6;
        background-color: #09090b;
    }

    /* ── Tabs (Industrial Design) ─────────────────────────────────── */
    QTabWidget::pane {
        border: none;
    }

    QTabBar {
        background: transparent;
    }

    QTabBar::tab {
        background: transparent;
        color: #a1a1aa;
        padding: 8px 12px;
        font-size: 11px;
        font-weight: 500;
        border: none;
        border-bottom: 2px solid transparent;
    }

    QTabBar::tab:selected {
        color: #3b82f6;
        border-bottom: 2px solid #3b82f6;
    }

    /* ── Buttons (Sharp & Solid) ──────────────────────────────────── */
    QPushButton {
        background-color: #18181b;
        color: #e4e4e7;
        border: 1px solid #27272a;
        border-radius: 4px;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 500;
    }

    QPushButton:hover {
        background-color: #27272a;
        border-color: #3f3f46;
    }

    QPushButton#PrimaryButton {
        background-color: #3b82f6;
        border: none;
        color: white;
        font-weight: 600;
    }

    QPushButton#PrimaryButton:hover {
        background-color: #2563eb;
    }

    QPushButton#IconButton {
        background-color: transparent;
        border: none;
        border-radius: 2px;
        padding: 4px;
        color: #71717a;
    }

    QPushButton#IconButton:hover {
        background-color: #18181b;
        color: #fafafa;
    }
    
    QPushButton#IconButton:checked {
        color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.1);
    }

    /* ── Form Elements ────────────────────────────────────────────── */
    QSpinBox, QDoubleSpinBox, QLineEdit {
        background-color: #18181b;
        color: #fafafa;
        border: 1px solid #27272a;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 11px;
    }

    QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #3b82f6;
    }

    /* ── Labels & Technical Data ──────────────────────────────────── */
    QLabel {
        font-size: 11px;
        color: #e4e4e7;
    }
    
    #Toast {
        background-color: #18181b;
        border: 1px solid #3b82f6;
        border-radius: 4px;
        font-weight: 600;
        color: #3b82f6;
    }

    /* ── Scroll Bars (Minimalist) ─────────────────────────────────── */
    QScrollBar:vertical {
        border: none;
        background: #09090b;
        width: 6px;
    }

    QScrollBar::handle:vertical {
        background: #27272a;
        min-height: 20px;
        border-radius: 3px;
    }
    
    /* ── Inspector Headers ───────────────────────────────────────── */
    QPushButton#SectionHeader {
        text-align: left;
        background-color: #111111;
        border: none;
        border-bottom: 1px solid #27272a;
        color: #71717a;
        font-weight: 700;
        font-size: 9px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding-left: 10px;
    }
"""
