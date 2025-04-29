from chatbot import ChatBot, SessionState
from utils.db_helpers import update_DB_Schema
import gradio as gr


def create_gradio_interface():
    def predict(message, history, state):
        if state is None:
            state = {"chatbot": ChatBot(SessionState())}
            state["chatbot"]._setup_context()
        
        # Add the user message to history immediately
        history = history + [[message, ""]]
        
        chatbot = state["chatbot"]
        response_generator = chatbot.process_user_input(message)
        
        response = ""
        for char in response_generator:
            response += char
            history[-1][1] = response
            yield history, state
    
    with gr.Blocks() as chat:
        gr.Markdown("# E-commerce Database Assistant")
        gr.Markdown("Ask questions about the database schema or get insights from your data.")
        
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="Ask about your e-commerce database...")
        state = gr.State(None)
        
        msg.submit(
            predict,
            [msg, chatbot, state],
            [chatbot, state]
        ).then(
            lambda: "",  # This clears the textbox after sending
            None,
            [msg]
        )
        
    return chat

if __name__ == "__main__":
    update_DB_Schema()
    chat = create_gradio_interface()
    chat.queue().launch()