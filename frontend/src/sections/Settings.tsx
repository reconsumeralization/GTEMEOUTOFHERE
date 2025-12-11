import { SectionCard } from '@/components/SectionCard';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';

export function SettingsSection() {
  const userId = useCosurvivalStore((state) => state.userId);
  const userRole = useCosurvivalStore((state) => state.userRole);

  return (
    <SectionCard title="Settings" description="Agency controls, preferences, and API access">
      <div className="space-y-4 text-sm text-white/70">
        <div className="rounded-2xl border border-white/10 p-4">
          <p className="text-xs uppercase text-white/50">Identity</p>
          <p>{userId}</p>
          <p className="text-xs text-white/50">Role: {userRole}</p>
        </div>
        <div className="rounded-2xl border border-white/10 p-4">
          <p className="text-xs uppercase text-white/50">Notifications</p>
          <p>Preference: Moderate cadence</p>
          <p className="text-xs">Adjust via forthcoming preference API.</p>
        </div>
        <div className="rounded-2xl border border-white/10 p-4">
          <p className="text-xs uppercase text-white/50">API Keys</p>
          <p>Managed via secret manager per governance policy.</p>
        </div>
      </div>
    </SectionCard>
  );
}
