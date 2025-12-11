import { useEffect } from 'react';
import { useReducedMotion } from 'framer-motion';

interface ConfettiTriggerProps {
  triggerKey: string;
}

export function ConfettiTrigger({ triggerKey }: ConfettiTriggerProps) {
  const prefersReducedMotion = useReducedMotion();

  useEffect(() => {
    if (!triggerKey || prefersReducedMotion) return;

    async function runConfetti() {
      const module = await import('canvas-confetti');
      const confetti = module.default;
      confetti({
        particleCount: 120,
        spread: 70,
        origin: { y: 0.6 }
      });
    }

    runConfetti();
  }, [triggerKey, prefersReducedMotion]);

  return null;
}
