import { TomOption } from 'tom-select/src/types';
import TomSelect from 'tom-select';
import { escape_html } from 'tom-select/src/utils';
import { getPlugins } from './config';
import { getElements } from '../util';

// Initialize <select> elements with statically-defined options
export function initStaticSelects(): void {
  for (const select of getElements<HTMLSelectElement>(
    'select:not(.tomselected):not(.no-ts):not([size]):not(.api-select):not(.color-select)',
  )) {
    new TomSelect(select, {
      ...getPlugins(select),
      maxOptions: undefined,
    });
  }
}

// Initialize color selection fields
export function initColorSelects(): void {
  function renderColor(item: TomOption, escape: typeof escape_html) {
    return `<div><span class="dropdown-item-indicator color-label" style="background-color: #${escape(
      item.value,
    )}"></span> ${escape(item.text)}</div>`;
  }

  for (const select of getElements<HTMLSelectElement>('select.color-select:not(.tomselected)')) {
    new TomSelect(select, {
      ...getPlugins(select),
      maxOptions: undefined,
      render: {
        option: renderColor,
        item: renderColor,
      },
    });
  }
}
