import type { PropsWithChildren, ReactNode } from 'react';

interface SectionCardProps extends PropsWithChildren {
  title: string;
  description?: string;
  icon?: ReactNode;
  actions?: ReactNode;
}

export function SectionCard({ title, description, children, icon, actions }: SectionCardProps) {
  return (
    <section className="glass-panel flex flex-col gap-4 p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="section-heading text-white">
            {icon}
            <span>{title}</span>
          </div>
          {description && <p className="mt-1 text-sm text-white/60">{description}</p>}
        </div>
        {actions}
      </div>
      <div>{children}</div>
    </section>
  );
}
