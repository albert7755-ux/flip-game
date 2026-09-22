[README (5).md](https://github.com/user-attachments/files/32497306/README.5.md)
# 債速配 Bond Match 排位賽

債券條件配對小遊戲，任何人開網址就能玩、輸入名字就上共同排行榜，**不需要註冊任何帳號**。

---

## 檔案有哪些

| 檔案 | 做什麼的 | 你會不會需要改 |
|---|---|---|
| `app.py` | Streamlit 外殼，負責把遊戲顯示出來 | 幾乎不用 |
| `game.html` | 遊戲本體（牌面、條件、排行榜） | 換債券時改這支 |
| `schema.sql` | Supabase 建表用的指令 | 只跑一次 |
| `requirements.txt` | 要安裝的套件 | 不用 |

照片已經包在 `game.html` 裡面了，不用另外放圖檔。

---

## 部署步驟

整個流程大概 15 分鐘，分成三段：先開資料庫、再上傳程式、最後把兩邊接起來。

### 第一段：開 Supabase 資料庫（放排行榜的地方）

1. 到 [supabase.com](https://supabase.com) 登入，點 **New project**
2. 專案名稱隨便取，密碼記下來（其實後面用不到），地區選 **Northeast Asia (Tokyo)** 比較快
3. 等它建好（約 2 分鐘）
4. 左邊選單點 **SQL Editor** → **New query**
5. 把 `schema.sql` **整份貼進去** → 按右下角 **Run**
6. 看到綠色的 `Success` 就成功了

接著把連線資訊抄下來：

7. 左下角 **Project Settings**（齒輪）→ **API**
8. 抄兩個東西：
   - **Project URL**：長得像 `https://abcdefgh.supabase.co`
   - **Project API keys** 底下的 **`anon` `public`** 那一把：很長一串 `eyJ...`

> ⚠️ 只抄 `anon public` 那一把。旁邊還有一把 `service_role`，那把是管理員金鑰，**絕對不要**放進程式裡。

### 第二段：把程式放上 GitHub

1. 在 GitHub 開一個新的 repository，例如 `nvda-flip`
2. 把這四個檔案上傳進去：`app.py`、`game.html`、`requirements.txt`、`schema.sql`
   （不熟 git 的話，GitHub 網頁上 **Add file → Upload files** 直接拖進去就好）

### 第三段：部署到 Streamlit Cloud 並接上資料庫

1. 到 [share.streamlit.io](https://share.streamlit.io) → **New app**
2. 選剛剛那個 repository，Main file path 填 `app.py` → **Deploy**
3. 部署完成後，右下角 **⋮ → Settings → Secrets**
4. 貼上這兩行，把值換成你第一段抄的：

```toml
SUPABASE_URL = "https://你的專案代號.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi...（很長一串）"
```

5. 按 **Save**，App 會自己重開
6. 重開後打一輪、填名字，排行榜出現你的名字就成功了

網址直接發給同事，他們點開就能玩。

---

## 平常怎麼維護

### 換成另一檔債券

打開 `game.html`，找到這兩個地方（都在 `<script>` 開頭附近，有註解標示）：

**① 排行榜代號** — 換一檔債就換一個 id，排行榜才不會混在一起：

```javascript
var BOARD_ID = "nvda-bond-11";        // 改成例如 "msft-bond-03"
```

**② 四組條件** — `PAIRS` 這一段就是牌面內容（頁面標題固定是「債速配」，不會透露是哪一檔債）：

```javascript
q:     綠色題目卡（txt 是大字，en 是底下的小字，可以不填）
a:     白色答案卡（txt 是數值；long: true 給比較長的代號用，字會自動縮小）
sheet: 下面「條件速覽」那一區的說明文字
```

順序不用管，程式會自己洗牌。

### 換照片

照片是用 base64 直接寫在 `game.html` 裡的，找到這一行：

```javascript
var PHOTO = "data:image/jpeg;base64,/9j/4AAQ....";
```

要換照片的話跟 Claude 說一聲，把新照片給它，它會幫你轉好這一行給你貼。

### 清掉排行榜

Supabase → **Table Editor** → `flip_scores` → 勾選要刪的列 → 刪除。
或在 SQL Editor 跑：

```sql
delete from public.flip_scores where board = 'nvda-bond-11';
```

---

## 常見狀況

**排行榜一直空的，但自己打完有成績**
Secrets 沒設定好。回 Streamlit 的 Settings → Secrets 檢查那兩行，注意值要用雙引號包起來。

**畫面下面被切掉 / 上面留一大片空白**
`app.py` 裡的 `FRAME_HEIGHT = 1750`，被切到就調大，空太多就調小。

**同事說打不開**
Streamlit Cloud 免費版的 App 太久沒人用會睡著，第一個人打開要等 30 秒左右喚醒。要避免的話得升級付費方案。

**有人用同一個名字**
排行榜是用名字認人的，同名會被當成同一個人，只留最好的成績。讓大家名字加個部門或編號就好。

---

## 安全性說明

- 程式裡放的 `anon` 金鑰是設計上就要公開給瀏覽器用的，外洩沒關係
- 資料庫只開放「讀取」和「新增一筆」，**沒有開放修改和刪除**，所以沒有人能改掉或洗掉別人的成績
- 資料表有檢查條件，步數、時間、名字長度不合理的會被擋下來
- 這裡面沒有任何客戶資料，只有名字和成績
