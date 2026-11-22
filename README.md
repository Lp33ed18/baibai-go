# 拜拜 Go：聽得懂長輩的拜拜路線夥伴

**BaiBai Go: A Voice-First Temple Route Companion for Seniors**

多媒體技術概論（115 學年度第 1 學期）期末專題，並參加 USR「共創長者幸福人生」成果競賽。

<p align="center"><img src="assets/baibaigo_demo.gif" alt="BaiBai Go 介面示意動畫：說話、推薦、地圖導航、平安抵達" width="260"></p>

## 這是什麼

長輩喜歡到廟裡拜拜，但常因為路不熟、樓梯多、怕走太遠而減少出門。拜拜 Go 讓長輩按一個大按鈕說「我想去拜拜」，就推薦附近合適的廟和路線，並用語音一步一步帶路，抵達後通知家人。

語音最適合長輩，但在戶外常常失靈：周圍吵、長輩講話小聲、高頻聽力退化。所以本組的技術重點是**語音的前後處理**：

```
Microphone
 → Input pre-processing      ← 本組實作：重取樣、語音偵測、頻譜相減降噪、音量正規化
 → Speech-to-Text API        （現成服務）
 → App logic: intent → temple & route recommendation
 → Text-to-Speech API        （現成服務）
 → Output processing         ← 本組實作：聽力補償 EQ、響度正規化
 → Speaker
```

介面以語音為主、打字與選單為輔；導航以語音指引為主、螢幕地圖為輔。

## 檔案導覽

| 檔案 | 內容 |
|---|---|
| [Midterm_Presentation.pptx](Midterm_Presentation.pptx) | 期中簡報（11 頁、英文，第 5 頁為介面示意動畫，放映模式才會動） |
| [Midterm_Script.md](Midterm_Script.md) | 逐頁英文講稿，含時間與建議講者 |
| [BaiBaiGo_mockup.html](BaiBaiGo_mockup.html) | 可點擊的介面示意（純前端、示範資料），用瀏覽器直接開啟 |
| [assets/baibaigo_demo.gif](assets/baibaigo_demo.gif) | 介面示意動畫 |
| [docs/project-log.md](docs/project-log.md) | 討論與決策紀錄：範圍怎麼收斂、簡報修正、助教回饋 |
| [docs/work-plan.md](docs/work-plan.md) | 目前的分工與六週時程（含期中後的調整） |
| [tools/](tools/) | 產生簡報與動畫的腳本 |

## 重新產生簡報與動畫

需要 Python 3 與 `python-pptx`、`Pillow`；動畫另需 Windows 上的 Microsoft Edge。

```bash
pip install python-pptx Pillow
```

```bash
python tools/build_deck.py
```

```bash
python tools/make_gif.py
```

輸出都放在 `build/`（不會進版本控制），不會覆蓋根目錄的檔案。根目錄的簡報有幾處在 PowerPoint 裡手動修改過的內容（標題頁成員名單、第 2 頁一個小標題），腳本不會產生這些修改；要更新正式簡報時，記得把手動修改補回去。`make_gif.py` 請在 PowerShell 或命令提示字元裡執行。

## 目前狀態

- 期中報告已完成（2026-11-12）。
- 介面示意與動畫是純前端，廟宇、距離、回覆都是示範資料，尚未接任何後端或真實地圖。
- 期中後依助教建議，路線推薦加入坡度與大眾運輸，詳見 [docs/work-plan.md](docs/work-plan.md)。

## 點子來源

本專題構想來自信義公益基金會「集點子」平台的〈長輩專屬拜拜路線推薦〉。
