import webcolors
import csv
import codecs


def closest_colour(requested_colour):
    min_distance = float('inf')
    closest_name = None
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        distance = rd + gd + bd
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name


def process_and_replace_colors(file_path, color_column_indices):
    updated_rows = []

    with codecs.open(file_path, 'r', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            updated_row = row[:]
            for color_column_index in color_column_indices:
                if len(row) > color_column_index:
                    hex_color = row[color_column_index]
                    try:
                        # 尝试将颜色字符串转换为RGB颜色
                        rgb_color = webcolors.hex_to_rgb(hex_color)
                        closest_color_name = closest_colour(rgb_color)
                        # 替代原单元格中的内容
                        updated_row[color_column_index] = closest_color_name
                    except ValueError:
                        # 如果转换失败，跳过不是有效颜色的数据
                        print(f"Skipped invalid color: {hex_color}")
            updated_rows.append(updated_row)

    # 请替换为你的输出文件路径
    output_file_path = "C:/Users/Fang/Desktop/信管/社会网络分析/csv数据/train_updated.csv"

    with codecs.open(output_file_path, 'w', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)


# 请替换为你的CSV文件路径
csv_file_path = "C:/Users/Fang/Desktop/信管/社会网络分析/csv数据/train#.csv"
color_column_indices = [18, 20, 21, 22, 23]  # 请根据颜色所在的列索引进行调整

process_and_replace_colors(csv_file_path, color_column_indices)
print("Processed and saved to train_updated.csv")

