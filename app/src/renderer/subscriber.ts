import type { AgentSubscriber } from "@ag-ui/client";
import { AnimationManager } from "./animation";

interface UiSubscriberOptions {
  outputEl: HTMLElement;
  animation: AnimationManager;
}

export function createUiSubscriber(options: UiSubscriberOptions): AgentSubscriber {
  const { outputEl, animation } = options;

  let activeAssistantLine: HTMLElement | null = null;
  let activeToolLine: HTMLElement | null = null;

  const scrollToBottom = () => {
    outputEl.scrollTop = outputEl.scrollHeight;
  };

  const appendLine = (className: string, text: string) => {
    const line = document.createElement("p");
    line.className = `text-line ${className}`;
    line.textContent = text;
    outputEl.appendChild(line);
    scrollToBottom();
    return line;
  };

  return {
    onTextMessageStartEvent() {
      activeAssistantLine = document.createElement("p");
      activeAssistantLine.className = "text-line text-line--assistant";
      outputEl.appendChild(activeAssistantLine);
      animation.startTyping();
      scrollToBottom();
    },
    onTextMessageContentEvent({ event }) {
      animation.appendDelta(activeAssistantLine, event.delta);
    },
    onTextMessageEndEvent() {
      animation.stopTyping();
      activeAssistantLine = null;
      scrollToBottom();
    },
    onToolCallStartEvent({ event }) {
      activeToolLine = appendLine("text-line--tool", `🔧 Tool call: ${event.toolCallName}`);
    },
    onToolCallArgsEvent({ event }) {
      if (event.delta && activeToolLine) {
        activeToolLine.textContent += event.delta;
        scrollToBottom();
      }
    },
    onToolCallResultEvent({ event }) {
      appendLine("text-line--tool", `🔍 Result: ${event.content ?? ""}`);
    },
    onToolCallEndEvent() {
      activeToolLine = null;
    },
    onRunFailedEvent({ error }) {
      animation.stopTyping();
      activeAssistantLine = null;
      appendLine(
        "text-line--error",
        `❌ ${error instanceof Error ? error.message : String(error)}`,
      );
    },
  };
}
