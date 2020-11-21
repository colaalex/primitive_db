"""
Модуль, содержащий функции для вывода информации на экран через графический
интерфейс
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import shelve as shl
from Scripts import config as cfg
from Library import parsers
from Library import base_work


class MainWindow(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        root.configure(background=cfg.primary_color)

        if root.winfo_screenheight() < 900:
            cfg.text_font = cfg.text_font.replace('15', '12')
            cfg.button_font = cfg.button_font.replace('15', '12')

        self.bd = self.open_bd()
        self.base = base_work.local_copy(self.bd)

        self.img = tk.PhotoImage(file=cfg.img_magnify)
        self.img1 = tk.PhotoImage(file=cfg.img_pencil)
        self.img2 = tk.PhotoImage(file=cfg.img_close)
        self.img3 = tk.PhotoImage(file=cfg.img_info)
        self.img4 = tk.PhotoImage(file=cfg.img_file)
        self.img5 = tk.PhotoImage(file=cfg.img_del)

        self.set_upper_frame(root).pack(anchor='n')
        self.tree = self.set_tree(root)
        self.tree.pack()
        self.update_tree(self.tree)

    def open_bd(self):
        """
        Входные данные: данный метод вызывается из конструктора класса, входных параметров нет
        Выходные данные: объект базы данных.
        Данный метод пытается открыть файл с базой данных. В случае, если файл не удалось открыть, пользователю
        предлагается выбрать файл с жесткого диска.
        """
        try:
            open(cfg.bd_path, 'rb')
        except FileNotFoundError:
            fn = filedialog.Open(root, filetypes=[('*.dat files', 'shl.dat')]).show()
            if fn != '':
                base = shl.open(fn.remove('.dat'))
                return base
        finally:
            return shl.open(cfg.bd_path_2)

    def set_tree(self, root):
        """
        Входные данные: родительский объект root, на котором будет находиться Treeview
        Выходные параметры: объект типа Treeview.
        Данный метод создает объект типа Treeview для вывода полей базы данных на экран
        """
        tree = ttk.Treeview(root, show='headings')
        tree['columns'] = ('Country', 'Population', 'Area', 'Capital', 'Language', 'Currency')

        tree.column('Country', width=cfg.tree_width)
        tree.column('Population', width=cfg.tree_width)
        tree.column('Area', width=cfg.tree_width)
        tree.column('Capital', width=cfg.tree_width)
        tree.column('Language', width=cfg.tree_width)
        tree.column('Currency', width=cfg.tree_width)

        tree.heading('Country', text='Country')
        tree.heading('Population', text='Population')
        tree.heading('Area', text='Area')
        tree.heading('Capital', text='Capital')
        tree.heading('Language', text='Language')
        tree.heading('Currency', text='Currency')

        tree.bind('<Double-Button-1>', lambda event: self.open_editor(False, tree))

        return tree

    def set_upper_frame(self, root):
        """
        Входные данные: родительский элемент root
        Выходные данные: объект Frame с кнопками управления БД
        Создает Frame с кнопками управления БД (поиск, удаление, запись)
        """
        frame = tk.Frame(root, background=cfg.primary_color)

        search = tk.Button(frame, text='Поиск', background=cfg.accent_color, foreground=cfg.button_fore,
                           font=cfg.button_font, relief=cfg.button_relief, command=self.open_search)
        search.grid(row=1, column=1, sticky='W')
        search.config(image=self.img, compound='left')
        search.bind('<Enter>', lambda event: self.over_button(search))
        search.bind('<Leave>', lambda event: self.leave_button(search))

        add = tk.Button(frame, text='Добавить запись', background=cfg.accent_color, foreground=cfg.button_fore,
                        font=cfg.button_font, relief=cfg.button_relief, command=lambda: self.open_editor(True, self.tree))
        add.grid(row=1, column=2, padx=2)
        add.config(image=self.img1, compound='left')
        add.bind('<Enter>', lambda event: self.over_button(add))
        add.bind('<Leave>', lambda event: self.leave_button(add))

        del_button = tk.Button(frame, text='Удалить запись', background=cfg.accent_color,
                               font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief,
                               command=lambda: self.delete(self.tree, self.tree.selection()))
        del_button.config(image=self.img5, compound='left')
        del_button.bind('<Enter>', lambda event: self.over_button(del_button))
        del_button.bind('<Leave>', lambda event: self.leave_button(del_button))
        del_button.grid(row=1, column=3)

        save_button = tk.Button(frame, text='Сохранить изменения', background=cfg.accent_color,
                                font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief,
                                command=lambda: base_work.save_copy(self.base, self.bd))
        save_button.config(image=self.img4, compound='left')
        save_button.bind('<Enter>', lambda event: self.over_button(save_button))
        save_button.bind('<Leave>', lambda event: self.leave_button(save_button))
        save_button.grid(row=1, column=4, padx=2, sticky='e')

        return frame

    def over_button(self, button):
        """
        Входные данные: объект кнопки
        Выходные данные: нет
        Меняет рельеф кнопки при наведении мыши
        """
        button.configure(relief='groove')

    def leave_button(self, button):
        """
        Входные данные: объект кнопки
        Выходные данные: нет
        Меняет рельеф кнопки после того как мышь убрана с кнопки
        """
        button.configure(relief=cfg.button_relief)

    def open_search(self):
        """
        Входные данные: нет
        Выходные данные: нет
        Данный метод открывает дочернее окно с формой поиска
        """
        top = tk.Toplevel()
        top.resizable(False, False)
        frame = tk.Frame(top, background=cfg.primary_color)
        frame.pack(fill='x')
        tk.Label(frame, text='Поиск', foreground=cfg.button_fore,
                 background=cfg.primary_color, padx=10, font=cfg.text_font).pack(side='left', fill='x')

        b = tk.Button(frame, command=top.destroy, text='Закрыть', background=cfg.accent_color,
                      font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief)
        b.config(image=self.img2, compound='left')
        b.bind('<Enter>', lambda event: self.over_button(b))
        b.bind('<Leave>', lambda event: self.leave_button(b))
        b.pack(side='right')

        frame1 = tk.LabelFrame(top, text='Критерии поиска')
        frame1.pack()

        label = tk.Label(frame1, text=cfg.text1, font=cfg.text_font, foreground=cfg.secondary_text, wraplength=500)
        label.config(image=self.img3, compound='left')
        label.grid(row=1, columnspan=3)
        count_label = tk.Label(frame1, text='Country', font=cfg.text_font, foreground=cfg.primary_text)
        count_entry = tk.Entry(frame1, width=70)
        count_label.grid(row=2, column=1, sticky='w')
        count_entry.grid(row=2, column=2, padx=10)

        popul_label = tk.Label(frame1, text='Population', font=cfg.text_font, foreground=cfg.primary_text)
        popul_label.grid(row=3, column=1, sticky='w')
        # настройка выпадающего меню
        tkvar = tk.StringVar(top)
        choices = {'=', '>=', '>', '<=', '<', 'Интервал'}
        tkvar.set('=')
        popup_menu = tk.OptionMenu(frame1, tkvar, *choices)
        popup_menu.grid(row=3, column=3, sticky='w')
        popul_entry = tk.Entry(frame1, width=70)
        popul_entry.grid(row=3, column=2)

        area_label = tk.Label(frame1, text='Area', font=cfg.text_font, foreground=cfg.primary_text)
        area_tkvar = tk.StringVar(top)
        area_tkvar.set('=')
        area_label.grid(row=4, column=1, sticky='w')
        area_entry = tk.Entry(frame1, width=70)
        area_entry.grid(row=4, column=2)
        area_popup = tk.OptionMenu(frame1, area_tkvar, *choices)
        area_popup.grid(row=4, column=3, sticky='w')

        capital_label = tk.Label(frame1, text='Capital', font=cfg.text_font, foreground=cfg.primary_text)
        capital_label.grid(row=5, column=1, sticky='w')
        capital_entry = tk.Entry(frame1, width=70)
        capital_entry.grid(row=5, column=2)

        lang_label = tk.Label(frame1, text='Language', font=cfg.text_font, foreground=cfg.primary_text)
        lang_label.grid(row=6, column=1, sticky='w')
        lang_entry = tk.Entry(frame1, width=70)
        lang_entry.grid(row=6, column=2)

        cur_label = tk.Label(frame1, text='Currency', font=cfg.text_font, foreground=cfg.primary_text)
        cur_label.grid(row=7, column=1, sticky='w')
        cur_entry = tk.Entry(frame1, width=70)
        cur_entry.grid(row=7, column=2)
        tree = self.set_tree(top)
        tree.configure(height=5)
        tree.bind('<Double-Button-1>', lambda event: self.open_editor(False, tree))
        search_button = tk.Button(frame1, text='Поиск', background=cfg.accent_color,
                                  font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief,
                                  command=lambda: self.search([count_entry.get(), (popul_entry, tkvar.get()),
                                                               (area_entry, area_tkvar), capital_entry.get(),
                                                               lang_entry.get(), cur_entry.get()], tree))
        search_button.config(image=self.img, compound='left')
        search_button.bind('<Enter>', lambda event: self.over_button(search_button))
        search_button.bind('<Leave>', lambda event: self.leave_button(search_button))
        search_button.grid(row=8, column=2, pady=5)

        label1 = tk.Label(top, text='Результаты поиска', font=cfg.button_font, foreground=cfg.primary_text)
        label1.pack()

        tree.pack()

        button_frame = tk.Frame(top)
        button_frame.pack(pady=5)

        save_button = tk.Button(button_frame, text='Сохранить результаты в файл', background=cfg.accent_color,
                                font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief,
                                command=lambda: self.report(tree))
        save_button.config(image=self.img4, compound='left')
        save_button.bind('<Enter>', lambda event: self.over_button(save_button))
        save_button.bind('<Leave>', lambda event: self.leave_button(save_button))
        save_button.grid(row=1, column=1)

        del_button = tk.Button(button_frame, text='Удалить выделенную запись', background=cfg.accent_color,
                               font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief,
                               command=lambda: self.delete(tree, tree.selection()))
        del_button.config(image=self.img5, compound='left')
        del_button.bind('<Enter>', lambda event: self.over_button(del_button))
        del_button.bind('<Leave>', lambda event: self.leave_button(del_button))
        del_button.grid(row=1, column=2, padx=5)

    def open_editor(self, create: bool, tree):
        """
        Входные данные: булева переменная create - запись создается с нуля или редактируется, tree  -объект типа TreeView
        Выходные данные: нет
        Открывает окно редактирования или создания записи, после нажатия на кнопку добавления, обновляет TreeView
        """
        editor = tk.Toplevel()
        editor.resizable(False, False)
        if not create and len(tree.selection()) > 0:
            prev_key = tree.item(tree.selection()[0])['values'][0]
        else:
            prev_key = None

        frame = tk.Frame(editor, background=cfg.primary_color)
        frame.pack(fill='x')
        tk.Label(frame, text='Редактор записи', foreground=cfg.button_fore,
                 background=cfg.primary_color, padx=10, font=cfg.button_font).pack(side='left', fill='x')

        b = tk.Button(frame, command=editor.destroy, text='Закрыть', background=cfg.accent_color,
                      font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief)
        b.config(image=self.img2, compound='left')
        b.bind('<Enter>', lambda event: self.over_button(b))
        b.bind('<Leave>', lambda event: self.leave_button(b))
        b.pack(side='right')

        field_frame = tk.Frame(editor)
        field_frame.pack(pady=10)

        tk.Label(field_frame, text='Country', font=cfg.button_font, foreground=cfg.primary_text)\
            .grid(row=1, column=1, sticky='w')
        count_entry = tk.Entry(field_frame, width=50)
        count_entry.grid(row=1, column=2, padx=7)

        tk.Label(field_frame, text='Population', font=cfg.button_font, foreground=cfg.primary_text)\
            .grid(row=2, column=1, sticky='w')
        popul_entry = tk.Entry(field_frame, width=50)
        popul_entry.grid(row=2, column=2, padx=7)

        tk.Label(field_frame, text='Area', font=cfg.button_font, foreground=cfg.primary_text) \
            .grid(row=3, column=1, sticky='w')
        area_entry = tk.Entry(field_frame, width=50)
        area_entry.grid(row=3, column=2, padx=7)

        tk.Label(field_frame, text='Capital', font=cfg.button_font, foreground=cfg.primary_text) \
            .grid(row=4, column=1, sticky='w')
        capital_entry = tk.Entry(field_frame, width=50)
        capital_entry.grid(row=4, column=2, padx=7)

        tk.Label(field_frame, text='Language', font=cfg.button_font, foreground=cfg.primary_text) \
            .grid(row=5, column=1, sticky='w')
        lang_entry = tk.Entry(field_frame, width=50)
        lang_entry.grid(row=5, column=2, padx=7)

        tk.Label(field_frame, text='Currency', font=cfg.button_font, foreground=cfg.primary_text) \
            .grid(row=6, column=1, sticky='w')
        cur_entry = tk.Entry(field_frame, width=50)
        cur_entry.grid(row=6, column=2, padx=7)

        add = tk.Button(editor, text='Добавить запись', background=cfg.accent_color,
                        font=cfg.button_font, foreground=cfg.button_fore, relief=cfg.button_relief,
                        command=lambda: self.edit_record(create, [count_entry, popul_entry, area_entry,
                                                                  capital_entry, lang_entry, cur_entry], tree, prev_key))
        add.config(image=self.img4, compound='left')
        add.bind('<Enter>', lambda event: self.over_button(add))
        add.bind('<Leave>', lambda event: self.leave_button(add))
        add.pack()

        if not create:
            count_entry.insert(0, prev_key)
            popul_entry.insert(0, self.base[prev_key]['Population'])
            area_entry.insert(0, self.base[prev_key]['Area'])
            capital_entry.insert(0, self.base[prev_key]['Capital'])
            lang_entry.insert(0, self.base[prev_key]['Language'])
            cur_entry.insert(0, self.base[prev_key]['Currency'])

    def edit_record(self, create, widgets, tree, prev_key=None):
        """
        Входные данные: булевая переменная create - запись создается или редактируется; список виджетов типа Entry;
        объект TreeView; prev_key - ключ предыдущей версии записи (если есть)
        Выходные данные: нет
        Проверяет значения текстовых полей на допустимые значения. Если все подходит по условию, происходит обновление
        базы данных и объектов TreeView
        """
        keep_updating = True
        for i in range(6):
            if widgets[i].get() == '' or (i in [1, 2] and not parsers.validate_singlenum_entry(widgets[i].get())):
                widgets[i].configure(background=cfg.color_red)
                keep_updating = False
        if keep_updating:
            keys = []
            for i in tree.get_children():
                keys.append(tree.item(i)['values'][0])
            key = widgets[0].get()
            if not create:
                self.base.pop(prev_key)
                keys.remove(prev_key)
                keys.append(key)
            self.base[key] = {'Population': widgets[1].get(), 'Area': widgets[2].get(), 'Capital': widgets[3].get(),
                              'Language': widgets[4].get(), 'Currency': widgets[5].get()}
            self.update_tree(tree, keys)
            self.update_tree(self.tree)
            for i in range(6):
                widgets[i].delete(0, tk.END)

    def report(self, tree):
        """
        Входные данные: объект TreeView
        Выходные данные: нет
        Составляет список ключей для функции base_work.total, вызывает ее и сохраняет файл в выбранную пользователем
        папку
        """
        keys = []
        for c in tree.get_children():
            keys.append(tree.item(c)['values'][0])
        text = base_work.total(keys, self.base)
        fn = filedialog.asksaveasfilename(initialdir=cfg.output_dir, filetypes=(('Текстовый файл', '*.txt'),))
        if fn == '':
            return
        with open(fn+'.txt', 'w') as f:
            f.write(text)

    def delete(self, tree, items):
        """
        Входные данные: объект TreeView для получения необходимых к удалению записей, а также его обновления; список
        выделенных элементов, подлежащих удалению
        Выходные данные: нет
        Метод удаляет из локальной копии БД выделенные элементы и обновляет объект TreeView
        """
        print(items)
        for i in items:
            key = tree.item(i)['values'][0]
            self.base.pop(key)
        self.update_tree(tree)  # обновление tree на экране поиска
        self.update_tree(self.tree)  # обновление tree на основном экране

    def search(self, widgets, tree):
        """
        Входные данные: список объектов типа Entry и значений выбора OptionMenu для проверки данных. Если поле содержит
        недопустимое значение, его цвет меняетмя на красный; объект TreeView, на котором будут размещены рез-ты поиска
        Выходные данные: нет
        Вызывает функции для проверки введенных значений, поиска и обновление TreeView с учетом результатов поиска
        """
        keep_search = True  # если значение флага станет False, прекратить поиск
        if widgets[1][1] == 'Интервал':
            if not parsers.validate_interval_entry(widgets[1][0].get()):
                keep_search = False
                widgets[1][0].configure(background=cfg.color_red)
        else:
            if not parsers.validate_singlenum_entry(widgets[1][0].get()):
                keep_search = False
                widgets[1][0].configure(background=cfg.color_red)
        if widgets[2][1] == 'Интервал':
            if not parsers.validate_interval_entry(widgets[2][0].get()):
                keep_search = False
                widgets[2][0].configure(background=cfg.color_red)
        else:
            if not parsers.validate_singlenum_entry(widgets[2][0].get()):
                keep_search = False
                widgets[2][0].configure(background=cfg.color_red)
        print(keep_search)
        if keep_search:
            print(widgets)
            keys = base_work.search(widgets, self.base)
            self.update_tree(tree, keys)

    def update_tree(self, tree, keys=None):
        """
        Входные данные: объект TreeView, который необходимо обновить; список ключей в порядке, необходимом для вывода
        (необязательный параметр), если не задан, будут взяты ключи из основной базы данных
        Выходные данные: происходит обновления поля класса, метод ничего не возвращает
        Метод использует базу данных и на ее основе формирует содержимое объекта tree
        """
        tree.delete(*tree.get_children())
        b = self.base
        if keys is None:
            keys = b.keys()
        for c in keys:
            tree.insert('', 0, values=(c, b[c]['Population'], b[c]['Area'],
                                       b[c]['Capital'], b[c]['Language'], b[c]['Currency']))


if __name__ == '__main__':
    root = tk.Tk()
    main = MainWindow(root)
    main.pack()
    root.resizable(False, False)
    icon = tk.PhotoImage(file=cfg.favicon)
    root.tk.call('wm', 'iconphoto', root._w, icon)
    root.title('Country Browser')
    root.mainloop()
