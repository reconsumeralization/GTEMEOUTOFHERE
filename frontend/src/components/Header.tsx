import { motion } from 'framer-motion';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';

interface HeaderProps {
  onSectionChange: (section: string) => void;
  activeSection: string;
}

const sections = [
  'overview',
  'pipeline',
  'governance',
  'tribe',
  'teacher',
  'recon',
  'advisor',
  'reviews',
  'settings'
];

export function Header({ activeSection, onSectionChange }: HeaderProps) {
  const userId = useCosurvivalStore((state) => state.userId);
  const userRole = useCosurvivalStore((state) => state.userRole);

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-black/60 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-white/60">Cosurvival</p>
          <h1 className="text-2xl font-semibold text-white">Connected Intelligence Network</h1>
          <p className="text-xs text-white/50">{userId} · {userRole}</p>
        </div>
        <nav className="flex flex-wrap gap-2 text-xs">
          {sections.map((section) => (
            <button
              key={section}
              type="button"
              onClick={() => onSectionChange(section)}
              className={`relative rounded-full px-3 py-1.5 capitalize transition ${
                activeSection === section ? 'bg-white text-black' : 'bg-white/5 text-white/70'
              }`}
            >
              {activeSection === section && (
                <motion.span
                  layoutId="active-pill"
                  className="absolute inset-0 rounded-full bg-white"
                  transition={{ type: 'spring', bounce: 0.25, duration: 0.4 }}
                />
              )}
              <span className="relative z-10">{section}</span>
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}
