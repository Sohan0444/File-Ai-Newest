declare global {
  interface Window {
    api: {
      invoke: (channel: string, ...args: any[]) => Promise<any>
    }
  }
}

export async function searchQuery(q: string) {
  return window.api.invoke('search:query', { q })
}

export async function openFile(path: string) {
  return window.api.invoke('file:open', path)
}
