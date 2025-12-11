import { SectionCard } from '@/components/SectionCard';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';
import type { PipelineStage } from '@/types/api';

const fallbackStages: PipelineStage[] = [
  {
    id: 'governance',
    label: 'Governance Gate',
    status: 'passed',
    updatedAt: new Date().toISOString(),
    link: '/output/governance_report.json'
  },
  {
    id: 'ingestion',
    label: 'Schema Ingestion',
    status: 'passed'
  },
  {
    id: 'extraction',
    label: 'MVP Extraction',
    status: 'running'
  },
  {
    id: 'unified',
    label: 'Unified Output',
    status: 'pending'
  }
];

export function PipelineSection() {
  const stages = useCosurvivalStore((state) => state.pipelineStages);
  const data = stages.length ? stages : fallbackStages;

  return (
    <SectionCard
      title="Pipeline & Artifacts"
      description="Governance → Ingestion → MVP → Unified JSON"
      actions={
        <a
          href="/output/pipeline_results.json"
          className="rounded-full border border-white/30 px-3 py-1 text-xs text-white/80"
        >
          View Results JSON
        </a>
      }
    >
      <div className="flex flex-col gap-4">
        {data.map((stage) => (
          <div key={stage.id} className="flex flex-col gap-1 rounded-xl border border-white/10 p-4">
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-white">{stage.label}</p>
              <span
                className={`rounded-full px-2 py-0.5 text-xs uppercase tracking-wide ${
                  stage.status === 'failed'
                    ? 'bg-red-500/20 text-red-300'
                    : stage.status === 'running'
                    ? 'bg-amber-500/20 text-amber-200'
                    : stage.status === 'passed'
                    ? 'bg-emerald-500/20 text-emerald-200'
                    : 'bg-white/10 text-white/70'
                }`}
              >
                {stage.status}
              </span>
            </div>
            {stage.updatedAt && (
              <p className="text-xs text-white/50">Updated {new Date(stage.updatedAt).toLocaleString()}</p>
            )}
            {stage.link && (
              <a
                className="text-xs text-sky-300 underline"
                href={stage.link}
                target="_blank"
                rel="noreferrer"
              >
                Open artifact
              </a>
            )}
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
