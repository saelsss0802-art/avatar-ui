const { contextBridge } = require('electron');

const apiUrl =
  process.env.SPECTRA_CORE_URL || 'http://127.0.0.1:8000/v1/think';
const apiKey = process.env.SPECTRA_API_KEY || '';

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

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data?.detail || response.statusText || 'Request failed';
    throw new Error(message);
  }
  return data;
};

contextBridge.exposeInMainWorld('spectraApi', {
  think,
});
