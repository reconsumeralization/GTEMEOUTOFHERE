import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { SectionCard } from '@/components/SectionCard';
import { fetchAdvisorSignals } from '@/lib/apiClient';

const severityColor: Record<string, string> = {
  critical: 'text-red-300',
  strong: 'text-orange-300',
  moderate: 'text-amber-300',
  weak: 'text-emerald-300'
};

export function AdvisorSection() {
  const { data } = useQuery({
    queryKey: ['advisor-signals'],
    queryFn: fetchAdvisorSignals,
    staleTime: 60_000
  });

  return (
    <SectionCard
      title="Advisor Feed"
      description="Explainable recommendations with agency-first controls"
    >
      <div className="space-y-4">
        {(data ?? []).map((signal) => (
          <motion.div
            key={signal.id}
            className="rounded-2xl border border-white/10 p-4"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="flex items-center justify-between">
              <p className="font-semibold text-white">{signal.title}</p>
              <span className={`text-xs uppercase ${severityColor[signal.severity]}`}>{signal.severity}</span>
            </div>
            <p className="mt-2 text-sm text-white/70">{signal.whyNow}</p>
            <div className="mt-3 text-xs text-white/50">
              <p>Confidence: {(signal.confidence * 100).toFixed(0)}%</p>
              <p>Evidence: {signal.evidence.join(', ')}</p>
            </div>
            <div className="mt-3 flex gap-2">
              <button className="rounded-full bg-white/10 px-3 py-1 text-xs text-white/80">
                View reasoning
              </button>
              <button className="rounded-full border border-white/20 px-3 py-1 text-xs text-white/80">
                Dismiss
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </SectionCard>
  );
}
