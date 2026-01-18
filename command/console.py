#!/usr/bin/env python3
"""
SPECTRA Console - Cyberpunk GUI
"""
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QFontDatabase, QPainter, QColor, QPen, QLinearGradient, QPixmap

load_dotenv()

APP_ROOT = Path(__file__).resolve().parents[1]
CORE_URL = "http://localhost:8000/v1/think"
SESSION_ID = "master-session"
API_KEY = os.getenv("SPECTRA_API_KEY", "")

# テーマ（avatar-ui classic に寄せた配色）
THEME_COLOR = "#00e676"
USER_COLOR = "#86ffe0"
PANEL_BG = "rgba(0, 20, 10, 0.35)"

# フォント候補（日本語優先）
FONT_FALLBACKS = [
    "Noto Sans JP",
    "Noto Sans CJK JP",
    "Yu Gothic UI",
    "Meiryo",
    "MS PGothic",
    "Segoe UI",
]
MONO_FALLBACKS = [
    "Cascadia Code",
    "JetBrains Mono",
    "Consolas",
]


# ===== スタイルシート =====
STYLESHEET = """
QMainWindow {{
    background-color: #000000;
}}

QWidget {{
    background-color: transparent;
    color: #dfffee;
    font-family: "Noto Sans JP", "Yu Gothic UI", "Meiryo", "Segoe UI", sans-serif;
}}

QFrame#mainFrame {{
    background-color: rgba(0, 0, 0, 0.45);
    border: 1px solid rgba(0, 230, 118, 0.6);
    border-radius: 8px;
}}

QFrame#chatFrame {{
    background-color: {panel_bg};
    border: 1px solid rgba(0, 230, 118, 0.4);
    border-radius: 6px;
}}

QFrame#avatarFrame {{
    background-color: {panel_bg};
    border: 1px solid rgba(0, 230, 118, 0.4);
    border-radius: 6px;
    min-width: 200px;
    max-width: 200px;
}}

QTextEdit {{
    background-color: transparent;
    color: #dfffee;
    border: none;
    padding: 12px;
    font-size: 13px;
    line-height: 1.5;
    selection-background-color: rgba(0, 230, 118, 0.25);
    font-family: "Cascadia Code", "Noto Sans JP", "Yu Gothic UI", "Meiryo", monospace;
}}

QLineEdit {{
    background-color: rgba(0, 0, 0, 0.6);
    color: #dfffee;
    border: 1px solid rgba(0, 230, 118, 0.45);
    border-radius: 6px;
    padding: 12px 16px;
    font-size: 14px;
    selection-background-color: rgba(0, 230, 118, 0.25);
}}

QLineEdit:focus {{
    border-color: {theme_color};
    background-color: rgba(0, 0, 0, 0.75);
}}

QPushButton {{
    background-color: {theme_color};
    color: #00150a;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #00cc66;
}}

QPushButton:pressed {{
    background-color: #00994d;
}}

QPushButton:disabled {{
    background-color: rgba(0, 60, 30, 0.8);
    color: #00150a;
}}

QLabel#titleLabel {{
    color: {theme_color};
    font-size: 18px;
    font-weight: bold;
    padding: 8px;
}}

QLabel#statusLabel {{
    color: rgba(0, 230, 118, 0.75);
    font-size: 11px;
    padding: 4px 8px;
}}

QScrollBar:vertical {{
    background: #0a0e14;
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background: #1a3a2a;
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: #00e676;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
""".format(panel_bg=PANEL_BG, theme_color=THEME_COLOR)


class ApiWorker(QThread):
    """バックグラウンドAPI呼び出し"""
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt: str):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            headers = {}
            if API_KEY:
                headers["x-api-key"] = API_KEY
            response = requests.post(
                CORE_URL,
                json={"prompt": self.prompt, "session_id": SESSION_ID},
                headers=headers,
                timeout=60
            )
            if response.ok:
                data = response.json()
                self.finished.emit(data.get("response", "（応答なし）"))
            else:
                self.error.emit(f"HTTP {response.status_code}")
        except Exception as e:
            self.error.emit(str(e))


def _find_asset(filename: str) -> Path | None:
    candidates = [
        APP_ROOT / filename,
        APP_ROOT / "command" / "assets" / filename,
        APP_ROOT / "command" / "assets" / "avatar" / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _install_fonts() -> list[str]:
    """同梱フォントがあれば読み込む（存在しなければ無視）。"""
    font_paths = [
        APP_ROOT / "command" / "assets" / "fonts" / "NotoSansJP-Regular.otf",
        APP_ROOT / "command" / "assets" / "fonts" / "NotoSansJP-Regular.ttf",
        APP_ROOT / "NotoSansJP-Regular.otf",
        APP_ROOT / "NotoSansJP-Regular.ttf",
    ]
    loaded_families: list[str] = []
    for path in font_paths:
        if not path.exists():
            continue
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id < 0:
            continue
        loaded_families.extend(QFontDatabase.applicationFontFamilies(font_id))
    return loaded_families


class CommandSurface(QWidget):
    """レトロ端末風の背景と走査線を描画する。"""
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 背景グラデーション
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor(0, 0, 0))
        grad.setColorAt(1.0, QColor(0, 8, 4))
        painter.fillRect(self.rect(), grad)

        # 上部ライン
        pen = QPen(QColor(0, 230, 118, 160), 2)
        painter.setPen(pen)
        painter.drawLine(24, 18, self.width() - 24, 18)

        # 走査線
        scan_pen = QPen(QColor(0, 0, 0, 40))
        painter.setPen(scan_pen)
        for y in range(0, self.height(), 4):
            painter.drawLine(0, y, self.width(), y)


class AvatarWidget(QFrame):
    """アバター表示エリア"""
    def __init__(self):
        super().__init__()
        self.setObjectName("avatarFrame")
        self.speaking = False
        self._mouth_open = False
        self._mouth_timer = QTimer(self)
        self._mouth_timer.setInterval(120)
        self._mouth_timer.timeout.connect(self._toggle_mouth)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # アバターエリア（将来的に画像を追加）
        self.avatar_area = QLabel()
        self.avatar_area.setFixedSize(180, 180)
        self.avatar_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar_area.setStyleSheet("""
            background-color: #0d1a14;
            border: 1px solid rgba(0, 230, 118, 0.6);
            border-radius: 4px;
            color: #00e676;
            font-size: 48px;
        """)
        self._idle_path = _find_asset("idle.png")
        self._talk_path = _find_asset("talk.png")
        self._idle_pixmap = QPixmap(str(self._idle_path)) if self._idle_path else None
        self._talk_pixmap = QPixmap(str(self._talk_path)) if self._talk_path else None
        if self._idle_pixmap:
            self._set_avatar_pixmap(self._idle_pixmap)
        else:
            self.avatar_area.setText("◉")
        layout.addWidget(self.avatar_area, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 名前
        name_label = QLabel("SPECTRA")
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("color: #00e676; font-size: 14px; font-weight: bold;")
        layout.addWidget(name_label)
        
        # ステータス
        self.status_label = QLabel("● ONLINE")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: rgba(0, 230, 118, 0.7); font-size: 11px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # リサイズ時に画像をフィット
        if self._idle_pixmap and not self.speaking:
            self._set_avatar_pixmap(self._idle_pixmap)
        elif self._talk_pixmap and self.speaking:
            self._set_avatar_pixmap(self._talk_pixmap)

    def _set_avatar_pixmap(self, pixmap: QPixmap):
        scaled = pixmap.scaled(
            self.avatar_area.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.avatar_area.setPixmap(scaled)

    def _toggle_mouth(self):
        if not self.speaking or not self._idle_pixmap or not self._talk_pixmap:
            return
        self._mouth_open = not self._mouth_open
        self._set_avatar_pixmap(self._talk_pixmap if self._mouth_open else self._idle_pixmap)

    def set_speaking(self, speaking: bool):
        self.speaking = speaking
        if speaking:
            self.status_label.setText("◉ SPEAKING...")
            self.status_label.setStyleSheet("color: #00e676; font-size: 11px;")
            self.avatar_area.setStyleSheet("""
                background-color: #0d1a14;
                border: 2px solid rgba(0, 230, 118, 0.9);
                border-radius: 4px;
                color: #00e676;
                font-size: 48px;
            """)
            if self._talk_pixmap:
                self._mouth_open = True
                self._set_avatar_pixmap(self._talk_pixmap)
                self._mouth_timer.start()
        else:
            self.status_label.setText("● ONLINE")
            self.status_label.setStyleSheet("color: rgba(0, 230, 118, 0.7); font-size: 11px;")
            self.avatar_area.setStyleSheet("""
                background-color: #0d1a14;
                border: 1px solid rgba(0, 230, 118, 0.6);
                border-radius: 4px;
                color: #00e676;
                font-size: 48px;
            """)
            self._mouth_timer.stop()
            if self._idle_pixmap:
                self._set_avatar_pixmap(self._idle_pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SPECTRA Console")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)
        self.worker = None

        self.setStyleSheet(STYLESHEET)
        self._setup_ui()
        
        # 起動メッセージ
        self._append_system("Spectra Communicator Online")
        self._append_system("AI Chat Ready")

    def _setup_ui(self):
        central = CommandSurface()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        # ヘッダー
        header = QHBoxLayout()
        
        title = QLabel("SPECTRA CONSOLE")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        
        header.addStretch()
        
        status = QLabel("◉ CONNECTED")
        status.setObjectName("statusLabel")
        header.addWidget(status)
        
        main_layout.addLayout(header)
        
        # メインフレーム
        main_frame = QFrame()
        main_frame.setObjectName("mainFrame")
        frame_layout = QHBoxLayout(main_frame)
        frame_layout.setContentsMargins(12, 12, 12, 12)
        frame_layout.setSpacing(12)
        
        # 左側: チャットエリア
        chat_container = QVBoxLayout()
        chat_container.setSpacing(8)
        
        # ターミナル出力ラベル
        terminal_label = QLabel("TERMINAL OUTPUT")
        terminal_label.setStyleSheet("color: rgba(0, 230, 118, 0.7); font-size: 10px;")
        chat_container.addWidget(terminal_label)
        
        # チャット表示
        chat_frame = QFrame()
        chat_frame.setObjectName("chatFrame")
        chat_inner = QVBoxLayout(chat_frame)
        chat_inner.setContentsMargins(0, 0, 0, 0)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_inner.addWidget(self.chat_display)
        
        chat_container.addWidget(chat_frame, stretch=1)
        frame_layout.addLayout(chat_container, stretch=1)
        
        # 右側: アバター
        self.avatar = AvatarWidget()
        frame_layout.addWidget(self.avatar)
        
        main_layout.addWidget(main_frame, stretch=1)
        
        # 入力エリア
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        prompt_label = QLabel(">")
        prompt_label.setStyleSheet("color: #00ff88; font-size: 18px; font-weight: bold;")
        input_layout.addWidget(prompt_label)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("メッセージを入力...")
        self.input_field.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.input_field, stretch=1)
        
        self.send_button = QPushButton("SEND")
        self.send_button.clicked.connect(self._send_message)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)

    def _append_system(self, text: str):
        self.chat_display.append(
            f'<p style="color: rgba(0, 230, 118, 0.7); margin: 4px 0;">'
            f'<span style="color: rgba(0, 230, 118, 0.45);">&gt;</span> {text}</p>'
        )

    def _append_user(self, text: str):
        self.chat_display.append(
            f'<p style="color: {USER_COLOR}; margin: 8px 0 4px 0;">'
            f'<span style="color: {THEME_COLOR}; font-weight: bold;">USER&gt;</span> {text}</p>'
        )

    def _append_spectra(self, text: str):
        self.chat_display.append(
            f'<p style="color: #e9fff3; margin: 4px 0 8px 0;">'
            f'<span style="color: {THEME_COLOR}; font-weight: bold;">Spectra&gt;</span> {text}</p>'
        )

    def _append_error(self, text: str):
        self.chat_display.append(
            f'<p style="color: #ff4444; margin: 4px 0;">'
            f'<span style="font-weight: bold;">[ERROR]</span> {text}</p>'
        )

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self._append_user(text)
        self.input_field.clear()
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        self.avatar.set_speaking(True)

        self.worker = ApiWorker(text)
        self.worker.finished.connect(self._on_response)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_response(self, response: str):
        self._append_spectra(response)
        self._enable_input()
        self.avatar.set_speaking(False)

    def _on_error(self, error: str):
        self._append_error(error)
        self._enable_input()
        self.avatar.set_speaking(False)

    def _enable_input(self):
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()


def main():
    app = QApplication(sys.argv)
    
    # 日本語フォントを明示的に設定
    installed = _install_fonts()
    font = QFont()
    font.setFamilies(installed + FONT_FALLBACKS + MONO_FALLBACKS)
    font.setPointSize(11)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
