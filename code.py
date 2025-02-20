import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import google.generativeai as genai
from bs4 import BeautifulSoup

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_law_page_html(query):
    """Playwright를 사용하여 국가법령정보센터 검색 결과를 HTML로 가져옵니다."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 브라우저 창 띄움
        page = await browser.new_page()

        # User-Agent 설정
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        await page.goto(f"https://www.law.go.kr/lsSc.do?section=&menuId=1&subMenuId=15&tabMenuId=81&eventGubun=060101&query={query}")

        try:
            await page.wait_for_load_state("networkidle")  # 네트워크 활동 대기
            await page.wait_for_timeout(5000)  # 추가로 5초 기다림

            # 특정 요소가 있는지 확인하고, 있으면 HTML 가져옴
            try:
                # 먼저 .result_list 시도
                content = await page.inner_html(".result_list", timeout=5000)
            except:  # .result_list 없으면 .lsListWrap 시도
                try:
                    content = await page.inner_html(".lsListWrap", timeout=5000)
                except:
                    content = await page.content() # 그것도 없으면 그냥 전체 페이지 가져옴.

        except Exception as e:
            print(f"페이지 로딩 중 오류 발생: {e}")
            await browser.close()
            return None

        await browser.close()
        return content  # content 반환


def ask_gemini_with_html(question, html_content):
    """Gemini API에 HTML 내용과 질문을 함께 보내 답변을 받습니다."""
    prompt = f"""다음 HTML 페이지 내용을 참고하여 질문에 답변해줘:

    {html_content[:100000]}

    질문: {question}
    """
    # tiktoken 등으로 토큰 수 예측, chunking 하는 것이 가장 좋음.

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Gemini API 호출 중 오류가 발생했습니다."



def extract_urls(html_content):
    """HTML 내용에서 URL을 추출하는 함수"""
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = []
    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']
        if url.startswith('http'):
            urls.append(url)
        elif url.startswith('/'):
            urls.append("https://www.law.go.kr" + url)
    return urls


async def main():
    user_question = input("궁금한 법 관련 내용을 질문해주세요: ")

    html_content = await get_law_page_html(user_question)

    if html_content:
            answer = ask_gemini_with_html(user_question, html_content)
            urls = extract_urls(html_content)

            print("\n답변:", answer)
            if urls:
                print("\n참고 URL:")
                for url in urls:
                    print(url)
    else:
        print("검색 결과를 가져오는 데 실패했습니다.")



if __name__ == "__main__":
    asyncio.run(main())
