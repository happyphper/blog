import os
import shutil

target_dir = '/Users/wangbaolong/workspace/happyphper/blog/posts/2026/0222'
img_target_dir = os.path.join(target_dir, 'images')

# (ImageName, TempSourcePath) 映射需要手动填写，从工具输出中提取
mappings = [
    ("flutter_platform_alert", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/flutter_platform_alert_1771722349929.png"),
    ("flutter_platform_widgets", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/flutter_platform_widgets_1771722369050.png"),
    ("flutter_simple_dependency_injection", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/flutter_simple_dependency_injection_1771722385481.png"),
    ("fuzzy", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/fuzzy_1771722401873.png"),
    ("gql_dio_link", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/gql_dio_link_1771722421763.png"),
]

for pkg_name, src_path in mappings:
    dest_path = os.path.join(img_target_dir, f"{pkg_name}.png")
    shutil.copy(src_path, dest_path)
    print(f"Copied {src_path} to {dest_path}")
    
    md_path = os.path.join(target_dir, f"{pkg_name}.md")
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 插入图片（在标题下方或前言上方）
        img_tag = f"![{pkg_name}](images/{pkg_name}.png)\n\n"
        # 寻找第一个标题结束的位置
        lines = content.split('\n')
        inserted = False
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith('# ') and not inserted:
                new_lines.append("")
                new_lines.append(img_tag)
                inserted = True
        
        final_content = '\n'.join(new_lines)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Updated {md_path}")

