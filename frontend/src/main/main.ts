import { app, BrowserWindow, ipcMain, shell } from 'electron'
import path from 'path'

let win: BrowserWindow | null = null

function createWindow() {
  const preloadPath = app.isPackaged 
    ? path.join(__dirname, 'preload.js') 
    : path.join(__dirname, 'preload.ts')

  win = new BrowserWindow({
    width: 1280,
    height: 800,
    backgroundColor: '#0b0f17',
    titleBarStyle: 'hiddenInset',
    webPreferences: {
      preload: preloadPath,
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  })

  if (!app.isPackaged) {
    win.loadURL('http://localhost:5173/index.html')
    win.webContents.openDevTools({ mode: 'detach' })
  } else {
    win.loadFile(path.join(__dirname, '../renderer/index.html'))
  }
}

app.whenReady().then(() => {
  createWindow()
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

ipcMain.handle('search:query', async (_e: any, { q }: any) => {
  const now = Date.now()
  return [
    { id: '1', name: 'design-spec.md', path: '/path/design-spec.md', size: 32145, type: 'md', modified: now, tags: ['docs'] },
    { id: '2', name: 'invoice.pdf', path: '/path/invoice.pdf', size: 129845, type: 'pdf', modified: now, tags: ['finance'] }
  ].filter(f => f.name.toLowerCase().includes((q || '').toLowerCase()))
})

ipcMain.handle('file:open', async (_e: any, filePath: string) => {
  await shell.openPath(filePath)
  return { ok: true }
})
