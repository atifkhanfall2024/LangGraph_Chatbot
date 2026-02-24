# here we are talking about condition edges
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional , Literal
from langgraph.graph import StateGraph , START , END
from openai import OpenAI
import os


load_dotenv()

#print(os.getenv("GOOGLE_API_KEY"))
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
# define state
user_input=input("Enter Input : " )
class State(TypedDict):
    User_Query:str
    llm_response:Optional[str]

 
# first we give user input to llm which give respnse

def Chatbot(state:State):
    print("Inside Chatbot 🤖" , state.get("User_Query"))
    response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        messages=[
            {"role":"user" , "content":state.get("User_Query")}
        ]
    )
    print(response.choices[0].message.content)
    state["llm_response"] =  response.choices[0].message.content
    return state


def Evaulations(state:State)-> Literal["Again_Gemini" , "EndNode"]:
    if True:
        return "EndNode"
    
    return "Again_Gemini"

def Again_Gemini(state:State):
    print("Inside Again Chatbot 🤖" , state.get("User_Query"))
    response = client.chat.completions.create(
        model='gemini-3-flash-preview',
        messages=[
            {"role":"user" , "content":state.get("User_Query")}
        ]
    )
    print("Second Response => " , response.choices[0].message.content)
    state["llm_response"] =  response.choices[0].message.content
    return state

def EndNode(state:State):
     return state

graph_builder = StateGraph(State)
graph_builder.add_node("Chatbot",Chatbot)
graph_builder.add_node("Again_Gemini" , Again_Gemini)

graph_builder.add_node("EndNode" , EndNode)


graph_builder.add_edge(START , "Chatbot")
graph_builder.add_conditional_edges("Chatbot" ,Evaulations )
graph_builder.add_edge("Again_Gemini" , "EndNode")
graph_builder.add_edge("EndNode" , END)

graph = graph_builder.compile()

updated_graph = graph.invoke(State({"User_Query":user_input}))
print("Updated Graph => " , updated_graph)