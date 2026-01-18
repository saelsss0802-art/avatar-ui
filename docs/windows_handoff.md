# Windows移行ハンドオフ（C:\dev 前提）

このメモは、WSL→Windows運用へ切り替える途中でチャットが切れても再開できるようにする引き継ぎです。

## 背景 / 決定
- 運用は Windows 統一にする（WSL 前提にしない）。
- Core は Windows 起動時に自動起動（タスクスケジューラ）。
- Console は Electron（`command/console`）を使用。

## ここまでの変更
- `docs/implementation_plan.md` を Windows 統一に合わせて更新。
- `README.md` を Windows 前提に換装（PowerShell 手順、タスクスケジューラ、cloudflared Windows 手順）。
- `command/console/` を追加（Electron UI）。
- `scripts/register-task.ps1` を追加（タスクスケジューラ登録）。

## 次にやること（Windows側で続行）
### 1) リポジトリを Windows に配置
```powershell
mkdir C:\dev
cd C:\dev
git clone <repository-url> spectra
cd spectra
```

### 2) venv と依存関係
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3) .env 作成
```powershell
@'
XAI_API_KEY=your-xai-api-key-here
SPECTRA_API_KEY=your-secret-key-here
'@ | Set-Content .env
```

### 4) Core の動作確認
```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn core.main:app --host 127.0.0.1 --port 8000
```
確認: `http://127.0.0.1:8000/health`

### 5) cloudflared（Windows）
```powershell
winget install --id Cloudflare.cloudflared
cloudflared tunnel login
cloudflared tunnel create spectra
cloudflared tunnel route dns spectra spectra.your-domain.com
cloudflared tunnel list
```

credentials を ProgramData にコピー:
```powershell
New-Item -ItemType Directory -Force C:\ProgramData\cloudflared | Out-Null
Copy-Item "$env:USERPROFILE\\.cloudflared\\<TUNNEL_ID>.json" "C:\\ProgramData\\cloudflared\\" -Force
```

`C:\ProgramData\cloudflared\config.yml` を作成:
```powershell
@'
tunnel: spectra
# SYSTEM で動かす場合は ProgramData を使う
credentials-file: C:/ProgramData/cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: spectra.your-domain.com
    service: http://localhost:8000
  - service: http_status:404
'@ | Set-Content "C:\\ProgramData\\cloudflared\\config.yml"
```

手動起動:
```powershell
cloudflared tunnel --config "C:\\ProgramData\\cloudflared\\config.yml" run spectra
```
Note: Windows版 `cloudflared` は自動更新されないため手動更新が必要。

### 6) Core 自動起動（Windowsタスク）
管理者 PowerShell で:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-task.ps1
```

### 7) Tunnel 自動起動（Windowsタスク）
管理者 PowerShell で:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/register-tunnel-task.ps1
```

## 注意点
- WSL で `winget` を実行しても Windows にインストールされるだけで、リポには影響しない。

## WSL から git push が失敗する場合
症状: `Could not resolve host: github.com`

一次対処（WSL bash）:
```bash
sudo sh -c 'printf "nameserver 1.1.1.1\nnameserver 8.8.8.8\n" > /etc/resolv.conf'
getent hosts github.com
```

恒久対応（WSL bash、実行後に Windows PowerShell で `wsl --shutdown` が必要）:
```bash
sudo tee /etc/wsl.conf > /dev/null <<'EOF'
[network]
generateResolvConf = false
EOF

sudo sh -c 'printf "nameserver 1.1.1.1\nnameserver 8.8.8.8\n" > /etc/resolv.conf'
```

代替手段（WSL から push せず、Windows 側で反映）:
```bash
mkdir -p /mnt/c/dev/spectra/patches
git format-patch origin/main --stdout > /mnt/c/dev/spectra/patches/spectra-wsl.patch
```

Windows PowerShell:
```powershell
cd C:\dev\spectra
git am .\patches\spectra-wsl.patch
git push
```
