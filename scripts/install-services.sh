#!/bin/bash
# SPECTRA サービスインストールスクリプト
# 使い方: sudo bash scripts/install-services.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== SPECTRA サービスをインストールします ==="

# サービスファイルをコピー
echo "1. サービスファイルをコピー..."
cp "$SCRIPT_DIR/spectra.service" /etc/systemd/system/
cp "$SCRIPT_DIR/spectra-tunnel.service" /etc/systemd/system/

# systemd をリロード
echo "2. systemd をリロード..."
systemctl daemon-reload

# サービスを有効化
echo "3. サービスを有効化..."
systemctl enable spectra spectra-tunnel

# サービスを起動
echo "4. サービスを起動..."
systemctl start spectra
sleep 2
systemctl start spectra-tunnel

# 状態確認
echo "5. 状態確認..."
systemctl status spectra --no-pager
systemctl status spectra-tunnel --no-pager

echo ""
echo "=== インストール完了！ ==="
echo ""
echo "便利コマンド:"
echo "  状態確認:   sudo systemctl status spectra spectra-tunnel"
echo "  ログ確認:   journalctl -u spectra -f"
echo "  再起動:     sudo systemctl restart spectra spectra-tunnel"
echo "  停止:       sudo systemctl stop spectra spectra-tunnel"
