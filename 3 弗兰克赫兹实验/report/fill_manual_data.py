#!/usr/bin/env python3
"""读取手动测量数据，生成 LaTeX 表格并写入 report tex 文件。"""

import os

base = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(base, "hcy_manual.txt")
tex_file = os.path.join(base, "hcy_report.tex")

# 读取数据
with open(data_file) as f:
    values = list(map(int, f.read().strip().split()))

# UG2K 从 0.5 到 100.0，步进 0.5
voltages = [0.5 * (i + 1) for i in range(len(values))]

# 固定列宽（使用 array 宏包的 w{对齐}{宽度} 列类型）
COL_W = "0.72cm"  # 每列宽度

# 每 10 个一组生成表格
lines = []
lines.append(r"{\fontsize{10pt}{14pt}\selectfont")
lines.append(r"仪器参数：$U_{F_1F_2}$ = 3.10 V，$U_{G_1K}$ = 1.25 V，$U_{G_2A}$ = 2.33 V")
lines.append("")

for group in range(0, len(values), 10):
    v_slice = voltages[group:group + 10]
    i_slice = values[group:group + 10]

    # 格式化电压
    v_strs = [f"{v:.1f}" for v in v_slice]

    n = len(v_slice)
    col_spec = "c|" + "r".join([""] * (n + 1)).replace("", "w{r}{" + COL_W + "}", n).rstrip("")
    # 简化：直接用 w{r}{宽度} 列
    col_spec = "c|" + " ".join([f"w{{r}}{{{COL_W}}}"] * n)

    lines.append(r"\vspace{0.15cm}")
    lines.append(r"\begin{tabular}{" + col_spec + "}")
    lines.append(r"    \toprule")
    lines.append(r"    $U_{G_2K}$（V） & " + " & ".join(v_strs) + r" \\")
    lines.append(r"    \midrule")
    lines.append(r"    $I_A$（nA） & " + " & ".join(str(x) for x in i_slice) + r" \\")
    lines.append(r"    \bottomrule")
    lines.append(r"\end{tabular}")
    lines.append("")

lines.append("}")

new_table = "\n".join(lines)

# 读取 tex 文件，替换占位表格
with open(tex_file) as f:
    tex = f.read()

# 定位要替换的区域：从 "表2：手动测量" 后面的 \vspace{0.3cm} 到 \newpage 之前
marker_start = r"{\fontsize{10pt}{14pt}\selectfont" + "\n" + r"仪器参数：$U_{F_1F_2}$"
marker_end = r"}" + "\n" + "\n" + r"\newpage" + "\n" + "\n" + r"% ========== 三、结果与分析 =========="

# Find the old table block
idx_start = tex.find(r"""{\fontsize{10pt}{14pt}\selectfont
仪器参数""")
if idx_start == -1:
    print("ERROR: 找不到手动测量表格起始位置")
    exit(1)

idx_end = tex.find(r"""
\newpage

% ========== 三、结果与分析 ==========""", idx_start)
if idx_end == -1:
    print("ERROR: 找不到手动测量表格结束位置")
    exit(1)

old_block = tex[idx_start:idx_end]
tex = tex[:idx_start] + new_table + tex[idx_end:]

with open(tex_file, "w") as f:
    f.write(tex)

print(f"成功写入 {len(values)} 个数据点（{voltages[0]:.1f}V ~ {voltages[-1]:.1f}V）到 {os.path.basename(tex_file)}")
print(f"共生成 {(len(values) + 9) // 10} 个表格")
