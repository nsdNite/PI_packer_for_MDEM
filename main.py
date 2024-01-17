# Python 3
# Production info packer for MDEM to be free from NUPAS macro
# This version 2.0 can pack any amount of sections
# dtat01, 2022

import os
import shutil

import tkfilebrowser
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk


# Функція для вибору директорії
def choose_dir():
    section_list_success.delete("0.0", END)
    section_list_fail.delete("0.0", END)
    dirs = list(tkfilebrowser.askopendirnames())
    print_s_list = []
    print_f_list = []
    for directory in dirs:
        print(directory)
        dir_path = directory
        check_pi_path = os.path.join(dir_path, "pi")
        check_cam_path = os.path.join(dir_path, "cam")
        check_cam = True
        check_pi = True
        if not os.path.exists(check_cam_path):
            check_cam = False
        if not os.path.exists(check_pi_path):
            check_pi = False
        if (check_pi, check_cam) == (False, False):
            fail_list.append(directory)
            print_f_list.append(os.path.basename(directory))
        else:
            success_list.append(directory)
            print_s_list.append(os.path.basename(directory))
    section_list_success.insert("0.0", ";".join(print_s_list))
    section_list_fail.insert("0.0", ";".join(print_f_list))
    return dirs


def start(dirs):
    if not dirs:
        messagebox.showwarning("Увага", "Ви не обрали секції.")
    else:
        result_packed.delete("0.0", END)
        result_drw.delete("0.0", END)
        for section in success_list:
            pack_pi(section)  # Що це?
        messagebox.showinfo("Шикарно!", "Процес завершено, дивіться результати.")

    # Створеняя директорій та піддерикторій продакшену у темпах.
    prj_no = prj_entry.get()  # читає ввод користувача в проект номер
    package_main_name = entry_option_1.get()
    temp_path = os.path.join("C:/temp/", f"{prj_no}_BATCH_PACK")
    if not os.path.exists(
            temp_path
    ):  # якщо такого шляху нема, то створюється директорія проекту
        os.mkdir(temp_path)
    # Створення папок у темп
    sec_name = os.path.basename(section)  # знаходимо номер секції
    prod_name = f"{prj_no}_{sec_name}_PROD_INFO"  # ім'я директорії пакета продакшену
    dwg_name = f"{prj_no}_{sec_name}_DRAWINGS"  # ім'я директорії креслень
    prod_dir = os.path.join(temp_path, prod_name)  # будуємо шлях для папки продакшену
    dwg_dir = os.path.join(temp_path, dwg_name)
    # шляхи до директорій всередені пакету:
    if package_main_name == "":
        package_main_name = "Complete_package"
    else:
        pass
    complete_p = os.path.join(prod_dir, f"{package_main_name}")
    plates_d = os.path.join(complete_p, "Plates/Cutting_data")
    profiles_d = os.path.join(complete_p, "Profiles/Single_profile_sketches")
    formed_d = os.path.join(complete_p, "Profiles/Formed_profiles_templates")
    reports_d = os.path.join(complete_p, "Reports")
    try:
        os.mkdir(prod_dir)
    except WindowsError:
        messagebox.showerror(
            "Помилка.",
            f"Знайдені застарілі пакети PI.\n"
            f"Будь ласка, видаліть старі результати пакування: "
            f"\n{temp_path}",
        )
    os.makedirs(complete_p)
    os.makedirs(plates_d)
    os.makedirs(profiles_d)
    os.mkdir(formed_d)
    os.makedirs(reports_d)
    cur_path = section
    prof_path = os.path.join(cur_path, "cam")
    plat_path = os.path.join(cur_path, "pi")
    print(plat_path, prof_path)
    for folder, subfolders, files in os.walk(plat_path):
        for file in files:
            path = os.path.join(folder, file)  # повний шлях до файлу
            if file.startswith("FP"):
                shutil.copy2(path, os.path.join(formed_d, file))
            elif file.endswith(".dxf"):
                shutil.copy2(path, os.path.join(plates_d, file))
            elif (
                    file.endswith(".list")
                    or file.endswith(".csv")
                    or file.endswith(".xlsx")
            ):
                shutil.copy2(path, os.path.join(reports_d, file))
            else:
                pass
    for folder, subfolders, files in os.walk(prof_path):
        for file in files:
            path = os.path.join(folder, file)
            if file.endswith(".pdf") or file.endswith(".dwg"):
                shutil.copy2(path, os.path.join(profiles_d, file))
    # репорти
    cog_report = os.path.join(reports_d, f"{prj_no}_{sec_name}_centre_of_gravity.csv")
    nestprof = os.path.join(reports_d, f"{prj_no}_{sec_name}_profile_nesting_list.txt")
    nestbar = os.path.join(reports_d, f"{prj_no}_{sec_name}_profile_bar_list.txt")
    partlist = os.path.join(reports_d, f"{prj_no}_{sec_name}_partlist.xlsx")
    weight_report = os.path.join(reports_d, f"{prj_no}_{sec_name}_block-weight.txt")
    bom_report = os.path.join(reports_d, f"{prj_no}_{sec_name}_BOM.csv")
    for folder, subfolders, files in os.walk(reports_d):
        for file in files:
            path = os.path.join(folder, file)
            if file.startswith("rep-cog"):
                os.rename(path, cog_report)
            elif file.startswith("nestprof"):
                os.rename(path, nestprof)
            elif file.startswith("nestbar"):
                os.rename(path, nestbar)
            elif file.endswith(".xlsx"):
                os.rename(path, partlist)
            elif file.startswith("rep-block"):
                os.rename(path, weight_report)
            elif file.startswith("rep-bom"):
                os.rename(path, bom_report)
            else:
                os.remove(path)
    # видаляємо пусті директорії
    check_empty_dir = [
        plates_d,
        profiles_d,
        formed_d,
        reports_d,
    ]
    for i in check_empty_dir:
        path = i
        if not os.listdir(path):
            os.rmdir(i)
    result_packed.insert(END, f"{sec_name}; ")
    # креслення
    cur_path = section
    temp_path_one = os.path.split(cur_path)[0]
    temp_path_two = os.path.split(temp_path_one)[0]
    drw_path = os.path.join(temp_path_two, "dxfout", prj_no, sec_name, "sheet")
    os.mkdir(dwg_dir)
    # Копіюємо креслення у директорію в темп
    for folder, subfolders, files in os.walk(drw_path):
        for file in files:
            path = os.path.join(folder, file)
            if file.endswith(".dwg") or file.endswith(".pdf") or file.endswith(".plt"):
                shutil.copy2(path, os.path.join(dwg_dir, file))
    if not os.listdir(dwg_dir):
        os.rmdir(dwg_dir)
    else:
        result_drw.insert(END, f"{sec_name}; ")


# Інтерфейс програми
root = ThemedTk()
root.geometry("500x450+500+300")
root.resizable(False, False)
root.title("Universal Production Packager v.2.0")
style = ttk.Style(root)
style.theme_use("clam")
# фрейми
frame_folder = ttk.Frame(root)
frame_folder.pack(pady=5, padx=10, fill=X)

frame_section_list = ttk.Frame(root)
frame_section_list.pack(pady=5, padx=10, fill=X)

frame_project = ttk.Frame(root)
frame_project.pack(pady=8, padx=10, fill=X)

frame_start = ttk.Frame(root)
frame_start.pack(pady=8, padx=10, fill=X)

frame_result_text = ttk.Frame(root)
frame_result_text.pack(pady=5, padx=10, fill=X)

results_label = ttk.Label(text="Результати пакування:", anchor=CENTER)
frame_result = ttk.LabelFrame(
    root, labelwidget=results_label, height=50, width=35, borderwidth=2, relief=RIDGE
)
frame_result.pack(pady=5, padx=10, fill=X)

options_label = ttk.Label(text="Налаштування (колись їх буде більше, обіцяю):")
frame_options = ttk.LabelFrame(
    root, labelwidget=options_label, height=50, width=35, borderwidth=2, relief=RIDGE
)
frame_options.pack(pady=5, padx=10, fill=X)

# кнопка вибору директорій
btn_dialog = ttk.Button(
    frame_folder, text="Вибрати директорії секцій", command=choose_dir
)
btn_dialog.pack(padx=0, fill=X)

# списки секцій з та без рі
section_list_s = ttk.Label(
    frame_section_list,
    text="Для наступних секцій буде спаковано PI та креслення (при наявності):",
)
section_list_s.pack(padx=5, fill=X)

section_list_success = Text(
    frame_section_list,
    height=3,
    width=35,
    padx=2,
    pady=0,
    wrap=WORD,
    relief=SOLID,
    borderwidth=1,
)
section_list_success.pack(fill=X)

section_list_f = ttk.Label(frame_section_list, text="У наступних секціях PI відсутній:")
section_list_f.pack(padx=5, fill=X)

section_list_fail = Text(
    frame_section_list,
    height=3,
    width=35,
    padx=2,
    pady=0,
    wrap=WORD,
    relief=SOLID,
    borderwidth=1,
)
section_list_fail.pack(fill=X)
# вказання проекту
prj_label = ttk.Label(frame_project, text="Вкажіть номер проекту:")
prj_label.pack(side=LEFT, padx=5)

prj_entry = Entry(frame_project, relief=SOLID, borderwidth=1)
prj_entry.pack(side=LEFT, expand=True, fill=X, ipady=3)
# кнопка старту
btn_start = ttk.Button(frame_start, text="Почати", command=start)
btn_start.pack(fill=X)

result_packed_label = ttk.Label(frame_result, text="PI спаковано для секцій:")
result_packed_label.configure(anchor=W, width=30)
result_packed_label.grid(row=0, column=0)

result_packed = Text(
    frame_result, height=2, width=35, padx=2, pady=0, relief=SOLID, borderwidth=1
)
result_packed.grid(row=0, column=1)

result_drw_label = ttk.Label(frame_result, text="DRW спаковано для секцій:")
result_drw_label.configure(anchor=W, width=30, padding=2)
result_drw_label.grid(row=1, column=0)

result_drw = Text(
    frame_result, height=2, width=35, padx=2, pady=0, relief=SOLID, borderwidth=1
)
result_drw.grid(row=1, column=1)

label_option_1 = ttk.Label(frame_options, text="Ім'я папки продакшену")
label_option_1.pack(side=LEFT, padx=5)

entry_option_1 = Entry(frame_options, relief=SOLID, borderwidth=1)
entry_option_1.insert(0, "Complete_package")
entry_option_1.pack(side=LEFT, expand=True, fill=X, ipady=3)

# задання фейл та успішних списків
fail_list = []
success_list = []
sec_dirs = []

root.mainloop()
