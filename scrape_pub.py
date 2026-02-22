import requests
from bs4 import BeautifulSoup
import time

def scrape_pub_packages(query="sdk:dart", start_page=1, end_page=1):
    """
    抓取 pub.dev 上的 Package 名字
    :param query: 搜索词，默认为所有 Dart SDK 包
    :param start_page: 开始页码
    :param end_page: 结束页码
    """
    base_url = "https://pub.dev/packages"
    package_list = []

    for page in range(start_page, end_page + 1):
        print(f"--- 正在爬取第 {page} 页 ---")
        params = {'q': query, 'page': page}
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status() # 检查请求是否成功
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # 抓取包含 package 标题的链接标签
            titles = soup.select('.packages-title a')
            
            if not titles:
                print("未发现更多包，抓取结束。")
                break
                
            for t in titles:
                name = t.text.strip()
                package_list.append(name)
                print(f"已发现: {name}")
            
            # 礼貌抓取：每页请求后增加延迟，防止被封 IP
            time.sleep(1.5)
            
        except Exception as e:
            print(f"抓取第 {page} 页时发生错误: {e}")
            break

    return package_list

if __name__ == "__main__":
    # 调用示例：抓取第 16 页到第 17 页
    all_names = scrape_pub_packages(start_page=46, end_page=50)
    
    print("\n" + "="*30)
    print(f"抓取完成！共获得 {len(all_names)} 个包名：")
    for idx, name in enumerate(all_names, 1):
        print(f"{idx}. {name}")
