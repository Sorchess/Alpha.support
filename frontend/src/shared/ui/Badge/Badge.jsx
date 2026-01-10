import "./Badge.scss";

export const Badge = ({ children, color = "gray" }) => {
  return <span className={`badge badge--${color}`}>{children}</span>;
};
