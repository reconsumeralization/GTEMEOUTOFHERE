import { useQuery } from '@tanstack/react-query';
import { SectionCard } from '@/components/SectionCard';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';
import { fetchRecommendations } from '@/lib/apiClient';

export function TeacherSection() {
  const userId = useCosurvivalStore((state) => state.userId);
  const { data } = useQuery({
    queryKey: ['teacher-recs', userId],
    queryFn: () => fetchRecommendations(userId),
    enabled: Boolean(userId)
  });

  const recs = data ?? [
    { skill: 'role_admin_read', frequency: 12 },
    { skill: 'role_case_manage', frequency: 9 },
    { skill: 'role_support_lead', frequency: 7 }
  ];

  return (
    <SectionCard title="TEACHER Lens" description="Learning pathways & role ladders">
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-2xl border border-white/10 p-4">
          <p className="text-xs uppercase text-white/50">Top Recommendations</p>
          <ul className="mt-3 space-y-3">
            {recs.map((rec) => (
              <li key={rec.skill} className="flex items-center justify-between text-sm text-white">
                <span className="font-medium">{rec.skill}</span>
                <span className="text-xs text-white/60">{rec.frequency} recent approvals</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-2xl border border-white/10 p-4">
          <p className="text-xs uppercase text-white/50">Progression Timeline</p>
          <div className="mt-3 space-y-2 text-xs text-white/70">
            <p>• Core access: Completed</p>
            <p>• Elevated permissions: In review</p>
            <p>• Mentor pathway: Pending governance sign-off</p>
          </div>
        </div>
      </div>
    </SectionCard>
  );
}
