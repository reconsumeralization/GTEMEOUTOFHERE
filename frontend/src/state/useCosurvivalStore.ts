import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  AdvisorSignal,
  CertificateMeta,
  GovernanceFlag,
  PipelineStage,
  ProviderScore,
  Recommendation,
  ReviewEntry,
  TribeGraphResponse
} from '@/types/api';

interface CosurvivalState {
  userId: string;
  userRole: string;
  csrfToken?: string;
  pipelineStages: PipelineStage[];
  governanceFlags: GovernanceFlag[];
  tribeGraph?: TribeGraphResponse;
  recommendations: Recommendation[];
  providers: ProviderScore[];
  advisorSignals: AdvisorSignal[];
  reviews: ReviewEntry[];
  certificates: CertificateMeta[];
  setUser: (id: string, role: string, csrf?: string) => void;
  setPipelineStages: (stages: PipelineStage[]) => void;
  setGovernanceFlags: (flags: GovernanceFlag[]) => void;
  setTribeGraph: (graph: TribeGraphResponse) => void;
  setRecommendations: (items: Recommendation[]) => void;
  setProviders: (items: ProviderScore[]) => void;
  setAdvisorSignals: (signals: AdvisorSignal[]) => void;
  setReviews: (entries: ReviewEntry[]) => void;
  addReview: (entry: ReviewEntry) => void;
  setCertificates: (certs: CertificateMeta[]) => void;
}

export const useCosurvivalStore = create<CosurvivalState>()(
  persist(
    (set) => ({
      userId: 'anonymous',
      userRole: 'consumer',
      pipelineStages: [],
      governanceFlags: [],
      recommendations: [],
      providers: [],
      advisorSignals: [],
      reviews: [],
      certificates: [],
      setUser: (id, role, csrf) => set({ userId: id, userRole: role, csrfToken: csrf }),
      setPipelineStages: (stages) => set({ pipelineStages: stages }),
      setGovernanceFlags: (flags) => set({ governanceFlags: flags }),
      setTribeGraph: (graph) => set({ tribeGraph: graph }),
      setRecommendations: (items) => set({ recommendations: items }),
      setProviders: (items) => set({ providers: items }),
      setAdvisorSignals: (signals) => set({ advisorSignals: signals }),
      setReviews: (entries) => set({ reviews: entries }),
      addReview: (entry) => set((state) => ({ reviews: [entry, ...state.reviews] })),
      setCertificates: (certs) => set({ certificates: certs })
    }),
    {
      name: 'cosurvival-store'
    }
  )
);
