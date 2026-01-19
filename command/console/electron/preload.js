const path = require('path');
const { contextBridge } = require('electron');

// Core APIのURLとAPIキーを環境変数から受け取る。
const apiUrl =
  process.env.SPECTRA_CORE_URL || 'http://127.0.0.1:8000/v1/think';
const apiKey = process.env.SPECTRA_API_KEY || '';

// UIからの入力をCoreに送信し、JSON応答を返す。
const think = async ({ prompt, sessionId, channel }) => {
  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(apiKey ? { 'x-api-key': apiKey } : {}),
    },
    body: JSON.stringify({
      prompt,
      session_id: sessionId,
      channel,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    const message = data?.detail ?? response.statusText;
    throw new Error(message);
  }
  return data;
};

// package.json から製品名とバージョンを取得する。
const getAppInfo = () => {
  const metadata = require(path.join(__dirname, '..', 'package.json'));
  return {
    name: metadata.name,
    version: metadata.version,
  };
};

// Core から Console 用設定を取得する。
const getConsoleConfig = async () => {
  const baseUrl = apiUrl.replace(/\/v1\/think$/, '');
  const response = await fetch(`${baseUrl}/console-config`, {
    headers: {
      ...(apiKey ? { 'x-api-key': apiKey } : {}),
    },
  });
  const data = await response.json();
  if (!response.ok) {
    const message = data?.detail ?? response.statusText;
    throw new Error(message);
  }
  return data;
};

// レンダラに必要最小限のAPIだけ公開する。
contextBridge.exposeInMainWorld('spectraApi', {
  think,
  getAppInfo,
  getConsoleConfig,
});
