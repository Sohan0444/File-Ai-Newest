"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
const path_1 = __importDefault(require("path"));
let win = null;
function createWindow() {
    const preloadPath = electron_1.app.isPackaged
        ? path_1.default.join(__dirname, 'preload.js')
        : path_1.default.join(__dirname, 'preload.ts');
    win = new electron_1.BrowserWindow({
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
    });
    if (!electron_1.app.isPackaged) {
        win.loadURL('http://localhost:5173/index.html');
        win.webContents.openDevTools({ mode: 'detach' });
    }
    else {
        win.loadFile(path_1.default.join(__dirname, '../renderer/index.html'));
    }
}
electron_1.app.whenReady().then(() => {
    createWindow();
    electron_1.app.on('activate', () => {
        if (electron_1.BrowserWindow.getAllWindows().length === 0)
            createWindow();
    });
});
electron_1.app.on('window-all-closed', () => {
    if (process.platform !== 'darwin')
        electron_1.app.quit();
});
electron_1.ipcMain.handle('search:query', async (_e, { q }) => {
    const now = Date.now();
    return [
        { id: '1', name: 'design-spec.md', path: '/path/design-spec.md', size: 32145, type: 'md', modified: now, tags: ['docs'] },
        { id: '2', name: 'invoice.pdf', path: '/path/invoice.pdf', size: 129845, type: 'pdf', modified: now, tags: ['finance'] }
    ].filter(f => f.name.toLowerCase().includes((q || '').toLowerCase()));
});
electron_1.ipcMain.handle('file:open', async (_e, filePath) => {
    await electron_1.shell.openPath(filePath);
    return { ok: true };
});
