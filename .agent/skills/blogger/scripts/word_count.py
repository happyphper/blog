#!/usr/bin/env python3
"""
博客文章质量检测脚本
用法：python word_count.py <markdown_file>
"""

import re
import sys
from pathlib import Path

def count_words(text):
    text = re.sub(r'```[\s\S]*?```', '', text)
    chinese = len(re.findall(r'[\u4e00-\u9fff]', text))
    english = len(re.findall(r'\b[a-zA-Z]+\b', text))
    return chinese + english

def count_headers(text):
    return {
        'h1': len(re.findall(r'^# [^#]', text, re.MULTILINE)),
        'h2': len(re.findall(r'^## [^#]', text, re.MULTILINE)),
        'h3': len(re.findall(r'^### [^#]', text, re.MULTILINE)),
        'h4': len(re.findall(r'^#### [^#]', text, re.MULTILINE)),
    }

def count_code_blocks(text):
    pattern = r'```(\w*)\n([\s\S]*?)```'
    matches = re.findall(pattern, text)
    return [{'lang': m[0] or 'none', 'lines': len(m[1].strip().split('\n'))} for m in matches]

def count_images(text):
    md = len(re.findall(r'!\[.*?\]\(.*?\)', text))
    ph = len(re.findall(r'IMAGE_PLACEHOLDER', text))
    return {'real': md, 'placeholder': ph}

def check_required(text):
    return {
        'title': bool(re.search(r'Flutter.*OpenHarmony', text, re.I)),
        'atomgit': 'atomgit.com' in text.lower(),
        'community': 'openharmonycrossplatform.csdn.net' in text,
        'no_gitcode': 'gitcode' not in text.lower(),
    }

def main():
    if len(sys.argv) < 2:
        print("用法：python word_count.py <file.md>")
        return
    
    content = Path(sys.argv[1]).read_text(encoding='utf-8')
    
    words = count_words(content)
    headers = count_headers(content)
    codes = count_code_blocks(content)
    images = count_images(content)
    required = check_required(content)
    
    print("=" * 50)
    print("📊 博客质量分析报告")
    print("=" * 50)
    print(f"\n📝 字数：{words} {'✅' if words >= 2000 else '⚠️ 建议≥2000'}")
    print(f"\n📑 标题：H1={headers['h1']} H2={headers['h2']} H3={headers['h3']} H4={headers['h4']}")
    print(f"   总计：{sum(headers.values())} 个")
    print(f"\n💻 代码块：{len(codes)} 个")
    if codes:
        min_lines = min(c['lines'] for c in codes)
        print(f"   最少行数：{min_lines} {'✅' if min_lines >= 5 else '⚠️'}")
    print(f"\n🖼️ 图片：{images['real']} 张，占位符：{images['placeholder']} 个")
    print(f"\n✅ 必需检查：")
    print(f"   标题规范：{'✅' if required['title'] else '❌'}")
    print(f"   AtomGit：{'✅' if required['atomgit'] else '❌'}")
    print(f"   社区链接：{'✅' if required['community'] else '❌'}")
    print(f"   无GitCode：{'✅' if required['no_gitcode'] else '❌'}")
    print("\n🔗 官方自查：https://www.csdn.net/qc")

if __name__ == '__main__':
    main()
