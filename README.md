# law
https://www.law.go.kr/LSW/main.html
# 법률 정보 검색 및 요약 챗봇 (feat. Gemini & Playwright)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 소개

이 프로젝트는 사용자가 입력한 질문에 대해 국가법령정보센터에서 관련 법률 정보를 검색하고, Google Gemini API를 활용하여 검색 결과를 요약 및 답변하는 챗봇입니다. Playwright를 사용하여 웹 페이지를 동적으로 스크래핑하고, BeautifulSoup4를 사용하여 HTML을 파싱합니다.

## 주요 기능

-   **국가법령정보센터 검색:** 사용자의 질문에 해당하는 법률 정보를 국가법령정보센터에서 검색합니다.
-   **동적 웹 스크래핑:** Playwright를 사용하여 검색 결과를 HTML 형태로 가져옵니다.
-   **Gemini API 연동:** Google Gemini 1.5 Flash 모델을 이용하여 검색 결과와 질문을 기반으로 답변을 생성합니다.
-   **URL 추출:** 검색 결과에서 관련 URL을 추출하여 사용자에게 제공합니다.
-  **비동기 처리**: `asyncio`를 사용하여 웹 스크래핑 및 API 호출을 비동기적으로 처리하여 성능을 향상시켰습니다.

## 기술 스택

-   **Python 3.9+**
-   **Playwright:** 웹 자동화 및 스크래핑
-   **BeautifulSoup4:** HTML 파싱
-   **Google Generative AI (Gemini 1.5 Flash):** 텍스트 생성 및 요약
-   **python-dotenv:** 환경 변수 관리
-   **asyncio**: 비동기 프로그래밍

## 설치 및 사용 방법

1.  **저장소 클론:**

    ```bash
    git clone https://github.com/[your-username]/[your-repository-name].git
    cd [your-repository-name]
    ```

2.  **의존성 설치:**

    ```bash
    pip install -r requirements.txt
    ```
    requirements.txt 예시:
    ```
    playwright
    beautifulsoup4
    google-generativeai
    python-dotenv
    ```
    그리고, playwright를 설치하면, 브라우저를 추가 설치해야 합니다.
    ```bash
    playwright install
    ```

3.  **환경 변수 설정:**

    -   `.env` 파일을 생성하고 Google API 키를 추가합니다.
        ```
        GOOGLE_API_KEY=your_google_api_key
        ```

4.  **챗봇 실행:**

    ```bash
    python main.py
    ```

    프로그램 실행 후, 프롬프트에 질문을 입력하면 챗봇이 답변을 제공합니다.

## 코드 구조

-   `main.py`: 메인 실행 파일. 사용자 입력 처리, 함수 호출, 결과 출력을 담당합니다.
-   `get_law_page_html(query)`: Playwright를 사용하여 국가법령정보센터 검색 결과를 HTML로 가져오는 비동기 함수입니다.
-   `ask_gemini_with_html(question, html_content)`: Gemini API에 HTML 내용과 질문을 함께 보내 답변을 받는 함수입니다.
-   `extract_urls(html_content)`: HTML 내용에서 URL을 추출하는 함수입니다.

## 기여

버그 수정, 기능 추가, 성능 개선 등 어떤 형태의 기여도 환영합니다. Pull Request를 통해 기여해주세요.

## 라이선스

MIT License

## 참고

-   국가법령정보센터: [https://www.law.go.kr/](https://www.law.go.kr/)
-   Playwright: [https://playwright.dev/](https://playwright.dev/)
-   Google Generative AI: [https://ai.google.dev/](https://ai.google.dev/)
-   BeautifulSoup: [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## 추가 개선사항 (To-Do)
- [ ] 사용자 인터페이스 개선 (ex: 웹 인터페이스, 챗봇 프레임워크 통합)
- [ ] 더 정확한 검색 결과 chunking 및 토큰 수 관리
- [ ] 검색 결과 필터링 옵션 추가 (ex: 법률, 시행령, 판례 등)
- [ ] 여러 검색 결과를 종합하여 답변하는 기능
- [ ] 테스트 코드 작성 및 CI/CD 구축
