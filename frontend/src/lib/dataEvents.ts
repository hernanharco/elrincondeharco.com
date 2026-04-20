// Sistema de eventos para sincronizar cambios entre admin y componentes públicos

// Tipos de datos válidos para eventos
type DataType = 'hero' | 'about' | 'stack' | 'projects' | 'passions' | 'footer' | 'site-settings' | 'showroom';

type DataChangeEvent = CustomEvent<{
  type: DataType;
  action: 'create' | 'update' | 'delete';
  data?: any;
}>;

// Función para disparar eventos desde el admin
export function dispatchDataChange(
  type: DataType,
  action: 'create' | 'update' | 'delete',
  data?: any
) {
  const event = new CustomEvent('dataChange', {
    detail: { type, action, data }
  });
  document.dispatchEvent(event);
}

// Hook para que los componentes escuchen cambios
export function listenForDataChange(
  type: DataType,
  callback: (event?: CustomEvent) => Promise<void> | void
) {
  const handler = async (e: Event) => {
    const customEvent = e as CustomEvent;
    if (customEvent.detail.type === type) {
      await callback(customEvent);
    }
  };

  document.addEventListener('dataChange', handler);

  // Return cleanup function
  return () => {
    document.removeEventListener('dataChange', handler);
  };
}
