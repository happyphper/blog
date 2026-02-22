import os
import shutil

target_dir = '/Users/wangbaolong/workspace/happyphper/blog/posts/2026/0222'
img_target_dir = os.path.join(target_dir, 'images')

mappings = [
    ("leancode_lint", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/leancode_lint_1771722563272.png"),
    ("local_auth", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/local_auth_1771722584432.png"),
    ("loggy", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/loggy_1771722602887.png"),
    ("mailer", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/mailer_1771722621531.png"),
    ("mason_logger", "/Users/wangbaolong/.gemini/antigravity/brain/31cc81c5-8098-4184-93aa-0091421f5a8b/mason_logger_1771722639953.png"),
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

