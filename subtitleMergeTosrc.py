import re
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime

"""
    合并字幕方法
"""


def is_chinese(text):
    """判断文本是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fa5]', text))


def is_english(text):
    """判断文本是否包含英文"""
    return bool(re.search(r'[a-zA-Z]', text))


def has_punctuation(text):
    """判断文本末尾是否有标点符号"""
    return bool(re.search(r'[.!?]$', text))


def merge_english_lines(lines, processed_lines):
    i = 0

    while i < len(lines):
        # 去除换行符
        line = lines[i]

        # 如果行不为空，则判断是否包含英文
        if line.strip():
            # 如果下一行不为空，则判断是否包含英文
            if i + 1 < len(lines):
                # 取得下一行
                next_line = lines[i + 1]

                # 判断两行是否都包含英文
                if is_english(line.strip()) and is_english(next_line.strip()):
                    # 如果line末尾没有标点符号，则在合并时添加空格
                    if not has_punctuation(line.strip()):
                        merged_line = line.strip() + " " + next_line.strip() + "\n"
                    else:
                        merged_line = line.strip() + next_line.strip() + "\n"
                    processed_lines.append(merged_line)
                    i += 2  # 跳过下一行
                else:
                    processed_lines.append(line)
                    i += 1
            else:
                processed_lines.append(line)
                i += 1
        else:
            processed_lines.append(line)
            i += 1


def merge_chinese_lines(lines, processed_lines):
    i = 0

    while i < len(lines):
        # 去除换行符
        line = lines[i]

        # 如果行不为空，则判断是否包含中文
        if line.strip():
            # 如果下一行不为空，则判断是否包含中文
            if i + 1 < len(lines):
                # 取得下一行
                next_line = lines[i + 1]

                # 判断两行是否都包含中文
                if is_chinese(line.strip()) and is_chinese(next_line.strip()):
                    # 保留原始换行符，并在 next_line 前添加空格
                    merged_line = line.strip() + " " + next_line.strip() + "\n"
                    processed_lines.append(merged_line)
                    i += 2  # 跳过下一行
                else:
                    processed_lines.append(line)
                    i += 1
            else:
                processed_lines.append(line)
                i += 1
        else:
            processed_lines.append(line)
            i += 1


def merge_lines(input_file, processed_lines, lang_func):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if lang_func == is_english:
        merge_english_lines(lines, processed_lines)
    elif lang_func == is_chinese:
        merge_chinese_lines(lines, processed_lines)


def browse_input_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)


def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)


def is_empty_line(line):
    return line.strip() == ''


def merge_subtitles(processed_english_lines, processed_chinese_lines, output_file):
    processed_lines = []
    i = 0
    j = 0

    while i < len(processed_english_lines) and j < len(processed_chinese_lines):
        if is_empty_line(processed_english_lines[i]) and is_empty_line(processed_chinese_lines[j]):
            processed_lines.append(processed_english_lines[i].strip())
            i += 1
            j += 1
            continue
        # 处理字幕编号
        english_subtitle_number = processed_english_lines[i].strip()
        chinese_subtitle_number = processed_chinese_lines[j].strip()

        if english_subtitle_number == chinese_subtitle_number:
            processed_lines.append(english_subtitle_number)
            i += 1
            j += 1

            # 处理时间戳
            if i < len(processed_english_lines) and j < len(processed_chinese_lines):
                english_timestamp = processed_english_lines[i].strip()

                processed_lines.append(english_timestamp)
                i += 1
                j += 1

                # 处理英文行
                if i < len(processed_english_lines):
                    english_line = processed_english_lines[i].strip()
                    i += 1

                    # 处理中文行
                    if j < len(processed_chinese_lines):
                        chinese_line = processed_chinese_lines[j].strip()
                        j += 1

                        # 合并中英文行
                        merged_line = f"{english_line}\n{chinese_line}"
                        processed_lines.append(merged_line)
                    else:
                        processed_lines.append(english_line)
                else:
                    processed_lines.append(english_timestamp)
        else:
            i += 1
            j += 1

    # Write the processed subtitles back to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines) + '\n')


def create_date_folder(base_folder):
    """创建以当前日期命名的文件夹"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_folder = os.path.join(base_folder, current_date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)
    return date_folder


def process_files():
    # 获取指定位置目录
    base_folder = filedialog.askdirectory(title="选择指定位置目录")
    if not base_folder:
        messagebox.showerror("错误", "请选择指定位置目录")
        return

    # 创建以当前日期命名的文件夹
    date_folder = create_date_folder(base_folder)

    # 从输入框中获取文件路径和输出文件路径
    input_english_file = input_english_entry.get()
    input_chinese_file = input_chinese_entry.get()
    output_file = output_entry.get()

    if not input_english_file or not input_chinese_file:
        messagebox.showerror("错误", "请输入文件路径")
        return

    if not output_file:
        messagebox.showerror("错误", "请选择输出文件")
        return

    try:
        # 确保输入文件存在于日期文件夹中
        input_english_filename = os.path.basename(input_english_file)
        input_chinese_filename = os.path.basename(input_chinese_file)

        input_english_file_path = os.path.join(date_folder, input_english_filename)
        input_chinese_file_path = os.path.join(date_folder, input_chinese_filename)

        # 复制输入文件到日期文件夹中
        if not os.path.exists(input_english_file_path):
            os.makedirs(os.path.dirname(input_english_file_path), exist_ok=True)
            os.replace(input_english_file, input_english_file_path)
        if not os.path.exists(input_chinese_file_path):
            os.makedirs(os.path.dirname(input_chinese_file_path), exist_ok=True)
            os.replace(input_chinese_file, input_chinese_file_path)

        # 更新输出文件路径为日期文件夹中的路径
        output_file_path = os.path.join(date_folder, os.path.basename(output_file))

        processed_english_lines = []
        processed_chinese_lines = []

        # 处理文件删除中文之间的换行符
        merge_lines(input_english_file_path, processed_english_lines, is_english)
        merge_lines(input_chinese_file_path, processed_chinese_lines, is_chinese)
        # 处理文件合并双语字幕
        merge_subtitles(processed_english_lines, processed_chinese_lines, output_file_path)
        messagebox.showinfo("成功", f"文件已处理并保存在：{output_file_path}")
    except Exception as e:
        messagebox.showerror("错误", f"处理过程中出现错误：{str(e)}")


def main():
    # Create the main window
    global root, input_chinese_entry, input_english_entry, output_entry

    root = tk.Tk()
    root.title("双语字幕混合")

    # Set window size
    root.geometry("500x230")

    # Create and place widgets
    input_english_label = tk.Label(root, text="选择输入英文字幕：")
    input_english_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    # 使用 Entry 小部件创建输入框
    input_english_entry = tk.Entry(root, width=40)
    # 使用 grid 布局管理器将 Entry 小部件放置在窗口中的特定位置。
    input_english_entry.grid(row=0, column=1, padx=10, pady=10)

    browse_input_english_button = tk.Button(root, text="浏览", command=lambda: browse_input_file(input_english_entry))
    browse_input_english_button.grid(row=0, column=2, padx=10, pady=10)

    input_chinese_label = tk.Label(root, text="选择输入中文字幕：")
    input_chinese_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    # 使用 Entry 小部件创建输入框
    input_chinese_entry = tk.Entry(root, width=40)
    # 使用 grid 布局管理器将 Entry 小部件放置在窗口中的特定位置。
    input_chinese_entry.grid(row=1, column=1, padx=10, pady=10)

    browse_input_chinese_button = tk.Button(root, text="浏览", command=lambda: browse_input_file(input_chinese_entry))
    browse_input_chinese_button.grid(row=1, column=2, padx=10, pady=10)

    output_label = tk.Label(root, text="选择输出文件位置：")
    output_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=2, column=1, padx=10, pady=10)

    browse_output_button = tk.Button(root, text="浏览", command=browse_output_file)
    browse_output_button.grid(row=2, column=2, padx=10, pady=10)

    process_button = tk.Button(root, text="开始处理", command=process_files)
    process_button.grid(row=3, column=0, columnspan=3, pady=20)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
