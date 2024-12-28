import tkinter as tk
from tkinter import ttk, scrolledtext
from nhs_digital_agent import NHSDigitalAgent
import threading
from PIL import Image, ImageTk

class NHSDigitalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NHS Digital Dataset Search")
        self.root.geometry("800x600")
        self.agent = NHSDigitalAgent()
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('NHS.TFrame', background='#005EB8')  # NHS Blue
        self.style.configure('NHS.TLabel', background='#005EB8', foreground='white')
        self.style.configure('NHS.TButton', background='#005EB8', foreground='white')

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, style='NHS.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header with NHS Logo
        header_frame = ttk.Frame(main_frame, style='NHS.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Load and display NHS logo
        try:
            logo_img = Image.open("Query.png")  # Make sure to have this image in your project directory
            logo_img = logo_img.resize((100, 40), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=self.logo_photo, style='NHS.TLabel')
            logo_label.pack(side=tk.LEFT, padx=5)
        except Exception as e:
            # Fallback if image is not found
            logo_label = ttk.Label(header_frame, text="NHS Digital", 
                                 font=('Arial', 16, 'bold'), style='NHS.TLabel')
            logo_label.pack(side=tk.LEFT, padx=5)
            print(f"Error loading logo: {e}")

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=10)

        # Search bar
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                    font=('Arial', 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Search button
        self.search_button = ttk.Button(search_frame, text="Search", 
                                      command=self.start_search)
        self.search_button.pack(side=tk.LEFT)

        # Results area
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                    wrap=tk.WORD, 
                                                    font=('Arial', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                  relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))

        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.start_search())

    def start_search(self):
        # Disable search button and update status
        self.search_button.config(state='disabled')
        self.status_var.set("Searching...")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Searching...\n")
        
        # Start search in a separate thread
        thread = threading.Thread(target=self.perform_search)
        thread.daemon = True
        thread.start()

    def perform_search(self):
        query = self.search_var.get()
        try:
            # Perform search
            results = self.agent.search_datasets(query)
            
            # Update GUI in the main thread
            self.root.after(0, self.update_results, results)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def update_results(self, results):
        self.results_text.delete(1.0, tk.END)
        
        if not results:
            self.results_text.insert(tk.END, "No results found.\n")
        else:
            self.results_text.insert(tk.END, f"Found {len(results)} datasets:\n\n")
            for i, result in enumerate(results, 1):
                self.results_text.insert(tk.END, f"{i}. {result['title']}\n")
                self.results_text.insert(tk.END, f"URL: {result['url']}\n")
                self.results_text.insert(tk.END, f"Description: {result['description']}\n")
                self.results_text.insert(tk.END, "\n" + "-"*50 + "\n\n")

        self.search_button.config(state='normal')
        self.status_var.set("Ready")

    def show_error(self, error_message):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Error: {error_message}\n")
        self.search_button.config(state='normal')
        self.status_var.set("Error occurred")

def main():
    root = tk.Tk()
    app = NHSDigitalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# nhs_gui.py
# (Previous imports remain the same)

class NHSDigitalGUI:
    def __init__(self, root):
        # (Previous initialization code remains the same)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def perform_search(self):
        query = self.search_var.get()
        if not query.strip():
            self.root.after(0, self.show_error, "Please enter a search term")
            return

        try:
            print(f"Performing search for: {query}")  # Debug print
            results = self.agent.search_datasets(query)
            print(f"Search completed, found {len(results)} results")  # Debug print
            self.root.after(0, self.update_results, results)
        except Exception as e:
            print(f"Error during search: {str(e)}")  # Debug print
            self.root.after(0, self.show_error, str(e))

    def update_results(self, results):
        self.results_text.delete(1.0, tk.END)
        
        if not results:
            self.results_text.insert(tk.END, "No results found.\n")
        else:
            self.results_text.insert(tk.END, f"Found {len(results)} datasets:\n\n")
            for i, result in enumerate(results, 1):
                self.results_text.insert(tk.END, f"{i}. {result['title']}\n", "title")
                self.results_text.insert(tk.END, f"URL: {result['url']}\n", "url")
                self.results_text.insert(tk.END, f"Description: {result['description']}\n", "description")
                self.results_text.insert(tk.END, "\n" + "-"*50 + "\n\n")

        self.search_button.config(state='normal')
        self.status_var.set("Ready")

    def show_error(self, error_message):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Error: {error_message}\n", "error")
        self.search_button.config(state='normal')
        self.status_var.set("Error occurred")

    def on_closing(self):
        print("Application closing...")  # Debug print
        self.root.destroy()

    def create_widgets(self):
        # (Previous widget creation code remains the same)
        
        # Add text tags for formatting
        self.results_text.tag_configure("title", font=('Arial', 12, 'bold'))
        self.results_text.tag_configure("url", font=('Arial', 10, 'italic'))
        self.results_text.tag_configure("description", font=('Arial', 10))
        self.results_text.tag_configure("error", font=('Arial', 12, 'bold'), foreground='red')