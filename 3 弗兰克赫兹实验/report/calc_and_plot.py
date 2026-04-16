#!/usr/bin/env python3
"""弗兰克-赫兹实验数据处理：绘图 + 逐差法计算第一激发电势。"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Heiti SC', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. 手动测量数据
# ============================================================
with open("hcy_manual.txt") as f:
    ia_manual = np.array(list(map(int, f.read().strip().split())), dtype=float)

ug2k_manual = np.arange(0.5, 0.5 * len(ia_manual) + 0.5, 0.5)

# ============================================================
# 2. 自动测量峰值数据（5 次）
# ============================================================
auto_peaks = np.array([
    [16.9, 27.7, 39.2, 50.9, 63.4, 75.8, 89.2],
    [16.7, 28.0, 39.2, 50.7, 63.2, 75.8, 88.8],
    [16.6, 27.7, 39.0, 50.5, 63.1, 75.4, 88.8],
    [16.8, 27.7, 39.0, 50.9, 62.8, 75.6, 88.8],
    [16.6, 27.7, 39.0, 50.9, 63.0, 75.6, 88.6],
])

# 每个峰取 5 次平均
avg_peaks = auto_peaks.mean(axis=0)
print("=" * 60)
print("自动测量各峰平均值:")
for n, v in enumerate(avg_peaks, 1):
    print(f"  峰 {n}: U_G2K = {v:.2f} V")

# ============================================================
# 3. 逐差法（自动测量）
# ============================================================
print("\n" + "=" * 60)
print("自动测量 - 逐差法计算第一激发电势:")
delta_auto = []
for i in range(3):
    du = avg_peaks[i + 4] - avg_peaks[i]
    u0i = du / 4
    delta_auto.append(u0i)
    print(f"  ΔU_{i+1} = U_{i+5} - U_{i+1} = {avg_peaks[i+4]:.2f} - {avg_peaks[i]:.2f} = {du:.2f} V, "
          f"U_0,{i+1} = {u0i:.2f} V")

u0_auto = np.mean(delta_auto)
print(f"\n  U_0(自动) = ({' + '.join(f'{x:.2f}' for x in delta_auto)}) / 3 = {u0_auto:.2f} V")
err_auto = abs(u0_auto - 11.61) / 11.61 * 100
print(f"  相对误差 = |{u0_auto:.2f} - 11.61| / 11.61 × 100% = {err_auto:.1f}%")

# ============================================================
# 4. 手动测量找峰值 & 逐差法
# ============================================================
from scipy.signal import find_peaks

peaks_idx, props = find_peaks(ia_manual, distance=15, prominence=30)
print("\n" + "=" * 60)
print("手动测量 - 峰值识别:")
manual_peak_v = ug2k_manual[peaks_idx]
manual_peak_i = ia_manual[peaks_idx]
for n, (v, i) in enumerate(zip(manual_peak_v, manual_peak_i), 1):
    print(f"  峰 {n}: U_G2K = {v:.1f} V, I_A = {i:.0f} nA")

if len(manual_peak_v) >= 7:
    print("\n手动测量 - 逐差法计算第一激发电势:")
    delta_manual = []
    for i in range(3):
        du = manual_peak_v[i + 4] - manual_peak_v[i]
        u0i = du / 4
        delta_manual.append(u0i)
        print(f"  ΔU_{i+1} = U_{i+5} - U_{i+1} = {manual_peak_v[i+4]:.1f} - {manual_peak_v[i]:.1f} = {du:.1f} V, "
              f"U_0,{i+1} = {u0i:.2f} V")
    u0_manual = np.mean(delta_manual)
    print(f"\n  U_0(手动) = {u0_manual:.2f} V")
    err_manual = abs(u0_manual - 11.61) / 11.61 * 100
    print(f"  相对误差 = {err_manual:.1f}%")

# ============================================================
# 5. 绘制手动测量 IA-UG2K 曲线
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ug2k_manual, ia_manual, 'b-', linewidth=1.2, label='手动测量数据')
ax.plot(manual_peak_v, manual_peak_i, 'ro', markersize=6, label='峰值')

for n, (v, i) in enumerate(zip(manual_peak_v, manual_peak_i), 1):
    ax.annotate(f'{n}\n({v:.1f}V)',
                xy=(v, i), xytext=(0, 12),
                textcoords='offset points', ha='center', fontsize=8,
                color='red')

ax.set_xlabel(r'$U_{G_2K}$ / V', fontsize=13)
ax.set_ylabel(r'$I_A$ / nA', fontsize=13)
ax.set_title(r'手动测量 $I_A$ - $U_{G_2K}$ 曲线', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('IA_UG2K_manual.pdf', dpi=300)
plt.savefig('IA_UG2K_manual.png', dpi=300)
print("\n已保存: IA_UG2K_manual.pdf / .png")

# ============================================================
# 6. 绘制自动测量峰值 & 线性拟合
# ============================================================
fig2, ax2 = plt.subplots(figsize=(8, 5))
ns = np.arange(1, 8)
ax2.plot(ns, avg_peaks, 'rs-', markersize=8, linewidth=1.5, label='峰值平均 $U_{G_2K}$')

# 线性拟合 U = k*n + b
coeffs = np.polyfit(ns, avg_peaks, 1)
fit_line = np.polyval(coeffs, ns)
ax2.plot(ns, fit_line, 'b--', linewidth=1, label=f'线性拟合: $U_0$={coeffs[0]:.2f} V/峰')

ax2.set_xlabel('峰值序号 $n$', fontsize=13)
ax2.set_ylabel(r'$U_{G_2K}$ / V', fontsize=13)
ax2.set_title('自动测量峰值电压 vs 峰序号', fontsize=14)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(ns)
plt.tight_layout()
plt.savefig('peaks_linear_fit.pdf', dpi=300)
plt.savefig('peaks_linear_fit.png', dpi=300)
print("已保存: peaks_linear_fit.pdf / .png")

print("\n" + "=" * 60)
print(f"线性拟合斜率（即 U_0）= {coeffs[0]:.2f} V")
print(f"截距（含接触电势差信息）= {coeffs[1]:.2f} V")

# ============================================================
# 7. 输出用于填充 tex 的数值
# ============================================================
print("\n" + "=" * 60)
print("===== 用于填充 TeX 报告的数值 =====")
print(f"自动测量平均峰值: {' & '.join(f'{v:.1f}' for v in avg_peaks)}")
print(f"U_0(自动逐差法) = {u0_auto:.2f} V")
print(f"相对误差(自动) = {err_auto:.1f}%")
if len(manual_peak_v) >= 7:
    print(f"手动测量峰值: {' & '.join(f'{v:.1f}' for v in manual_peak_v[:7])}")
    print(f"U_0(手动逐差法) = {u0_manual:.2f} V")
    print(f"相对误差(手动) = {err_manual:.1f}%")
