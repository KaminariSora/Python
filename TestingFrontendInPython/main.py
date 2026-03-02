import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QFrame, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# ---------- Product Card ----------
class ProductCard(QFrame):
    def __init__(self, name, price):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #ddd;
            }
            QPushButton {
                background-color: #6C5CE7;
                color: white;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #5a4bd1;
            }
        """)
        self.setFixedSize(200, 220)

        layout = QVBoxLayout()

        title = QLabel(name)
        title.setFont(QFont("Arial", 10, QFont.Bold))

        price_label = QLabel(f"{price} ฿")
        price_label.setStyleSheet("color: green; font-weight: bold;")

        btn = QPushButton("Add to Cart")

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(price_label)
        layout.addWidget(btn)

        self.setLayout(layout)

# ---------- Main Window ----------
class MarketplaceUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Marketplace")
        self.setGeometry(100, 100, 1000, 600)

        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.addWidget(QLabel("Categories"))

        for cat in ["Art", "Stationery", "Tech", "Clothes"]:
            btn = QPushButton(cat)
            btn.setStyleSheet("text-align:left; padding:8px;")
            sidebar.addWidget(btn)

        sidebar.addStretch()

        sidebar_widget = QFrame()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(180)
        sidebar_widget.setStyleSheet("background:#f1f2f6;")

        # Main content
        content_layout = QVBoxLayout()

        # Header
        header = QHBoxLayout()
        title = QLabel("🛍️ AI Marketplace")
        title.setFont(QFont("Arial", 16, QFont.Bold))

        search = QLineEdit()
        search.setPlaceholderText("Search product...")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(search)

        # Product Grid
        grid = QGridLayout()

        products = [
            ("Sketch Book", 120),
            ("Digital Art Tablet", 3500),
            ("Sticker Pack", 50),
            ("Canvas Bag", 200),
            ("Water Color Set", 450),
            ("Anime Poster", 99),
        ]

        row, col = 0, 0
        for name, price in products:
            card = ProductCard(name, price)
            grid.addWidget(card, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        container = QWidget()
        container.setLayout(grid)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")

        content_layout.addLayout(header)
        content_layout.addWidget(scroll)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(content_widget)

# ---------- Run App ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarketplaceUI()
    window.show()
    sys.exit(app.exec_())