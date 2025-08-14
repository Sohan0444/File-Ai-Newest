import React, { useState, useEffect } from 'react'

interface CommandPaletteProps {
  open: boolean
  onClose: () => void
  onAction: (action: string) => void
}

const commands = [
  { id: 'search', label: 'Search files', icon: '🔍' },
  { id: 'reindex', label: 'Reindex files', icon: '🔄' },
  { id: 'settings', label: 'Settings', icon: '⚙️' },
  { id: 'help', label: 'Help', icon: '❓' }
]

export default function CommandPalette({ open, onClose, onAction }: CommandPaletteProps) {
  const [query, setQuery] = useState('')
  const [selectedIndex, setSelectedIndex] = useState(0)

  const filteredCommands = commands.filter(cmd => 
    cmd.label.toLowerCase().includes(query.toLowerCase())
  )

  useEffect(() => {
    if (open) {
      setQuery('')
      setSelectedIndex(0)
    }
  }, [open])

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!open) return

      switch (e.key) {
        case 'Escape':
          onClose()
          break
        case 'ArrowDown':
          e.preventDefault()
          setSelectedIndex(prev => 
            prev < filteredCommands.length - 1 ? prev + 1 : 0
          )
          break
        case 'ArrowUp':
          e.preventDefault()
          setSelectedIndex(prev => 
            prev > 0 ? prev - 1 : filteredCommands.length - 1
          )
          break
        case 'Enter':
          e.preventDefault()
          if (filteredCommands[selectedIndex]) {
            onAction(filteredCommands[selectedIndex].id)
            onClose()
          }
          break
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [open, selectedIndex, filteredCommands, onClose, onAction])

  if (!open) return null

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-base border border-white/10 rounded-lg shadow-soft w-full max-w-md mx-4">
        <div className="p-4 border-b border-white/10">
          <input
            type="text"
            placeholder="Type a command..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-white placeholder-white/50 focus:outline-none text-lg"
            autoFocus
          />
        </div>
        
        <div className="max-h-64 overflow-auto">
          {filteredCommands.length === 0 ? (
            <div className="p-4 text-white/50 text-center">
              No commands found
            </div>
          ) : (
            filteredCommands.map((cmd, index) => (
              <button
                key={cmd.id}
                onClick={() => {
                  onAction(cmd.id)
                  onClose()
                }}
                className={`w-full p-4 text-left flex items-center gap-3 transition-colors ${
                  index === selectedIndex
                    ? 'bg-neon/20 text-neon'
                    : 'text-white hover:bg-white/5'
                }`}
              >
                <span className="text-xl">{cmd.icon}</span>
                <span>{cmd.label}</span>
              </button>
            ))
          )}
        </div>
        
        <div className="p-4 border-t border-white/10 text-xs text-white/50">
          Use ↑↓ to navigate, Enter to select, Esc to close
        </div>
      </div>
    </div>
  )
}
