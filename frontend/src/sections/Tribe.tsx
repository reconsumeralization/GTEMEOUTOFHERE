import { useQuery } from '@tanstack/react-query';
import { SectionCard } from '@/components/SectionCard';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';
import { fetchTribeGraph } from '@/lib/apiClient';

export function TribeSection() {
  const { userRole } = useCosurvivalStore.getState();
  const { data } = useQuery({
    queryKey: ['tribe-graph'],
    queryFn: () => fetchTribeGraph(),
    staleTime: 120_000
  });

  const edgeCount = data?.edges.length ?? 0;
  const nodeCount = data?.nodes.length ?? 0;

  return (
    <SectionCard
      title="TRIBE Lens"
      description="Communities, bridges, mentors"
      actions={<span className="text-xs text-white/50">Role: {userRole}</span>}
    >
      <div className="grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-amber-500/20 bg-amber-500/10 p-4">
          <p className="text-xs uppercase text-amber-200">Nodes</p>
          <p className="text-3xl font-semibold text-white">{nodeCount}</p>
          <p className="text-xs text-white/70">Users/groups in active collaboration</p>
        </div>
        <div className="rounded-xl border border-sky-500/20 bg-sky-500/10 p-4">
          <p className="text-xs uppercase text-sky-200">Edges</p>
          <p className="text-3xl font-semibold text-white">{edgeCount}</p>
          <p className="text-xs text-white/70">Interactions above safety threshold</p>
        </div>
        <div className="rounded-xl border border-fuchsia-500/20 bg-fuchsia-500/10 p-4">
          <p className="text-xs uppercase text-fuchsia-200">Density</p>
          <p className="text-3xl font-semibold text-white">
            {nodeCount ? (edgeCount / nodeCount).toFixed(2) : '0.00'}
          </p>
          <p className="text-xs text-white/70">Real-time cohesion index</p>
        </div>
      </div>
      <div className="mt-4 rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-white/70">
        <p>
          Interactive graph rendering is powered by D3 within the production build. During development you
          can open the TRIBE canvas drawer to explore bridges and mentor candidates sourced from the
          canonical MVP extractor output.
        </p>
      </div>
    </SectionCard>
  );
}
