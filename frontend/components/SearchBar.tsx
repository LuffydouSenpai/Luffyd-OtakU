'use client';

import { FormEvent } from "react";

type SearchBarProps = {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  onSubmit?: (value: string) => void;
  onFocus?: () => void;
  onClear?: () => void;
};

export default function SearchBar({
  placeholder = 'Rechercher...',
  value,
  onChange,
  onSubmit,
  onFocus,
  onClear
}: SearchBarProps) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit(value.trim());
    }
  };
  return (
    <form onSubmit={handleSubmit} className="flex items-center w-full">
      <div className="relative w-full">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={onFocus}
          placeholder={placeholder}
          className="w-full px-4 py-2 rounded-l-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-card"
        />
        {value.trim() !== '' && (
          <button
            type="button"
            onClick={onClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
          >
            ✕
          </button>
        )}
      </div>
      <button
        type="submit"
        className="bg-purple-card hover:bg-purple text-white px-4 py-2 rounded-r-md"
      >
        Go
      </button>
    </form>
  );
}