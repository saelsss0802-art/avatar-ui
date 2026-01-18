const outputEl = document.getElementById('output');
const inputEl = document.getElementById('input');
const avatarImg = document.getElementById('avatar-img');
const metaBar = document.getElementById('meta');
const avatarLabel = document.getElementById('avatar-label');

const idleSrc = avatarImg?.dataset.idle || avatarImg?.getAttribute('src');
const talkSrc = avatarImg?.dataset.talk || avatarImg?.getAttribute('src');
const sessionKey = 'spectra-session-id';
const storedSessionId = window.localStorage.getItem(sessionKey);
const sessionId = storedSessionId || crypto.randomUUID();
if (!storedSessionId) {
  window.localStorage.setItem(sessionKey, sessionId);
}

const addLine = (className, text) => {
  if (!outputEl) {
    return;
  }
  const line = document.createElement('div');
  line.className = `text-line ${className}`.trim();
  line.textContent = text;
  outputEl.appendChild(line);
  outputEl.scrollTop = outputEl.scrollHeight;
};

const setTalking = (isTalking) => {
  if (!avatarImg) {
    return;
  }
  avatarImg.src = isTalking ? talkSrc : idleSrc;
};

if (metaBar) {
  metaBar.textContent = 'spectra-command ui';
}

if (avatarLabel) {
  avatarLabel.textContent = 'SPECTRA';
}

addLine('text-line--system', '> SYSTEM SPECTRA COMMAND ONLINE');
addLine('text-line--system', '> SESSION STANDBY');

if (inputEl) {
  let isRunning = false;

  inputEl.addEventListener('keydown', (event) => {
    if (event.isComposing || event.key !== 'Enter') {
      return;
    }
    event.preventDefault();

    if (isRunning) {
      return;
    }

    const value = inputEl.value.trim();
    if (!value) {
      return;
    }

    addLine('text-line--user', `USER> ${value}`);
    inputEl.value = '';

    setTalking(true);
    isRunning = true;
    inputEl.disabled = true;

    const request = window.spectraApi?.think;
    if (!request) {
      addLine('text-line--error', 'ERROR> Core API is unavailable.');
      setTalking(false);
      inputEl.disabled = false;
      isRunning = false;
      return;
    }

    request({ prompt: value, sessionId, channel: 'command' })
      .then((data) => {
        const text = data?.response || '(no response)';
        addLine('text-line--assistant', `Spectra> ${text}`);
      })
      .catch((error) => {
        const message = error?.message || 'Request failed';
        addLine('text-line--error', `ERROR> ${message}`);
      })
      .finally(() => {
        setTalking(false);
        inputEl.disabled = false;
        inputEl.focus();
        isRunning = false;
      });
  });
}
