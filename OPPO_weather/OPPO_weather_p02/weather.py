import os
import re

def batch_rename_final(folder_path):
    os.chdir(folder_path)
    
    # 获取所有 mp4 文件并排序
    files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    files.sort()

    for index, old_name in enumerate(files, start=1):
        # 1. 基础判定逻辑
        is_night = any(k in old_name for k in ['晴夜', '星空', '月亮', '黑夜'])
        period = "夜晚" if is_night else "白天"
        
        # 2. 天气具体化逻辑
        status = ""
        
        # --- 雨 ---
        if '雷雨' in old_name:
            status = "大雨"
        elif '雨' in old_name:
            status = "小雨"
            
        # --- 雪 ---
        elif '雪' in old_name:
            # 逻辑：提到雪山通常是大雪场景，其余为下雪（小雪）
            status = "大雪" if '雪山' in old_name else "小雪"
            
        # --- 雾/阴 ---
        elif '雾' in old_name:
            status = "有雾"
        elif '阴' in old_name or '阴沉' in old_name:
            status = "阴天"
            
        # --- 需要区分白天夜晚的类别 ---
        elif '晴' in old_name:
            status = f"{period}晴"
        elif '多云' in old_name:
            status = f"{period}多云"
        elif '星空' in old_name:
            status = "夜晚晴"
        elif '沙尘' in old_name:
            status = f"{period}沙尘"
        else:
            status = "未知天气"

        # 3. 整合最终名称
        # 根据需求：雨、雪、雾、阴不需要加“白天/夜晚”前缀
        no_period_weathers = ["大雨", "小雨", "大雪", "小雪", "有雾", "阴天"]
        
        if status in no_period_weathers:
            weather_desc = status
        else:
            weather_desc = status # 已经带了白天/夜晚前缀
            
        # 构造文件名：序号_描述.mp4
        new_name = f"{str(index).zfill(2)}_{weather_desc}.mp4"
        
        try:
            os.rename(old_name, new_name)
            print(f"完成: {old_name} -> {new_name}")
        except Exception as e:
            print(f"出错: {old_name} -> {e}")

if __name__ == "__main__":
    batch_rename_final('.')