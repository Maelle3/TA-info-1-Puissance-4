from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class Puissance4(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.partie = False
        Window.clearcolor = (0, 0, 0.75, 0)
        Window.size = (1000, 600)
        self.score1 = 0
        self.score2 = 0
        self.nouveau_joueur()
        self.plateau = [6 * [0] for i in range(7)]

    def on_size(self, x, taille):
        self.hauteur = taille[1]
        self.largeur = self.hauteur * 5 / 3
        Window.size = (self.largeur / 2, self.hauteur / 2)
        self.d = self.largeur * 0.09
        self.canvas.clear()
        if self.partie:
            self.update_plateau()

    def on_touch_down(self, touch):
        # ### on clique la case se colorie
        if self.partie:
            self.add_pion(touch.x, self.tour)

    def add_pion(self, x, tour):

        for k in range(7):
            if x >= self.largeur * 0.01 + k * self.largeur * 0.1 and \
                    x <= self.largeur * 0.01 + (k+1) * self.largeur * 0.1:
                i = 0
                while i < 6:
                    if self.plateau[k][i] != 0:
                        i += 1
                    else:
                        if tour % 2 == 0:
                            self.plateau[k][i] = 1
                            self.canvas.add(Color(1, 1, 0.3))
                            self.canvas.add(Ellipse(pos=(self.largeur * 0.01 + k * self.largeur * 0.1,
                                                         self.largeur * 0.005 + i * self.largeur * 0.1),
                                                    size=(self.d, self.d)))
                            i = 6
                        else:
                            self.plateau[k][i] = 2
                            self.canvas.add(Color(1, 0, 0.2))
                            self.canvas.add(Ellipse(pos=(self.largeur * 0.01 + k * self.largeur * 0.1,
                                                         self.largeur * 0.005 + i * self.largeur * 0.1),
                                                    size=(self.d, self.d)))
                            i = 6
                        self.tour += 1
        self.test_victoire_colonne(self.tour - 1)
        self.test_victoire_diago_droite(self.tour - 1)
        self.test_victoire_diago_gauche(self.tour - 1)
        self.test_victoire_ligne(self.tour - 1)
        self.test_egalite(self.tour - 1)

    def test_victoire_ligne(self, tour):
        joueur = tour % 2 + 1
        for k in range(4):
            for i in range(6):
                if self.plateau[k][i] == joueur and self.plateau[k + 1][i] == joueur and \
                        self.plateau[k + 2][i] == joueur and self.plateau[k + 3][i] == joueur:
                    self.partie = False
                    self.fin_partie(joueur)

    def test_victoire_colonne(self, tour):
        joueur = tour % 2 + 1
        for k in range(7):
            for i in range(3):
                if self.plateau[k][i] == joueur and self.plateau[k][i + 1] == joueur and \
                        self.plateau[k][i + 2] == joueur and self.plateau[k][i + 3] == joueur:
                    self.partie = False
                    self.fin_partie(joueur)

    def test_victoire_diago_gauche(self, tour):
        joueur = tour % 2 + 1
        for k in range(4):
            for i in range(3):
                if self.plateau[6 - k][i] == joueur and self.plateau[5 - k][i + 1] == joueur and \
                        self.plateau[4 - k][i + 2] == joueur and self.plateau[3 - k][i + 3] == joueur:
                    self.partie = False
                    self.fin_partie(joueur)

    def test_victoire_diago_droite(self, tour):
        joueur = tour % 2 + 1
        for k in range(4):
            for i in range(3):
                if self.plateau[k][i] == joueur and self.plateau[k + 1][i + 1] == joueur and \
                        self.plateau[k + 2][i + 2] == joueur and self.plateau[k + 3][i + 3] == joueur:
                    self.partie = False
                    self.fin_partie(joueur)

    def test_egalite(self, tour):
        if tour == 41 and self.partie:
            self.partie = False
            self.fin_partie(0)

    def fin_partie(self, joueur):
        if joueur == 0:
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(text="Il n'y a pas de gagnant"))
            content1 = Button(text="Nouvelle partie")
            box.add_widget(content1)
            content3 = Button(text="Nouveaux joueurs")
            box.add_widget(content3)
            content2 = Button(text='Arrêter de jouer')
            box.add_widget(content2)
            self.popup = Popup(title='Match nul !', content=box, size_hint=(None, None),
                               size=(self.largeur * 0.4, self.largeur * 0.4), auto_dismiss=False)
            content1.bind(state=self.callback)
            content2.bind(state=self.callback2)
            content3.bind(state=self.callback3)
            self.popup.open()
        else:
            if joueur == 1:
                self.score1 += 1
                box = BoxLayout(orientation='vertical')
                box.add_widget(Label(text='Bravo ' + self.joueur1))
            else:
                self.score2 += 1
                box = BoxLayout(orientation='vertical')
                box.add_widget(Label(text='Bravo ' + self.joueur2))
            content1 = Button(text="Nouvelle partie")
            box.add_widget(content1)
            content3 = Button(text="Nouveaux joueurs")
            box.add_widget(content3)
            content2 = Button(text='Arrêter de jouer')
            box.add_widget(content2)
            self.popup = Popup(title='Victoire !', content=box, size_hint=(0.5, 0.5),
                               auto_dismiss=False)
            content1.bind(state=self.callback)
            content2.bind(state=self.callback2)
            content3.bind(state=self.callback3)
            self.popup.open()

    def callback2(self, instance, value):
        if value == 'down':
            Window.close()

    def callback(self, instance, value):
        if value == 'down':
            self.popup.dismiss()
            self.remove_widget(self.texte1)
            self.remove_widget(self.texte2)
            self.nouvelle_partie()

    def callback3(self, instance, value):
        if value == 'down':
            self.popup.dismiss()
            self.remove_widget(self.texte1)
            self.remove_widget(self.texte2)
            self.score1 = 0
            self.score2 = 0
            self.nouveau_joueur()

    def nouvelle_partie(self):
        self.plateau = [6 * [0] for i in range(7)]
        self.update_plateau()
        self.tour = 0
        self.partie = True

    def nouveau_joueur(self):
        layout = BoxLayout(padding=10, orientation='vertical')
        btn1 = Button(text="OK", size_hint=(1, 0.2))
        btn1.bind(on_press=self.buttonClicked)
        layout.add_widget(Label(text='Tapez le nom du joueur 1', size_hint=(1, 0.15)))
        self.txt1 = TextInput(text='', multiline=False, size_hint=(1, 0.25))
        layout.add_widget(self.txt1)
        layout.add_widget(Label(text='Tapez le nom du joueur 2', size_hint=(1, 0.15)))
        self.txt2 = TextInput(text='', multiline=False, size_hint=(1, 0.25))
        layout.add_widget(self.txt2)
        self.popup = Popup(title='Noms des joueurs', content=layout, size_hint=(0.5, 0.5),
                           auto_dismiss=False)
        layout.add_widget(btn1)
        self.popup.open()
        self.partie = False

    def buttonClicked(self, btn):
        self.popup.dismiss()
        self.joueur1 = self.txt1.text
        self.joueur2 = self.txt2.text
        self.nouvelle_partie()

    def update_plateau(self):
        for k in range(7):
            for i in range(6):
                if self.plateau[k][i] == 1:
                    self.canvas.add(Color(1, 1, 0.3))
                    self.canvas.add(Ellipse(pos=(self.largeur * 0.01 + k * self.largeur * 0.1, self.largeur * 0.005 +
                                                 i * self.largeur * 0.1), size=(self.d, self.d)))
                elif self.plateau[k][i] == 2:
                    self.canvas.add(Color(1, 0, 0.2))
                    self.canvas.add(Ellipse(pos=(self.largeur * 0.01 + k * self.largeur * 0.1, self.largeur * 0.005 +
                                                 i * self.largeur * 0.1), size=(self.d, self.d)))
                else:
                    self.canvas.add(Color(0.9, 0.9, 0.85))
                    self.canvas.add(Ellipse(pos=(self.largeur * 0.01 + k * self.largeur * 0.1, self.largeur * 0.005 +
                                                 i * self.largeur * 0.1), size=(self.d, self.d)))
        self.texte1 = Label(pos=(self.largeur * 0.8, self.largeur * 0.4), text=self.joueur1 + ' : ' + str(self.score1),
                            font_size=str(self.largeur * 0.02) + 'sp')
        self.add_widget(self.texte1)
        self.texte2 = Label(pos=(self.largeur * 0.8, self.largeur * 0.2), text=self.joueur2 + ' : ' + str(self.score2),
                            font_size=str(self.largeur * 0.02) + 'sp')
        self.add_widget(self.texte2)


class Puissance4App(App):
    def build(self):
        return Puissance4()


if __name__ == '__main__':
    Puissance4App().run()
