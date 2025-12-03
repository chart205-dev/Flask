$apiUrl = "http://127.0.0.1:5000/items"

# 50 回繰り返し
for ($i = 1; $i -le 50; $i++) {

    # ランダムな 1〜100 の数字
    $price = Get-Random -Minimum 1 -Maximum 100

    # JSON データ
    $json = @{
        item_name = "Item_$i"
        price     = $price
    } | ConvertTo-Json

    # ★PowerShell では headers を辞書形式にする必要があります
    $headers = @{
        "Content-Type" = "application/json"
    }

    # POST リクエスト
    Invoke-WebRequest `
        -Uri $apiUrl `
        -Method POST `
        -Headers $headers `
        -Body $json

    Write-Host "Sent Item_$i : price = $price"
}
