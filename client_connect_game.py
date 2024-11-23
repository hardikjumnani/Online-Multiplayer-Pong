from customtkinter import *
import random
import string

def random_username(length: int = 8) -> str:
    return random.choices(string.ascii_lowercase, (3*length)//4) + random.choices(string.digits, length//4)

class ConnectGameWindow:
    def __init__(self, root: CTk):
        self._root = root

        self._root.geometry('400x300+100+50')
        self._root.title('OMP | Hardik J.')

        # Variables
        var_username = StringVar()
        var_server_ip = StringVar()

        # Widgets
        lbl_players_online = CTkLabel(self._root, text='Players Online: ---', font=('Calibra', 14), text_color='yellow')
        lbl_players_online.pack(anchor='e')
        # ------------
        lbl_title = CTkLabel(self._root, text='OMP | Hardik J.', font=('Calibra', 20, 'bold'))
        lbl_title.pack(pady=10)
        # ------------
        frm_username = CTkFrame(self._root, fg_color='transparent')
        frm_username.pack(padx=20, pady=5)

        lbl_username = CTkLabel(frm_username, text='Username', bg_color='transparent')
        lbl_username.grid(row=0, column=0, padx=10, pady=5)

        txt_username = CTkEntry(frm_username, textvariable=var_username)
        txt_username.grid(row=0, column=1, padx=10, pady=5)
        # ------------
        frm_server_ip = CTkFrame(self._root, fg_color='transparent')
        frm_server_ip.pack(padx=20, pady=5)

        lbl_server_ip = CTkLabel(frm_server_ip, text='Server IP', fg_color='transparent')
        lbl_server_ip.grid(row=0, column=0, padx=10, pady=5)

        txt_server_ip = CTkEntry(frm_server_ip, textvariable=var_server_ip)
        txt_server_ip.grid(row=0, column=1, padx=10, pady=5)
        #------------
        btn_connect = CTkButton(self._root, command=self.fn_connect, text='Connect', font=('Helvetica', 18, 'bold'))
        btn_connect.pack(pady=20)
        #------------
        lbl_info = CTkLabel(self._root, text='', text_color='white')
        lbl_info.pack(pady=20)


    def fn_connect():
        """This tries to connect to server and find a game for the user."""
        ...


if __name__ == '__main__':
    root = CTk()
    ConnectGameWindow(root)
    root.mainloop()