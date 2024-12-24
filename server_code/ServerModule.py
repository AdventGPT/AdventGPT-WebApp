import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.facebook.auth
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import litellm
from VectorDB.search import create_client, vector_search
from rich import print
import os
from litellm import completion, completion_cost

system_role = """\
You are an expert in Seventh Day Adventist theology. Providing a set of Ellen White Reference your task is to follow instructions like:
- Question Answering
- Making reports
- Create sermons
- Etc

The refferences are provided in the following format:

-----
Book:{Contains the book name}
Chapter: {Contains the name of the chapter}
Content: {reference content}
-----

Please use the reference as the context for following the instruction demanded. 
Responde in Markdown format, and use the reference provided as primary source of information.
Appart from the reference provided you can fill the gaps using your knowledge in history, hebrew and aramaic.
Please, provide the reference you used to reach conclusion in this format: [*Book - Chapter*]

"""

prompt_template = """\
Given the followigs references:
{references}
-----

{prompt}
"""
refereces_template = """\
-----
Book:{book}
Chapter: {chapter}
Content: {content}
"""

@anvil.server.callable
def start_asking(question):
    # Launch the background task from server-side code
    task = anvil.server.launch_background_task('ask', question)
    return task  # Return the task to the client
  

#@anvil.server.callable
@anvil.server.background_task
def ask(question):

  # Define your query
  references_list = []
  client = create_client()
  
  documents = vector_search(client, question)
  for document in documents:
    references_list.append(refereces_template.format(book=document["book"], chapter=document["chapter_title"], content = document["content"]))
  #references
  user_prompt = prompt_template.format(references="".join(references_list), prompt=question)  

  messages=[ {"role": "system", "content": system_role},  # Define the system role
                 {"role": "user", "content": user_prompt}     # User query
               ]
  api_key = anvil.secrets.get_secret("OPENAI_API_KEY")
  response= completion(
    model="gpt-4o",  # Specify the model
    messages=messages,    # Provide the conversation history
    max_tokens=1024*30,   # Set the maximum number of tokens for a longer response
    api_key=api_key  # Pass the API key directly
  )
  
  # Get the response content and token usage
  response_content = response['choices'][0]['message']['content']
  cost = completion_cost(completion_response=response)
  formatted_cost = f"${float(cost):.10f}"
  print(f"Cost: ${formatted_cost}")
  return response_content

  
  
  
