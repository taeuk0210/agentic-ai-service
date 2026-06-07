# agentic-ai-service

agentic ai service backbone structure

```bash
User(API)        Agent(Orchestrator)        Service(Chat/LLM/Tool)        Infra(Cache/LLM/VDB)
    |                     |                           |                              |
    |---- UserRequest --->|                           |                              |
    |                     |------ validate_user ----->|                              |
    |                     |    (세션ID, 접근권한)     |                              |
    |                     |                           |                              |
    |                     |---- validate_content ---->|                              |
    |                     |     (user_input 검증)     |--(Prompt Injection 체크)->[ LLM ]
    |                     |                           |                              |
    |                     |--- get_chat_histories --->|                              |
    |                     |   (이전 대화 목록 조회)   |---(과거 대화 이력 획득)-->[Cache]
    |                     |                           |                              |
    |                     |---- route_user_intent --->|                              |
    |                     |   (의도 파악 및 라우팅)   |---(필요한 툴 목록 분류)-->[ LLM ]
    |                     |                           |                              |
    |                     |--- execute (Parallel) --->|                           [ API ]
    |                     |   (비동기 툴 병렬실행)    |---(문서 검색/외부 API)--->[ VDB ]
    |                     |                           |                           [EMBED]
    |                     |--- request_user_input --->|                              |
    |                     |   (최종 답변 생성 요청)   |--(컨텍스트 결합 후 추론)->[ LLM ]
    |                     |                           |                              |
    |                     |---- validate_content ---->|                              |
    |                     |    (agent_output 검증)    |---(탈옥/정보 유출 체크)-->[ LLM ]
    |                     |                           |                              |
    |                     |--- set_chat_histories --->|                              |
    |                     |   (신규 대화 이력 누적)   |--(대화 쌍 적재 및 갱신)-->[Cache]
    |                     |                           |                              |
    |<-- UserResponse ----|                           |                              |
```