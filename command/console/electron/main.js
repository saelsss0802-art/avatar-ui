const path = require('path');
const { app, BrowserWindow } = require('electron');

const envPath =
  process.env.SPECTRA_ENV_PATH || path.join(__dirname, '..', '..', '..', '.env');

require('dotenv').config({ path: envPath });

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
      sandbox: true,
    },
  });

  mainWindow.loadFile(path.join(__dirname, '..', 'index.html'));
};

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
