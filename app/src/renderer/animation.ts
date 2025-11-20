interface AnimationSettings {
  mouthAnimationInterval: number;
  getAvatarImagePath: (isIdle: boolean) => string;
}

interface SoundManager {
  playTypeSound?: () => void;
}

export class AnimationManager {
  private talkingInterval: ReturnType<typeof setInterval> | null = null;

  constructor(
    private settings: AnimationSettings,
    private soundManager?: SoundManager,
    private avatarImg: HTMLImageElement | null = document.getElementById("avatar-img") as HTMLImageElement | null,
    private output: HTMLElement | null = document.querySelector("#pane-output .text-scroll"),
  ) {}

  setAvatar(img: HTMLImageElement | null) {
    this.avatarImg = img;
  }

  setOutput(el: HTMLElement | null) {
    this.output = el;
  }

  startMouthAnimation() {
    if (this.talkingInterval) {
      return;
    }

    let mouthOpen = false;
    this.talkingInterval = window.setInterval(() => {
      const nextPath = this.settings.getAvatarImagePath(!mouthOpen);
      if (nextPath && this.avatarImg) {
        this.avatarImg.src = nextPath;
      }
      mouthOpen = !mouthOpen;
    }, this.settings.mouthAnimationInterval);
  }

  stopMouthAnimation() {
    if (this.talkingInterval) {
      clearInterval(this.talkingInterval);
      this.talkingInterval = null;
    }

    const idlePath = this.settings.getAvatarImagePath(true);
    if (idlePath && this.avatarImg) {
      this.avatarImg.src = idlePath;
    }
  }

  startTyping() {
    this.startMouthAnimation();
  }

  stopTyping() {
    this.stopMouthAnimation();
  }

  appendDelta(element: HTMLElement | null, delta: string | undefined) {
    if (!delta || !element) {
      return;
    }

    element.textContent += delta;
    if (this.output) {
      this.output.scrollTop = this.output.scrollHeight;
    }

    if (delta.trim()) {
      this.soundManager?.playTypeSound?.();
    }
  }
}
