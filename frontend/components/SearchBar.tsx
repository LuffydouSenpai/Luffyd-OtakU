'use client';

import { FormEvent } from "react";

type SearchBarProps = {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  onSubmit?: (value: string) => void;
};

export default function SearchBar({
  placeholder = 'Rechercher...',
  value,
  onChange,
  onSubmit,
}: SearchBarProps) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit(value.trim());
    }
  };
  return (
    <form onSubmit={handleSubmit} className="flex items-center w-full">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
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