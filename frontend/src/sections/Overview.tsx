import { motion } from 'framer-motion';
import { SectionCard } from '@/components/SectionCard';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';

const defaultStats = [
  { label: 'Users', value: '12,482', subtitle: '+3.2% past 30d' },
  { label: 'Providers', value: '238', subtitle: '99.1% avg. reliability' },
  { label: 'Governance Pass Rate', value: '100%', subtitle: 'Last 14 runs' },
  { label: 'Advisor Signals', value: '4', subtitle: '2 moderate · 2 weak' }
];

export function OverviewSection() {
  const pipelineStages = useCosurvivalStore((state) => state.pipelineStages);

  return (
    <SectionCard
      title="Mission Control"
      description="Unified snapshot of TRIBE · TEACHER · RECON"
    >
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {defaultStats.map((stat) => (
          <motion.div
            key={stat.label}
            className="rounded-2xl border border-white/10 bg-white/5 p-4"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-xs uppercase text-white/60">{stat.label}</p>
            <p className="text-2xl font-semibold text-white">{stat.value}</p>
            <p className="text-xs text-white/50">{stat.subtitle}</p>
          </motion.div>
        ))}
      </div>
      <div className="mt-6">
        <p className="text-xs uppercase text-white/60">Pipeline</p>
        <ol className="mt-2 flex flex-wrap gap-4">
          {(pipelineStages.length
            ? pipelineStages
            : [
                { id: 'governance', label: 'Governance', status: 'passed' },
                { id: 'ingestion', label: 'Ingestion', status: 'passed' },
                { id: 'extraction', label: 'Extraction', status: 'passed' },
                { id: 'unified', label: 'Unified Output', status: 'running' }
              ]
          ).map((stage) => (
            <li key={stage.id} className="flex items-center gap-2">
              <span
                className={`h-2 w-2 rounded-full ${
                  stage.status === 'failed'
                    ? 'bg-red-500'
                    : stage.status === 'running'
                    ? 'bg-amber-400'
                    : 'bg-emerald-400'
                }`}
              />
              <span className="text-sm text-white/80">{stage.label}</span>
            </li>
          ))}
        </ol>
      </div>
    </SectionCard>
  );
}
