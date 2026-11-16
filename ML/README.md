# 两类流体在 (M, N) 平面上的分界

数据：`fluids.csv`（实际为 **制表符分隔**，扩展名虽为 .csv；脚本会自动识别分隔符）
样本：31 种流体，其中 class 1 共 21 种、class 2 共 10 种。

## 一、结论（可直接写进论文）

| 项目 | 结果 |
|---|---|
| **推荐分界** | **N\* = 12.16**，判据 `N > N*` → class 1 |
| 可接受区间 | **10.94 < N\* < 13.38**（区间内任意取值，31/31 分类结果完全相同） |
| 准确率 | 100%（31/31） |
| **M 能否单独区分** | **不能**。两类 M ranges 在 **[42.08, 44.00] g/mol 重叠** |
| M 单独最优阈值 | M\* = 37.04 g/mol，仍有 1 例判错（96.8%） |
| 二维分界线（备选） | **N = 23.27 − 0.2699 M**（即 0.005058 M + 0.018744 N = 0.436163），31/31 正确，LOO 0 错 |
| 支持向量 | Propylene（class 1）、Ethane（class 2） |

关键证据：

- class 1 的 N ∈ [13.38, 211.88]，class 2 的 N ∈ [3.02, 10.94] → **N 方向完全不重叠**
- class 1 的 M ∈ [42.08, 444.92]，class 2 的 M ∈ [2.02, 44.00] → **M 方向重叠**
- 重叠区间的三例：CO₂（M = 44.00, N = 7.18, class 2）与 Propylene / CycloPropane（M = 42.08, N = 16.13 / 16.64, class 1）

因此：**这两类流体实际上由分子复杂度 N 单独分开，摩尔质量 M 不是判别变量。**

## 二、采用的分类方法

### 1. 一维阈值规则（主结果）

- 在排序后的样本中，枚举所有相邻值的中点作为候选阈值；
- 以**误分类数最少**为第一准则，**两类间隔最大**（margin 最大）为并列时的第二准则；
- 本质上就是"硬间隔线性分类器 + 强制决策面垂直于某一坐标轴"，等价于单层决策树（one-split CART）。

### 2. 二维最大间隔直线（备选，用于给出 (M, N) 平面上的界线）

- 目标：`w_M·M + w_N·N = b` 的硬间隔 SVM 解；
- 无需求解二次规划（不依赖 scikit-learn/SciPy）：在 **z-score 标准化**后的特征平面上做角度扫描，取两类投影间隙最大的方向；
- **为什么标准化**：M 的单位是 g/mol、N 为无量纲，量纲与跨度都不同，不标准化时 margin 会被跨度大的坐标主导（脚本同时输出 raw-scale 结果，其权重 0.26 M + 0.97 N 明显偏向 M，说明该结果不可直接解释）。

### 3. 验证与不确定性

- **留一法（LOO）**：一维规则 LOO 0 例判错、2 例"落在重新拟合后的间隔内"（数据本身只能确定阈值区间，无法唯一确定阈值，故记为 ambiguous 而非 error）；二维直线 LOO 0 例判错。
- **区间敏感性**：在 (10.94, 13.38) 内均匀取 501 个阈值，分类结果与 N\* = 12.16 完全一致。

## 三、可写进论文的英文表述（建议直接改用）

> The complex and simple fluids were separated in the plane of molar mass *M* and molecular
> complexity *N*. A single-threshold rule was first fitted by exhaustive search
> over the midpoints of consecutive sorted values, retaining the split that
> minimises the number of misclassified fluids and, among ties, maximises the
> margin between the classes; this is a hard-margin linear classifier constrained
> to one axis. The classes are perfectly separated by molecular complexity,
> *N*\* = 12.16, and any cut in the interval (10.94, 13.38) reproduces the same
> labelling of all 31 fluids. Molar mass alone cannot separate the classes,
> because the two ranges overlap between 42.08 and 44.00 g/mol (CO₂ at
> *M* = 44.00 g/mol, *N* = 7.18, against propylene and cyclopropane at
> *M* = 42.08 g/mol, *N* = 16.13 and 16.64); the best *M*-only threshold still
> misclassifies one fluid. A two-descriptor maximum-margin boundary,
> obtained from a hard-margin support vector machine fitted on z-scored
> descriptors, is *N* = 23.3 − 0.27 *M* and reproduces the classification with
> no leave-one-out error, but it does not improve on the single-descriptor rule.
> The class boundary is therefore placed at *N*\* ≈ 12, with an admissible range
> of 10.9–13.4.

## 四、运行说明

```bash
# 在任意位置运行；默认读取脚本同目录的 fluids.csv，并在同目录写出结果
python3 classify_fluids.py

# 指定数据与输出目录
python3 classify_fluids.py --csv fluids.csv --outdir .

# 服务器/无图形界面时关闭自动预览，或调整 PNG 宽度
python3 classify_fluids.py --no-show --png-width 2000

# 改字体与图的物理宽度（单位均为 pt，1 pt = 1/72 in）
python3 classify_fluids.py --font 9 --width-pt 345      # 9 pt 字、12.2 cm 宽
python3 classify_fluids.py --font 10 --width-pt 460     # 10 pt 字、16.2 cm 宽
```

### 字体与尺寸（重要）

图的画布按**物理尺寸**生成：默认宽 **460 pt = 16.2 cm**，因此 `--font 12` 就是**真正的 12 pt**——只要在 LaTeX 里用

```latex
\includegraphics[width=16.2cm]{fig_boundary.eps}
```

即按原始尺寸插入，字体与正文 12 pt 完全一致；若缩到 14 cm，实际字体会变成 12×14/16.2 ≈ 10.4 pt。

各元素的字号（以 `--font 12` 为例，单位 pt）：

| 元素 | 字号 |
|---|---|
| 刻度数字、坐标轴标题 | **12**（= `--font`） |
| 主标题 | 13.8（`font × 1.15`） |
| 副标题 | 10.2（`font × 0.85`） |
| 图例 | 11.4（`font × 0.95`） |
| `N*` 注释 | 9.6（`font × 0.80`） |
| 点标注（MM、MDM…） | 8.6（`font × 0.72`） |

> 旧版本的画布是 900×620 pt（31.7×21.9 cm），刻度字号写 10 意味着"图宽 31.7 cm 时 10 pt"；一旦按 16 cm 插入，实际只剩约 5 pt，这就是之前与论文其他图不匹配的原因。

依赖：**numpy**（分析）＋ **rsvg-convert**（SVG→PNG/PDF，必需）＋ **pdftops**（PDF→EPS，可选；缺失时自动回退到 `rsvg-convert -f eps`）。不需要 matplotlib。

每次运行会自动生成 `fig_boundary.png`、`fig_boundary.eps`（另有 `fig_boundary.pdf` 与源文件 `.svg`），并**自动用系统图片查看器打开 PNG**（`xdg-open` → `gio open` → `open` → `eog` → `feh` 依次尝试）；没有图形界面时只打印文件路径，用 `--no-show` 可彻底关闭预览。

## 五、输出文件

| 文件 | 内容 |
|---|---|
| `classify_fluids.py` | 全部分析代码（阈值搜索、最大间隔直线、LOO、SVG 绘图） |
| `results.txt` | 可直接阅读的结果摘要 |
| `results.json` | 结构化结果（阈值、区间、直线系数、支持向量、LOO 等） |
| `fig_boundary.png` | 位图预览（默认宽 1400 px，白底），运行后自动弹出 |
| `fig_boundary.eps` | 矢量图（BoundingBox = 图幅实际 pt 尺寸，默认 460×321 pt，字体已嵌入），LaTeX 直接 `\includegraphics` |
| `fig_boundary.pdf` | 矢量 PDF，便于快速检查或转其他格式 |
| `fig_boundary.svg` | 绘图源文件（改样式后可重新导出） |

图示约定：白底、无网格；两类分别标注为 **complex fluids**（原 class 1）与 **simple fluids**（原 class 2）；虚线图例给出 `N = 23.27 - 0.27 M`。

## 六、注意事项

1. **阈值不是唯一点**：数据只能确定 N\* ∈ (10.94, 13.38)，报告 12.16 只是区间中点；论文中建议同时给出区间。
2. **样本量小（31）且完美可分**，因此任何"泛化精度"都偏乐观；本报告因此只报告 LOO 与区间敏感性，不做 k 折交叉验证。
3. **二维直线依赖于标准化方式**：若换用其他缩放（如 min-max、robust scale），直线的斜率会变化——这正说明 M 方向的权重并非由数据唯一确定，**建议论文以 N\* 为主结论**，二维直线只作为图示。
4. 类别标签方向：脚本自动把**平均 N 更大**的一类记为"high"，本数据中即 class 1；如标签含义相反，输出会自动对应，无需改代码。
