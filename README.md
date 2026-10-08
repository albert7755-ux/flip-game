[Uploading README (8).md…]()
# 固收七人組 Team Match

認人翻牌遊戲：14 張牌、7 組，翻開名字再翻出本人就配成一對。七組全對後會解鎖團隊合照和一段結語。任何人開網址就能玩，輸入名字就上共同排行榜。

---

## 檔案

| 檔案 | 做什麼的 |
|---|---|
| `app.py` | Streamlit 外殼 |
| `game.html` | 遊戲本體（名字、照片、排行榜） |
| `requirements.txt` | 要安裝的套件 |

七張個人照和一張團隊合照都包在 `game.html` 裡，不用另外放圖檔。

---

## 部署

比「債速配」簡單，因為 **Supabase 不用重做** —— 用同一個專案、同一張 `flip_scores` 表就好。

1. GitHub 開一個新的 repository，例如 `team-match`
2. 把 `app.py`、`game.html`、`requirements.txt` 三個檔案上傳進去
3. [share.streamlit.io](https://share.streamlit.io) → **New app** → 選這個 repo，Main file path 填 `app.py` → **Deploy**
4. 部署完 → **⋮ → Settings → Secrets**，貼上跟債速配**一模一樣**的那兩行：

```toml
SUPABASE_URL = "https://你的專案代號.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi...（很長一串）"
```

5. 存檔，等 App 重開，打一輪試試看

排行榜用 `BOARD_ID = "fi-team-7"`，跟債速配的 `nvda-bond-11` 分開算，兩邊成績不會混在一起。

---

## 先在自己電腦看看

不想先部署也可以：把 `game.html` 下載下來，**直接點兩下**用瀏覽器打開就能玩。
照片、配對、計時、成員名單都正常，只有排行榜會顯示讀取失敗（因為沒接上資料庫）。

---

## 平常怎麼改

### 改名字或換照片

`game.html` 裡找到 `PEOPLE` 這一段（`<script>` 開頭附近，有註解標示）：

```javascript
{ id: "p1", zh: "惟恂", en: "VALERIE", photo: "data:image/jpeg;base64,/9j/..." }
```

- `zh` 是牌面上的大字
- `en` 是底下的小字
- `photo` 是照片，很長一串 base64

改名字直接改 `zh` / `en` 就好。換照片的話把新照片給 Claude，它會轉好整行給你貼。

### 加人或減人

照上面的格式增減一列就好，`id` 不要重複。牌數會自動跟著變（人數 × 2），版面也會自己排。

### 加職稱或負責業務

目前「成員名單」只顯示名字。想加職稱和負責業務，把內容給 Claude，它幫你加欄位。

### 改結語那段話

`game.html` 裡搜尋 `恭喜你全部認完`，那一整塊 `<section class="sheet finale">` 就是結語區，
標題和兩段內文直接改文字即可。要換合照的話把新照片給 Claude。

結語看過一次就會記在瀏覽器裡，之後再進來不用重玩也看得到。
想讓它重新鎖回去（例如你改了文案想重看解鎖動畫），清掉瀏覽器資料就好。

### 清掉排行榜

Supabase → SQL Editor：

```sql
delete from public.flip_scores where board = 'fi-team-7';
```

---

## 常見狀況

**畫面被切掉 / 下面一大片空白**
`app.py` 裡的 `FRAME_HEIGHT = 1900`，被切到就調大，空太多就調小。
這個數字是抓「結語合照展開後」的高度，所以還沒破關前下面會有一段空白，是正常的。

**排行榜讀取失敗**
錯誤訊息會直接寫原因。多半是 Secrets 沒填或填錯。

**同事說打不開**
Streamlit Cloud 免費版太久沒人用會睡著，第一個開的人要等 30 秒左右。

---

## 提醒

這個網址是公開的，拿到連結的人都看得到這七張照片和名字。發到內部群組沒問題，但發之前記得跟七位同仁說一聲。
