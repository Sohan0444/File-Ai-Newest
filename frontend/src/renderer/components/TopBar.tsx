import React from 'react'

interface TopBarProps {
  query: string
  setQuery: (q: string) => void
  onSearch: () => void
  onOpenPalette: () => void
}

export default function TopBar({ query, setQuery, onSearch, onOpenPalette }: TopBarProps) {
  return (
    <div className="h-16 bg-panel/50 backdrop-blur-sm border-b border-white/10 flex items-center px-6 gap-4">
      <div className="flex-1 relative">
        <input
          type="text"
          placeholder="Search files..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSearch()}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white placeholder-white/50 focus:outline-none focus:border-neon/50"
        />
        <button
          onClick={onSearch}
          className="absolute right-2 top-1/2 -translate-y-1/2 bg-neon/20 hover:bg-neon/30 text-neon px-3 py-1 rounded text-sm transition-colors"
        >
          Search
        </button>
      </div>
      <button
        onClick={onOpenPalette}
        className="bg-accent/20 hover:bg-accent/30 text-accent px-4 py-2 rounded-lg transition-colors"
      >
        ⌘K
      </button>
    </div>
  )
}
