import { describe, it, expect } from 'vitest';
import { collectDroppedImageFiles, collectInputFiles } from '$lib/uploads';

function makeFile(name: string, type: string): File {
  return new File(['content'], name, { type });
}

/**
 * Minimal DataTransfer stub — jsdom doesn't provide the DataTransfer constructor.
 * Only `files` (a FileList-like) is needed by collectDroppedImageFiles.
 */
function makeDataTransfer(files: File[]): DataTransfer {
  const fileList = {
    length: files.length,
    item: (index: number) => files[index] ?? null,
    [Symbol.iterator]: function* () {
      for (const f of files) yield f;
    },
  } as FileList;
  // Attach files by index for Array.from() compatibility
  for (let i = 0; i < files.length; i++) {
    (fileList as any)[i] = files[i];
  }
  return { files: fileList } as unknown as DataTransfer;
}

describe('collectDroppedImageFiles', () => {
  it('returns only image/* files from a mixed DataTransfer', () => {
    const files = [
      makeFile('photo.jpg', 'image/jpeg'),
      makeFile('doc.pdf', 'application/pdf'),
      makeFile('logo.png', 'image/png'),
      makeFile('script.js', 'text/javascript'),
      makeFile('icon.svg', 'image/svg+xml'),
    ];
    const dt = makeDataTransfer(files);

    const result = collectDroppedImageFiles(dt);

    expect(result).toHaveLength(3);
    expect(result[0].name).toBe('photo.jpg');
    expect(result[1].name).toBe('logo.png');
    expect(result[2].name).toBe('icon.svg');
  });

  it('returns empty array when no image files are dropped', () => {
    const files = [
      makeFile('doc.pdf', 'application/pdf'),
      makeFile('data.json', 'application/json'),
    ];
    const dt = makeDataTransfer(files);

    const result = collectDroppedImageFiles(dt);

    expect(result).toHaveLength(0);
  });

  it('returns all files when all are images', () => {
    const files = [
      makeFile('a.jpg', 'image/jpeg'),
      makeFile('b.webp', 'image/webp'),
    ];
    const dt = makeDataTransfer(files);

    const result = collectDroppedImageFiles(dt);

    expect(result).toHaveLength(2);
    expect(result.map((f) => f.name)).toEqual(['a.jpg', 'b.webp']);
  });

  it('returns empty array for empty DataTransfer', () => {
    const dt = makeDataTransfer([]);

    const result = collectDroppedImageFiles(dt);

    expect(result).toHaveLength(0);
  });
});

describe('collectInputFiles', () => {
  it('returns File array from input element', () => {
    const files = [
      makeFile('photo.jpg', 'image/jpeg'),
      makeFile('logo.png', 'image/png'),
    ];
    const fileList = {
      length: files.length,
      item: (index: number) => files[index] ?? null,
      [Symbol.iterator]: function* () {
        for (const f of files) yield f;
      },
      ...Object.fromEntries(files.map((f, i) => [i, f])),
    } as FileList;

    const input = document.createElement('input');
    input.type = 'file';
    input.multiple = true;
    Object.defineProperty(input, 'files', { value: fileList });

    const result = collectInputFiles(input);

    expect(result).toHaveLength(2);
    expect(result[0].name).toBe('photo.jpg');
    expect(result[1].name).toBe('logo.png');
  });

  it('returns empty array when input has no files', () => {
    const input = document.createElement('input');
    input.type = 'file';
    Object.defineProperty(input, 'files', { value: null });

    const result = collectInputFiles(input);

    expect(result).toHaveLength(0);
  });
});
