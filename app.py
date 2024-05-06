import os 
import chainlit as cl

from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from langchain.chains import LLMChain

from langchain.memory.buffer import ConversationBufferMemory

from langchain.prompts import PromptTemplate


text_to_sql_template = """
You are an SQL assistant chatbot named "Namaste SQL". Your expertise is 
exclusively in providing queries of SQL which user has asked.
This includes any sql queries related to creation,deletion or updation of tables or databases. 
You do not provide information outside of this scope.
If a question is not about SQL queries respond with, "I specialize 
only in SQL queries."
Chat History: {chat_history}
Question: {question}
Answer:"""


load_dotenv()
gemini_key=os.getenv('gemini_token')
os.environ['GOOGLE_API_KEY']=gemini_key 
conversation_memory=ConversationBufferMemory(memory_key="chat_history",max_len=50,return_messages=True,)
llm_google=GoogleGenerativeAI(model="models/gemini-pro",)
sql_query_prompt_template= PromptTemplate(input_variables=["chat_history", "question"],template=text_to_sql_template)

def ask_bot(user_message):

    print(user_message)

    text =user_message

    result=llm_google.invoke(text)



    return result




@cl.on_chat_start
def quey_llm():
    
    llm_chain = LLMChain(llm=llm_google, 
                         prompt=sql_query_prompt_template,
                         memory=conversation_memory)
    
    cl.user_session.set("llm_chain", llm_chain)



@cl.on_message
async def query_llm(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")
    
    response = await llm_chain.acall(message.content, 
                                     callbacks=[
                                         cl.AsyncLangchainCallbackHandler()])
    
    await cl.Message(response["text"]).send()



'''@cl.on_message
async def main(user_message: cl.Message):
    
    # Your custom logic goes here...
    result=ask_bot(user_message.content)
    # Send a response back to the user
    await cl.Message(
        content=f"Received: {result}",
    ).send()'''


     

    
    

    



'''if __name__=='main':
    text='Join a customer table with a transaction table on customer _id and find the average of transactions per customer'

    print(llm_google.invoke(text))'''





