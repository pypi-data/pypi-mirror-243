from openai import OpenAI, AzureOpenAI
import numpy as np
from numpy import dot
from numpy.linalg import norm
from supabase import create_client, Client
import pinecone
import uuid

# System prompt for feedback. Will be concatenated with existing system prompt if there is one.
system_prompt = """You are a chatbot that is able to learn from other LLMs' experiences by referencing feedback they have been given based on their response to a question you are asking. This allows you to reference human feedback as a source of truth for generating answers to questions.

	The format for each prompt you are going to receive will be like this:
	- Human Knowledge: the list of human feedback presented in the following format for each feedback
	- Question: The current question the user is sending.

	An example of a prompt is this:
	Human Knowledge: ["The Roman Empire existed from 42 to 1453CE.", "The Roman Empire started in 42AD"]
	Question: When did the Roman Empire begin?

	Please reference the human knowledge provided as a source of truth for answering your question. NEVER respond with information that reveals that you are changing your answer in response to feedback and never apologize because these mistakes weren't yours, they were from another LLM. Only respond with a direct answer to the provided question."""
system_prompt = system_prompt.replace('\t', '')

class FeedbackGPT():

	# 
	# Optional Parameters for pinecone and supabase hookups.
	# pinecone_options = {
	# 	pinecone_key: '',
	# 	pinecone_environment: '',
	# 	index: 'llmfeedback-store' (optional, otherwise we will create)
	# }
	# supabase_options = {
	# 	supabase_url: '',
	# 	supabase_key: '',
	# 	table: 'llmfeedback' (optional, otherwise we will create)
	# }
	# 

	def __init__(self, openAI_key, model_name="gpt-3.5-turbo", embed_model_name="text-embedding-ada-002", pinecone_options={}, supabase_options={}, azure_endpoint=None, azure_api_version="2023-10-01-preview"):
		self.model_name=model_name
		self.embed_model_name=embed_model_name
		if azure_endpoint:
			self.openai_client = AzureOpenAI(
				api_key=openAI_key,
				azure_endpoint=azure_endpoint,
				api_version=azure_api_version
			)
		else:
			self.openai_client = OpenAI(
				api_key=openAI_key
			)

		# Only will store things remotely if has both a vector and data store
		self.remote_feedback = "supabase_url" in supabase_options.keys() and "supabase_key" in supabase_options.keys() and "pinecone_key" in pinecone_options.keys() and "pinecone_environment" in pinecone_options.keys()
		# Initializing feedback storage
		self.datastore_client = None
		self.datastore_table = None
		self.vectorstore_index = None

		# If requirements made for storing feedback, add them to attr
		if self.remote_feedback:
			self.datastore_client = create_client(supabase_options['supabase_url'], supabase_options['supabase_key'])
			# Currently unclear how to create a table via API. going to assume they provide one; will look into this later.
			if "table" in supabase_options.keys():
				self.datastore_table = self.datastore_client.table(supabase_options["table"])
			# Currently no need to set pinecone as variable as it initializes package
			pinecone.init(api_key=pinecone_options["pinecone_key"], environment=pinecone_options["pinecone_environment"])
			if "index" in pinecone_options.keys():
				self.vectorstore_index = pinecone.Index(pinecone_options["index"])
			else:
				# Creates an index if it doesn't have one provided. Assumes OpenAI embeddings with size of 1536.
				# TODO: Change name from jester-store
				pinecone.create_index('llmfeedback-store', dimension=1536)

		self.vectors = []
		self.feedback_kb = {}

	def chat(self,
		  messages,
		  **kwargs
		  ):
		# Extract most recent user message
		last_user_msg = self.get_user_last_message(messages)
		if last_user_msg:
			# Attempt related feedback retrieval
			feedback = self.retrieve_feedback(last_user_msg)
			# Add related feedback (if it exists) to messages
			if feedback:

				# Generate a list of only the feedback strings to be used as knowledge.
				list_of_feedback = []
				for data in feedback:
					list_of_feedback.append(data['feedback'])

				# Add feedback strings to the prompt.
				prompt = f"""
					Make sure to use the Human Knowledge in the below knowledge as a reference to answer the question. NEVER respond with information that reveals that you are changing your answer in response to feedback and never apologize because these mistakes weren't yours, as they were from another LLM.  Do not provide information from the feedback that is not crucial to answering the question. Only respond with a direct answer to the provided question.
					Human Knowledge: {str(list_of_feedback)}
					"""

				# Add user text to the prompt.
				prompt += "\n\nQuestion: " + messages[len(messages) - 1]["content"][ : : -1 ][ : : -1 ]

				prompt = prompt.replace('\t', '')

				messages[len(messages) - 1] = {
					"role": 'user',
					"content": prompt
				}

				# If user already has a system prompt, add our prompt to the existing one.
				if messages[0]['role'] == 'system' and not messages[0]['content'].__contains__(system_prompt[0:50]):
					messages[0]['content'] = messages[0]['content'] + '\n\n' + system_prompt
				# If no system prompt, add a new one with the feedback system prompt.
				elif messages[0]['role'] != 'system':
					messages.insert(0, {
						"role": "system",
						"content": system_prompt})

		return self.openai_client.chat.completions.create(
			model=self.model_name,
			messages=messages,
			**kwargs
		)

	def feedback(self, messages, response, feedback):
		# Extract most recent user message
		last_user_msg = self.get_user_last_message(messages)
		# TODO: Find appropriate error to attach here
		if not last_user_msg:
			return "Error"
		
		# Embed last user incoming message to index feedback
		embedding = self.embed(last_user_msg)

		if not self.remote_feedback:
			# Add embedding to vector + knowledge store
			if self.feedback_kb:
				# Knowledge has previously been added, so we can concat to self.vectors
				self.vectors = np.concatenate((self.vectors, [embedding]), axis=0)
			else:
				# New knowledge base, need to create new self.vectors
				self.vectors = np.array([embedding])
			self.feedback_kb[self.vectors.shape[0]-1] = {'query': last_user_msg, 'response': response, 'feedback': feedback}
		else:
			# Must add embedding to pinecone + insert into database
			id = uuid.uuid4()
			self.datastore_table.insert({"id": str(id), "query": last_user_msg, "response": response, "feedback": feedback}).execute()
			embedded_obj = {"id": str(id), "values": embedding}
			self.vectorstore_index.upsert(vectors=[embedded_obj])

	def retrieve_feedback(self, message, threshold=0.8):
		# If there's no knowledge stored yet, return nothing
		if not self.feedback_kb and self.remote_feedback != True:
			return {}
		
		# Embed incoming message
		embedding = self.embed(message)

		result = ''
		# If storing locally, then use the local mapping.
		if self.remote_feedback != True:
			result = [self.vector_search(embedding, threshold)]
		# If need the remote, then query pinecone to determine matches.
		else:
			# Cannot get threshold-based via pinecone, will look into other vector DBs to accomodate this.
			# TODO: See other vector DBs to use threshold of similarity based querying
			matches = self.vectorstore_index.query(top_k=3, vector=list(embedding))
			matches = map(lambda x: x["id"], matches.matches)
			knowledge = self.datastore_table.select('*').in_('id', matches).execute()
			result = knowledge.data
		# Find most similar vector and return knowledge associated with most similar vector
		return result

	def vector_search(self, embedding, threshold):
		# Calculate cosine similarity between incoming embedding and vector store
		# Dot product of embedding against each embedding entry in vector store
		dots = embedding.dot(self.vectors.T)
		# Product of vector magnitudes
		norms = norm(self.vectors, axis=1) * norm(embedding)
		similarities = dots/norms
		if np.max(similarities) < threshold:
			return ""
		else:
			return self.feedback_kb[np.argmax(similarities)]

	def get_user_last_message(self, messages):
		last_user_msg = None
		for msg in reversed(messages):
			if msg['role'] == "user":
				last_user_msg = msg['content']
				break
		return last_user_msg

	def embed(self, text):
		response = self.openai_client.embeddings.create(
			input=text,
			model=self.embed_model_name
		)
		embedding = response.data[0].embedding
		return np.array(embedding)