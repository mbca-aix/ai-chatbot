# google 에서 제공하는 LLM API 를 사용하기
# Google AI Studio 플랫폼 사이트에서 키발급

# 라이브러리 설치
#pip install -q -U google-genai

#0. api key 는 노출되면 안됨. 그래서 별도의 환경변수파일 .env 에 저장하여 dotenv모듈로 불러서 적용
# 단, 우리의 챗봇을 streamlit cloud 에 배포할 예정. 애석하게 이곳은 .env 를 설정할 수 없음
# 그래서 streamlit에서 제공하는 비밀값을 저장하는 속성 secrets 를 활용 [secrets에 등록될 값들은 .streamlit폴더 안에 secrets.toml 파일로 등록. 이 파일을 GitHub를 통해 배포되면 안됨. 노출되면 일정시간 후에 정지됨. 다시 키발급 필요]
import streamlit as st
if "GEMINI_API_KEY" in st.secrets:
    api_key= st.secrets["GEMINI_API_KEY"]

#1. 라이브러리 사용
from google import genai
#2. 요청 사용자 객체 생성
client= genai.Client(api_key=api_key)

# 답변에 참고할 데이터를 리턴해주는 함수 만들기
import datetime
def get_today():
    """ 이 함수는 오늘의 날짜에 대한 답변에 사용됩니다.  """
    now= datetime.datetime.now()
    return {'location':'korea seoul', 'year':now.year, 'month':now.month, 'day':now.day }


# 응답 제어를 위한 하이퍼파라미터 설정
from google.genai import types
config= types.GenerateContentConfig(
    max_output_tokens=10000,
    response_mime_type='text/plain',
    #system_instruction='넌 만물박사야. 넌 최대 100글자안에서 어린이도 이해할 수 있게 뭐든 설명해.',
    #system_instruction='넌 모든 대답을 개조식으로 해.'
    system_instruction='넌 불량 고등학생이야. 비속어를 조금 사용하고 뭐든 100글자 안에 말해. 날짜에 관련된 질문 외에 다른 걸 물어보면. 미안하다고 해.',
    # 응답할때 특정 기능함수를 참고하여 답변.
    tools=[get_today],
)


# '질문'을 파라미터로 받아서 GET AI 로 응답한 글씨를 리턴해주는 기능함수 만들기
def get_ai_response(question):
    response= client._models.generate_content(
        model="gemini-3-flash-preview",
        #model="gemini-2.5-flash",
        contents=question,
        #모델의 응답방법을 설정하기 -하이퍼 파라미터 설정
        config= config
    )
    return response.text


#---------------------------------------------------------------
#3. 채팅 UI 만들기

#1) 페이지 기본 설정 -- 브라우저의 탭영역에 표시되는 내용.
st.set_page_config(
    page_title='AI 불량봇',
    page_icon='./logo/logo_chatbot.png'
)

#2) HEADER 영역 (레이아웃 : 이미지 + 제목 영역 가로 배치)
col1, col2= st.columns([1.2, 4.8])

with col1:
    st.image("./logo/logo_chatbot.png", width=200)

with col2:
    #제목(h1)+서브안내글씨(p) [색상을 다르게.. 하려면 HTML코드로 구현]
    st.markdown(
        """
        <h1 style='margin-bottom:0;'>AI 불량봇</h1>
        <p style='margin-top:0; color:gray'>이 챗봇은 모든 답변을 불량 고등학생처럼 합니다. 상처받지 마세요.</p>
        """,
        unsafe_allow_html=True
    )

#구분선
st.markdown("---")

#3) 채팅 UI 구현

#a. messages 라는 이름의 변수가  session_state에 존재하는지 확인. 후 없으면 첫 문자 지정
if "messages" not in st.session_state:
    st.session_state.messages= [
        {'role':'assistant', 'content':'무엇이든 물어봐!'},
    ]

#b. sesstion_state에 저장된 "messages"의 메세지들을 채팅 UI로 그려내기
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

#c. 사용자 채팅메세지를 입력받아 session_state에 저장하고 UI 갱신
question= st.chat_input('질문을 입력해보든가.')
if question:
    question= question.replace('\n','  \n')
    st.session_state.messages.append({'role':'user','content':question})
    st.chat_message('user').write(question)

    #응답 - AI 응답요구기능 함수 호출 ... 응답대기 시간동안 보여줄 스피터 프로그래스 요소 필요
    with st.spinner('AI가 응답 중입니다... 잠시만 기다리세요.'):
        response= get_ai_response(question)
        st.session_state.messages.append({'role':'assistant', 'content':response})
        st.chat_message('assistant').write(response)

#----------------------------------------------------------
# streamlit 웹앱 배포
#1. streamlit community cloud 배포
#2. GitHub에 프로젝트를 업로드
#3. new app 을 통해 앱을 만들어 Github 저장소와 연결
#4. 자동 배포됨.
