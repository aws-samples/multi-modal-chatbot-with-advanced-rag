import base64
import streamlit as st  # 모든 streamlit 명령은 "st" alias로 사용할 수 있습니다.
import bedrock as glib  # 로컬 라이브러리 스크립트에 대한 참조
from langchain.callbacks import StreamlitCallbackHandler

##################### Functions ########################
def parse_image(metadata, tag):
    if tag in metadata: 
        st.image(base64.b64decode(metadata[tag]))

def parse_table(metadata, tag):
    if tag in metadata:
        st.markdown(metadata[tag], unsafe_allow_html=True)

def parse_metadata(metadata):
    # Image, Table 이 있을 경우 파싱해 출력
    category = "None"
    if "category" in metadata:
        category = metadata["category"]
        if category == "Table":
            # parse_table(metadata, "text_as_html") # 테이블 html은 이미지로 대체
            parse_image(metadata, "image_base64")
        elif category == "Image":
            parse_image(metadata, "image_base64")
        else: 
            pass
    st.markdown(' - - - ')

def show_document_info_label():
    with st.container(border=True):
        if st.session_state.document_type == "Default":
            st.markdown('''📝 현재 기본 문서인 [**상록초등학교 교육 과정 문서**](https://d14ojpq4k4igb1.cloudfront.net/school_edu_guide.pdf)를 활용하고 있습니다.''')
            st.markdown('''다른 문서로 챗봇 서비스를 이용해보고 싶다면 왼쪽 사이드바의 Document type에서 *'Custom'* 옵션을 클릭하고, 진행자의 안내에 따라 문서를 새로 인덱싱하여 사용해보세요.''')
        else:
            st.markdown('''**💁‍♀️ 새로운 문서로 챗봇 서비스를 이용하고 싶으신가요?**''') 
            st.markdown('''- **진행자의 안내에 따라 SageMaker Notebook에서 인덱싱 스크립트를 실행한 뒤** 이용 가능합니다.''')
            st.markdown('''- 기존 문서 (상록초등학교 교육 과정)로 돌아가고 싶다면 사이드바의 Document type에서 *'Default'* 옵션을 선택하면 바로 변경할 수 있습니다.''')
    
# 'Separately' 옵션 선택 시 나오는 중간 Context를 탭 형태로 보여주는 UI
def show_context_with_tab(contexts):
    tab_category = ["Semantic", "Keyword", "Without Reranker", "Similar Docs"]
    tab_contents = {
        tab_category[0]: [],
        tab_category[1]: [],
        tab_category[2]: [],
        tab_category[3]: []
    }
    for i, contexts_by_doctype in enumerate(contexts):
        tab_contents[tab_category[i]].append(contexts_by_doctype)
    tabs = st.tabs(tab_category)
    for i, tab in enumerate(tabs):
        category = tab_category[i]
        with tab:
            for contexts_by_doctype in tab_contents[category]:
                for context in contexts_by_doctype:
                    st.markdown('##### `정확도`: {}'.format(context["score"]))
                    for line in context["lines"]:
                        st.write(line)
                    parse_metadata(context["meta"])
                    
# 'All at once' 옵션 선택 시 4개의 컬럼으로 나누어 결과 표시하는 UI
# TODO: HyDE, RagFusion 추가 논의 필요
def show_answer_with_multi_columns(answers): 
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('''### `Lexical search` ''')
        st.write(answers[0])
    with col2:
        st.markdown('''### `Semantic search` ''')
        st.write(answers[1])
    with col3:
        st.markdown('''### + `Reranker` ''')
        st.write(answers[2])
    with col4:
        st.markdown('''### + `Parent_docs` ''') 
        st.write(answers[3])

####################### Application ###############################
st.set_page_config(layout="wide")
st.title("AWS Q&A Bot with Advanced RAG!")  # page 제목

st.markdown('''- 이 챗봇은 Amazon Bedrock과 Claude v3 Sonnet 모델로 구현되었습니다.''')
st.markdown('''- 다음과 같은 Advanced RAG 기술을 사용합니다: **Hybrid Search, ReRanker, and Parent Document, HyDE, Rag Fusion**''')
st.markdown('''- 원본 데이터는 Amazon OpenSearch에 저장되어 있으며, Amazon Titan 임베딩 모델이 사용되었습니다.''')
st.markdown('''    ''')

# Store the initial value of widgets in session state
if "document_type" not in st.session_state:
    st.session_state.document_type = "Default"
if "showing_option" not in st.session_state:
    st.session_state.showing_option = "Separately"
if "search_mode" not in st.session_state:
    st.session_state.search_mode = "Hybrid search"
if "hyde_or_ragfusion" not in st.session_state:
    st.session_state.hyde_or_ragfusion = "None"
disabled = st.session_state.showing_option=="All at once"

with st.sidebar: # Sidebar 모델 옵션
    with st.container(border=True):
        st.radio(
            "Document type:",
            ["Default", "Custom"],
            captions = ["챗봇이 참고하는 자료로 기본 문서(상록초등학교 자료)가 사용됩니다.", "원하시는 문서를 직접 업로드해보세요."],
            key="document_type",
        )
    with st.container(border=True):
        st.radio(
            "UI option:",
            ["Separately", "All at once"],
            captions = ["아래에서 설정한 파라미터 조합으로 하나의 검색 결과가 도출됩니다.", "여러 옵션들을 한 화면에서 한꺼번에 볼 수 있습니다."],
            key="showing_option",
        )
    st.markdown('''### Set parameters for your Bot 👇''')
    with st.container(border=True):
        search_mode = st.radio(
            "Search mode:",
            ["Lexical search", "Semantic search", "Hybrid search"],
            captions = [
                "키워드의 일치 여부를 기반으로 답변을 생성합니다.",
                "키워드의 일치 여부보다는 문맥의 의미적 유사도에 기반해 답변을 생성합니다.", 
                "아래의 Alpha 값을 조정하여 Lexical/Semantic search의 비율을 조정합니다."
                ],
            key="search_mode",
            disabled=disabled
            )
        alpha = st.slider('Alpha value for Hybrid search ⬇️', 0.0, 1.0, 0.51, 
                          disabled=st.session_state.search_mode != "Hybrid search",
                          help="""Alpha=0.0 이면 Lexical search,   \nAlpha=1.0 이면 Semantic search 입니다."""
                          )
        if search_mode == "Lexical search":
            alpha = 0.0
        elif search_mode == "Semantic search":
            alpha = 1.0

    col1, col2 = st.columns(2)
    with col1:
        reranker = st.toggle("Reranker", 
                             help="""초기 검색 결과를 재평가하여 순위를 재조정하는 모델입니다.   
                             문맥 정보와 질의 관련성을 고려하여 적합한 결과를 상위에 올립니다.""",
                             disabled=disabled)
    with col2:
        parent = st.toggle("Parent Docs", 
                           help="""답변 생성 모델이 질의에 대한 답변을 생성할 때 참조한 정보의 출처를 표시하는 옵션입니다.""", 
                           disabled=disabled)

    with st.container(border=True):
        hyde_or_ragfusion = st.radio(
            "Choose a RAG option:",
            ["None", "HyDE", "RAG-Fusion"],
            captions = [
                "", 
                "문서와 질의 간의 의미적 유사도를 측정하기 위한 임베딩 기법입니다. 하이퍼볼릭 공간에서 거리를 계산하여 유사도를 측정합니다.", 
                "검색과 생성을 결합한 모델로, 검색 모듈이 관련 문서를 찾고 생성 모듈이 이를 참조하여 답변을 생성합니다. 두 모듈의 출력을 융합하여 최종 답변을 도출합니다."
                ],
            key="hyde_or_ragfusion",
            disabled=disabled
            ) 
        hyde = hyde_or_ragfusion == "HyDE"
        ragfusion = hyde_or_ragfusion == "RAG-Fusion"

###### 'Separately' 옵션 선택한 경우 ######
if st.session_state.showing_option == "Separately":
    show_document_info_label()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요, 무엇이 궁금하세요?"}
        ]
    # 지난 답변 출력
    for msg in st.session_state.messages:
        # 지난 답변에 대한 컨텍스트 출력
        if msg["role"] == "assistant_context": 
            with st.chat_message("assistant"):
                with st.expander("Context 확인하기 ⬇️"):
                    show_context_with_tab(contexts=msg["content"])
                    
        elif msg["role"] == "hyde_or_fusion":
            with st.chat_message("assistant"):
                with st.expander("중간 답변 확인하기 ⬇️"):
                    msg["content"]
                    
        elif msg["role"] == "assistant_column":
            # 'Separately' 옵션일 경우 multi column 으로 보여주지 않고 첫 번째 답변만 출력
            st.chat_message(msg["role"]).write(msg["content"][0]) 
        else:
            st.chat_message(msg["role"]).write(msg["content"])
    
    # 유저가 쓴 chat을 query라는 변수에 담음
    query = st.chat_input("Search documentation")
    if query:
        # Session에 메세지 저장
        st.session_state.messages.append({"role": "user", "content": query})
        
        # UI에 출력
        st.chat_message("user").write(query)
        
        # Streamlit callback handler로 bedrock streaming 받아오는 컨테이너 설정
        st_cb = StreamlitCallbackHandler(
            st.chat_message("assistant"), 
            collapse_completed_thoughts=True
            )
        # bedrock.py의 invoke 함수 사용
        response = glib.invoke(
            query=query, 
            streaming_callback=st_cb, 
            parent=parent, 
            reranker=reranker,
            hyde = hyde,
            ragfusion = ragfusion,
            alpha = alpha,
            document_type=st.session_state.document_type
        )
        # response 로 메세지, 링크, 레퍼런스(source_documents) 받아오게 설정된 것을 변수로 저장
        answer = response[0]
        contexts = response[1]
        if hyde or ragfusion:
            mid_answer = response[2]

        # UI 출력
        st.chat_message("assistant").write(answer)
        
        if hyde:
            with st.chat_message("assistant"):
                with st.expander("HyDE 중간 생성 답변 ⬇️"):
                    mid_answer
        if ragfusion:
            with st.chat_message("assistant"):
                with st.expander("RAG-Fusion 중간 생성 쿼리 ⬇️"):
                    mid_answer  
        with st.chat_message("assistant"): 
            with st.expander("정확도 별 컨텍스트 보기 ⬇️"):
                show_context_with_tab(contexts)
        
        # Session 메세지 저장
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        if hyde or ragfusion:
            st.session_state.messages.append({"role": "hyde_or_fusion", "content": mid_answer})

        st.session_state.messages.append({"role": "assistant_context", "content": contexts})
        # Thinking을 complete로 수동으로 바꾸어 줌
        st_cb._complete_current_thought()

###### 2) 'All at once' 옵션 선택한 경우 ######
else:
    with st.container(border=True):
        st.markdown('''현재 기본 문서인 [상록초등학교 교육 과정 문서](https://file.notion.so/f/f/d82c0c1c-c239-4242-bd5e-320565fdc9d4/6057662b-2d01-4284-a65f-cc17d050a321/school_edu_guide.pdf?id=a2f7166b-f663-4740-aa06-ec559567011a&table=block&spaceId=d82c0c1c-c239-4242-bd5e-320565fdc9d4&expirationTimestamp=1718100000000&signature=wxS5AgYuK085mNvynkUZsRyqyMuqE_ucoCNfM4jRnU0&downloadName=school_edu_guide.pdf)를 활용하고 있습니다.''')
        st.markdown('''다른 문서로 챗봇 서비스를 이용해보고 싶다면 왼쪽 사이드바의 Document type에서 'Custom' 옵션을 클릭해 문서를 업로드해보세요.''')
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요, 무엇이 궁금하세요?"}
        ]
    # 지난 답변 출력
    for msg in st.session_state.messages:
        if msg["role"] == "assistant_column":
            answers = msg["content"]
            show_answer_with_multi_columns(answers)
        elif msg["role"] == "assistant_context": 
            pass # 'All at once' 옵션 선택 시에는 context 로그를 출력하지 않음
        else:
            st.chat_message(msg["role"]).write(msg["content"])
    
    # 유저가 쓴 chat을 query라는 변수에 담음
    query = st.chat_input("Search documentation")
    if query:
        # Session에 메세지 저장
        st.session_state.messages.append({"role": "user", "content": query})
        
        # UI에 출력
        st.chat_message("user").write(query)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('''### `Lexical search` ''')
            st.markdown(":green[: Alpha 값이 0.0]으로, 키워드의 정확한 일치 여부를 판단하는 Lexical search 결과입니다.")
        with col2:
            st.markdown('''### `Semantic search` ''')
            st.markdown(":green[: Alpha 값이 1.0]으로, 키워드 일치 여부보다는 문맥의 의미적 유사도에 기반한 Semantic search 결과입니다.")
        with col3:
            st.markdown('''### + `Reranker` ''')
            st.markdown(""": 초기 검색 결과를 재평가하여 순위를 재조정하는 모델입니다. 문맥 정보와 질의 관련성을 고려하여 적합한 결과를 상위에 올립니다.
                        :green[Alpha 값은 왼쪽 사이드바에서 설정하신 값]으로 적용됩니다.""")
        with col4:
            st.markdown('''### + `Parent Docs` ''')
            st.markdown(""": 질의에 대한 답변을 생성할 때 참조하는 문서 집합입니다. 답변 생성 모델이 참조할 수 있는 관련 정보의 출처가 됩니다.
                        :green[Alpha 값은 왼쪽 사이드바에서 설정하신 값]으로 적용됩니다.""")
        
        with col1:
            # Streamlit callback handler로 bedrock streaming 받아오는 컨테이너 설정
            st_cb = StreamlitCallbackHandler(
                st.chat_message("assistant"), 
                collapse_completed_thoughts=True
                )
            answer1 = glib.invoke(
                query=query, 
                streaming_callback=st_cb, 
                parent=False, 
                reranker=False,
                hyde = False,
                ragfusion = False,
                alpha = 0, # Lexical search
                document_type=st.session_state.document_type
                )[0]
            st.write(answer1)
            st_cb._complete_current_thought() # Thinking을 complete로 수동으로 바꾸어 줌
        with col2:
            st_cb = StreamlitCallbackHandler(
                st.chat_message("assistant"), 
                collapse_completed_thoughts=True
                )
            answer2 = glib.invoke(
                query=query, 
                streaming_callback=st_cb, 
                parent=False, 
                reranker=False,
                hyde = False,
                ragfusion = False,
                alpha = 1.0, # Semantic search
                document_type=st.session_state.document_type
                )[0]
            st.write(answer2)
            st_cb._complete_current_thought() 
        with col3:
            st_cb = StreamlitCallbackHandler(
                st.chat_message("assistant"), 
                collapse_completed_thoughts=True
                )
            answer3 = glib.invoke(
                query=query, 
                streaming_callback=st_cb, 
                parent=False, 
                reranker=True, # Add Reranker option
                hyde = False,
                ragfusion = False,
                alpha = alpha, # Hybrid search
                document_type=st.session_state.document_type
                )[0]
            st.write(answer3)
            st_cb._complete_current_thought() 
        with col4:
            st_cb = StreamlitCallbackHandler(
                st.chat_message("assistant"), 
                collapse_completed_thoughts=True
            )
            answer4 = glib.invoke(
                query=query, 
                streaming_callback=st_cb, 
                parent=True, # Add Parent_docs option
                reranker=True, # Add Reranker option
                hyde = False,
                ragfusion = False,
                alpha = alpha, # Hybrid search
                document_type=st.session_state.document_type
                )[0]
            st.write(answer4)
            st_cb._complete_current_thought()

        # Session 메세지 저장
        answers = [answer1, answer2, answer3, answer4]
        st.session_state.messages.append({"role": "assistant_column", "content": answers})
