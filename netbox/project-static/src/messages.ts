import { Toast } from 'bootstrap';

/**
 * Find any active messages from django.contrib.messages and show them in a toast.
 */
export function initMessages(): void {
  const elements = document.querySelectorAll<HTMLDivElement>(
    'body > div#django-messages > div.toast',
  );
  for (const element of elements) {
    if (element !== null) {
      const toast = new Toast(element);
      if (!toast.isShown()) {
        toast.show();
      }
    }
  }
}
