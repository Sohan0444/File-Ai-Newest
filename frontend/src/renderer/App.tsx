import React, { useState } from 'react'
import TopBar from './components/TopBar'
import Filters, { FiltersState } from './components/Filters'
import FileGrid, { FileItem } from './components/FileGrid'
import DetailsPanel from './components/DetailsPanel'
import CommandPalette from './components/CommandPalette'

export default function App() {
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState<FiltersState>({ types: [], tag: '', date: 'any' })
  const [items, setItems] = useState<FileItem[]>([])
  const [selected, setSelected] = useState<FileItem | null>(null)
  const [paletteOpen, setPaletteOpen] = useState(false)

  return (
    <div className="h-screen w-screen grid grid-cols-[1fr_360px] grid-rows-[64px_1fr]">
      <div className="col-span-2">
        <TopBar 
          query={query} 
          setQuery={setQuery} 
          onSearch={async () => {
            const res = await (await import('./lib/ipc')).searchQuery(query)
            setItems(res)
          }}
          onOpenPalette={() => setPaletteOpen(true)}
        />
      </div>
      <div className="p-4">
        <Filters value={filters} onChange={setFilters} />
        <FileGrid items={items} onSelect={setSelected} />
      </div>
      <div className="p-4">
        <DetailsPanel item={selected} />
      </div>
      <CommandPalette 
        open={paletteOpen} 
        onClose={() => setPaletteOpen(false)} 
        onAction={() => {}}
      />
    </div>
  )
}
