interface BrandLogoProps {
  compact?: boolean
  responsive?: boolean
  className?: string
}

export const BrandLogo = ({ compact = false, responsive = false, className = '' }: BrandLogoProps) => (
  <span className={`inline-flex items-center gap-3 ${className}`}>
    <img
      src="/sentinelops-logo.png"
      alt="SentinelOps"
      className={`${responsive ? 'h-auto w-10 md:w-44' : compact ? 'h-auto w-10' : 'h-auto w-44 max-w-full'} shrink-0 object-contain object-left`}
    />
  </span>
)
