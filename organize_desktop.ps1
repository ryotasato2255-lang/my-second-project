# デスクトップ整理スクリプト
# 使い方: このファイルを右クリック → "PowerShellで実行"

# 文字化け防止
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# デスクトップのパスを取得
$desktop = [Environment]::GetFolderPath("Desktop")
Write-Host "デスクトップ: $desktop" -ForegroundColor Cyan

# 拡張子 → フォルダ名のマッピング
$extensionMap = @{
    ".jpg"  = "画像"; ".jpeg" = "画像"; ".png" = "画像"
    ".gif"  = "画像"; ".bmp"  = "画像"; ".webp" = "画像"
    ".mp4"  = "動画"; ".mov"  = "動画"; ".avi"  = "動画"
    ".xlsx" = "Excel"; ".xls" = "Excel"; ".csv" = "Excel"
    ".docx" = "Word"; ".doc" = "Word"
    ".pptx" = "PowerPoint"; ".ppt" = "PowerPoint"
    ".pdf"  = "PDF"
    ".txt"  = "メモ・テキスト"; ".md" = "メモ・テキスト"
    ".py"   = "スクリプト"; ".js" = "スクリプト"; ".bat" = "スクリプト"; ".ps1" = "スクリプト"
    ".zip"  = "圧縮ファイル"; ".rar" = "圧縮ファイル"; ".7z" = "圧縮ファイル"
    ".tmp"  = "削除候補"; ".bak" = "削除候補"
}

# ファイル名キーワード → フォルダ名のマッピング（順番に評価）
$keywordMap = @(
    @{ Keywords = @("ZZZ削除予定", "ゴミ箱に入れ忘れ", "あとで消す"); Folder = "削除候補" }
    @{ Keywords = @("スクリーンショット", "screenshot", "Screenshot");   Folder = "スクリーンショット" }
    @{ Keywords = @("TODO", "todo", "タスク");                           Folder = "メモ・テキスト" }
    @{ Keywords = @("会議メモ", "議事録", "メモ");                       Folder = "メモ・テキスト" }
    @{ Keywords = @("見積書", "請求書", "領収書");                       Folder = "経理書類" }
    @{ Keywords = @("売上", "データ分析", "集計");                       Folder = "データ・分析" }
    @{ Keywords = @("報告書", "レポート");                               Folder = "報告書" }
    @{ Keywords = @("プレゼン", "presentation");                         Folder = "PowerPoint" }
)

# スキップするファイル
$skipFiles = @("desktop.ini", "thumbs.db")

# ファイルを収集して移動
$files = Get-ChildItem -Path $desktop -File
$count = 0

foreach ($file in $files) {
    if ($skipFiles -contains $file.Name.ToLower()) { continue }

    # 移動先フォルダを決定
    $targetFolder = $null

    # キーワードで判定
    foreach ($rule in $keywordMap) {
        foreach ($keyword in $rule.Keywords) {
            if ($file.Name -like "*$keyword*") {
                $targetFolder = $rule.Folder
                break
            }
        }
        if ($targetFolder) { break }
    }

    # 拡張子で判定
    if (-not $targetFolder) {
        $ext = $file.Extension.ToLower()
        if ($extensionMap.ContainsKey($ext)) {
            $targetFolder = $extensionMap[$ext]
        } else {
            $targetFolder = "その他"
        }
    }

    # 移動先ディレクトリを作成
    $destDir = Join-Path $desktop $targetFolder
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir | Out-Null
    }

    # 同名ファイルがある場合はリネーム
    $destFile = Join-Path $destDir $file.Name
    $i = 1
    while (Test-Path $destFile) {
        $newName = "$($file.BaseName)_$i$($file.Extension)"
        $destFile = Join-Path $destDir $newName
        $i++
    }

    # 移動
    Move-Item -Path $file.FullName -Destination $destFile
    Write-Host "  $targetFolder/ <- $($file.Name)" -ForegroundColor Green
    $count++
}

Write-Host ""
Write-Host "✓ $count ファイルを整理しました！" -ForegroundColor Cyan
Write-Host ""
Write-Host "Enterキーで閉じる..."
Read-Host
