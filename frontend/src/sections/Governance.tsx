import { SectionCard } from '@/components/SectionCard';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';
import type { GovernanceFlag } from '@/types/api';

const fallback: GovernanceFlag[] = [
  {
    id: 'pii-hash',
    title: 'PII Hashing Required',
    description: 'Columns `email`, `employee_id` auto-hashed with salt.',
    severity: 'weak'
  },
  {
    id: 'bias',
    title: 'Bias guardrail review',
    description: 'Teacher progression flagged for additional interpretation review.',
    severity: 'moderate',
    remediation: 'Attach methodology note to output before publishing.'
  }
];

export function GovernanceSection() {
  const flags = useCosurvivalStore((state) => state.governanceFlags);
  const data = flags.length ? flags : fallback;

  return (
    <SectionCard
      title="Governance & Risk"
      description="Triple Balance verdicts · severity · remediation"
      actions={
        <a className="text-xs text-sky-300 underline" href="/output/governance_report.json">
          Download report
        </a>
      }
    >
      <div className="flex flex-col gap-3">
        {data.map((flag) => (
          <div key={flag.id} className="rounded-xl border border-white/10 p-4">
            <div className="flex items-center justify-between">
              <p className="font-semibold text-white">{flag.title}</p>
              <span
                className={`text-xs uppercase ${
                  flag.severity === 'critical'
                    ? 'text-red-300'
                    : flag.severity === 'strong'
                    ? 'text-orange-300'
                    : flag.severity === 'moderate'
                    ? 'text-amber-300'
                    : 'text-emerald-300'
                }`}
              >
                {flag.severity}
              </span>
            </div>
            <p className="text-sm text-white/70">{flag.description}</p>
            {flag.remediation && (
              <p className="text-xs text-white/50">Next step: {flag.remediation}</p>
            )}
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
