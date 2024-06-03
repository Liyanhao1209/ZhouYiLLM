import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with open('../../../config/visualize.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 使用with语句打开文件，确保最后文件会被正确关闭
with open(config["file_path"], 'r', encoding='utf-8') as file:
    # 读取并解析JSON数据
    json_data = json.load(file)

# 将JSON数据转换为DataFrame
df = pd.DataFrame(json_data)

# 定义一个列名列表，列出想要删除的列
columns_to_drop = ['Tot_problem_nums', 'Solved_problem_nums']

# 使用drop函数删除指定的列，inplace=True表示直接在原DataFrame上修改
df.drop(columns=columns_to_drop, inplace=True)

# 提取type_stats列并转换为新的DataFrame
type_stats_df = pd.DataFrame(df['type_stats'].tolist())
df = df[['llm_name', 'Solve_rate']]


# 定义一个转换函数，将分数字符串转换为小数并保留两位小数
def convert_fraction_to_decimal(fraction_str):
    try:
        numerator, denominator = map(int, fraction_str.split('/'))
        return round(numerator / denominator, 2)
    except (ValueError, ZeroDivisionError):
        return None


type_stats_df = type_stats_df.apply(lambda col: col.apply(lambda x: convert_fraction_to_decimal(x)))
# 将转换后的DataFrame与原始DataFrame合并
df_with_scores = pd.concat([df, type_stats_df], axis=1)
# 将'Solve_rate'列的字符串转换为浮点数
df_with_scores['Solve_rate'] = df_with_scores['Solve_rate'].astype(float)
df_with_scores.iloc[:, 1:] = df_with_scores.iloc[:, 1:].applymap(lambda x: f"{x:.2%}")

# 移除百分号并转换为浮点数
df_with_scores.iloc[:, 1:] = df_with_scores.iloc[:, 1:].applymap(
    lambda x: float(x.strip('%')) if isinstance(x, str) else x
)

df_with_scores.rename(columns={'Solve_rate': '总计'}, inplace=True)
df = df_with_scores

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def draw_pict1(df):
    # 定义颜色
    colors = {"总计": "red", "卦辞": "orange", "爻辞": "green",
              "彖传": "blue", "象传": "purple", "系辞传": "brown",
              "卦间关系": "pink", "爻间关系": "gray", "上下卦": "olive",
              "成语": "cyan", "人物著作": "teal", "基础知识": "indigo",
              "序卦传": "crimson", "杂卦传": "darkgoldenrod",
              "说卦传": "lightblue", "文言传": "lightgreen"}
    # 设置图形的大小
    fig, ax = plt.subplots(figsize=(17, 10))

    # 定义柱的宽度和间隔
    bar_width = 0.05
    group_spacing = 0.3

    # 计算每个模型柱的位置
    indices = np.arange(len(df)) * (len(df.columns[1:]) * bar_width + group_spacing)

    # 绘制每个指标的柱状图/一次循环画出一个类别所有模型的柱状图
    for i, column in enumerate(df.columns[1:]):
        bar_positions = indices + i * bar_width
        ax.bar(bar_positions, df[column], width=bar_width, label=column, color=colors[column])

    # 设置x轴的位置在模型名称的中间
    ax.set_xticks(indices + (len(df.columns[1:]) * bar_width) / 2 - bar_width / 2)
    ax.set_xticklabels(df["llm_name"], rotation=45, ha='right')

    # 添加图表标题和标签
    ax.set_title('各模型的评价指标')
    ax.set_xlabel('模型名称')
    ax.set_ylabel('百分比')
    # 添加水平虚线
    for y in [30, 35, 40, 50, 60, 70, 80]:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    # 添加图例，并将图例放置在图表的右侧
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    # 显示图表
    plt.tight_layout()
    plt.show()


def draw_pict2(df):
    colors = [
        "#FF5733", "#FFD700", "#F6FF33", "#FF33A6", "#A633FF", "#33FFF6", "#3357FF",   "#993366", "#996633"
    ]

    attributes = df.columns[1:]
    bar_width = 0.075
    index = np.arange(len(attributes))

    fig, ax = plt.subplots(figsize=(20, 8))

    # 同样的道理，这里一次绘画出一个模型的所有类别的柱状图
    for i, model in enumerate(df['llm_name']):
        values = df.loc[i, attributes]
        ax.bar(index + i * bar_width, values, bar_width, label=model, color=colors[i])

    ax.set_xlabel('分类')
    ax.set_ylabel('得分')
    ax.set_title('各模型的评价指标')
    ax.set_xticks(index + bar_width * (len(df['llm_name']) / 2))
    ax.set_xticklabels(attributes)
    # 添加水平虚线
    for y in [30, 35, 40, 50, 60, 70, 80, 100]:
        ax.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    ax.legend(loc='upper right')

    plt.show()


draw_pict1(df)
draw_pict2(df)
