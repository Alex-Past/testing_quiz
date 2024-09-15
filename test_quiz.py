import tkinter as tk
from tkinter import messagebox
import json

# Путь к файлу для хранения вопросов
QUESTIONS_FILE = "questions.json"

# Загрузка вопросов из файла
def load_questions():
    try:
        with open(QUESTIONS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Сохранение вопросов в файл
def save_questions(questions):
    with open(QUESTIONS_FILE, "w") as file:
        json.dump(questions, file, indent=4)

questions = load_questions()

# тесты
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование")
        self.root.geometry("500x500+700+300")

        self.current_question = 0
        self.score = 0
        
        # Создание интерфейса тестирования
        self.question_label = tk.Label(root, text="", wraplength=400)
        self.question_label.pack(pady=10)
        
        # Для хранения выбранного варианта
        self.options_var = tk.StringVar(value="")  
        
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=10)
        
        self.next_button = tk.Button(
            root,
            text="Следующий вопрос",
            command=self.check_answer
        )
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()
        
        self.start_button = tk.Button(
            root,
            text="Начать тестирование",
            command=self.start_testing
        )
        self.start_button.pack(pady=10)        
        
        self.add_question_button = tk.Button(
            root,
            text="Вопросы",
            command=self.open_add_question_window
        )
        self.add_question_button.pack(pady=100)        
    
    def load_question(self):
        if self.current_question >= len(questions):
            self.show_results()
            return
        
        question_data = questions[self.current_question]
        self.question_label.config(text=question_data["question"])
        
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        for option in question_data["options"]:
            tk.Radiobutton(
                self.options_frame,
                text=option,
                variable=self.options_var,
                value=option
            ).pack(anchor=tk.W)
        
        self.options_var.set(None)  # Сброс выбранного варианта
    
    def check_answer(self):
        selected_option = self.options_var.get()
        if selected_option == questions[self.current_question]["answer"]:
            self.score += 1
        
        self.current_question += 1
        self.load_question()
    
    def show_results(self):
        messagebox.showinfo(
            "Результаты",
            f"Вы ответили правильно на {self.score} "
            f"из {len(questions)} вопросов.")
        self.next_button.pack_forget()
        self.root.quit()
    
    def start_testing(self):
        if not questions:
            messagebox.showwarning(
                "Предупреждение",
                "Нет доступных вопросов для тестирования."
            )
            return
        self.current_question = 0
        self.score = 0
        self.load_question()
        self.next_button.pack(pady=10)
        self.start_button.pack_forget()
        self.add_question_button.pack_forget()
    
    def open_add_question_window(self):
        AddQuestionWindow(self.root)

# работа с вопросами
class AddQuestionWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Добавить или удалить вопрос")
        
        # Вопрос
        self.question_label = tk.Label(self.top, text="Вопрос:")
        self.question_label.pack(pady=5)
        self.question_entry = tk.Entry(self.top, width=50)
        self.question_entry.pack(pady=5)
        
        # Варианты ответов
        self.options_entries = []
        self.options_label = tk.Label(
            self.top,
            text="Варианты ответов (по одному в строке):"
        )
        self.options_label.pack(pady=5)
        
        for _ in range(4):
            entry = tk.Entry(self.top, width=50)
            entry.pack(pady=2)
            self.options_entries.append(entry)
        
        # Правильный ответ
        self.answer_label = tk.Label(self.top, text="Правильный ответ:")
        self.answer_label.pack(pady=5)
        self.answer_entry = tk.Entry(self.top, width=50)
        self.answer_entry.pack(pady=5)
        
        # Кнопка сохранения
        self.save_button = tk.Button(
            self.top,
            text="Сохранить",
            command=self.save_question
        )
        self.save_button.pack(pady=10)
        
        # Список вопросов
        self.questions_listbox = tk.Listbox(self.top, width=80, height=10)
        self.questions_listbox.pack(pady=10)
        self.update_questions_listbox()
        
        # Кнопка удаления вопроса
        self.delete_button = tk.Button(
            self.top,
            text="Удалить выбранный вопрос",
            command=self.delete_question
        )
        self.delete_button.pack(pady=10)
    
    def update_questions_listbox(self):
        self.questions_listbox.delete(0, tk.END)
        for i, q in enumerate(questions):
            self.questions_listbox.insert(tk.END, f"{i + 1}. {q['question']}")
    
    def save_question(self):
        question_text = self.question_entry.get()
        options = [
            entry.get() for entry in self.options_entries if entry.get()
        ]
        answer = self.answer_entry.get()
        
        if not question_text or len(options) < 2 or answer not in options:
            messagebox.showerror(
                "Ошибка",
                "Пожалуйста, заполните все поля корректно."
            )
            return
        
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
        
        save_questions(questions)
        self.update_questions_listbox()
        
        self.question_entry.delete(0, tk.END)
        for entry in self.options_entries:
            entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Вопрос добавлен успешно!")

    def delete_question(self):
        selected_index = self.questions_listbox.curselection()
        if not selected_index:
            messagebox.showwarning(
                "Предупреждение",
                "Пожалуйста, выберите вопрос для удаления."
            )
            return
        
        index = selected_index[0]
        del questions[index]
        save_questions(questions)
        self.update_questions_listbox()
        messagebox.showinfo("Успех", "Вопрос удален успешно!")

# Запуск приложения
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = QuizApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка при запуске программы: {e}")
