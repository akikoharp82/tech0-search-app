# search_pages() の全体 — コメントを手がかりに自分で書いてみよう

def search_pages(query: str, pages: list) -> list:
    # ↑ 「: str」「: list」は型ヒント / 「-> list」は戻り値の型宣言

    # ① キーワードが空欄ならすぐ終了（空リストを返す）
    # ↓ ここにコードを書いてください
    if not query.strip():
        return []

    # ② 結果を入れる空のリストを用意
    # ↓ ここにコードを書いてください
    results = [] 

    # ③ query を小文字に統一（.lower() を使う）
    # ↓ ここにコードを書いてください
    query_lower = query.lower()
    # ④ ページを1件ずつ取り出してループ（for ループ）
    # ↓ ここにコードを書いてください
    for page in pages:
        # ⑤ title + description + keywords を1つの文字列に結合
        # ↓ ここにコードを書いてください
        search_text = " ".join({
            page["title"],
            page["description"],
            " ".join(page["keywords"]),
        })
        # ⑥ キーワードが含まれていたら results に追加（.append() を使う）
        # ↓ ここにコードを書いてください
        if query_lower in search_text.lower():
            results.append(page)
    # ⑦ マッチしたページのリストを return する
    # ↓ ここにコードを書いてください
    return results

import re  # re = Regular Expression（正規表現）標準ライブラリ、pip install 不要

def highlight_match(text: str, query: str) -> str:

    if not query:       # キーワードが空なら何もしない
        return text

    # re.compile() でパターンを作る
    # re.escape(query) で特殊文字を安全に扱う / re.IGNORECASE で大文字小文字を区別しない
    # ↓ ここにコードを書いてください
    pattern =re.compile(
        re.escape(query),
        re.IGNORECASE
    )

    # pattern.sub(置換後, 元テキスト) でマッチ部分を置換する
    # 「**DX**」← Markdown で ** で囲むと太字になる
    # ↓ ここにコードを書いてください（return も含む）
    return pattern.sub(f"**{query}**", text)

