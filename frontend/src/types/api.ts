export type SeverityLevel = 'weak' | 'moderate' | 'strong' | 'critical';

export interface PipelineStage {
  id: string;
  label: string;
  status: 'pending' | 'running' | 'passed' | 'failed';
  updatedAt?: string;
  link?: string;
}

export interface GovernanceFlag {
  id: string;
  title: string;
  description: string;
  severity: SeverityLevel;
  remediation?: string;
}

export interface TribeGraphEdge {
  source: string;
  target: string;
  weight: number;
}

export interface TribeGraphResponse {
  nodes: string[];
  edges: TribeGraphEdge[];
}

export interface Recommendation {
  skill: string;
  frequency: number;
}

export interface ProviderScore {
  provider_id: string;
  reliability: number;
  total_activities: number;
  error_count: number;
  grade: 'A' | 'B' | 'C' | 'F';
}

export interface AdvisorSignal {
  id: string;
  title: string;
  severity: SeverityLevel;
  whyNow: string;
  evidence: string[];
  confidence: number;
  alternatives: string[];
}

export interface ReviewEntry {
  id: string;
  author: string;
  lens: string;
  summary: string;
  createdAt: string;
  highlights: string[];
}

export interface CertificateMeta {
  id: string;
  title: string;
  issuedAt: string;
  hash: string;
  downloadUrl?: string;
}

export interface BootstrapPayload {
  csrfToken?: string;
  currentUser?: string;
  userRole?: string;
  lastPipelineRun?: string | null;
}
