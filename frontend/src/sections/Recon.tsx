import { useQuery } from '@tanstack/react-query';
import { SectionCard } from '@/components/SectionCard';
import { fetchProviders } from '@/lib/apiClient';

export function ReconSection() {
  const { data } = useQuery({
    queryKey: ['recon-providers'],
    queryFn: () => fetchProviders(),
    staleTime: 120_000
  });

  const providers = data?.slice(0, 5) ?? [
    { provider_id: 'prov-101', reliability: 0.992, total_activities: 640, error_count: 5, grade: 'A' },
    { provider_id: 'prov-212', reliability: 0.965, total_activities: 482, error_count: 17, grade: 'B' }
  ];

  return (
    <SectionCard title="RECON Lens" description="Provider reliability · ethics · value flows">
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm text-white/80">
          <thead className="text-left text-xs uppercase text-white/40">
            <tr>
              <th className="pb-2">Provider</th>
              <th className="pb-2">Reliability</th>
              <th className="pb-2">Activities</th>
              <th className="pb-2">Errors</th>
              <th className="pb-2">Grade</th>
            </tr>
          </thead>
          <tbody>
            {providers.map((provider) => (
              <tr key={provider.provider_id} className="border-t border-white/5">
                <td className="py-3 font-medium text-white">{provider.provider_id}</td>
                <td className="py-3">{(provider.reliability * 100).toFixed(2)}%</td>
                <td className="py-3">{provider.total_activities.toLocaleString()}</td>
                <td className="py-3">{provider.error_count}</td>
                <td className="py-3 font-semibold">{provider.grade}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </SectionCard>
  );
}
