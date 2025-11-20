import { contextBridge } from "electron";

contextBridge.exposeInMainWorld("avatarBridge", {});
