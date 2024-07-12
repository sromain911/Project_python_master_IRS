import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.username = None
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()  # Démarrer le thread de réception ici
    
    def connect(self):
        self.sock.sendto(b"Hello server", (self.host, self.port))
    
    def set_username(self, username):
        self.username = username
    
    def send_message(self, message):
        try:
            print(f"Sending message: {message}")  # Ajouter un print pour afficher le message envoyé
            self.sock.sendto(message.encode('utf-8'), (self.host, self.port))
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def receive_messages(self):
        while True:
            try:
                message, _ = self.sock.recvfrom(1024)
                message = message.decode('utf-8')
                if message:
                    self.message_received(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
    
    def message_received(self, message):
        chat_window.receive_message(message)
    
    def disconnect(self):
        self.sock.close()

class ChatWindow:
    def __init__(self, client, master):
        self.client = client
        self.master = master
        self.master.title("Chat")
        
        self.chat_history = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.chat_history.pack(padx=10, pady=10)
        
        self.message_entry = tk.Entry(self.master, width=50)
        self.message_entry.pack(padx=10, pady=10)
        
        send_button = tk.Button(self.master, text="Send", command=self.send_message)
        send_button.pack(padx=10, pady=10)
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.client.set_username(simpledialog.askstring("Username", "Enter your username:"))
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client.send_message(f"{self.client.username}: {message}\n")
            self.message_entry.delete(0, tk.END)
    
    def receive_message(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message)
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)
    
    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.client.disconnect()
            self.master.destroy()

def main():
    host = simpledialog.askstring("Server Address", "Enter server IP address:")
    port = 9999  # Adjust port number as needed
    
    client = ChatClient(host, port)
    client.connect()
    
    root = tk.Tk()
    chat_window = ChatWindow(client, root)
    root.mainloop()

if __name__ == "__main__":
    main()
