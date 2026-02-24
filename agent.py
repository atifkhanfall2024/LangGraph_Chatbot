from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph , START , END
from langchain_core.messages import AIMessage , HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from pathlib import Path

key = Path(__file__).resolve().parent / ".env"
if not  key:
    raise ValueError("key is not present")
print(key)
load_dotenv(key)

llm = init_chat_model(
    model="gemini-3-flash-preview",
    model_provider="google-genai"
)

# to create state => in state we keep some piece of data
class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]

# to define nodes     
def chatbot(state:MessagesState):
    print("Inside Chatbot" , state)
    response = llm.invoke(state.get("messages"))
    print(f"LLM Response => {response}" )
    return {"messages":[response]}

def agent(state:MessagesState):
    print("Inside agent Node" , state)
    return {"messages":[AIMessage(content="Hi there am your second node")]}


graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("agent" , agent)

# now added edges
graph_builder.add_edge(START , "chatbot")
graph_builder.add_edge("chatbot" , "agent")
graph_builder.add_edge("agent",END)



graph  = graph_builder.compile()


# this is the initial state
updated_state = graph.invoke(MessagesState({"messages":[HumanMessage(content="Hi there am Muhammad atif khan your developer")]}))

print( "Updated State ",updated_state)