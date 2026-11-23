import sys
import random
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QTextEdit,
)
from PyQt6.QtGui import (
    QFont,
    QShortcut,
    QKeySequence
)


class Satunnaisgeneraattori(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Satunnaislukugeneraattori")

        layout = QGridLayout()

        layout.addWidget(QLabel("Kierrosmäärä:"), 0, 0, 1, 2)
        self.kierrokset = QLineEdit()
        layout.addWidget(self.kierrokset, 0, 2, 1, 2)
        

        # Alin arvo
        self.alin = self.luo_kentta(
            layout,
            "Alin arvo:",
            1,
            0
        )

        # Ylin arvo
        self.ylin = self.luo_kentta(
            layout,
            "Ylin arvo:",
            1,
            2
        )

        # Toinen alin
        self.alin2 = self.luo_kentta(
            layout,
            "Toisen arvon alin arvo:",
            3,
            0
        )

        # Toinen ylin
        self.ylin2 = self.luo_kentta(
            layout,
            "Toisen arvon ylin arvo:",
            3,
            2
        )
        
        # Kaikki kentät yhdessä
        self.kentat = [
            self.kierrokset,
            self.alin,
            self.ylin,
            self.alin2,
            self.ylin2
        ]

        layout.addItem(
            QSpacerItem(20, 30, QSizePolicy.Policy.Minimum,
                        QSizePolicy.Policy.Fixed),
            5, 0
        )

        # Nappi
        self.nappi = QPushButton("Arvo luku")
        layout.addWidget(self.nappi, 6, 0, 1, 2)
        self.nappi.setDefault(True)


        self.nappi.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Tyhjennys
        for nappain in ["Esc", "F5"]:
            shortcut = QShortcut(QKeySequence(nappain), self)
            shortcut.activated.connect(self.tyhjennys)
        

        # Tulos
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText("Tulokset näkyvät tässä")
        self.result.setFixedHeight(120)
        self.result.setFont(QFont("Consolas", 10))

        layout.addWidget(self.result, 6, 2, 1, 2)

        self.setLayout(layout)
        self.kierrokset.setFocus()

        for kentta in self.kentat:
            kentta.returnPressed.connect(self.laske)

        self.nappi.clicked.connect(self.laske)

    def laske(self):
        try:
            kierrokset = self.hae_luku(self.kierrokset, "Kierrosmäärä")
            
            if kierrokset <= 0:
                self.result.setPlainText("Kierrosmäärän pitää olla suurempi kuin 0")
                return
            
            min_arvo = self.hae_luku(self.alin, "Alin arvo")
            max_arvo = self.hae_luku(self.ylin, "Ylin arvo")

            min_arvo2 = self.hae_luku(self.alin2, "Toinen alin arvo")
            max_arvo2 = self.hae_luku(self.ylin2, "Toinen ylin arvo")
            

            if min_arvo > max_arvo:
                self.result.setPlainText("Alimman arvon täytyy olla pienempi!")
                return
            
            if min_arvo2 > max_arvo2:
                self.result.setPlainText(
                "Toisen arvon alimman arvon täytyy olla pienempi!")
                return


            tulokset = []

            for i in range(kierrokset):
                luku = random.randint(min_arvo, max_arvo)
                luku2 = random.randint(min_arvo2, max_arvo2)

                tulokset.append(
                    f"{i+1:3}. {luku:>7} : {luku2:>7}"
                )

            self.result.setPlainText(
                "\n".join(tulokset)
            )

        except ValueError as e:
            self.result.setPlainText(str(e))

    # Tyhjennysfunktio
    def tyhjennys(self):
        for kentta in self.kentat:
            kentta.clear()
            
        self.result.clear()

    def hae_luku(self, kentta, nimi):
        teksti = kentta.text().strip()
        
        if not teksti:
            raise ValueError(f"{nimi} puuttuu")
        
        try:
            return int(teksti)

        except ValueError:
            raise ValueError(f"{nimi} ei ole kokonaisluku")
        
    # Kenttäapufunktio
    def luo_kentta(self, layout, otsikko, rivi, sarake):
        layout.addWidget(QLabel(otsikko), rivi, sarake, 1, 2)

        kentta = QLineEdit()
        layout.addWidget(kentta, rivi + 1, sarake, 1, 2)

        return kentta

ohjelma = QApplication(sys.argv)

sovellusikkuna = Satunnaisgeneraattori()
sovellusikkuna.resize(600, 200)
sovellusikkuna.show()

sys.exit(ohjelma.exec())