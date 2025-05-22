'use client';
import { useState } from 'react';

type SearchBarProps = {
  placeholder?: string;
  onSearch: (value: string) => void;
};

export default function SearchBar({ placeholder = 'Rechercher...', onSearch }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center w-full">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className="w-full px-4 py-2 rounded-l-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple2"
      />
      <button
        type="submit"
        className="bg-purple2 hover:bg-purple text-white px-4 py-2 rounded-r-md"
      >
        Go
      </button>
    </form>
  );
}