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
def ask(question):
  # Initialize the LiteLLM client
  client = litellm.Client(api_key="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")
  # Define your query
  references_list = []
  client = create_client()
  
  documents = vector_search(client, question)
  for document in documents:
    references_list.append(refereces_template.format(book=document["book"], chapter=document["chapter_title"], content = document["content"]))
  #references
  user_prompt = prompt_template(references="".join(references_list), prompt=question)
  
  
  # Query the ChatGPT-4-0314 model
  response = client.chat_complete(
      model="o1",
      messages=[ {"role": "system", "content": system_role},  # Define the system role
                 {"role": "user", "content": user_prompt}     # User query
               ]
  )
  
  # Get the response content and token usage
  response_content = response['choices'][0]['message']['content']
  usage = response['usage']
  
  # Extract tokens used
  prompt_tokens = usage['prompt_tokens']  # Tokens in the input
  completion_tokens = usage['completion_tokens']  # Tokens in the response
  #total_tokens = usage['total_tokens']  # Total tokens used
  
  # Calculate the cost
  # OpenAI pricing (as of this date) is $0.03/1K tokens for prompts and $0.06/1K tokens for completions.
  prompt_cost = (prompt_tokens / 1000) * 0.03
  completion_cost = (completion_tokens / 1000) * 0.06
  total_cost = prompt_cost + completion_cost
  print(f"Cost: ${total_cost}")
  return response_content

  
  
  
