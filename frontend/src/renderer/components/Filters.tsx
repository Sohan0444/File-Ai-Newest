import React from 'react'

export interface FiltersState {
  types: string[]
  tag: string
  date: string
}

interface FiltersProps {
  value: FiltersState
  onChange: (filters: FiltersState) => void
}

const fileTypes = ['PDF', 'MD', 'TXT', 'DOC', 'XLS', 'PPT', 'IMG', 'VID', 'AUD']

export default function Filters({ value, onChange }: FiltersProps) {
  const toggleType = (type: string) => {
    const newTypes = value.types.includes(type)
      ? value.types.filter(t => t !== type)
      : [...value.types, type]
    onChange({ ...value, types: newTypes })
  }

  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-sm font-medium text-white/70 mb-2">File Types</h3>
        <div className="flex flex-wrap gap-2">
          {fileTypes.map(type => (
            <button
              key={type}
              onClick={() => toggleType(type)}
              className={`px-3 py-1 rounded-full text-xs transition-colors ${
                value.types.includes(type)
                  ? 'bg-neon/20 text-neon border border-neon/30'
                  : 'bg-white/5 text-white/50 border border-white/10 hover:bg-white/10'
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>
      
      <div>
        <h3 className="text-sm font-medium text-white/70 mb-2">Tag Filter</h3>
        <input
          type="text"
          placeholder="Filter by tag..."
          value={value.tag}
          onChange={(e) => onChange({ ...value, tag: e.target.value })}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-white placeholder-white/50 focus:outline-none focus:border-neon/50 text-sm"
        />
      </div>
      
      <div>
        <h3 className="text-sm font-medium text-white/70 mb-2">Date Range</h3>
        <select
          value={value.date}
          onChange={(e) => onChange({ ...value, date: e.target.value })}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-neon/50 text-sm"
        >
          <option value="any">Any time</option>
          <option value="today">Today</option>
          <option value="week">This week</option>
          <option value="month">This month</option>
          <option value="year">This year</option>
        </select>
      </div>
    </div>
  )
}
