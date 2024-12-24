from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import time


class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.wellcome_message = "```Hello I am an expert in EGW Writtings, how can I help you.```"
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
          self.item['chat_output'] += "\n\n```" + self.user[i] + "```"
        if i < len(self.system):
          self.item['chat_output'] += "\n" + self.system[i]
    self.refresh_data_bindings()
                       

    
  def send_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    ask = self.item['chat_input_text']
    self.user.append(ask)
    self.item['chat_input_text'] = ''
    self.render()

    try:
      task = anvil.server.call('start_asking', ask, self.model_selection.selected_value, int(self.context_retrieval.selected_value))
      while not task.is_completed():
        time.sleep(1)  # Wait a bit before checking again

    # Get the result
      responce, cost = task.get_return_value()
      self.cost_lable.text=cost
      self.system.append(responce)
      self.render()
    except anvil.server.TimeoutError:
        # Show a notification banner if timeout occurs
        Notification("The request timed out. Please try again.", title="Timeout Error", style="error").show()

  def input_text_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    # Todo 
    #   if enter, send
    #   If control+enter, add \n
    pass

  def model_selection_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def clean_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['chat_output'] = self.wellcome_message
    self.user = []
    self.system = []
    self.refresh_data_bindings()
    self.cost_lable.text = ""


    
    
    