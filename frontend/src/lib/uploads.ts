/**
 * uploads.ts — Pure functions for drag-drop and file input handling.
 *
 * Extracted from ProjectsEditor.svelte (REQ-TS-EXTRACTION).
 * These functions filter and collect files without side effects.
 */

/**
 * Collect only image/* files from a DataTransfer (drag-drop event).
 * Non-image files (PDFs, scripts, etc.) are silently ignored.
 */
export function collectDroppedImageFiles(dt: DataTransfer): File[] {
  const result: File[] = [];
  for (const file of Array.from(dt.files)) {
    if (file.type.startsWith('image/')) {
      result.push(file);
    }
  }
  return result;
}

/**
 * Collect all files from an HTMLInputElement (file picker).
 * Returns an array copy of the FileList.
 */
export function collectInputFiles(input: HTMLInputElement): File[] {
  if (!input.files) return [];
  return Array.from(input.files);
}
