// Sistema de eventos para sincronizar cambios entre admin y componentes públicos

type DataChangeEvent = CustomEvent<{
  type: 'hero' | 'about' | 'stack' | 'projects' | 'passions' | 'footer';
  action: 'create' | 'update' | 'delete';
  data?: any;
}>;

// Función para disparar eventos desde el admin
export function dispatchDataChange(
  type: DataChangeEvent['detail']['type'],
  action: DataChangeEvent['detail']['action'],
  data?: any
) {
  const event = new CustomEvent('dataChange', {
    detail: { type, action, data }
  });
  document.dispatchEvent(event);
}

// Hook para que los componentes escuchen cambios
export function listenForDataChange(
  type: DataChangeEvent['detail']['type'],
  callback: () => void | Promise<void>
) {
  const handler = async (e: Event) => {
    const event = e as DataChangeEvent;
    if (event.detail.type === type) {
      await callback();
    }
  };
  
  document.addEventListener('dataChange', handler);
  
  // Retorna función de limpieza
  return () => {
    document.removeEventListener('dataChange', handler);
  };
}
