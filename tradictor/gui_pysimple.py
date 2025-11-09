import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# === FUNCIONES DE TRADUCCIÓN SIMPLIFICADAS ===
def translate_java_to_js(code):
    code = code.replace("System.out.println", "console.log")
    code = code.replace("public class", "// Clase convertida desde Java\nclass")
    code = code.replace("public static void main(String[] args)", "function main()")
    return code

def translate_java_to_cpp(code):
    code = code.replace("System.out.println", "cout <<")
    code = code.replace("public class", "// Clase convertida desde Java\nclass")
    code = code.replace("public static void main(String[] args)", "int main()")
    return '#include <iostream>\nusing namespace std;\n\n' + code


# === FUNCIÓN PRINCIPAL ===
def translate():
    src = text_input.get("1.0", tk.END)
    if not src.strip():
        messagebox.showwarning("Advertencia", "Por favor pega código Java para traducir.")
        return
    tgt = target_var.get()
    if tgt == "JavaScript":
        out = translate_java_to_js(src)
    else:
        out = translate_java_to_cpp(src)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, out)

def clear_text():
    text_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)

def save_output():
    output = text_output.get("1.0", tk.END)
    if not output.strip():
        messagebox.showwarning("Advertencia", "No hay texto para guardar.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output)
        messagebox.showinfo("Guardado", "Archivo guardado correctamente.")


# === INTERFAZ ===
root = tk.Tk()
root.title("Traductor de Código Java → JavaScript / C++")
root.geometry("800x700")
root.configure(bg="#e8f0fe")

tk.Label(root, text="Traductor de Código", font=("Helvetica", 18, "bold"), bg="#e8f0fe").pack(pady=10)
tk.Label(root, text="Pega tu código Java:", bg="#e8f0fe").pack()

text_input = scrolledtext.ScrolledText(root, width=90, height=15, wrap=tk.WORD, font=("Consolas", 10))
text_input.pack(padx=10, pady=5)

frame = tk.Frame(root, bg="#e8f0fe")
frame.pack(pady=5)

tk.Label(frame, text="Lenguaje destino:", bg="#e8f0fe").pack(side=tk.LEFT)
target_var = tk.StringVar(value="JavaScript")
tk.OptionMenu(frame, target_var, "JavaScript", "C++").pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Traducir", command=translate, bg="#007ACC", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Limpiar", command=clear_text, bg="#d9534f", fg="white", width=12).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Salida traducida:", bg="#e8f0fe").pack(pady=5)
text_output = scrolledtext.ScrolledText(root, width=90, height=15, wrap=tk.WORD, font=("Consolas", 10))
text_output.pack(padx=10, pady=5)

tk.Button(root, text="Guardar salida", command=save_output, bg="#5cb85c", fg="white", width=15).pack(pady=10)

root.mainloop()
