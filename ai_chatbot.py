#0. 모듈 설치
#pip install streamlit
#pip install openai
#pip install dotenv

#1. 환경변수 .env 파일의 openai api key 값을 읽어오는 모듈 사용
from dotenv import load_dotenv
load_dotenv()

#2. OpenAI 생성형 api를 요청하는 객체생성
from openai import OpenAI
client= OpenAI()

# 사용자 '질문'을 파라미터로 받아 OPENAI API로 응답한 글씨를 리턴해주는 기능함수 만들기
def get_ai_response(question):
    response= client.responses.create(
        model='gpt-4o-mini',
        max_output_tokens=10000,
        temperature=1.5,
        instructions='너는 고양이야. 이름은 네코냥이야. 고양이처럼 답변해.', #지침(프롬프트엔지니어링 기법 적용될수 있음.)

        input=question,  #사용자의 질문
    )

    #응답결과중 메타데이터를 제외한 응답글씨를 리턴!
    return response.output_text
#-----------------------------------------------------

#3. 채팅 UI 만들기
import streamlit as st

#1] 페이지 기본설정 - 브라우저의 탭영역에 표시되는 내용
st.set_page_config(
    page_title='AI 네코냥봇',
    page_icon='./logo/logo_nekonyang.png'
)

#2] 화면을 2개의 영역으로 분리
col1, col2= st.columns([1.2, 4.8])

with col1:
    st.image('./logo/logo_nekonyang.png', width=200)

with col2:
    #화면을 HTML로 만들어보기
    st.markdown(
        '''
        <h1 style='margin-bottome:0;'>AI 네코냥😹봇</h1>
        <p style='color:gray; margin-top:0;'>이 챗봇은 모든 답변을 고양이처럼 합니다. 일상의 소소한 이야기를 나눠요.</p>
        ''',
        unsafe_allow_html=True
    )

#구분선
st.markdown('---')

#a. messages 라는 이름의 변수가 st.session_state에 있는지 확인 후 첫 메세지 저장
if "messages" not in st.session_state:
    st.session_state.messages= [{'role':'assistant', 'content':'무엇이든 물어보세요.'}]

#b. 저장된 메세지들을 화면에 표시(이전 메세지들이 표시되는 역할)
for msg in st.session_state.messages:
    st.chat_message(msg['role']).markdown(msg['content'])

#c. 사용자 채팅메세지를 입력받아 session_state에 저장하고 화면에 표시
question= st.chat_input('질문을 입력하세요.')
if question:
    question= question.replace('\n','  \n')
    st.session_state.messages.append({'role':'user','content':question})
    st.chat_message('user').markdown(question)

    #응답 - AI 응답요구 기능 함수 호출....[응답할때까지 시간이 걸리기에...spinner]
    with st.spinner('AI 네코냥봇이 응답 중입니다... 잠시만 기다려 주세요.'):
        response= get_ai_response(question=question)
        st.session_state.messages.append({'role':'assistant','content':response})
        st.chat_message('assistant').markdown(response)




#-------------------------------------------
#[실행] 터미널에서 streamlit run 파일명.py


#---------------------------------------
#[배포] 스트림릿으로 만든 웹앱을 배포 [streamlit은 기본적으로 html/css/js 로 변환해주는 기능은 없음]

# Streamlit Community Cloud 배포
#1) 프로젝트 GitHub에 업로드
#2) Streamlit Cloud 접속 및 (GitHub계정)로그인
#3) [New app]버튼을 클릭 후 GitHub 저장소를 선택
#4) 그러면 자동으로 배포됨(도메일 일부 수정 가능)
