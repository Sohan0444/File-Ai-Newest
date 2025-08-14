import React from 'react'

export interface FileItem {
  id: string
  name: string
  path: string
  size: number
  type: string
  modified: number
  tags: string[]
}

interface FileGridProps {
  items: FileItem[]
  onSelect: (item: FileItem) => void
}

const getFileIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'pdf': return '📄'
    case 'md': return '📝'
    case 'txt': return '📄'
    case 'doc': return '📄'
    case 'xls': return '📊'
    case 'ppt': return '📊'
    case 'img': return '🖼️'
    case 'vid': return '🎥'
    case 'aud': return '🎵'
    default: return '📄'
  }
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

export default function FileGrid({ items, onSelect }: FileGridProps) {
  if (items.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-white/50">
        <div className="text-center">
          <div className="text-4xl mb-4">📁</div>
          <div>No files found</div>
          <div className="text-sm">Try adjusting your search or filters</div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="grid grid-cols-1 gap-2">
        {items.map(item => (
          <div
            key={item.id}
            onClick={() => onSelect(item)}
            className="bg-panel/50 backdrop-blur-sm border border-white/10 rounded-lg p-4 hover:bg-panel/70 hover:border-white/20 transition-all cursor-pointer"
          >
            <div className="flex items-center gap-3">
              <div className="text-2xl">{getFileIcon(item.type)}</div>
              <div className="flex-1 min-w-0">
                <div className="font-medium text-white truncate">{item.name}</div>
                <div className="text-sm text-white/50">
                  {formatFileSize(item.size)} • {new Date(item.modified).toLocaleDateString()}
                </div>
              </div>
              <div className="flex gap-1">
                {item.tags.map(tag => (
                  <span
                    key={tag}
                    className="px-2 py-1 bg-neon/20 text-neon text-xs rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
