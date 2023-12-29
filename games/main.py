from MainWindow import Ui_MainWindow
from MainWindowLogIn import Ui_MainWindowLogIn
from MainWindowNewAccount import Ui_MainWindowNewAccount
from MainWindowRating import Ui_MainWindowRating
from MainWindowChooseGame import Ui_WindowChooseGame
from MainWindowXo import Ui_MainWindowXo
from PyQt5.QtWidgets import *
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

NAMES_OF_ROWS_IN_RATING = ['Крестики-нолики']
NAMES_OF_COLUMNS_IN_RATING = ['Всего игр', 'Побед', 'Поражений']


class MainClass(Ui_MainWindow, Ui_MainWindowLogIn, Ui_MainWindowXo,
                Ui_MainWindowNewAccount, Ui_WindowChooseGame,
                Ui_MainWindowRating, QMainWindow):
    def __init__(self):
        super().__init__()
        self.go_main_window()
        self.count_id = 0

    def go_main_window(self):
        self.setupUi(self)
        self.log_in_profile.clicked.connect(self.go_log_in_window)
        self.new_profile.clicked.connect(self.new_account_window)

    def go_log_in_window(self):
        self.setupUiLogIn(self)
        self.pushButton_cancel_login.clicked.connect(self.go_main_window)
        self.pushButton_ok_login.clicked.connect(self.correct_data_login)

    def correct_data_login(self):
        login, password = self.log_in_input_login.text(), self.password_input_login.text()
        if not login and not password:
            self.label_of_error_login.setText('Пожалуйста введите данные')
        else:
            with sqlite3.connect('profiles_for_games_db.sqlite') as con:
                cur = con.cursor()
                profile = cur.execute(f'SELECT * FROM profiles WHERE profile = "{login}"').fetchone()
                if not profile:
                    self.label_of_error_login.setText("Такого аккаунта не существует.")
                elif str(profile[2]) != password:
                    self.label_of_error_login.setText('Неправильный пароль. Попробуйте снова.')
                else:
                    self.ID_OF_PLAYING_USER = profile[0]
                    self.go_choose_game_window()

    def correct_data_register(self):
        login, password = self.log_in_input.text(), self.password_input.text()
        if not login and not password:
            self.label_of_error.setText('Пожалуйста введите данные')
        else:
            with sqlite3.connect('profiles_for_games_db.sqlite') as con:
                cur = con.cursor()
                profile = cur.execute(f'SELECT * FROM profiles WHERE profile = "{login}"').fetchone()
                if profile:
                    self.label_of_error.setText("Такой аккаунт уже существует")
                else:
                    cur.execute(f"INSERT INTO profiles(profile,password) VALUES{(login, password)}")
                    con.commit()
                    self.ID_OF_PLAYING_USER = cur.execute(f'SELECT * FROM profiles '
                                                          f'WHERE profile = "{login}"').fetchone()[0]
                    cur.execute(f"INSERT INTO all_games VALUES{(self.ID_OF_PLAYING_USER, 1, 1)}")
                    cur.execute(f"INSERT INTO wins VALUES{(self.ID_OF_PLAYING_USER, 1, 1)}")
                    cur.execute(f"INSERT INTO defeats VALUES{(self.ID_OF_PLAYING_USER, 1, 1)}")
                    con.commit()
                    self.go_choose_game_window()

    def new_account_window(self):
        self.setupUiNewAccount(self)
        self.pushButton_ok.clicked.connect(self.correct_data_register)
        self.pushButton_cancel.clicked.connect(self.go_main_window)

    def go_choose_game_window(self):
        self.setupUiChooseGame(self)
        self.exit_profile_button.clicked.connect(self.go_main_window)
        self.show_rating_of_games.clicked.connect(self.go_rating_window)
        self.xo_button.clicked.connect(self.go_xo_window)

    def go_rating_window(self):
        self.setupUiRating(self)
        with sqlite3.connect('profiles_for_games_db.sqlite') as con:
            cur = con.cursor()
            id_login = cur.execute(f'SELECT * FROM profiles').fetchall()
        for profile in id_login:
            self.choose_profile.addItem(str(profile[1]), profile[0])
        self.search_button.clicked.connect(self.fill_rating_table)
        self.back_to_menu_button.clicked.connect(self.go_choose_game_window)

    def fill_rating_table(self):
        self.table_of_rating.clear()
        list_of_data = self.get_users_rating_data()
        self.table_of_rating.setVerticalHeaderLabels(NAMES_OF_ROWS_IN_RATING)
        self.table_of_rating.setHorizontalHeaderLabels(NAMES_OF_COLUMNS_IN_RATING)
        if list_of_data[0]:
            for j in range(3):
                if list_of_data[0][j + 1]:
                    self.table_of_rating.setItem(j, 0, QTableWidgetItem(str(list_of_data[0][j + 1] - 1)))
                else:
                    self.table_of_rating.setItem(j, 0, QTableWidgetItem('-'))
        else:
            for j in range(3):
                self.table_of_rating.setItem(j, 0, QTableWidgetItem('-'))
        for i in range(1, 3):
            if list_of_data[i]:
                for j in range(2):
                    if list_of_data[i][j + 1]:
                        self.table_of_rating.setItem(j, i, QTableWidgetItem(str(list_of_data[i][j + 1] - 1)))
                    else:
                        self.table_of_rating.setItem(j, i, QTableWidgetItem('-'))
            else:
                for j in range(2):
                    self.table_of_rating.setItem(j, i, QTableWidgetItem('-'))

    def get_users_rating_data(self):
        with sqlite3.connect('profiles_for_games_db.sqlite') as con:
            cur = con.cursor()
            profile = self.choose_profile.currentText()
            id_of_profile = cur.execute(f'SELECT * FROM profiles WHERE profile = "{profile}"').fetchone()[0]
            all_games = cur.execute(f'SELECT * FROM all_games WHERE id = {id_of_profile}').fetchone()
            wins = cur.execute(f'SELECT * FROM wins WHERE id = {id_of_profile}').fetchone()
            defeats = cur.execute(f'SELECT * FROM defeats WHERE id = {id_of_profile}').fetchone()
            return [all_games, wins, defeats]


    def go_xo_window(self):
        self.setupUiXo(self)
        self.buttons = [[self.button_1, self.button_2, self.button_3], [self.button_4,
                                                                        self.button_5, self.button_6],
                        [self.button_7, self.button_8,
                         self.button_9]]
        self.x_radiobutton.setChecked(True)
        with sqlite3.connect('profiles_for_games_db.sqlite') as con:
            cur = con.cursor()
            id_login = cur.execute(f'SELECT * FROM profiles WHERE id != {self.ID_OF_PLAYING_USER}').fetchall()
        for profile in id_login:
            self.profile_of_dival.addItem(str(profile[1]), profile[0])
        self.counter = 0
        self.turn_on_xo_table()
        for buttons in self.buttons:
            for button in buttons:
                button.clicked.connect(self.set_sign)
                button.clicked.connect(self.play_xo)
        self.new_game_button.clicked.connect(self.go_xo_window)
        self.back_to_choose_game.clicked.connect(self.go_choose_game_window)

    def set_sign(self):
        if self.x_radiobutton.isChecked() and self.counter == 0:
            self.player = 'X'
            self.player_sign, self.dival_sign = 'X', 'O'
            self.counter += 1
        elif self.o_radiobutton.isChecked() and self.counter == 0:
            self.player = 'O'
            self.player_sign, self.dival_sign = 'O', 'X'
            self.counter += 1

    def play_xo(self):
        self.sender().setText(self.player)
        self.sender().setDisabled(True)
        self.isWin()

    def isWin(self):
        if self.player == 'O':
            self.player = 'X'
        else:
            self.player = 'O'
        ans = []
        for i in range(3):
            temp = self.buttons[i][0].text() + self.buttons[i][1].text() + self.buttons[i][2].text()
            ans.append(temp)
        for j in range(3):
            temp = self.buttons[0][j].text() + self.buttons[1][j].text() + self.buttons[2][j].text()
            ans.append(temp)
        temp = self.buttons[0][0].text() + self.buttons[1][1].text() + self.buttons[2][2].text()
        ans.append(temp)
        temp = self.buttons[0][2].text() + self.buttons[1][1].text() + self.buttons[2][0].text()
        ans.append(temp)
        if 'XXX' in ans:
            self.label_of_game_result.setText('Победа крестиков!')
            self.turn_off_xo_table()
            with sqlite3.connect('profiles_for_games_db.sqlite') as con:
                cur = con.cursor()
                if self.dival_sign == 'X':
                    id_login_of_winner = cur.execute(f'SELECT * FROM profiles WHERE profile '
                                                     f'= {self.profile_of_dival.currentText()}').fetchone()[0]
                    id_login_of_defeated = self.ID_OF_PLAYING_USER
                else:
                    id_login_of_defeated = cur.execute(f'SELECT * FROM profiles WHERE profile '
                                                       f'= {self.profile_of_dival.currentText()}').fetchone()[0]
                    id_login_of_winner = self.ID_OF_PLAYING_USER
                cur.execute(f'UPDATE wins SET xo_game = xo_game + 1'
                            f' WHERE id = {id_login_of_winner}')
                cur.execute(f'UPDATE defeats SET xo_game = xo_game + 1'
                            f' WHERE id = {int(id_login_of_defeated)}')
                cur.execute(f'UPDATE all_games SET xo_game = xo_game + 1'
                            f' WHERE id in {(id_login_of_defeated, id_login_of_winner)}')
        elif 'OOO' in ans:
            self.label_of_game_result.setText('Победа ноликов!')
            self.turn_off_xo_table()
            with sqlite3.connect('profiles_for_games_db.sqlite') as con:
                cur = con.cursor()
                if self.dival_sign == 'O':
                    id_login_of_winner = cur.execute(f'SELECT * FROM profiles WHERE profile '
                                                     f'= {self.profile_of_dival.currentText()}').fetchone()[0]
                    id_login_of_defeated = self.ID_OF_PLAYING_USER
                else:
                    id_login_of_defeated = cur.execute(f'SELECT * FROM profiles WHERE profile '
                                                       f'= {self.profile_of_dival.currentText()}').fetchone()[0]
                    id_login_of_winner = self.ID_OF_PLAYING_USER
                cur.execute(f'UPDATE wins SET xo_game = xo_game + 1'
                            f' WHERE id = {id_login_of_winner}')
                cur.execute(f'UPDATE defeats SET xo_game = xo_game + 1'
                            f' WHERE id = {id_login_of_defeated}')
                cur.execute(f'UPDATE all_games SET xo_game = xo_game + 1'
                            f' WHERE id in {(id_login_of_defeated, id_login_of_winner)}')
        elif list(map(len, ans)) == [3, 3, 3, 3, 3, 3, 3, 3]:
            self.label_of_game_result.setText('Ничья')
            self.turn_off_xo_table()

    def turn_off_xo_table(self):
        self.new_game_button.setDisabled(False)
        for buttons in self.buttons:
            for button in buttons:
                button: QPushButton
                button.setDisabled(True)

    def turn_on_xo_table(self):
        for buttons in self.buttons:
            for button in buttons:
                button: QPushButton
                button.setDisabled(False)
        self.new_game_button.setDisabled(True)


sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainClass()
    ex.show()
    sys.exit(app.exec())
