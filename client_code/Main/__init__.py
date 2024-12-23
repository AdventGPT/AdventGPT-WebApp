from ._anvil_designer import MainTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.wellcome_message = "Hello I am an expert in EGW Writtings, how can I help you."
    self.item['chat_output'] = self.wellcome_message
    self.item['chat_input_text'] = ""
    self.init_components(**properties)
    anvil.users.login_with_form()
    self.system = []
    self.user = []
    self.render()
    print(f"This user has logged in: {anvil.users.get_user()['email']}")

  def render(self):
    self.item['chat_output'] = self.wellcome_message
    for i in range(max(len(self.user), len(self.system))):
        if i < len(self.user):
          self.item['chat_output'] += "\n\n" + self.user[i]
        if i < len(self.system):
          self.item['chat_output'] += "\n > " + self.system[i]
    self.refresh_data_bindings()
                       

    
  def send_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.user.append(self.item['chat_input_text'])
    self.system.append("Ok ok ok")
    self.render()

  def input_text_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    # Todo 
    #   if enter, send
    #   If control+enter, add \n
    pass


    
    
    