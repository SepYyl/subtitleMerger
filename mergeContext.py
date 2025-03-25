from itertools import zip_longest
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def is_chinese(text):
    """判断文本是否包含中文"""
    return bool(re.search(r'[\u4e00-\u9fa5]', text))

def process_srt_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('\n\n')
    processed_lines = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        if len(lines) < 3:
            continue

        text_lines = lines[2:]
        en_parts = []
        zh_parts = []

        for line in text_lines:
            line = line.strip()
            if not line:
                continue
            # 拆分中英文片段
            parts = re.findall(r'([\u4e00-\u9fa5。？！]+)|([a-zA-Z0-9,.!? ]+)', line)
            for part in parts:
                zh_part, en_part = part
                if zh_part:
                    zh_parts.append(zh_part.strip())
                if en_part:
                    en_parts.append(en_part.strip())

        # 合并并清理空格
        en_text = ' '.join(en_parts).strip()
        zh_text = ' '.join(zh_parts).strip()

        # 分割句子（增强正则表达式）
        en_sentences = re.findall(r'([^.!?]+[.!?]+)|([^.!?]+$)', en_text)
        en_sentences = [''.join(s).strip() for s in en_sentences if ''.join(s).strip()]
        zh_sentences = re.findall(r'([^.。？！]+[。？！]+)|([^.。？！]+$)', zh_text)
        zh_sentences = [''.join(s).strip() for s in zh_sentences if ''.join(s).strip()]

        # 强制补全标点
        def ensure_ending(sentence, lang='en'):
            if lang == 'en':
                if not sentence.endswith(('.', '!', '?')):
                    return sentence + '.'  # 补英文句号
            else:
                if not sentence.endswith(('。', '？', '！')):
                    return sentence + '。'  # 补中文句号
            return sentence

        # 交替添加句子
        for en, zh in zip_longest(en_sentences, zh_sentences):
            if en:
                processed_lines.append(ensure_ending(en))
            if zh:
                processed_lines.append(ensure_ending(zh, 'zh'))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(processed_lines))

# def process_srt_file(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as f:
#         content = f.read()
#
#     blocks = content.split('\n\n')
#     processed_lines = []
#
#     for block in blocks:
#         block = block.strip()
#         if not block:
#             continue
#         lines = block.split('\n')
#         if len(lines) < 3:
#             continue
#
#         text_lines = lines[2:]
#         en_parts = []
#         zh_parts = []
#
#         for line in text_lines:
#             line = line.strip()
#             if not line:
#                 continue
#             if is_chinese(line):
#                 zh_parts.append(line)
#             else:
#                 en_parts.append(line)
#
#         # 合并并清理空格（仅用于分割句子，不再直接添加到processed_lines）
#         en_text = re.sub(r'\s+', ' ', ' '.join(en_parts)).strip()
#         zh_text = re.sub(r'\s+', ' ', ' '.join(zh_parts)).strip()
#
#         # 分割句子
#         en_sentences = re.split(r'(?<=[.!?])\s*', en_text)
#         zh_sentences = re.split(r'(?<=[。？！])\s*', zh_text)
#
#         en_sentences = [s.strip() for s in en_sentences if s.strip()]
#         zh_sentences = [s.strip() for s in zh_sentences if s.strip()]
#
#         # 交替添加分割后的句子（仅保留这一部分）
#         for en, zh in zip_longest(en_sentences, zh_sentences):
#             if en:
#                 processed_lines.append(en)
#             if zh:
#                 processed_lines.append(zh)
#
#     with open(output_file, 'w', encoding='utf-8') as f:
#         f.write('\n'.join(processed_lines))


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
    input_file = input_entry.get()
    output_folder = output_entry.get()

    if not input_file:
        messagebox.showerror("错误", "请输入文件路径")
        return

    if not output_folder:
        output_folder = "C:/Users/sepy2/Desktop"  # 默认输出路径

    try:
        output_file = f"{output_folder}/{input_file.split('/')[-1].replace('.srt', '_processed.srt')}"
        process_srt_file(input_file, output_file)
        messagebox.showinfo("成功", f"文件已处理并保存在：{output_file}")
    except Exception as e:
        messagebox.showerror("错误", f"处理过程中出现错误：{str(e)}")

def main():
    global root, input_entry, output_entry

    root = tk.Tk()
    root.title("SRT 文件处理工具")
    root.geometry("500x200")

    # 界面组件
    input_label = tk.Label(root, text="选择输入文件：")
    input_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    input_entry = tk.Entry(root, width=40)
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    browse_input_button = tk.Button(root, text="浏览", command=browse_input_file)
    browse_input_button.grid(row=0, column=2, padx=10, pady=10)

    output_label = tk.Label(root, text="选择输出目录：")
    output_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    output_entry = tk.Entry(root, width=40)
    output_entry.grid(row=1, column=1, padx=10, pady=10)
    output_entry.insert(0, "C:/Users/sepy2/Desktop")
    browse_output_button = tk.Button(root, text="浏览", command=browse_output_folder)
    browse_output_button.grid(row=1, column=2, padx=10, pady=10)

    process_button = tk.Button(root, text="开始处理", command=process_files)
    process_button.grid(row=2, column=0, columnspan=3, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
