import re
import tkinter as tk
from tkinter import filedialog, messagebox

"""
    字幕内去除异常换行
"""
def is_chinese(text):
    """判断文本是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fa5]', text))

def is_english(text):
    """判断文本是否包含中文"""
    return bool(re.search(r'[a-zA-Z]', text))


def merge_chinese_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 创建一个空列表，用于存储处理后的行
    processed_lines = []
    i = 0

    while i < len(lines):
        # 去除换行符
        line = lines[i].strip()

        # 如果行不为空，则判断是否包含中文
        if line:
            # 如果下一行不为空，则判断是否包含中文
            if i + 1 < len(lines):
                # 取得下一行
                next_line = lines[i + 1].strip()
                # 判断两行是否都包含中文
                # if is_chinese(line) and is_chinese(next_line):
                if is_english(line) and is_english(next_line):
                    # 合并两行
                    merged_line = line + next_line
                    processed_lines.append(merged_line)
                    i += 2  # 跳过下一行
                # 不包含中文直接追加
                else:
                    processed_lines.append(line)
                    i += 1
            # 如果为空就直接添加
            else:
                processed_lines.append(line)
                i += 1
        # 如果为空就跳过
        else:
            processed_lines.append(line)
            i += 1

    # Write the processed subtitles back to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines) + '\n')


def browse_input_file():
    filename = filedialog.askopenfilename(filetypes=[("SRT Files", "*.srt")])
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)


def browse_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)


def process_files():
    # 从输入框中获取文件路径和输出目录
    input_file = input_entry.get()
    output_folder = output_entry.get()

    if not input_file:
        messagebox.showerror("错误", "请输入文件路径")
        return

    if not output_folder:
        output_folder = "C:/Users/sepy2/Desktop"

    try:
        # Get the output file name based on the input file name
        # 设置输出名
        output_file = f"{output_folder}/{input_file.split('/')[-1].replace('.srt', '_processed.srt')}"
        # 处理文件删除中文之间的换行符
        merge_chinese_lines(input_file, output_file)
        messagebox.showinfo("成功", f"文件已处理并保存在：{output_file}")
    except Exception as e:
        messagebox.showerror("错误", f"处理过程中出现错误：{str(e)}")


def main():
    # Create the main window
    global root, input_entry, output_entry

    root = tk.Tk()
    root.title("SRT 文件去重复行工具")

    # Set window size
    root.geometry("500x200")

    # Create and place widgets
    input_label = tk.Label(root, text="选择输入文件：")
    input_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

    # 使用 Entry 小部件创建输入框
    input_entry = tk.Entry(root, width=40)
    # 使用 grid 布局管理器将 Entry 小部件放置在窗口中的特定位置。
    input_entry.grid(row=0, column=1, padx=10, pady=10)

    browse_input_button = tk.Button(root, text="浏览", command=browse_input_file)
    browse_input_button.grid(row=0, column=2, padx=10, pady=10)

    output_label = tk.Label(root, text="选择输出目录：")
    output_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=1, column=1, padx=10, pady=10)
    output_entry.insert(0, "C:/Users/sepy2/Desktop")  # 设置默认输出路径

    browse_output_button = tk.Button(root, text="浏览", command=browse_output_folder)
    browse_output_button.grid(row=1, column=2, padx=10, pady=10)

    process_button = tk.Button(root, text="开始处理", command=process_files)
    process_button.grid(row=2, column=0, columnspan=3, pady=20)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
