import { useEffect, useState } from 'react';
import { useBootstrap } from '@/hooks/useBootstrap';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';
import { Header } from '@/components/Header';
import { OverviewSection } from '@/sections/Overview';
import { PipelineSection } from '@/sections/Pipeline';
import { GovernanceSection } from '@/sections/Governance';
import { TribeSection } from '@/sections/Tribe';
import { TeacherSection } from '@/sections/Teacher';
import { ReconSection } from '@/sections/Recon';
import { AdvisorSection } from '@/sections/Advisor';
import { ReviewsSection } from '@/sections/Reviews';
import { SettingsSection } from '@/sections/Settings';

const sectionComponents: Record<string, JSX.Element> = {
  overview: <OverviewSection />,
  pipeline: <PipelineSection />,
  governance: <GovernanceSection />,
  tribe: <TribeSection />,
  teacher: <TeacherSection />,
  recon: <ReconSection />,
  advisor: <AdvisorSection />,
  reviews: <ReviewsSection />,
  settings: <SettingsSection />
};

export default function App() {
  const bootstrap = useBootstrap();
  const setUser = useCosurvivalStore((state) => state.setUser);
  const [activeSection, setActiveSection] = useState<keyof typeof sectionComponents>('overview');

  useEffect(() => {
    setUser(bootstrap.currentUser ?? 'anonymous', bootstrap.userRole ?? 'consumer', bootstrap.csrfToken);
  }, [bootstrap, setUser]);

  return (
    <div className="min-h-screen">
      <Header activeSection={activeSection} onSectionChange={(section) => setActiveSection(section as any)} />
      <main className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-8">
        {sectionComponents[activeSection]}
      </main>
    </div>
  );
}
