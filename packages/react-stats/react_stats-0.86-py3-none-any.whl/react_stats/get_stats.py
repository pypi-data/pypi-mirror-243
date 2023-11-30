

#!/usr/bin/env python3
import io
import sys
import os
import csv
import re
from tabulate import tabulate
from react_stats.exts import exts_dict
import chardet
import pandas as pd
import asciibars as a_bars

exts_tresor = exts_dict()
table_size = 25
MAX_DIR_SIZE = 1024 * 1024 * 100
exclude_dirs = [
    "myenv", 
    ".git", 
    ".next", 
    "node_modules", 
    "venv",
    "build",
    "dist",
    ".cache",
    ".vscode",
    ".idea",
    "public",
    "assets",
    "logs",
    ".github",
    "coverage",
    "storybook-static",
    "docs",
    "__tests__",
    "__mocks__",
    "migrations",
    "locales",
    ".history",
    "tmp",
    "temp",
    ".yarn",
    ".npm"
]

def main():
    
    path = os.getcwd()
    file_tresor = []
    hook_tresor = []
    total_lines = 0
    
    for dirpath, dirnames, filenames in os.walk(path):
        
        dirnames[:] = [dir for dir in dirnames if dir not in exclude_dirs]
        os.chdir(dirpath)
        
        if any(excluded in dirpath for excluded in exclude_dirs):
            continue
        else:
            os.chdir(dirpath)
            for file in filenames:
                
                _, ext = os.path.splitext(file)
                if ext not in exts_tresor:
                    continue
                else:
                    line_count, hook_count = count_hooks_and_lines(file)
                    file_tresor.append([file, line_count, exts_tresor[ext]])
                    total_lines += line_count

                    if hook_count['all hooks'] == 0:
                        continue
                    else:
                        hook_tresor.append(list(hook_count.values()))
    

    og_length = len(file_tresor)
    file_tresor = sorted(file_tresor, key=lambda x: x[1], reverse=True)[:table_size]
    cs_length = len(file_tresor)
    hook_tresor = sorted(hook_tresor, key=lambda x: x[1], reverse=True)
    
    
    lang_df = make_lang_df(file_tresor)
    lang_chart = make_lang_chart(lang_df)
    hooks_table = make_hooks_table(hook_tresor)
    files_table = make_files_table(file_tresor)
    stat_file = make_stat_file(path, files_table, hooks_table, lang_chart, og_length, cs_length, total_lines)
    

def get_directory_size(start_path="."):
    total_size = 0
    for dirpath, root, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size
    

def count_hooks_and_lines(file_path):
    
    line_count = 0
    filename = os.path.basename(file_path)
    
    hook_count = {
        "file": filename,
        "all hooks": 0,
        "useState": 0,
        "useEffect": 0,
        "useContext": 0,
        "otherHooks": 0,
        "customHooks": 0
    }
    hook_patterns = {
        "useState": r"const\s+\[\s*(.*?),\s*(.*?)\s*\]\s*=\s*useState\((.*?)\)",
        "useEffect": r"useEffect\(\s*\(\)\s*=>\s*\{(?:[^}]+|\n)+\}(,\s*\[.*?\]\s*)?\)",
        "useContext": r"const\s*([\w\s{},]+)\s*=\s*useContext\(\s*[-a-zA-Z0-9_]+\s*\)",
        "otherHooks": r"\buse(?!State\b|Effect\b|Context\b)(Callback|DebugValue|DeferredValue|Id|ImperativeHandle|InsertionEffect|LayoutEffect|Memo|Reducer|Ref|SyncExternalStore|Transition)\b",
        "customHooks": r"\buse(?!State\b|Effect\b|Context\b|Callback\b|DebugValue\b|DeferredValue\b|Id\b|ImperativeHandle\b|InsertionEffect\b|LayoutEffect\b|Memo\b|Reducer\b|Ref\b|SyncExternalStore\b|Transition\b)[A-Z]\w+\("
    }
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                
                if line.strip() == "":
                    continue
                elif line.startswith("#"):
                    continue
                elif line.startswith("//"):
                    continue
                elif line.startswith("/*"):
                    continue
                else:
                    
                    line_count += 1
                    for hook, pattern in hook_patterns.items():
                        
                        try:
                            matches = re.findall(pattern, line)
                            
                            hook_count[hook] += len(matches)
                            hook_count['all hooks'] += len(matches)
                            
                        except Exception as e:
                            print(f"Error in count_hooks for {file}: {e}")
            
            # print(f"line count: {line_count}")              
            # print(hook_count)
                
    except UnicodeDecodeError:
        print(f"Could not decode {file_path}. Skipping...")
        
    except FileNotFoundError:
        print(f"File {file_path} not found. Skipping...")
        
    except PermissionError:
        print(f"No permission to read {file_path}. Skipping...")
        
    except Exception as e:
        print(f"An unknown error occurred while reading {file_path}: {e}")

    return line_count, hook_count




def make_files_table(file_tresor):
    headers =["files","lines","language"]
    table = tabulate(file_tresor, headers, tablefmt="rst")
    return table

def make_lang_df(file_tresor):
    df = pd.DataFrame(file_tresor, columns=["Filename", "Lines", "Language"])
    lang_df = df.groupby('Language')['Lines'].sum().reset_index()
    
    total_lines = lang_df['Lines'].sum()
    lang_df['Percentage'] = round((lang_df['Lines'] / total_lines) * 100, 2)
    
    lang_df = lang_df.sort_values(by='Percentage', ascending=False)
    return lang_df


def make_stat_file(path, files_table, hooks_table, lang_chart, og_length, cs_length, total_lines):

    stats_path = os.path.join(path, "stats.txt")
    with open(stats_path, "w") as stats_file:
        stats_file.write("\n\n")
        stats_file.write(lang_chart)
        stats_file.write("\n\n") 
        stats_file.write(files_table)
        stats_file.write(f"\n * showing {cs_length}/{og_length} files")
        stats_file.write("\n\n")
        stats_file.write("\n\n")
        stats_file.write(hooks_table)
        stats_file.write("\n\n")
        stats_file.write("\n\n")
        stats_file.write(f"Total Files: {og_length} \n")
        stats_file.write(f"Total Lines: {total_lines}")

 

# Bar Chart 1
def make_lang_chart(lang_df):

    if lang_df.empty:
        print("No data to plot.")
        return ""

    data = []
    for _, row in lang_df.iterrows():
        data.append((str(row['Language']), float(row['Percentage'])))
          
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    a_bars.plot(data, unit='▓', neg_unit='░', neg_max=100, count_pf='%')
    sys.stdout = old_stdout

    return new_stdout.getvalue()



# Hooks Table
def make_hooks_table(hook_tresor):
    headers =["file", "all hooks","useState","useEffect","useContext","otherHooks","customHooks"]
    table = tabulate(hook_tresor, headers, tablefmt="presto")
    return table


def change_table():
    
    row_number = input("How many rows do you want to show?")
    table_size = row_number
    print(table_size)

    
    
if __name__ == "__main__":
    main()