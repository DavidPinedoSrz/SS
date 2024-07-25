from tkinter import messagebox
from Login.forms.master.form_master import MasterPanel
from Login.persistence.repository.auth_user_repository import AuthUserRepositroy
import Login.util.encoding_decoding as end_dec
from Login.persistence.model import Auth_User
from Login.forms.login.other_form_login_designer import FormLoginDesigner
from Login.forms.registration.form import FormRegister
from MenuSideBar.formularios.Part_form_maestro_design import PartMenu

class PartForm(FormLoginDesigner):

    def __init__(self):
        self.auth_repository = AuthUserRepositroy()
        super().__init__()

    def verificar(self):
        user_db: Auth_User = self.auth_repository.getUserById(
            int(self.user_id.get()))
        if(self.isUser(user_db)):
            self.isPassword(self.password.get(), user_db)

    def userRegister(self):
        FormRegister().mainloop()

    def isUser(self, user: Auth_User):
        status: bool = True
        if(user == None):
            status = False
            messagebox.showerror(
                message="El usuario no existe por favor registrese", title="Mensaje",parent=self.ventana)            
        return status

    def isPassword(self, password: str, user: Auth_User):
        b_password = end_dec.decrypt(user.password)
        if(password == b_password):
            self.ventana.destroy()
            PartMenu().mainloop()
        else:
            messagebox.showerror(
                message="La contraseña no es correcta", title="Mensaje")