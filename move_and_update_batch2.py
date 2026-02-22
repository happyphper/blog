import os
import shutil

target_dir = '/Users/wangbaolong/workspace/happyphper/blog/posts/2026/0222'
img_target_dir = os.path.join(target_dir, 'images')

mappings = [
    ("hive_flutter", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/hive_flutter_1771722457038.png"),
    ("icalendar_parser", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/icalendar_parser_1771722471676.png"),
    ("icon_font_generator", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/icon_font_generator_1771722490876.png"),
    ("l", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/l_log_1771722512625.png"),
    ("latlong2", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/latlong2_1771722531951.png"),
]

for pkg_name, src_path in mappings:
    dest_path = os.path.join(img_target_dir, f"{pkg_name}.png")
    shutil.copy(src_path, dest_path)
    print(f"Copied {src_path} to {dest_path}")
    
    md_path = os.path.join(target_dir, f"{pkg_name}.md")
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        img_tag = f"![{pkg_name}](images/{pkg_name}.png)\n\n"
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

