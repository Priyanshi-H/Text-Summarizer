import tkinter as tk
from tkinter import filedialog, Text, messagebox
from tkinter.scrolledtext import ScrolledText

class TextSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarizer")

        self.file_path = tk.StringVar()

        # File selection frame
        file_frame = tk.Frame(root)
        file_frame.pack(pady=10)

        file_label = tk.Label(file_frame, text="Select a text file:")
        file_label.pack(side=tk.LEFT)

        file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.pack(side=tk.LEFT)

        browse_button = tk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.LEFT)

        summarize_button = tk.Button(root, text="Summarize", command=self.summarize)
        summarize_button.pack(pady=10)

        # Original and summary text frame
        text_frame = tk.Frame(root)
        text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Original text display
        original_text_frame = tk.Frame(text_frame)
        original_text_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        original_text_label = tk.Label(original_text_frame, text="Original Text:")
        original_text_label.pack()

        self.original_text = ScrolledText(original_text_frame, height=20, width=40)
        self.original_text.pack(fill=tk.BOTH, expand=True)

        # Summary text display
        summary_text_frame = tk.Frame(text_frame)
        summary_text_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        summary_text_label = tk.Label(summary_text_frame, text="Summary:")
        summary_text_label.pack()

        self.summary_text = ScrolledText(summary_text_frame, height=20, width=40)
        self.summary_text.pack(fill=tk.BOTH, expand=True)

        # Copy summary button
        copy_button = tk.Button(summary_text_frame, text="Copy Summary", command=self.copy_summary)
        copy_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.file_path.set(file_path)
        if file_path:
            with open(file_path, 'r') as file:
                original_text = file.read()
                self.original_text.delete('1.0', tk.END)
                self.original_text.insert(tk.END, original_text)

    def summarize(self):
        file_path = self.file_path.get()
        if file_path:
            from Text_summerizer import summarize_text_file
            result = summarize_text_file(file_path)
            self.summary_text.delete('1.0', tk.END)
            self.summary_text.insert(tk.END, result['summary'])
        else:
            messagebox.showwarning("No file selected", "Please select a text file to summarize.")

    def copy_summary(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.summary_text.get('1.0', tk.END).strip())
        messagebox.showinfo("Copied", "Summary text copied to clipboard.")

def main():
    root = tk.Tk()
    app = TextSummarizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
