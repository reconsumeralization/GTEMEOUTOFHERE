import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCosurvivalStore } from '@/state/useCosurvivalStore';
import { SectionCard } from '@/components/SectionCard';
import { submitReview } from '@/lib/apiClient';
import { ConfettiTrigger } from '@/components/ConfettiTrigger';

const formSchema = z.object({
  lens: z.enum(['tribe', 'teacher', 'recon']),
  summary: z.string().min(10, 'Share at least 10 characters'),
  highlights: z.string().optional()
});

type FormValues = z.infer<typeof formSchema>;

export function ReviewsSection() {
  const addReview = useCosurvivalStore((state) => state.addReview);
  const userId = useCosurvivalStore((state) => state.userId);
  const reviews = useCosurvivalStore((state) => state.reviews);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting }
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { lens: 'tribe' }
  });

  async function onSubmit(values: FormValues) {
    const entry = await submitReview({
      author: userId,
      lens: values.lens,
      summary: values.summary,
      highlights: values.highlights?.split(',').map((item) => item.trim()).filter(Boolean) ?? []
    });
    addReview(entry);
    reset();
  }

  return (
    <SectionCard
      title="Reviews & Recognition"
      description="Structured reflections routed through governance"
    >
      <div className="grid gap-6 lg:grid-cols-2">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-xs uppercase text-white/60">Lens</label>
            <select
              {...register('lens')}
              className="mt-1 w-full rounded-xl border border-white/10 bg-black/30 p-2 text-white"
            >
              <option value="tribe">TRIBE</option>
              <option value="teacher">TEACHER</option>
              <option value="recon">RECON</option>
            </select>
          </div>
          <div>
            <label className="block text-xs uppercase text-white/60">Summary</label>
            <textarea
              {...register('summary')}
              className="mt-1 w-full rounded-xl border border-white/10 bg-black/30 p-3 text-sm text-white"
              rows={4}
              placeholder="What did you observe that others should know?"
            />
            {errors.summary && <p className="text-xs text-red-300">{errors.summary.message}</p>}
          </div>
          <div>
            <label className="block text-xs uppercase text-white/60">Highlights (comma separated)</label>
            <input
              {...register('highlights')}
              className="mt-1 w-full rounded-xl border border-white/10 bg-black/30 p-2 text-sm text-white"
              placeholder="Bridge spotted, Learning partner invited, etc."
            />
          </div>
          <button
            type="submit"
            disabled={isSubmitting}
            className="rounded-full bg-white px-4 py-2 text-sm font-semibold text-black disabled:opacity-40"
          >
            Submit review
          </button>
        </form>
        <div className="space-y-3">
          {reviews.length === 0 && (
            <p className="text-sm text-white/60">
              No reviews yet. Submit reflections to unlock badges and certificates.
            </p>
          )}
          {reviews.map((review) => (
            <div key={review.id} className="rounded-2xl border border-white/10 p-4">
              <p className="text-xs uppercase tracking-[0.3em] text-white/50">{review.lens}</p>
              <p className="mt-2 text-sm text-white">{review.summary}</p>
              <p className="text-xs text-white/50">
                by {review.author} · {new Date(review.createdAt).toLocaleString()}
              </p>
              {review.highlights.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2 text-[10px] uppercase text-white/60">
                  {review.highlights.map((highlight) => (
                    <span key={highlight} className="rounded-full bg-white/10 px-2 py-0.5">
                      {highlight}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
      <ConfettiTrigger triggerKey={reviews[0]?.id ?? ''} />
    </SectionCard>
  );
}
