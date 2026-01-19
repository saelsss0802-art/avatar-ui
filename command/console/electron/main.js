// Electronの起動に必要な標準モジュールを読み込む。
const path = require('path');
const { app, BrowserWindow } = require('electron');

// .envの読み込み場所を明示し、ElectronからAPIキーを使えるようにする。
const envPath =
  process.env.SPECTRA_ENV_PATH || path.join(__dirname, '..', '..', '..', '.env');

// 環境変数をロードしてpreloadで参照できるようにする。
require('dotenv').config({ path: envPath });

// メインウィンドウを作成し、UI（index.html）を読み込む。
const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 1024,
    height: 640,
    backgroundColor: '#000000',
    show: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, '..', 'index.html'));
};

app.whenReady().then(() => {
  createWindow();

  // macOSはドックから復帰したときに再生成する。
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Windows/Linuxは全ウィンドウが閉じたら終了する。
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
