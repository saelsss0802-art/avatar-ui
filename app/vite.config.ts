import { defineConfig } from 'vite'
import electron from 'vite-plugin-electron'
import renderer from 'vite-plugin-electron-renderer'
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    electron([
      {
        entry: resolve(__dirname, 'src/main/index.ts'),  // 絶対パス
        vite: {
          build: {
            outDir: resolve(__dirname, 'dist-electron'),
          },
        },
      },
    ]),
    renderer(),
  ],
  root: 'src/renderer',  // 開発時のroot
  publicDir: resolve(__dirname, 'src/renderer/assets'),
  build: {
    outDir: resolve(__dirname, 'dist/renderer'),
  },
})
