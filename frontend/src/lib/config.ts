const API_BASE_URL = import.meta.env.PUBLIC_API_URL;

export async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const config: RequestInit = {
    ...options,
    headers: { ...options?.headers },
  };

  if (!(options?.body instanceof FormData)) {
    config.headers = {
      ...config.headers,
      "Content-Type": "application/json",
    };
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    let errorMessage = "Error desconocido del servidor";
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // usar mensaje por defecto
    }
    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}
