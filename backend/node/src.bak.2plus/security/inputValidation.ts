/**
 * Security: Input Validation Utilities
 * Ready for integration with pentest scanners
 */
export function sanitizeString(input: string): string {
    return input.replace(/[<>]/g, '');
}
