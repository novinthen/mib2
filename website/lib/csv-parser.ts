// Strict CSV parser with schema validation
// Fails on duplicate IDs, broken references, missing critical columns, or malformed numbers

import fs from 'fs';

export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export function parseCSV<T>(filePath: string): T[] {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.split('\n').filter((line) => line.trim());

  if (lines.length < 2) {
    throw new ValidationError(`${filePath}: No data rows found`);
  }

  const headers = lines[0].split(',').map((h) => h.trim());
  const rows: T[] = [];
  const seenIds = new Set<string>();

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    const values = parseCSVLine(line);

    if (values.length !== headers.length) {
      throw new ValidationError(
        `${filePath}:${i + 1}: Expected ${headers.length} fields, got ${values.length}`
      );
    }

    const row: Record<string, string> = {};
    headers.forEach((header, idx) => {
      row[header] = values[idx];
    });

    // Check for duplicate IDs if there's an id field
    const idField = Object.keys(row).find((k) =>
      k.toLowerCase().includes('_id') && k !== 'source_id' && k !== 'conflict_id'
    );
    if (idField && row[idField]) {
      if (seenIds.has(row[idField])) {
        throw new ValidationError(
          `${filePath}:${i + 1}: Duplicate ID ${row[idField]}`
        );
      }
      seenIds.add(row[idField]);
    }

    rows.push(row as T);
  }

  return rows;
}

function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += char;
    }
  }

  result.push(current.trim());
  return result;
}

export function parseNumber(value: string, context: string): number {
  if (!value || value === '') {
    return 0;
  }

  const cleaned = value.replace(/,/g, '');
  const num = parseFloat(cleaned);

  if (isNaN(num)) {
    throw new ValidationError(`${context}: Invalid number "${value}"`);
  }

  if (num < 0) {
    throw new ValidationError(`${context}: Negative number not allowed "${value}"`);
  }

  return num;
}

export function validateRequired(value: string | undefined, field: string, context: string): void {
  if (!value || value.trim() === '') {
    throw new ValidationError(`${context}: Required field "${field}" is missing or empty`);
  }
}

export function validateForeignKey<T, K extends keyof T>(
  value: string,
  registry: T[],
  keyField: K,
  context: string
): void {
  if (!value || value === '') return; // Allow empty for optional references

  const found = registry.some((item) => String(item[keyField]) === value);
  if (!found) {
    throw new ValidationError(
      `${context}: Foreign key "${value}" not found in ${String(keyField)} registry`
    );
  }
}
