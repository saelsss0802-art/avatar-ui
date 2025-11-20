import { agent, agentConfig } from "../core/agent";
import { loggerSubscriber } from "../core/loggerSubscriber";
import { createUiSubscriber } from "./subscriber";
import { AnimationManager } from "./animation";

// グローバルsubscriber登録（ロガー）
agent.subscribe(loggerSubscriber);

const inputEl = document.getElementById("input") as HTMLInputElement | null;
const outputEl = document.querySelector("#pane-output .text-scroll") as HTMLElement | null;
const avatarImg = document.getElementById("avatar-img") as HTMLImageElement | null;
const metaBar = document.getElementById("meta");

if (metaBar) {
  metaBar.textContent = "avatar-ui v1.0.0";
}

if (!inputEl || !outputEl || !avatarImg) {
  throw new Error("UI elements missing");
}

const animation = new AnimationManager(
  {
    mouthAnimationInterval: 120,
    getAvatarImagePath: (isIdle) => {
      if (isIdle) {
        return avatarImg.dataset.idle ?? avatarImg.src;
      }
      return avatarImg.dataset.talk ?? avatarImg.dataset.idle ?? avatarImg.src;
    },
  },
);
animation.setAvatar(avatarImg);
animation.setOutput(outputEl);

const appendLine = (className: string, text: string) => {
  const line = document.createElement("p");
  line.className = `text-line ${className}`;
  line.textContent = text;
  outputEl.appendChild(line);
  outputEl.scrollTop = outputEl.scrollHeight;
};

let isRunning = false;

inputEl.addEventListener("keydown", async (event) => {
  if (event.isComposing || event.key !== "Enter") {
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

  appendLine("text-line--user", `> ${value}`);
  inputEl.value = "";

  const userMessage = {
    id: crypto.randomUUID(),
    role: "user" as const,
    content: value,
  };

  agent.messages.push(userMessage);

  isRunning = true;
  try {
    await agent.runAgent(
      {
        runId: crypto.randomUUID(),
        threadId: agentConfig.threadId,
      },
      createUiSubscriber({
        outputEl,
        animation,
      }),
    );
  } catch (error) {
    console.error(error);
    appendLine(
      "text-line--error",
      `❌ ${error instanceof Error ? error.message : String(error)}`,
    );
  } finally {
    isRunning = false;
  }
});
