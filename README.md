# agentic-ai-service
agentic ai service backbone structure
```bash
유저(Client)      Agent(Orchestrator)    Auth/Guard/Intent/Tool    Infra(Cache/DB/VDB)
     │                     │                     │                     │
     │── 1. UserRequest ──▶│                     │                     │
     │   (query, session)  │                     │                     │
     │                     │── 2. UserContext 생성                     │
     │                     │      (raw_query)    │                     │
     │                     │                     │                     │
     │                     │── 3. validate_input(raw_query) ──────────▶│
     │                     │◀─ 4. clean_query 반환 ────────────────────│
     │                     │                     │                     │
     │                     │── 5. get_accessible_knowledge_sources() ─▶│
     │                     │                     │                     │── 6. 권한 조회 (RDB)
     │                     │◀─ 7. accessible_sources 반환 ─────────────│
     │                     │                     │                     │
     │                     │── 8. route_request(clean_query, sources) ▶│
     │                     │◀─ 9. tool_name, params 반환 ──────────────│
     │                     │                     │                     │
     │                     │── 10. execute(tool_name, params) ────────▶│
     │                     │                     │                     │── 11. 유사도 검색 (VDB)
     │                     │◀─ 12. tool_result_context 반환 ───────────│
     │                     │                     │                     │
     │                     │── 13. generate_response(prompt) ─────────▶│ (LLM Service)
     │                     │                     │                     │── 14. API 호출 (LLM Infra)
     │                     │◀─ 15. llm_response 반환 ──────────────────│
     │                     │                     │                     │
     │                     │── 16. validate_output(llm_response) ─────▶│
     │                     │◀─ 17. final_answer 반환 ──────────────────│
     │                     │                     │                     │
     │                     │──────────────────────────────────────────▶│ 18. 대화기록 세션 저장 (Redis)
     │                     │──────────────────────────────────────────▶│ 19. 대화로그 및 피드백 영속 저장 (RDB)
     │                     │                     │                     │
     │◀─ 20. AgentResponse─│                     │                     │
     │   (final_answer)    │                     │                     │
     ```