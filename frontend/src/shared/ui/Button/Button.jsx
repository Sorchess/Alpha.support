import "./Button.scss";

export const Button = ({
  children,
  variant = "primary",
  size = "medium",
  className = "",
  loading = false,
  disabled,
  ...props
}) => {
  const classes = `button button--${variant} button--${size} {className}`;

  return (
    <button className={classes} disabled={disabled || loading} {...props}>
      {loading ? "..." : children}
    </button>
  );
};
