const cvMarkers = [/###\s+Name:/i, /##\s+Tailored CV/i, /#\s+Petro/i, /Tailored CV Snapshot/i];
const coverLetterMarkers = [/\bDear\b/, /\bHello\b/, /Cover Letter/i];

function stripBeforeMarker(text: string, markers: RegExp[]): string {
  const trimmed = text.trim();
  for (const marker of markers) {
    const match = trimmed.search(marker);
    if (match >= 0) {
      return trimmed.slice(match).trim();
    }
  }
  return trimmed;
}

export function sanitizeCvText(text: string): string {
  return stripBeforeMarker(text, cvMarkers);
}

export function sanitizeCoverLetterText(text: string): string {
  return stripBeforeMarker(text, coverLetterMarkers);
}
