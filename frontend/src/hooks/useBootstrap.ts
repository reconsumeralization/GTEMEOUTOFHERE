import { useMemo } from 'react';
import type { BootstrapPayload } from '@/types/api';

declare global {
  interface Window {
    __COSURVIVAL_BOOTSTRAP__?: BootstrapPayload;
  }
}

export function useBootstrap(): BootstrapPayload {
  return useMemo(() => {
    if (typeof window === 'undefined') {
      return {};
    }
    return window.__COSURVIVAL_BOOTSTRAP__ || {};
  }, []);
}
