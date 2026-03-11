$desktop = [Environment]::GetFolderPath("Desktop")

# テキストファイル系
"あとで整理する" | Out-File "$desktop\無題のドキュメント.txt"
"あとで整理する（本物）" | Out-File "$desktop\無題のドキュメント (1).txt"
"こっちが本物" | Out-File "$desktop\無題のドキュメント (2).txt"

"Q1振り返り会議`n参加者：田中、鈴木、山田`n※あとで清書する" | Out-File "$desktop\会議メモ_2024_03_15.txt"
"Q1振り返り会議（最新）`n※これが最新版です" | Out-File "$desktop\会議メモ_最新版.txt"
"Q1振り返り会議（最新・修正済み）`n※今度こそ本当の最新版" | Out-File "$desktop\会議メモ_最新版_修正済み.txt"

"やること`n- デスクトップ整理する`n- 確定申告`n- 歯医者予約`n- 母の誕生日プレゼント" | Out-File "$desktop\TODO.txt"
"やること（本物）`n- 上のTODO.txtは古いやつ`n- こっちが最新" | Out-File "$desktop\TODO2.txt"

"※絶対に見ないこと`nGmail: xxxxxxxx`n銀行: 0000`nWi-Fi: password123" | Out-File "$desktop\パスワード一覧.txt"

"削除予定のファイルたち`n（でもまだ消せない…）" | Out-File "$desktop\ZZZ削除予定_あとで消す.txt"

"大事な気がする`nでもどこに整理すればいいか不明`nとりあえずデスクトップに置いとく" | Out-File "$desktop\なんか大事なファイル.txt"

"tmpファイル" | Out-File "$desktop\ゴミ箱に入れ忘れ.tmp"

# Officeファイルに見せかけたダミー
"[PPTX v1]" | Out-File "$desktop\プレゼン資料_v1.pptx"
"[PPTX v2]" | Out-File "$desktop\プレゼン資料_v2.pptx"
"[PPTX v3 final]" | Out-File "$desktop\プレゼン資料_v3_最終.pptx"
"[PPTX truly final]" | Out-File "$desktop\プレゼン資料_v3_最終_本当に最終.pptx"
"[PPTX boss approved]" | Out-File "$desktop\プレゼン資料_v3_最終_本当に最終_上司確認済み.pptx"
"[Office lock file]" | Out-File "$desktop\~`$プレゼン資料_v3_最終.pptx"

"[Word draft]" | Out-File "$desktop\報告書_2024年Q1_draft.docx"
"[Word final]" | Out-File "$desktop\報告書_2024年Q1_final.docx"
"[Word final v2]" | Out-File "$desktop\報告書_2024年Q1_final_v2.docx"

"[Excel estimate]" | Out-File "$desktop\見積書_田中商事.xlsx"
"[Excel estimate revised]" | Out-File "$desktop\見積書_田中商事_修正版.xlsx"
"[Excel sales 2023]" | Out-File "$desktop\売上集計_2023年度.xlsx"
"[Excel sales 2024]" | Out-File "$desktop\売上集計_2024年度.xlsx"

# CSV
"名前,売上,利益`n田中,100000,30000`n鈴木,200000,60000" | Out-File "$desktop\データ分析結果.csv"
"名前,売上,利益`n田中,100000,30000`n鈴木,200000,60000`n佐藤,300000,90000" | Out-File "$desktop\データ分析結果_修正.csv"

# 画像に見せかけたダミー
"[PNG screenshot]" | Out-File "$desktop\スクリーンショット 2024-01-08 14.23.45.png"
"[PNG screenshot]" | Out-File "$desktop\スクリーンショット 2024-01-22 09.11.02.png"
"[PNG screenshot]" | Out-File "$desktop\スクリーンショット 2024-02-03 18.47.33.png"
"[PNG screenshot]" | Out-File "$desktop\スクリーンショット 2024-02-14 22.05.17.png"
"[PNG screenshot]" | Out-File "$desktop\スクリーンショット 2024-03-01 11.30.00.png"
"[JPG]" | Out-File "$desktop\image001.jpg"
"[JPG]" | Out-File "$desktop\image002.jpg"
"[JPG]" | Out-File "$desktop\image003.jpg"

# コード系
"# なんか作ってたやつ`n# あとで整理`nprint('hello world')`n# TODO: ちゃんと書く" | Out-File "$desktop\script.py"
"# scriptのコピー`nprint('hello world')" | Out-File "$desktop\script_copy.py"
"<!DOCTYPE html><html><body><h1>テスト</h1><!-- あとで修正 --></body></html>" | Out-File "$desktop\Untitled-1.html"
"<!DOCTYPE html><html><body><h1>テスト2</h1></body></html>" | Out-File "$desktop\Untitled-2.html"

# フォルダ
New-Item -ItemType Directory -Force -Path "$desktop\新しいフォルダー" | Out-Null
"とりあえずここに入れておく" | Out-File "$desktop\新しいフォルダー\readme.txt"
New-Item -ItemType Directory -Force -Path "$desktop\新しいフォルダー (2)" | Out-Null
"こっちも何か入れた気がする" | Out-File "$desktop\新しいフォルダー (2)\readme.txt"

New-Item -ItemType Directory -Force -Path "$desktop\temp" | Out-Null
"作業中のファイル（消さないこと！！！）" | Out-File "$desktop\temp\作業中.txt"

New-Item -ItemType Directory -Force -Path "$desktop\old_backup_DO_NOT_DELETE" | Out-Null
"[ZIP backup]" | Out-File "$desktop\old_backup_DO_NOT_DELETE\重要データ_古い.zip"
"[ZIP backup 2022]" | Out-File "$desktop\old_backup_DO_NOT_DELETE\重要データ_バックアップ_2022.zip"

New-Item -ItemType Directory -Force -Path "$desktop\ダウンロード済み" | Out-Null
"[EXE]" | Out-File "$desktop\ダウンロード済み\installer_chrome_setup.exe"
"[EXE]" | Out-File "$desktop\ダウンロード済み\zoom_installer.exe"
"[PDF]" | Out-File "$desktop\ダウンロード済み\請求書_202401.pdf"
"[PDF]" | Out-File "$desktop\ダウンロード済み\請求書_202402.pdf"

New-Item -ItemType Directory -Force -Path "$desktop\音楽" | Out-Null
"[MP3]" | Out-File "$desktop\音楽\song_download_001.mp3"
"[MP3]" | Out-File "$desktop\音楽\song_download_002.mp3"

Write-Host "デスクトップのカオス化完了！" -ForegroundColor Green
Write-Host "$(Get-ChildItem $desktop | Measure-Object).Count 個のアイテムを作成しました"
