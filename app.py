# ① ライブラリのインポート
import streamlit as st
import json
from search import search_pages, highlight_match   # Step3 で学んだ関数！
from datetime import datetime

# ② データの読み書き関数（Step2 で学んだ json.load / json.dump を使う）

def load_pages():
    with open("pages.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_pages(pages):
    with open("pages.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

# ③ ページ設定・タイトル
st.set_page_config(
    page_title='Tech0 Search v0.1',
    page_icon='🔍'
)
st.title('🔍 Tech0 Search v0.1')
st.caption('PROJECT ZERO ーTech0 12期プロフィール検索ー')

# ④ タブを作る
tab1, tab2, tab3 = st.tabs(['🔍 検索', '📝 登録', '📚 一覧'])
pages = load_pages()

# ⑤ 検索タブ
with tab1:
    query = st.text_input(
        'キーワードを入力して「検索」を押してください',
        placeholder='例：DX、新規事業'
    )
    search_clicked = st.button('🔍 検索')

    if query and search_clicked:
        results = search_pages(query, pages)
        st.caption(f"検索結果：{len(results)}件")

        if results:
            for page in results:
                st.divider()
                st.markdown(
                    f"<h3 style='color:#2E8B57;'>{page['title']}</h3>",
                    unsafe_allow_html=True
                )
                st.markdown(highlight_match(page['description'], query))
                st.write(f"👤 担当: {page['author']}")
                st.write(f"🏷️ キーワード: {', '.join(page['keywords'])}")
                
                if page.get("url"):
                    st.markdown(
                        f'🔗 <a href="{page["url"]}" target="_blank">{page["url"]}</a>',
                        unsafe_allow_html=True
                    )

                st.write(f"🕒 登録日: {page.get('created_at', '未設定')}")
        else:
            st.info("該当するページはありませんでした。")

# ⑥ 登録タブ
with tab2:
    st.subheader("新規ページの登録")
    st.caption("新しく追加したいページ情報を入力してください。登録後、自動で一覧に反映されます。")

    if st.session_state.get("register_success"):
        st.success("登録完了しました。")
        st.session_state["register_success"] = False

    with st.form("register_form", clear_on_submit=True, enter_to_submit=False):
        title = st.text_input("タイトル")
        description = st.text_area("説明文")
        author = st.text_input("担当者")
        category = st.selectbox(
            "カテゴリー",
            ["自己紹介", "研究紹介", "業務紹介", "ブログ", "その他"]
        )
        keywords_text = st.text_input(
            "キーワード（カンマ区切り）",
            placeholder="例：DX, 新規事業, AI"
        )
        url = st.text_input("URL", placeholder="https://example.com")

        submitted = st.form_submit_button("登録する")

    if submitted:
        existing_ids = [page.get("id", 0) for page in pages]
        new_id = max(existing_ids, default=0) + 1

        new_page = {
            "id": new_id,
            "title": title,
            "description": description,
            "author": author,
            "category": category,
            "keywords": [k.strip() for k in keywords_text.split(",") if k.strip()],
            "url": url,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        pages.append(new_page)
        save_pages(pages)

        st.session_state["register_success"] = True
        st.rerun()

# ⑦ 一覧タブ
with tab3:
    st.subheader("登録ページ一覧")
    st.caption("登録済みのページを新しい順に表示しています。タイトルを押すと詳細を確認できます。")

    sorted_pages = sorted(
        pages,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    st.markdown(f"**登録総数：{len(sorted_pages)}件**")

    for page in sorted_pages:
        with st.expander(page['title']):
            st.write(f"🕒 登録日: {page.get('created_at', '未設定')}")
            st.write(f"📄 説明文: {page['description']}")
            st.write(f"👤 担当者: {page['author']}")
            st.write(f"📂 カテゴリー: {page.get('category', '未設定')}")
            st.write(f"🏷️ キーワード: {', '.join(page['keywords'])}")

            if page.get("url"):
                st.markdown(
                    f'🔗 <a href="{page["url"]}" target="_blank">{page["url"]}</a>',
                    unsafe_allow_html=True
                )
            else:
                st.write("🔗 URL: 未設定")