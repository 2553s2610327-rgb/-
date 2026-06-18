# -------------------------
        # 결과 출력 및 아카이브 저장
        # -------------------------
        st.success("🎉 자리 배치 완료!")

        # 아카이브 저장을 위한 데이터 구조화
        current_layout = []
        index = 0
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                row_cells.append(names[index])
                index += 1
            current_layout.append(row_cells)
        
        # 세션 스테이트 초기화 및 저장
        if "archive" not in st.session_state:
            st.session_state.archive = []
            
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 중복 저장 방지를 위한 간단한 체크
        if not st.session_state.archive or st.session_state.archive[0]["layout"] != current_layout:
            st.session_state.archive.insert(0, {
                "id": time.time(),
                "time": now,
                "rows": rows,
                "cols": cols,
                "layout": current_layout
            })

        # 화면에 그리기
        for r in range(rows):
            cols_ui = st.columns(cols)
            for c in range(cols):
                name = current_layout[r][c]
                if name == "빈자리":
                    cols_ui[c].markdown(
                        "<div style='text-align:center; padding:15px; border-radius:10px; background-color:#eeeeee;'>🪑 빈자리</div>",
                        unsafe_allow_html=True
                    )
                else:
                    cols_ui[c].markdown(
                        f"<div style='text-align:center; padding:15px; border-radius:10px; background-color:#d1e7dd; font-weight:bold;'>{name}</div>",
                        unsafe_allow_html=True
                    )
