import React from 'react'
import { FileItem } from './FileGrid'
import { openFile } from '../lib/ipc'

interface DetailsPanelProps {
  item: FileItem | null
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

export default function DetailsPanel({ item }: DetailsPanelProps) {
  if (!item) {
    return (
      <div className="h-full flex items-center justify-center text-white/50">
        <div className="text-center">
          <div className="text-4xl mb-4">📄</div>
          <div>Select a file to view details</div>
        </div>
      </div>
    )
  }

  const handleOpen = async () => {
    try {
      await openFile(item.path)
    } catch (error) {
      console.error('Failed to open file:', error)
    }
  }

  return (
    <div className="h-full bg-panel/30 backdrop-blur-sm border border-white/10 rounded-lg p-6">
      <div className="space-y-6">
        <div>
          <h2 className="text-xl font-semibold text-white mb-2">{item.name}</h2>
          <div className="text-sm text-white/50 break-all">{item.path}</div>
        </div>
        
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-white/70">Size:</span>
            <span className="text-white">{formatFileSize(item.size)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-white/70">Type:</span>
            <span className="text-white">{item.type.toUpperCase()}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-white/70">Modified:</span>
            <span className="text-white">{new Date(item.modified).toLocaleString()}</span>
          </div>
        </div>
        
        {item.tags.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-white/70 mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {item.tags.map(tag => (
                <span
                  key={tag}
                  className="px-3 py-1 bg-neon/20 text-neon text-sm rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}
        
        <div className="pt-4">
          <button
            onClick={handleOpen}
            className="w-full bg-neon/20 hover:bg-neon/30 text-neon py-3 rounded-lg transition-colors font-medium"
          >
            Open File
          </button>
        </div>
      </div>
    </div>
  )
}
